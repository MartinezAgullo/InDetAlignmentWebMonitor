#!/bin/sh

wwwdir=`dirname $0`
#echo "$wwwdir"
#echo "echo $RUNLOCALTEST"


#if [ x`echo $RUNLOCALTEST` != "xTrue" ] 
#then
#    echo " --environment-- global IDAlignment web monitoring!"
    #export PATH=/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/pytools/1.8_python2.7/x86_64-slc6-gcc47-opt/bin:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/app/releases/ROOT/5.34.07a/x86_64-slc6-gcc47-opt/root/bin:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/Python/2.7.3/x86_64-slc6-gcc47-opt/bin:/afs/cern.ch/atlas/software/releases/18.0.0/gcc-alt-472/x86_64-slc6-gcc47-opt/:${PATH}

    #export PYTHONPATH=/afs/cern.ch/atlas/software/releases/18.0.0/GAUDI/v23r6p1/InstallArea/python:/afs/cern.ch/atlas/software/releases/18.0.0/external/ZSI/2.1-a1/lib/python:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/pygraphics/1.4_python2.7/x86_64-slc6-gcc47-opt/lib/python2.7/site-packages:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/pytools/1.8_python2.7/x86_64-slc6-gcc47-opt/lib/python2.7/site-packages:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/app/releases/COOL/COOL_2_8_18/x86_64-slc6-gcc47-opt/python:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/app/releases/CORAL/CORAL_2_3_27/x86_64-slc6-gcc47-opt/python:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/app/releases/CORAL/CORAL_2_3_16/x86_64-slc6-gcc47-opt/lib:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/app/releases/ROOT/5.34.07a/x86_64-slc6-gcc47-opt/root/lib:/afs/cern.ch/user/a/atlidbs/packages/lib/python:/afs/cern.ch/atlas/software/releases/18.0.0/tdaq-common/tdaq-common-01-23-00/installed/share/lib/python:/afs/cern.ch/atlas/software/releases/18.0.0/tdaq-common/tdaq-common-01-23-00/installed/x86_64-slc6-gcc47-opt/lib:/afs/cern.ch/atlas/software/releases/18.0.0/dqm-common/dqm-common-00-23-00/installed/share/lib/python

    #export LD_LIBRARY_PATH=/afs/cern.ch/atlas/software/releases/18.0.0/AtlasCore/18.0.0/InstallArea/x86_64-slc6-gcc47-opt/lib:/afs/cern.ch/atlas/software/releases/18.0.0/GAUDI/v23r6p1/InstallArea/x86_64-slc6-gcc47-opt/lib:/afs/cern.ch/atlas/software/releases/18.0.0/LCGCMT/LCGCMT_65/InstallArea/x86_64-slc6-gcc47-opt/lib:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/valgrind/3.5.0/x86_64-slc6-gcc47-opt/lib/valgrind:/afs/cern.ch/atlas/software/releases/18.0.0/gcc-alt-472/x86_64-slc6-gcc47-opt/lib64:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/coin3d/3.1.3.p2/x86_64-slc6-gcc47-opt/lib:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/soqt/1.5.0_qt4.8.4_coin3d3.1.3p2/x86_64-slc6-gcc47-opt/lib:/usr/lib64:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/Python/2.7.3/x86_64-slc6-gcc47-opt/lib:/afs/cern.ch/atlas/software/releases/18.0.0/tdaq-common/tdaq-common-01-23-00/installed/x86_64-slc6-gcc47-opt/lib:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/Java/JDK/1.6.0/amd64/jre/lib/amd64:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/Java/JDK/1.6.0/amd64/jre/lib/amd64/server:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/Java/JDK/1.6.0/amd64/jre/lib/amd64/native_threads:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/Java/JDK/1.6.0/amd64/jre/lib/amd64/xawt:/afs/cern.ch/atlas/software/releases/18.0.0/dqm-common/dqm-common-00-23-00/installed/x86_64-slc6-gcc47-opt/lib:/afs/cern.ch/atlas/software/releases/18.0.0/sw/lcg/external/qwt/6.0.1_qt4.8.4/x86_64-slc6-gcc47-opt/lib
#else
#    echo " --environment-- this is a local test!"
#fi

#echo " --environment-- exports completed."
#echo "\n"
#echo " --environment-- wwwdir = " $wwwdir
#echo " --environment-- options = " $*
# delete old files (1 day old)
find $wwwdir/constant/*.png -mtime +1 -exec /bin/rm -f {} \;
find $wwwdir/constant/*.eps -mtime +1 -exec /bin/rm -f {} \;
find $wwwdir/constant/*.root -mtime +1 -exec /bin/rm -f {} \;
# delete all files
#find $wwwdir/constant/*.png -exec /bin/rm -f {} \;
#find $wwwdir/constant/*.eps -exec /bin/rm -f {} \;
#find $wwwdir/constant/*.root -exec /bin/rm -f {} \;

# execute macro that creates the plots
python $wwwdir/plot/readConstants.py $* 
