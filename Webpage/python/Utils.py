import os, commands
from InDetAlignmentWebMonitor.MsgHelper import msgServer

# =====================================================================
#  utils
# =====================================================================
class utils:
    def __init__(self, debugLevel):
        
        self.msg = msgServer('Utils', debugLevel)
        
    # =================================================================================
    #  checkAthenaRelease
    # =================================================================================
    def checkAthenaRelease(self):
        self.msg.printDebug('In checkAthenaRelease()')
            
        cmd = 'more %s/../README.txt | grep WorkDir' % os.environ['WorkDir_DIR']
        # cmd = 'more %s/README.txt | grep WorkDir' % os.environ['TestArea']
        formerAthenaRelease = commands.getoutput(cmd).replace(' ', '').split('-')[1]
        try:
            if os.environ['AtlasVersion'] != formerAthenaRelease:
                self.msg.printError('InDetAlignmentWebMonitor was compiled with another athena release (%s != %s)' % (formerAthenaRelease, os.environ['AtlasVersion']))
                self.msg.printError('please, try to run again from a clean session and the following release: %s!' % formerAthenaRelease)
                sys.exit()
        except KeyError:
            self.msg.printError('please, setup the following athena release: %s!' % formerAthenaRelease)
            sys.exit()

    # =====================================================================
    #  createDir
    # =====================================================================
    def createDir(self, mydir):
        if os.path.exists(mydir):self.msg.printDebug("%s folder exists" % mydir)
        if not os.path.exists(mydir): os.system('mkdir -p %s' % mydir)
        if (not os.access(mydir, os.W_OK)):
            self.msg.printFatal("%s folder is not writable. STOP execution. " % mydir )
            exit()
