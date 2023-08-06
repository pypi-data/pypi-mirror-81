#!/usr/bin/env python
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

'''Density expansion on plane waves'''

import time
import ctypes
import copy
import numpy

from pyscf import lib
from pyscf import gto
from pyscf.pbc.df import incore
from pyscf.pbc.gto import pseudo
from pyscf.pbc.df import aft
from pyscf.pbc.df import ft_ao
from pyscf.pbc import gto as pbcgto

from mpi4pyscf.lib import logger
from mpi4pyscf.tools import mpi
from mpi4pyscf.pbc.df import aft_jk as mpi_aft_jk
from mpi4pyscf.pbc.df import aft_ao2mo as mpi_aft_ao2mo

comm = mpi.comm
rank = mpi.rank


@mpi.parallel_call
def get_nuc(mydf, kpts=None):
    mydf = _sync_mydf(mydf)
# Call the serial code because pw_loop and ft_loop methods are overloaded.
    vne = aft.get_nuc(mydf, kpts)
    return mpi.reduce(vne)

@mpi.parallel_call
def get_pp_loc_part1(mydf, kpts=None):
    mydf = _sync_mydf(mydf)
    vne = aft.get_pp_loc_part1(mydf, kpts)
    return mpi.reduce(vne)

@mpi.parallel_call
def get_pp(mydf, kpts=None):
    if kpts is None:
        kpts_lst = numpy.zeros((1,3))
    else:
        kpts_lst = numpy.reshape(kpts, (-1,3))

    mydf = _sync_mydf(mydf)
    vpp = aft.get_pp_loc_part1(mydf, kpts_lst)
    vpp = mpi.reduce(lib.asarray(vpp))

    if rank == 0:
        vloc2 = pseudo.pp_int.get_pp_loc_part2(mydf.cell, kpts_lst)
        vppnl = pseudo.pp_int.get_pp_nl(mydf.cell, kpts_lst)
        for k in range(len(kpts_lst)):
            vpp[k] += numpy.asarray(vppnl[k] + vloc2[k], dtype=vpp.dtype)

        if kpts is None or numpy.shape(kpts) == (3,):
            vpp = vpp[0]
        return vpp

def _int_nuc_vloc(mydf, nuccell, kpts, intor='int3c2e_sph', aosym='s2', comp=1):
    '''Vnuc - Vloc'''
    cell = mydf.cell
    nkpts = len(kpts)

# Use the 3c2e code with steep s gaussians to mimic nuclear density
    fakenuc = aft._fake_nuc(cell)
    fakenuc._atm, fakenuc._bas, fakenuc._env = \
            gto.conc_env(nuccell._atm, nuccell._bas, nuccell._env,
                         fakenuc._atm, fakenuc._bas, fakenuc._env)

    kptij_lst = numpy.hstack((kpts,kpts)).reshape(-1,2,3)
    ishs = mpi.work_balanced_partition(numpy.arange(cell.nbas),
                                       costs=numpy.arange(1, cell.nbas+1))
    if len(ishs) > 0:
        ish0, ish1 = ishs[0], ishs[-1]+1
        buf = incore.aux_e2(cell, fakenuc, intor, aosym='s2', kptij_lst=kptij_lst,
                            shls_slice=(ish0,ish1,0,cell.nbas,0,fakenuc.nbas))
    else:
        buf = numpy.zeros(0)

    charge = cell.atom_charges()
    charge = numpy.append(charge, -charge)  # (charge-of-nuccell, charge-of-fakenuc)
    nao = cell.nao_nr()
    nchg = len(charge)
    nao_pair = nao*(nao+1)//2
    buf = buf.reshape(nkpts,-1,nchg)
# scaled by 1./mpi.pool.size because nuc is mpi.reduced in get_nuc function
    buf = numpy.einsum('kxz,z->kx', buf, 1./mpi.pool.size*charge)
    mat = numpy.empty((nkpts,nao_pair), dtype=numpy.complex128)
    for k in range(nkpts):
        mat[k] = mpi.allgather(buf[k])

    if (rank == 0 and
        cell.dimension == 3 and intor in ('int3c2e', 'int3c2e_sph',
                                          'int3c2e_cart')):
        assert(comp == 1)
        charges = cell.atom_charges()

        nucbar = sum([z/nuccell.bas_exp(i)[0] for i,z in enumerate(charges)])
        nucbar *= numpy.pi/cell.vol

        ovlp = cell.pbc_intor('int1e_ovlp_sph', 1, lib.HERMITIAN, kpts)
        for k in range(nkpts):
            if aosym == 's1':
                mat[k] += nucbar * ovlp[k].reshape(nao_pair)
            else:
                mat[k] += nucbar * lib.pack_tril(ovlp[k])

    return mat


def _sync_mydf(mydf):
    mydf.unpack_(comm.bcast(mydf.pack()))
    return mydf


@mpi.register_class
class AFTDF(aft.AFTDF):

    def pack(self):
        return {'verbose'   : self.verbose,
                'max_memory': self.max_memory,
                'blockdim'  : self.blockdim,
                'eta'       : self.eta,
                'kpts'      : self.kpts,
                'mesh'      : self.mesh}
    def unpack_(self, dfdic):
        self.__dict__.update(dfdic)
        return self

    def prange(self, start, stop, step=None):
        # affect pw_loop and ft_loop function
        size = stop - start
        mpi_size = mpi.pool.size
        segsize = (size+mpi_size-1) // mpi_size
        if step is None:
            step = segsize
        else:
            step = min(step, segsize)
        start = min(size, start + rank * segsize)
        stop = min(size, start + segsize)
        return lib.prange(start, stop, step)
    mpi_prange = prange

    _int_nuc_vloc = _int_nuc_vloc
    get_nuc = get_nuc
    get_pp = get_pp

    get_eri = get_ao_eri = mpi_aft_ao2mo.get_eri
    ao2mo = get_mo_eri = mpi_aft_ao2mo.general

    def get_jk(self, dm, hermi=1, kpts=None, kpts_band=None,
               with_j=True, with_k=True, omega=None, exxdiv='ewald'):
        '''Gamma-point calculation by default'''
        # J/K for RSH functionals
        if omega is not None:
            return aft._sub_df_jk_(self, dm, hermi, kpts, kpts_band,
                                   with_j, with_k, omega, exxdiv)

        if kpts is None:
            if numpy.all(self.kpts == 0):
                kpts = numpy.zeros(3)
            else:
                kpts = self.kpts
        else:
            kpts = numpy.asarray(kpts)

        if kpts.shape == (3,):
            return mpi_aft_jk.get_jk(self, dm, hermi, kpts, kpts_band, with_j,
                                     with_k, exxdiv)

        vj = vk = None
        if with_k:
            vk = mpi_aft_jk.get_k_kpts(self, dm, hermi, kpts, kpts_band, exxdiv)
        if with_j:
            vj = mpi_aft_jk.get_j_kpts(self, dm, hermi, kpts, kpts_band)
        return vj, vk


    def loop(self, serial_mode=True):
        # mpi.pool.worker_status = P (pending) means the caller on master
        # process runs in serial mode.
        # 3-index tensor should be generated on each process and sent to
        # the master process.  E.g. the call to with_df.loop in dfccsd
        serial_mode = mpi.pool.worker_status == 'P'
        if serial_mode:
            return loop_yield_then_reduce(self)
        else:
            return aft.AFTDF.loop(self)

    def get_naoaux(self, serial_mode=True):
        naux = aft.AFTDF.get_naoaux(self)
        if mpi.pool.worker_status == 'P':
            return naux
        else:
            ps = list(self.mpi_prange(0, naux))
            return ps[-1][1] - ps[0][0]


@mpi.reduced_yield
def loop_yield_then_reduce(mydf):
    for Lpq in aft.AFTDF.loop(mydf):
        yield Lpq


if __name__ == '__main__':
    # run with mpirun -n
    from pyscf.pbc import gto as pgto
    from mpi4pyscf.pbc import df
    cell = pgto.Cell()
    cell.atom = 'He 1. .5 .5; C .1 1.3 2.1'
    cell.basis = {'He': [(0, (2.5, 1)), (0, (1., 1))],
                  'C' :'gth-szv',}
    cell.pseudo = {'C':'gth-pade'}
    cell.a = numpy.eye(3) * 2.5
    cell.mesh = [11] * 3
    cell.build()
    numpy.random.seed(19)
    kpts = numpy.random.random((5,3))

    mydf = df.AFTDF(cell)
    v = mydf.get_nuc()
    print(v.shape)
    v = mydf.get_pp(kpts)
    print(v.shape)

    cell = pgto.M(atom='He 0 0 0; He 0 0 1', a=numpy.eye(3)*4, mesh=[11]*3)
    mydf = df.AFTDF(cell)
    nao = cell.nao_nr()
    dm = numpy.ones((nao,nao))
    vj, vk = mydf.get_jk(dm)
    print(vj.shape)
    print(vk.shape)

    dm_kpts = [dm]*5
    vj, vk = mydf.get_jk(dm_kpts, kpts=kpts)
    print(vj.shape)
    print(vk.shape)

    mydf.close()

