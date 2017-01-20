source /nfs/farm/g/lsst/u1/software/redhat6-x86_64-64bit-gcc44/DMstack/twinkles_stack/loadLSST.bash
export SLAC_INSTALL_DIR=/nfs/farm/g/lsst/u1/software/redhat6-x86_64-64bit-gcc44
export PATH=${SLAC_INSTALL_DIR}/anaconda/py-2.7.11/bin:${SLAC_INSTALL_DIR}/git/1.8.4.5/bin:${SLAC_INSTALL_DIR}/git/git-lfs-1.4.1:$PATH
echo 'added /nfs/farm/g/lsst/u1/software/redhat6-x86_64-64bit-gcc44/anaconda/py-2.7.11/bin, git 1.8.4.5, and git-lfs 1.4.1 to PATH'

setup lsst_sims
setup -r /nfs/farm/g/desc/u1/imsim_deep/sims_GalSimInterface -j
setup -r /nfs/farm/g/desc/u1/imsim_deep/sims_catUtils -j
setup -r /nfs/farm/g/desc/u1/imsim_deep/sims_utils -j
setup -r /gpfs/slac/kipac/fs1/g/desc/imsim_deep/imSim -j
setup -r /gpfs/slac/kipac/fs1/g/desc/imsim_deep/imsim_deep_pipeline -j
PS1="[twinkles_stack] "
