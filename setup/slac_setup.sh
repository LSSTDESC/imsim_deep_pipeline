source /gpfs/slac/kipac/fs1/g/desc/imsim_deep/DMstack/LSST_Stack_2017-01-19/loadLSST.bash

#source /nfs/farm/g/desc/u1/software/redhat6-x86_64-64bit-devtoolset-3/DMstack/twinkles_20170221/loadLSST.bash
export SLAC_INSTALL_DIR=/nfs/farm/g/lsst/u1/software/redhat6-x86_64-64bit-gcc44
export PATH=${SLAC_INSTALL_DIR}/git/1.8.4.5/bin:${SLAC_INSTALL_DIR}/git/git-lfs-1.4.1:$PATH
echo 'added /nfs/farm/g/lsst/u1/software/redhat6-x86_64-64bit-gcc44/anaconda/py-2.7.11/bin, git 1.8.4.5, and git-lfs 1.4.1 to PATH'

setup lsst_sims
setup -r /gpfs/slac/kipac/fs1/g/desc/imsim_deep/sims_psf_fixes/sims_GalSimInterface -j
#setup -r /gpfs/slac/kipac/fs1/g/desc/imsim_deep/sims_psf_fixes/sims_catUtils -j
setup -r /gpfs/slac/kipac/fs1/g/desc/imsim_deep/imSim -j
setup -r /gpfs/slac/kipac/fs1/g/desc/imsim_deep/imsim_deep_pipeline -j

## Use a copy of the SED library on gpfs to avoid nfs file contention issues.
#export SIMS_SED_LIBRARY_DIR=/gpfs/slac/kipac/fs1/g/desc/imsim_deep/sims_sed_library/2017.01.24
#export SIMS_SED_LIBRARY_DIR_EXTRA=/gpfs/slac/kipac/fs1/g/desc/imsim_deep/sims_sed_library/2017.01.24

#PS1="[twinkles_2017-02-21_stack] "
PS1="[gpfs_stack] "
