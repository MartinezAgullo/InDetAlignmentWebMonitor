# Project: InDetAlignmentWebMonitor

Package for monitoring the track-based ID alignment results obtained at the calibration loop and show them as a web-based service [https://atlasalignment.cern.ch/webapp](https://atlasalignment.cern.ch/webapp).

## Getting started

Follow these instructions to install and compile the [InDetAlignmentWebMonitor](https://gitlab.cern.ch/atlas-idalignment/InDetAlignmentWebMonitor) package within release 21. A useful tutorial can be found [here](https://twiki.cern.ch/twiki/bin/view/AtlasComputing/InDetAlignTutorialRun2Rel21). Let's assume you will be working from ```~/work/alignment/webMonitoring/```:

```
mkdir -p ~/work/alignment/webMonitoring/
cd ~/work/alignment/webMonitoring/
setupATLAS
lsetup "asetup Athena,21.0.50,here" git pyami
# Checkout athena, and switch to the 21.0 analysis branch
git atlas init-workdir -b 21.0 https://:@gitlab.cern.ch:8443/atlas/athena.git
cd athena
git clone -b master https://:@gitlab.cern.ch:8443/$USER/InDetAlignmentWebMonitor.git
git atlas addpkg InDetAlignmentMonitoring
mkdir -p ../build && cd ../build
cmake ../athena/Projects/WorkDir
cmake --build ./
source */setup.sh
mkdir -p ../run; cd ../run
```

The instructions shown above assume that you have a fork of the [InDetAlignmentWebMonitor](https://gitlab.cern.ch/atlas-idalignment/InDetAlignmentWebMonitor) project. This is used in case you want to contribute to the code development. If you are not plannig to contribute, just use ```git clone -b master https://:@gitlab.cern.ch:8443/atlas-idalignment/InDetAlignmentWebMonitor.git```. 

It is also assume that release 21.0.50 is used. It is very easy to check which production releases are available, just by looking in CVMFS, e.g., ```ls /cvmfs/atlas.cern.ch/repo/sw/software/```. You can replace the command ```asetup Athena,21.0.50,here``` with any other release using [asetup](https://twiki.cern.ch/twiki/bin/view/AtlasComputing/AtlasSetup) and then compile the packages.

If one needs to update other packages, for example package X, just do:

```
cd ~/work/alignment/webMonitoring/athena/
git atlas addpkg X
cd ..
rm -rf build; mkdir build; cd build
cmake ../athena/Projects/WorkDir
cmake --build .
```

## How to run InDetAlignmentWebMonitor on lxplus

### Clean setup on lxplus

Log into lxplus and go to the directory you installed the [InDetAlignmentWebMonitor](https://gitlab.cern.ch/atlas-idalignment/InDetAlignmentWebMonitor) package (following the [previous steps](https://gitlab.cern.ch/atlas-idalignment/InDetAlignmentWebMonitor#getting-started)), i.e. ```~/work/alignment/webMonitoring/``` (as previously assumed). Then, just run the ```update_runs.py``` script:

```
cd ~/work/alignment/webMonitoring/run/
update_runs.py
```

Alternatively, you can setup the athena release and then run the ```update_runs.py``` script:
```
cd ~/work/alignment/webMonitoring/
setupATLAS --quiet
lsetup "asetup Athena,21.0.50,here" git pyami --quiet
cd build
source $CMTCONFIG/setup.sh
cd ../run
update_runs.py
```

If you are running _local_ _tests_, use ```update_runs.py -t```. Check for further options with ```-h```.

## For developers

### Configuring a remote for your fork

You must configure a remote that points to the upstream repository in GitLab to sync changes you make in your fork with the original repository. This also allows you to sync changes made in the original repository with your fork.

To list the current configured remote repository for your fork, just type:

```
git remote -v
```

To specify a (new) remote upstream repository that will be synced with the fork:
```
git remote add upstream https://:@gitlab.cern.ch:8443/atlas-idalignment/InDetAlignmentWebMonitor.git
```

### Syncing your fork with the upstream

You should sync your fork of a repository to keep it up-to-date with the upstream repository. So, you have to fetch the branches and their respective commits from the upstream repository. Commits to master will be stored in a local branch, upstream/master. Then, you can pull changes from the upstream master to your local master.

```
git fetch upstream
git pull upstream master
```

Use ```git pull upstream master -p``` or ```git pull upstream master -f``` in order to prune tracking branches no longer on remote or force overwrite of local branch, respectively.
