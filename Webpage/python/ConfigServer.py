import os
from InDetAlignmentWebMonitor.MsgHelper import msgServer
from InDetAlignmentWebMonitor.Utils import utils

# =====================================================================
#  configServer
# =====================================================================
class configServer:
    def __init__(self, year, configfile, workingDir, localtest, debugLevel):
        
        self.msg = msgServer('configServer', debugLevel)
        
        self.year = str(year)
        self.localtest = localtest

        self.maxNumberOfRunsToAnalyze = 10000

        # default folders
        self.folderName = "secure/"
        self.dataFolderName = "database/"
        self.configFolderName = "config/"
        self.webFolderName = "WebPage/"

        # make sure that the last character of workingDir is a slash
        if not workingDir.endswith('/'): workingDir += '/'
        self.workingDir = workingDir
        if self.localtest: os.system('ln -sf %s' % (os.path.abspath('..')+'/athena/InDetAlignmentWebMonitor/'+self.dataFolderName))
        else: self.workingDir = '/var/vhost/atlas-alignment/'

        # symbolic link to config directory
        os.system('ln -sf %s' % (os.path.abspath('..')+'/athena/InDetAlignmentWebMonitor/'+self.configFolderName))

        # check and prepare config file
        self.configfile = configfile
        if not os.path.isfile(self.configfile):
            msg.printError("Configuration file %s is not found. Please, check the requested file!" % self.configfile) 
            exit()

        # monitoring folder
        self.monitoringFolderName = self.workingDir + "Monitor/"
        #self.monitorFolder =  alignWebRoot + "/database/Monitor"
        self.detailedPlotsRoot = self.monitoringFolderName + "detailed_plots/"
        self.detailed_plots = self.detailedPlotsRoot + self.year + "/"
        self.mergedFilesFolder = self.monitoringFolderName + "MergedMonitoringFiles"

        self.calibLoop = "/afs/cern.ch/user/a/atlidali/w0/calibLoop/web/database/"
        self.analysisLogFilesFolder = "/afs/cern.ch/user/a/atlidali/w0/calibLoop/checker/log_forEachRun/"
        self.runInfoDBfile = "server_runinfo%s.db" % year

        self.server = self.workingDir + self.dataFolderName
        self.server_alignfiles = self.workingDir + self.webFolderName + "alignlogfiles/" + self.year + "/"
        self.bsHandshakeFolder = self.workingDir + self.webFolderName + "bshandshake/"
        self.runAnalysisLogFolder = self.workingDir + self.webFolderName + "runanalysislog/" + self.year + "/"

        # check if the athena release is well configured
        utilities = utils(debugLevel)

        # create needed directories
        utilities.createDir(self.server_alignfiles)
        utilities.createDir(self.bsHandshakeFolder)
        utilities.createDir(self.runAnalysisLogFolder)

        # get the complete list of analysis log files
        self.analysisLogFiles = os.popen("ls %s | grep '.log'" % self.analysisLogFilesFolder).readlines()


    # =====================================================================
    #  printConfig
    # =====================================================================
    def printConfig(self):
        self.msg.printDebug('In printConfig()')
        self.msg.printInfo("==================================================================================================")
        self.msg.printInfo("==                                  Configuration                                               ==")
        self.msg.printInfo("==================================================================================================")
        self.msg.printInfo("runLocalTest = %s" % self.localtest)
        self.msg.printInfo("alignWebRoot = %s" % self.workingDir)
        self.msg.printInfo("alignWebYear = %s" % self.year)
        self.msg.printInfo("--------------------------------------------------------------------------------------------------")
        self.msg.printInfo("server = %s" % self.server)
        self.msg.printInfo("server_alignfiles = %s" % self.server_alignfiles)
        self.msg.printInfo("calibLoop = %s" % self.calibLoop)
        self.msg.printInfo("analysisLogFilesFolder = %s" % self.analysisLogFilesFolder)
        self.msg.printInfo("runInfoDBfile = %s" % self.runInfoDBfile)
        self.msg.printInfo("bsHandshakeFolder = %s" % self.bsHandshakeFolder)
        self.msg.printInfo("monitoringFolderName = %s" % self.monitoringFolderName)
        self.msg.printInfo("detailed_plots = %s" % self.detailed_plots)
        self.msg.printInfo("mergedFilesFolder = %s" % self.mergedFilesFolder)
        self.msg.printInfo("==================================================================================================")


    # =====================================================================
    #  getInDetAlignmentMonitoringPath
    # =====================================================================
    def getInDetAlignmentMonitoringPath(self):
        mydir = os.path.abspath('..')+'/athena/InnerDetector/InDetMonitoring/InDetAlignmentMonitoring/share/'

        print mydir

        if not os.path.exists(mydir):
            self.msg.printWarning("InDetAlignmentMonitoring is not found, please, check your setup!")
            exit()
        return mydir


    # =====================================================================
    #  ExtractLBGroupFiles
    # =====================================================================
    def ExtractLBGroupFiles(self,runNumber, inputList):
        # this function extracts from a list of files, those that belong to a given run number (run number = element 0, file name = element 1)
        # Note that for listOfRuns['monitoringFilesIter0'] contains a list and not a dictionary
        outputList = []
        if isinstance(inputList, (list)):
            #self.msg.printDebug("inputList is a list")
            for element in inputList:
                if (element[0] == runNumber):
                    outputList.append(element[1]) #Fill outputList
                                          
        if isinstance(inputList, (dict)):
            #self.msg.printDebug("inputList is a dict")
            for element in inputList:
                #print "element = " + element
                #print "runNumber = " + runNumber
                #print "inputList[element]" + inputList[element]
                if (element == runNumber):
                    outputList.append(inputList[element]) #Fill outputList
        return outputList


    # =====================================================================
    #  GetFoldersWithCalibLoopOutput
    # =====================================================================
    def GetFoldersWithCalibLoopOutput(self):
        self.msg.printDebug('In GetFoldersWithCalibLoopOutput()')
        abspath = []
        logicName = []

        self.msg.printInfo('Reading configuration file: %s' % self.configfile)
        for line in open(self.configfile, "r").readlines():
            if line.startswith('#') or line.startswith('%'): continue
            line = line.rstrip().replace(' ','')
            if line.startswith('path'):
                line = line.split('=')[-1]
                line = line.split(',')
                if len(line) == 2:
                    abspath.append(line[0])
                    logicName.append(line[1])
                    self.msg.printInfo(' + input folder: %s (%s)' % (line[0], line[1]))
                else:
                    self.msg.printError("Problem reading the configuration file %s. Please, check the requested file!" % self.configfile) 
                    exit()

        # print abspath
        # print logicName
        return abspath, logicName


    # =====================================================================
    #  GetAnalysisLogFiles
    # =====================================================================
    def GetAnalysisLogFiles (self, runNumber, printLevel = 0):
        self.msg.printDebug('In GetAnalysisLogFiles()')

        analysisLogFilesForRun = []
        if '_backup' in runNumber:
            striped = runNumber.rstrip('_backup')
            self.msg.printDebug("This is the backup folder for run " +str(striped) + ".")
            runNumber = str(int(striped))
        else: runNumber = str(int(runNumber))
        
        # print self.analysisLogFiles

        # try to find an file for this run
        for i in self.analysisLogFiles:
            # print " + " + i.rstrip()
            if runNumber in i.rstrip():
                analysisLogFilesForRun.append(i)
                self.msg.printDebug("Run %s has this analysis log file: %s " %(runNumber, i.rstrip()))
                # os.system("more %s%s" % (self.analysisLogFilesFolder, i.rstrip()))
        # self.msg.printDebug("Returning: "+ str(analysisLogFilesForRun))        
        return analysisLogFilesForRun


    # =====================================================================
    #  ExtractBSHandShakeInfo
    # =====================================================================
    def ExtractBSHandShakeInfo (self, runNumber, inputFile, printLevel=0):
        # extract the BS HandShake info for a given run from the BS Handshake file

        self.msg.printDebug("In ExtractBSHandShakeInfo()")
        self.msg.printDebug(" + Run = " + str(runNumber))
        self.msg.printDebug(" + BS HandShake file = "+ str(inputFile))

        with open(inputFile) as bsFile:
            linesInFile = bsFile.readlines()    

        runFound = False
        runBSHSTimeStamp = "None"
        runBSHSAuthor = "Unknown"   
        for thisLine in linesInFile:
            if (not runFound):
                words = thisLine.split()
                #self.msg.printDebug("Length of words: "+str(len(words)))
                if (str(runNumber) in thisLine):
                    runFound = True
                    #runBSHSTimeStamp = thisLine[0:19]
                    runBSHSTimeStamp = words[0]
                    runBSHSAuthor = words[4]
        if (runFound):
            self.msg.printDebug( " + Run " + runNumber + " BS HandShake -> timestamp: " + runBSHSTimeStamp + "  author: " + runBSHSAuthor)
        return (runBSHSTimeStamp, runBSHSAuthor)


    # =====================================================================
    #  ExtractAnalysisStatus
    # =====================================================================
    def ExtractAnalysisStatus (self, runNumber, inputFile, printLevel=10):
        # extract the analysis status of the calibration loop alignment results for a given run

        with open(self.analysisLogFilesFolder+inputFile) as statusFile:
            linesInFile = statusFile.readlines()    

        L11Result = "Unknown"
        L16Result = "Unknown"
        submission = "Unknown"
        timestamp = "Unknown"

        for thisLine in linesInFile:
            # print thisLine
            if ("L11_RESULTS_GOOD" in thisLine):
                L11Result = "Good"
            if ("L11_RESULTS_NOT_GOOD" in thisLine):
                L11Result = "Problems"
            if ("L16_RESULT_GOOD" in thisLine):
                L16Result = "Good"
            if ("Submission is canceled" in thisLine):    
                submission = "Cancelled"
            if ("Completed Process Successfully" in thisLine):
                words = thisLine.split()
                #print "  <ExtractAnalysisStatus> len of words:",len(words)
                submission = "Completed"
                timestamp = words[2]
            elif ("Saved log file to: /afs" in thisLine):
                words = thisLine.split()
                #print "  <ExtractAnalysisStatus> len of words:",len(words)
                submission = "Completed"
                timestamp = words[2]
        # end of loop on files  

        if (printLevel >= 1):
            self.msg.printDebug( "Run "+ str(runNumber) + "  L11Result: " + str(L11Result) + "  L16Result: " + str(L16Result) + "  submission: " + str(submission) + "  timestamp: " + str(timestamp))
            
        return (L11Result, L16Result, submission, timestamp)


    # =====================================================================
    #  Touch
    # =====================================================================
    def Touch(self, path):
        import time
        now = time.time()
        try:
            # assume it's there
            os.utime(path, (now, now))
        except os.error:
            # if it isn't, try creating the directory,
            # a file with that name
            os.makedirs(os.path.dirname(path))
            open(path, "w").close()
            os.utime(path, (now, now))
        return


    # =====================================================================
    #  endBanner
    # =====================================================================
    def endBanner(self):
        self.msg.printInfo("=======================================================================================")
        self.msg.printInfo("==                            COMPLETED                                              ==")
        self.msg.printInfo("=======================================================================================")



