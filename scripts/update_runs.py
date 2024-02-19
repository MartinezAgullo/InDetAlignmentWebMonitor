#!/usr/bin/env python
import os, sys, commands, subprocess, tarfile, time, glob, datetime
try: import cPickle as pickle
except: import pickle
from optparse import OptionParser
import json

from InDetAlignmentWebMonitor.RunInfo import runInfo
from InDetAlignmentWebMonitor.ConfigServer import configServer
from InDetAlignmentWebMonitor.MsgHelper import msgServer
from InDetAlignmentWebMonitor.AMIHelper import amiServer
from InDetAlignmentWebMonitor.Utils import utils

def enum(**enums): return type('Enum', (), enums)
DebugLevel = enum(DEBUG=0, INFO=1, WARNING=2, ERROR=3, FATAL=4)


# =================================================================================
#  main
# =================================================================================
def main(argv):
    parser = OptionParser()
    parser.add_option("-w", "--workdir", dest="workingDir", default=os.environ['PWD'],
                      help="set the working directory [default: %default]", metavar="DIR")
    parser.add_option("-y", "--year", dest="year", default=datetime.datetime.today().year, type="int",
                      help="set which year you want to retrieve [default: %default]", metavar="YEAR")
    parser.add_option("-c", "--configfile", dest="configfile", default="config/config_data%d_13TeV.txt" % datetime.datetime.today().year,
                      help="set the configuration file to be used", metavar="FILE")
    parser.add_option("--run", dest="RUNlist", default="",
                      help="set RUNs to extract/update information [default: %default]", metavar="list")
    parser.add_option("-r", "--reprocess", action="store_true", dest="reprocess", default=False,
                      help="reprocess without reading db file [default: %default]")
    parser.add_option("-d", "--debugLevel", dest="debugLevel", default=0, type="int",
                      help="set debug level (DEBUG=0, INFO=1, WARNING=2, ERROR=3, FATAL=4) [default: %default]", metavar="LEVEL")
    parser.add_option("-t", "--localtest", action="store_true", dest="localtest", default=False,
                      help="run a local test [default: %default]")
    (options, args) = parser.parse_args()

    global msg
    msg = msgServer('update_runs', options.debugLevel)

    global ami
    ami = amiServer(options.year, options.debugLevel)

    global config
    config = configServer(options.year, options.configfile, options.workingDir, options.localtest, options.debugLevel)
    config.printConfig()

    global RUNlist
    RUNlist = options.RUNlist.replace(' ','').split(',')
    
    global utilities
    utilities = utils(options.debugLevel)

    # check if the athena release is well configured
    utilities.checkAthenaRelease()

    # update runs for the InDetAlignmentWebMonitor package
    UpdateRuns(options.reprocess, options.debugLevel)
    config.endBanner()

# =================================================================================
#  UpdateRuns
# =================================================================================
def UpdateRuns(reprocess, debugLevel):
    msg.printDebug('In UpdateRuns()')

    # define folders to spy for new data
    allabspath, logicName = config.GetFoldersWithCalibLoopOutput()
    if len(allabspath) == 0:
        msg.printFatal("No input paths are found! Please, check your configuration file")
        exit()

    msg.printInfo("List of folders where to search for new runs/data:")
    abspath = [] #List of folders with runs for the selected year
    for counter,testfolder in enumerate(allabspath):
        if os.path.isdir(testfolder) and os.path.isdir(testfolder):
            abspath += [ testfolder ]
            msg.printInfo(" + %d. folder: %s, logicName %s" % (counter, testfolder, logicName[counter]))

    # retrieve the BeamSpot handshake file. This file will be linked in the page
    fileWithBSHandshakeInfo = "%sHandShake_log_%s.txt" %(config.bsHandshakeFolder, config.year)
    msg.printDebug("BS HandShake logfile: %s" % fileWithBSHandshakeInfo)

    # copy the handshake logfile from atlidali
    mvbshandshake_cmd = "cp %s %s" % ("/afs/cern.ch/user/a/atlidali/w0/calibLoop/checker/log/HandShake_log.txt", fileWithBSHandshakeInfo)      
    (bshandshake_status, bshandshake_output) = commands.getstatusoutput(mvbshandshake_cmd)
    if (bshandshake_status !=0):
        msg.printWarning("A problem ocurred while copying the BS HandShake logfile. Output follows:")
        msg.printWarning(bshandshake_output)
        os.system('touch %s' % fileWithBSHandshakeInfo)
        msg.printInfo("Empty BS HandShake file succesfully created!")
    else:
        msg.printInfo("BS HandShake file succesfully stored!")
    msg.printDebug(" + BS HandShake logfile: %s" % fileWithBSHandshakeInfo)

    # load the run data from the server_runinfo201X.db if necessary
    Dope = runInfo(msg.getDebugLevel()) # here we initialize the object Info which contains a dictionary with al the information of the runs
    if reprocess and RUNlist == ['']: # Case  "-r": load the info from server_runinfo20XX.db 
        msg.printDebug("Reprocessing all runs")
        try: 
            os.remove('%s%s' % (config.server, config.runInfoDBfile))
            msg.printInfo(('Removing run info database %s from %s' % (config.runInfoDBfile, config.server)))
        except: msg.printInfo(('Run info database %s was not found' % (config.runInfoDBfile)))
        msg.printInfo('New run info database file %s will be created' % (config.runInfoDBfile))
        os.system('touch %s%s' % (config.server, config.runInfoDBfile))
        Dope.DB = {} #Initilalize the DB
       
    else: # load the info from server_runinfo20XX.db
        try:
            Dope.DB = pickle.load( open(config.server + config.runInfoDBfile,'r') )
            #Dope.DB = pickle.load( open('/afs/cern.ch/user/m/martinpa/work/alignment/webMonitoring/run/database/server_runinfo2018.db.salva','r') ) #test: To compare with Salva's db
            msg.printInfo("Run info file %s succesfully read!" % config.runInfoDBfile)    
        except:
            msg.printWarning("Attempt of reading from run info file %s has failed! ==> New %s will be created!" % (config.runInfoDBfile, config.runInfoDBfile))
            Dope.DB = {}
            os.system('touch %s%s' % (config.server, config.runInfoDBfile))

    # initialize the list
    if 'RunsWithNewData' not in Dope.listOfRuns.keys(): Dope.listOfRuns['RunsWithNewData'] = []
    if 'runsWithNewRecordDate' not in Dope.listOfRuns.keys():  Dope.listOfRuns['runsWithNewRecordDate'] = [] # it may be possible to remove this list

    # start a loop on the input folders where to search for runs 
    if msg.getDebugLevel() == 4: msg.printBold("Starting loop over all folders where to search for runs")
    for i in range(len(abspath)):
        msg.printInfo("===========================================================================================")
        msg.printInfo("===========================================================================================")
        msg.printInfo("Searching for new runs folder: " )
        msg.printBold(" + %d. folder: %s" % (i,abspath[i]))

        runListInTestingFolder = []
        # os.system("ls %s" % abspath[i]) 
        runListInTestingFolder = commands.getoutput("ls %s" % abspath[i]).splitlines() # make an "ls" on the command line and pick the elements
        if 'README.txt' in runListInTestingFolder: runListInTestingFolder.remove('README.txt')

        # extract data project and stream names:Separates the pathname
        # uses the last folder name as 'dataStreamName' and the folder containing it as 'dataProject'
        wordsInPathName = abspath[i]
        if wordsInPathName.endswith('/'): wordsInPathName = wordsInPathName[:-1]
        wordsInPathName = wordsInPathName.split("/")
        dataStreamName = wordsInPathName[-1] # last word
        dataProjectName = wordsInPathName[-2] # the word before the last
        # msg.printDebug( "runlistInTestingFolder = " + str(runListInTestingFolder) +" of stream " + str(dataStreamName) + " \n (project: "+ str(dataProjectName) +") contains "+ str(len(runListInTestingFolder)) + " runs in total")
        msg.printInfo( " + project: " + dataProjectName )       
        msg.printInfo( " + stream: " + dataStreamName )
        msg.printInfo( " + logic name: " + logicName[i])

        msg.printInfo("   -> Runs available: " + str(runListInTestingFolder))
        msg.printInfo("   -> runlistInTestingFolder contains " + str(len(runListInTestingFolder)) + " runs in total for this folder ("+str(abspath[i])+")")

        # loop over runs in input directory
        runcount = 0
        listOfRunsToBeIgnored = []
        if len(RUNlist) > 0 and type(RUNlist) == list and not RUNlist == ['']: # -- run case
            msg.printDebug("List of runs to extract information selected with the --run option: " + str(RUNlist))
            for run in sorted(runListInTestingFolder):
                if '_' in run: run = run.split('_')[0] # this line is to remove the "_backup"
                if str(int(run)) not in RUNlist and str(run) not in RUNlist:
                    listOfRunsToBeIgnored += [ run ]
                    # msg.printDebug( " - run number to be ignored: %s" % (run))
                    runListInTestingFolder.remove(run)
                    continue
                runcount +=1
                msg.printDebug( " + #%03i run number to be processed: %s" % (runcount, run))
        
        if len(listOfRunsToBeIgnored) > 0: 
            msg.printWarning("   -> Runs to be ignored: " + str(listOfRunsToBeIgnored))
            msg.printWarning("   -> listOfRunsToBeIgnored contains " + str(len(listOfRunsToBeIgnored)) + " runs in total to be ignred in this folder ("+str(abspath[i])+")")

        if  RUNlist == ['']: runcount = 1 # This is for avoid triggering the "No valid/requested runs in the folder"

        # check if directories are filled or empty
        for run in sorted(runListInTestingFolder):
            RunFolderEmpty = False
            if os.path.isdir(str(abspath[i]) + "/"+str(run)) == True:
                if len(os.listdir(str(abspath[i]) + "/"+str(run)+"/")) == 0:
                    RunFolderEmpty = True
                if len(os.listdir(str(abspath[i]) + "/"+str(run)) ) == 1:
                    if os.path.isdir(str(abspath[i]) + "/"+str(run)+"/data18_13TeV."+str(run)+".calibration_IDTracks.merge.RAW") == True:
                        if len(os.listdir(str(abspath[i]) + "/"+str(run)+"/data18_13TeV."+str(run)+".calibration_IDTracks.merge.RAW")) == 0: RunFolderEmpty = True
                        else: RunFolderEmpty = False

            if RunFolderEmpty == True:
                runListInTestingFolder.remove(run)
                msg.printWarning("Despite the existence of "+str(abspath[i])+ ", the folder for run "+ str(run) + " is empty.")
    
        # runListInTestingFolder is a list that contains the list of runs availble at abspath[i]
        # abspath[i] is a list containg the the different folders of Tier0 for the indicated year

        msg.printInfo("   -> Runs to be processed: " + str(runListInTestingFolder))

        # Loop on all runs of this folder (abspath[i])
        if msg.getDebugLevel() == 0 and len(runListInTestingFolder) > 0: msg.printBold("Starting loop over all runs in the folder " + abspath[i])
        else: msg.printWarning("No requested run(s) in the folder: " + abspath[i] + "/") 

        runcount = 0
        for run in sorted(runListInTestingFolder): # this loop goes over all runs in the Tier0 folder
            # CAVEAT: run = int(run) #run is not an integer because some runs are named "3342466_backup"
            msg.printBlue("=======================================================================")
            msg.printBlue("======          Processing run: "+str(run)+"   ==   (%03d/%03d)        ======" %(runcount+1, len(runListInTestingFolder)))
            msg.printBlue("=======================================================================")
           
            thisRunInfoWasUpdated = False
 
            if reprocess and not RUNlist == ['']: # Case  "-r --run"
                if run in Dope.DB.keys():
                    msg.printInfo("The run " + str(run) + " was in the database " + str(config.runInfoDBfile))
                    msg.printInfo("Reprocessing run " + str(run) + "")

                    if msg.getDebugLevel() == 0:
                        msg.printRed("=======================================================================")
                        msg.printRed("Showing the old information of run " + str(run) + ":")
                        if debugLevel == 0: Dope.print_DB_values(run, "red")
                        msg.printRed("=======================================================================")

                    msg.printInfo("Reprocessing run " + str(run) + " info from " + str(config.runInfoDBfile))
                else: msg.printInfo("The run " + str(run) + " was not found in " + str(config.runInfoDBfile)+". New run. Initializing it.")

                msg.printDebug("Initializing run "+ str(run) + " in the DB ") # Reprocess case: initialise it
                Dope.initialize(run) # here the default values for the Dope.DB[run] are set
                Dope.add_element(run, 'project', dataProjectName)
                Dope.add_element(run, 'year', config.year)
                Dope.append_to_list('RunsWithNewData',run)
           
            if run not in Dope.DB.keys(): # Adding new runs in cases "--run", "-r" or "default"
                msg.printInfo("NEW RUN FOUND ** NEW RUN FOUND ** NEW RUN FOUND ** ")
                msg.printInfo("The run "+str(run)+" was not fund in " + str(config.runInfoDBfile) +". New run. Initializing it.")
                Dope.initialize(run)
                Dope.add_element(run, 'project', dataProjectName)
                Dope.add_element(run, 'year', config.year)
                Dope.append_to_list('RunsWithNewData',run)
            
            runcount += 1
            if (runcount > config.maxNumberOfRunsToAnalyze): continue

            if (runcount > len(runListInTestingFolder)): msg.getDebugLevel() == 0

            #if (run in runinfo.keys()): # The Object.keys() method returns an array of a given object's own enumerable properties
            # if run is in the runinfo.keys(), it means the run is already known and exists in the DB
            # - it may have not all info already filled
            # - or may be it has been reprocessed and needs an update
            # 

            # = Actions on existing runs =
                #
                # 1) check the beam spot handshake info for every already recorded run, in case it may need to be updated
                #
            if (run in Dope.DB.keys()):
                msg.printDebug("Run "+str(run)+" already exists in the DB")
                msg.printDebug("This is the BS HandShake info already existing for run "+ str(run) + " in DB file %s " %(config.runInfoDBfile))
                msg.printDebug(" + timestamp: " + Dope.DB[run]['bshandshake'])
                msg.printDebug(" + author: "+ Dope.DB[run]['bshsauthor'])
                Dope.DB[run]['bshandshake']='?'
                 # update the BS HandShake info if needed 
                if ('?' in Dope.DB[run]['bshandshake']):
                    msg.printWarning("Run "+ str(run) + " BS HandShake info still unknown --> inspect BS HandShake summary file!")
                    bstimestamp = config.ExtractBSHandShakeInfo(run, fileWithBSHandshakeInfo) # bstimestamp = ("date time" , "author")
                    if (bstimestamp[0] != "None"):
                        # store time stamp and author
                        #Dope.append_to_list('runBSHandShake',(run, bstimestamp[0], bstimestamp[1]))
                        #Dope.append_to_list('runsWithBSHSUpdate',run)
                        #msg.printInfo("Run "+ run + " has been updated with the BS HandShake data with "+ str(Dope.listOfRuns['runBSHandShake']))

                        # add information into the DB
                        Dope.add_element(run, 'bshandshake', bstimestamp[0])
                        Dope.add_element(run, 'bshsauthor', bstimestamp[1])
                        msg.printInfo( "    --- UPDATE --- run[%s]['bshandshake']= %s" %(run, Dope.DB[run]['bshandshake'])) 
                        msg.printInfo( "    --- UPDATE --- run[%s]['bshsauthor']= %s" %(run, Dope.DB[run]['bshsauthor']))

                    else: msg.printWarning("Run "+ str(run) + " BS HandShake info still unknown --> inspect BS HandShake summary file!")
                else: msg.printDebug("Run %s does not need to update the BS HandShake info " %run)

                #
                # 2) check the alignment constants and DB upload status for this run
                #
                # -- check if runAnalysisLog file exists for this run
                msg.printDebug("This is the DB uploading info alredy existing for run %s in DB file %s " % (run, config.runInfoDBfile))
                msg.printDebug(" + L11Results: "+ Dope.DB[run]['L11Results'])
                msg.printDebug(" + L16Results: "+ Dope.DB[run]['L16Results'] )
                msg.printDebug(" + DBsubmission: "+ Dope.DB[run]['DBsubmission']) 
                msg.printDebug(" + DBtimestamp: "+ Dope.DB[run]['DBtimestamp'] )
                msg.printDebug(" + analysisfile: "+ Dope.DB[run]['analysisfile'])

                # get the list of analysis log files for a given run
                analysisLogFiles = config.GetAnalysisLogFiles(run)
                if (len(analysisLogFiles)>0): # check whether the analysis log file exists
                    # if there are many files, for this run, take the last one
                    analysisLogFile = (analysisLogFiles[len(analysisLogFiles)-1]).rstrip() 
                    msg.printInfo("Run %s, analysisLogFile = %s (more updated one)" %(run,analysisLogFile))

                    # check if the analysis log file is newer than the stored one. If so the run info needs update
                    shortName = (analysisLogFile.split("/"))[-1]
                    updateThisRunInfo = False
                    if (shortName != Dope.DB[run]['analysisfile']):
                        updateThisRunInfo = True
                        msg.printInfo( "New analysis log file found for run "+run)
                        msg.printInfo( " + New file: " + shortName)
                        msg.printInfo( " + Old file: " + Dope.DB[run]['analysisfile'])

                        # add information into the DB
                        Dope.add_element(run, 'analysisfile', shortName)
                    else: msg.printDebug( "Analysis log file of run " + run + " is the same as the already stored:" + Dope.DB[run]['analysisfile'])

                    if updateThisRunInfo:
                        # check the analysis status of this runs
                        analysisStatus = config.ExtractAnalysisStatus(run, analysisLogFile)

                        # store time stamp, plus L11 and L16 status
                        Dope.append_to_list('runAnalysisStatus',(run, (analysisStatus[0], analysisStatus[1], analysisStatus[2], analysisStatus[3], shortName)))
                        Dope.append_to_list('runsWithAnalysisUpdate',run)
                        msg.printInfo( "runAnalysisStatus: " + str(Dope.listOfRuns['runAnalysisStatus']))

                        # add information into the DB
                        Dope.add_element(run, 'L11Results', analysisStatus[0])
                        Dope.add_element(run, 'L16Results', analysisStatus[1])
                        Dope.add_element(run, 'DBsubmission', analysisStatus[2])
                        Dope.add_element(run, 'DBtimestamp', analysisStatus[3])
                        Dope.add_element(run, 'DBtimestamp',shortName) 

                        msg.printDebug( "    --- UPDATE -1- run[%s]['L11Results']= %s" %(run, Dope.DB[run]['L11Results'])) 
                        msg.printDebug( "    --- UPDATE -2- run[%s]['L16Results']= %s" %(run, Dope.DB[run]['L16Results']) )
                        msg.printDebug( "    --- UPDATE -3- run[%s]['DBsubmission']= %s" %(run, Dope.DB[run]['DBsubmission'])) 
                        msg.printDebug( "    --- UPDATE -4- run[%s]['DBtimestamp']= %s" %(run, Dope.DB[run]['DBtimestamp']) )
                        msg.printDebug( "    --- UPDATE -5- run[%s]['DBAnalysisfile']= %s" %(run, Dope.DB[run]['analysisfile'])) 

                        mvAnalysisLogFile_cmd = "cp %s%s %s%s" %(config.analysisLogFilesFolder, analysisLogFile, config.runAnalysisLogFolder, shortName)
                        # msg.printDebug("execute command: " + mvAnalysisLogFile_cmd)
                        (command_status, command_output) = commands.getstatusoutput(mvAnalysisLogFile_cmd)
                        if (command_status !=0):
                            msg.printERROR( "Problem occured during: " + mvAnalysisLogFile_cmd)
                            msg.printERROR(" --> "+ command_output)
                        else:
                            # RunsWithNewData is the list of new runs found or runs with new
                            # data (ie, calibloop did not finished by the time of last update)
                            Dope.append_to_list('RunsWithNewData',run)
                    # up to here if update is needed
                    else:
                        msg.printInfo( "Run %s does not need an update of the L11 and L16 analysis info: (%s)" %(run, shortName))
                else:
                    msg.printInfo ("No analysisLogFiles found for run: "+run)

                #
                # check if there was some update since the last time the info of this run was filled  
                # by testing the record date
                #
                folderOfThisRun = "%s/%s" % (abspath[i],run)
                theLatestUpdateTime = time.ctime(os.path.getmtime(folderOfThisRun))
                msg.printInfo( "Calib loop folders of run %s last modified: %s" %(run, theLatestUpdateTime))
                msg.printInfo( " + DB info runinfo[%s][runRecordDate]= %s" %(run, Dope.DB[run]['runRecordDate']))
                if (theLatestUpdateTime not in Dope.DB[run]['runRecordDate']):
                    Dope.append_to_list('runsWithNewRecordDate',run) #runsWithNewRecordDate flags runs that have some update in the calib loop folder
                    Dope.append_to_list('runRecordDate',(run, theLatestUpdateTime))
                
                    # add information into the DB
                    Dope.add_element(run, 'runRecordDate', theLatestUpdateTime)
                    msg.printInfo("Calib loop data of run %s has been updated recently (at %s)" %(run, theLatestUpdateTime))
                else:
                    msg.printInfo("Run %s does not need an update of calib loop data (last update: %s)" %(run, theLatestUpdateTime))
            #  - here ends the activities in already existing runs recorded in the DB file -

            # ================================================================================================
            # - Now loop on NEW runs and on those that need an update of the calibration loop details
            # ================================================================================================
            if (run in Dope.listOfRuns['runsWithNewRecordDate']):
                msg.printInfo("** RUN %s NEEDS UPDATE OF CALIB LOOP RECORDS ** " %(run))
                #
                # 1) check the output of the calibration loop
                #
                calibLoopContent = os.popen("ls %s/%s" % (abspath[i],run)).readlines() # for 2017 .tgz files exist
                msg.printDebug( "Lists of folders (calibLoopContent) for run " + run + " (total: " + str(len(calibLoopContent))+" folders)")
                for thiscontent in calibLoopContent:
                    msg.printDebug( " - %s" %(thiscontent.rstrip()))
                msg.printDebug( " - end of list - of existing folders for run "+run )
                #
                # Usually each run is processed just once, but it could be that some runs are processed more than once due to some 
                # change in the conditions or whatever. Each time the calibrationLoop is run it produces a set of folders, so one has 
                # to keep the last. It is possible to recognize each pass by the suffix c0, c1, c... of the folders
                # Therefore: check all folders and find the last update (by checking the suffix)
                currentSuffixID = 0
                if (len(calibLoopContent)>1): # check there is more than one file
                    for thiscontent in calibLoopContent:
                        if (thiscontent.rstrip()[-2] == "c"):
                            thisSuffixID = int(thiscontent.rstrip()[-1])
                            if (thisSuffixID > currentSuffixID):
                                currentSuffixID = thisSuffixID
                                msg.printDebug("New suffix ID found for the calibration loop processed folders: "+ str(currentSuffixID))
                processSuffixID = "c%d" % currentSuffixID
                msg.printDebug("Suffix ID of the calibration loop processed folders: %s " % processSuffixID)
                # now that the suffix is known, extract the list of folders that belong to the processing (of that suffix)
                calibLoopContent = commands.getoutput("ls -d %s/%s/*.%s" % (abspath[i],run,processSuffixID)).splitlines()
                # print calibLoopContent
                if 'No such file or directory' in calibLoopContent[0]: # For 2017 case
                    calibLoopContent = commands.getoutput("ls -d %s/%s/*.%s.tgz" % (abspath[i],run,processSuffixID)).splitlines()
                # for i in calibLoopContent: msg.printDebug(i) 
                msg.printDebug("List of folders (calibLoopContent) with suffix " + processSuffixID + " for run " + run + " (total "+ str(len(calibLoopContent))+" folders)" )
                for thiscontent in calibLoopContent:
                    msg.printDebug( " - %s" %(thiscontent.rstrip()))
                    if 'cannot access' in (thiscontent.rstrip()):
                        msg.printError("Could not accsses to the calibration loop content. Please, check the path: %s/%s/*.%s.tgz" %((abspath[i],run,processSuffixID)))
                msg.printDebug(" - end of list - of existing folders for run "+run) 

                # For 2016 reprocessing (November 2016) some files come out wit c00 sufix instead of c0.
                # so if the suffix "x" was decided but the numbers of files is 0 --> then try c0x
                if len(calibLoopContent)==0:
                     processSuffixID = "c%02d" % currentSuffixID
                     calibLoopContent = os.popen("ls -d %s/%s/*.%s" % (abspath[i],run,processSuffixID)).readlines()
                     msg.printDebug( "New suffix scheme !!! -> use "+  processSuffixID)
                     
                if len(calibLoopContent)>1:
                    # this already contains some folders. May be its processing at the calibration loop is already finished. But may be it is a new run
                    # so the information is partial and new folders and data will appear later. 
                    # let's grab the already existing info

                    msg.printDebug(" ----------------------------------------------------------------------------------------------------------------")
                    msg.printDebug(" -- START LOOP - on 'calibLoopContent' for run: " + run + " (remember it has in total: "+str(len(calibLoopContent))+" folders) --")
                    msg.printDebug(" -- Based directory = %s/%s/ --" % (abspath[i],run))
                    msg.printDebug(" ----------------------------------------------------------------------------------------------------------------")

                    mycounter = 0;
                    for directory in calibLoopContent:
                        mycounter += 1
                        if (mycounter>1000) or (mycounter > len(calibLoopContent)): 
                            msg.printFatal( " - Early exit - Many folders processed - Early exit -")
                            exit() 
                        if  not config.localtest: msg.printDebug( "Dealing with contents of folder ->>"+ directory.rstrip() + "<<-")

                        # --------------------------
                        # Load the monitoring files
                        # --------------------------
                        # func_idalignmerge: If necessary, it appends the run to the lists 'runsWithMonitoringIterXmissing' and 'listOfRunsWithNewData'
                        #Dope.PrintListOfRuns()
                        msg.printInfo("In subdirectory = " + directory.split('/')[-1])

                        if not 'runsWithMonitoringIter0missing' in Dope.listOfRuns: Dope.listOfRuns['runsWithMonitoringIter0missing'] = []
                        if not 'monitoringFilesIter0' in Dope.listOfRuns: Dope.listOfRuns['monitoringFilesIter0'] = {}
                        if not 'runsWithMonitoringIter1missing' in Dope.listOfRuns: Dope.listOfRuns['runsWithMonitoringIter1missing'] = []
                        if not 'monitoringFilesIter1' in Dope.listOfRuns: Dope.listOfRuns['monitoringFilesIter1'] = {}
                        if not 'runsWithMonitoringIter2missing' in Dope.listOfRuns: Dope.listOfRuns['runsWithMonitoringIter2missing'] = []
                        if not 'monitoringFilesIter2' in Dope.listOfRuns: Dope.listOfRuns['monitoringFilesIter2'] = {}
                        if not 'runsWithMonitoringIter3missing' in Dope.listOfRuns: Dope.listOfRuns['runsWithMonitoringIter3missing'] = []
                        if not 'monitoringFilesIter3' in Dope.listOfRuns: Dope.listOfRuns['monitoringFilesIter3'] = {}

                        for j in range(0, Dope.numOfIters):
                            if "idalignmerge.ROOT_MON.Iter%d" % j in directory:
                                msg.printInfo((" + New idalignmerge.ROOT_MON.Iter%d for run " % j) + run + ' found!')
                                Dope.func_idalignmerge(directory, j, run,'runsWithMonitoringIter%dmissing' % j,'monitoringFilesIter%d' % j)

                        # --------------------------------------------------------
                        # Load the alignlog files with alignment constants results
                        # --------------------------------------------------------
                        if not 'runsWithConstantsIter0missing' in Dope.listOfRuns: Dope.listOfRuns['runsWithConstantsIter0missing'] = []
                        if not 'runsWithConstantsIter2missing' in Dope.listOfRuns: Dope.listOfRuns['runsWithConstantsIter2missing'] = []    
                                
                        # -> extract alignlogfiles from the TAR_FILES --> Iter0
                        if "idalignsolve.TAR_ALIGNFILES.Iter0" in directory:
                            Dope.ExtractAlignLogFiles_B(run,0, directory,config.server_alignfiles,logicName[i],'runsWithConstantsIter0missing')

                        if (run in Dope.listOfRuns['runsWithConstantsIter0missing']): # 'runsWithConstantsIter0missing' contains a set of runs and 'constantsFile' is a dictionary which relates those runs to an alignlogfileIter0.txt
                            Dope.add_element(run, 'constantsFile',Dope.listOfRuns['constantsFile'][run])
                            thisRunInfoWasUpdated = True
                            msg.printDebug( "    --- UPDATE --- Iter0 constants -- run[%s]['constantsFile']= %s" %(run, Dope.DB[run]['constantsFile']))
                                    
                        # -> extract alignlogfiles from the TAR_FILES --> Iter0 (second time dunno why)
                        msg.printDebug(" + New :: check if idalignsolve.TAR_ALIGNFILES.Iter0 is in runcontent")
                        if "idalignsolve.TAR_ALIGNFILES.Iter0" in directory:
                            Dope.ExtractAlignLogFiles_A(run,0, directory,config.server_alignfiles,logicName[i],'runsWithConstantsIter0missing')

                            
                        # -> extract alignlogfiles from the TAR_FILES --> Iter2    
                        msg.printDebug("Check if idalignsolve.TAR_ALIGNFILES.Iter2 is in runcontent")
                        if "idalignsolve.TAR_ALIGNFILES.Iter2" in directory:
                             Dope.ExtractAlignLogFiles_A(run,2, directory, config.server_alignfiles,logicName[i],'runsWithConstantsIter2missing') 
                             
                    # monitoringFilesIterX
                    thisRunInfoWasUpdated= Dope.func_UpdateIterB(run, 0,'runsWithMonitoringIter0missing','monitoringFileIter0','monitoringFilesIter0')
                    thisRunInfoWasUpdated= Dope.func_UpdateIterB(run, 1,'runsWithMonitoringIter1missing','monitoringFileIter1','monitoringFilesIter1')
                    thisRunInfoWasUpdated= Dope.func_UpdateIterB(run, 2,'runsWithMonitoringIter2missing','monitoringFileIter2','monitoringFilesIter2')
                    thisRunInfoWasUpdated= Dope.func_UpdateIterB(run, 3,'runsWithMonitoringIter3missing','monitoringFileIter3','monitoringFilesIter3')

                    # constantsFilesIterX
                    if (run in Dope.listOfRuns['runsWithConstantsIter0missing']):
                        Dope.add_element(run, 'constantsFileIter0', config.ExtractLBGroupFiles(run,Dope.listOfRuns['constantsFilesIter0']))
                        thisRunInfoWasUpdated = True
                        msg.printDebug( "    --- UPDATE --- Iter0 constants -- run[%s]['constantsFileIter0']= %s" %(run, Dope.DB[run]['constantsFileIter0']))

                    if (run in Dope.listOfRuns['runsWithConstantsIter2missing']):
                        Dope.add_element(run, 'constantsFileIter2',config.ExtractLBGroupFiles(run, Dope.listOfRuns['constantsFilesIter2']))
                        thisRunInfoWasUpdated = True
                        msg.printDebug( "    --- UPDATE --- Iter2 constants -- run[%s]['constantsFileIter2']= %s" %(run, Dope.DB[run]['constantsFileIter2']))
                    
                    # up to here: actions for runs with many folders ending with cX (X for the processing step)

                else:
                    # this run contains only one file or folder --> keep a record of it an wait till it may get more data
                    msg.printInfo("Run %s has no calib loop folders " %run )
                    if ('RunsWithNewData' not in Dope.listOfRuns): Dope.append_to_list('RunsWithNewData',run)
                    if (run not in Dope.listOfRuns['RunsWithNewData']): Dope.append_to_list('RunsWithNewData',run) 
                    if ('runsWithNewRecordDate' not in Dope.listOfRuns or run not in Dope.listOfRuns['runsWithNewRecordDate']):
                        folderOfThisRun = "%s/%s" % (abspath[i],run)
                        theLatestUpdateTime = time.ctime(os.path.getmtime(folderOfThisRun))
                        #Dope.append_to_list('runsWithNewRecordDate',run)
                        Dope.append_to_list('runRecordDate',(run, theLatestUpdateTime))
                        msg.printDebug("Calib loop folders of run %s last modified: %s" %(run, theLatestUpdateTime))
                        for element in Dope.listOfRuns['runRecordDate']: 
                            if (element[0] == run):
                                Dope.add_element(run, 'recorddate', element[1])
                        msg.printDebug("    --- UPDATE --- run[%s]['recorddate']= %s" %(run, Dope.DB[run]['recorddate']))

            # Up to here, these were the actions for the new runs and for runs with a new record date (updated runs)    
            # this closes the if clause: if ((run not in runinfo.keys()) or (run in runsWithNewRecordDate)):
    
            Dope.add_element(run, 'stream',dataStreamName)    # This changes, therefore this has to be update everytime
            Dope.add_element(run, 'processing', logicName[i]) # This changes, therefore this has to be update everytime
           
            # retrieve run information from AMI
            ami.getDataPeriodsForRun(run)
            ami.getDatasetInfo(run, dataProjectName, dataStreamName)
            ami.printAmiDB(run)

            # The class amiServer has a self.DB={} that works like the one of RunInfo
            msg.printDebug(" Checking if an update on period and/or subperiod is necessary for run " + str(run))
            if '?' in Dope.DB[run]['period']  or '?' in Dope.DB[run]['subperiod'] :
                msg.printDebug(" Run " + str(run) + " need and update from AMI for:")
               
                if '?' in Dope.DB[run]['period']  and  '?' in Dope.DB[run]['subperiod'] :
                    msg.printDebug("   - The period")
                    msg.printDebug("   - The subperiod")
                    if int(run) in ami.DB.keys():
                        if '?' not in  ami.DB[int(run)]['level2']['period'] and 'period' in  ami.DB[int(run)]['level2']:
                            Dope.add_element(run, 'period', ami.DB[int(run)]['level2']['period'])
                            thisRunInfoWasUpdated = True
                            #if (run not in Dope.listOfRuns['RunsWithNewData']): Dope.append_to_list('RunsWithNewData',run)
                        else:
                            msg.printDebug("The period for run " +str(run) + " is not available in AMI")
                            Dope.append_to_list('runsWithPeriodMissing',run)
                        if '?' not in ami.DB[int(run)]['level1']['period'] and 'period' in  ami.DB[int(run)]['level1']:
                            Dope.add_element(run, 'subperiod', ami.DB[int(run)]['level1']['period'])
                            thisRunInfoWasUpdated = True
                            #if (run not in Dope.listOfRuns['RunsWithNewData']): Dope.append_to_list('RunsWithNewData',run)
                        else:
                            msg.printDebug("The subperiod for run " +str(run) + " is not available in AMI")
                            Dope.append_to_list('runsWithPeriodMissing',run)
                    else:
                        msg.printDebug("The info of run " + str(run) + " was not found in AMI")
                        #Dope.append_to_list('runsWithPeriodMissing',run)

                if '?' in Dope.DB[run]['period']  and '?' not  in Dope.DB[run]['subperiod']:
                    msg.printDebug("   - The subperiod")
                    if int(run) in ami.DB.keys():
                        if '?' not in ami.DB[int(run)]['level1']['period']  and 'period' in  ami.DB[int(run)]['level1']: 
                            Dope.add_element(run, 'subperiod', ami.DB[int(run)]['level1']['period'])
                            thisRunInfoWasUpdated = True
                            #if (run not in Dope.listOfRuns['RunsWithNewData']): Dope.append_to_list('RunsWithNewData',run)
                        else:
                            msg.printDebug("The subperiod for run " +str(run) + " is not available in AMI")
                            #Dope.append_to_list('runsWithPeriodMissing',run)
                    else: msg.printWarning("The info of run " + str(run) + " was not found in AMI")

                if '?' not in Dope.DB[run]['period']  and '?' in Dope.DB[run]['subperiod'] :
                   msg.printDebug("   - The period")
                   if int(run) in ami.DB.keys():
                       if '?' not in  ami.DB[int(run)]['level2']['period'] and 'period' in  ami.DB[int(run)]['level2']:
                           Dope.add_element(run, 'period', ami.DB[int(run)]['level2']['period'])
                           thisRunInfoWasUpdated = True
                           if (run not in Dope.listOfRuns['RunsWithNewData']): Dope.append_to_list('RunsWithNewData',run)
                       else:
                           msg.printDebug("The period for run " +str(run) + " is not available in AMI")
                           #Dope.append_to_list('runsWithPeriodMissing',run)
                   else: msg.printDebug("The info of run " + str(run) + " was not found in AMI")
            else: msg.printDebug(" No update is necessary on period and/or subperiod for run " +  str(run))
            
            
            
            if 'lastModified' in ami.DB[int(run)].keys():
                if '?' in Dope.DB[run]['amiStatus'] or '?' in Dope.DB[run]['totalEvents'] or '?' in Dope.DB[run]['creationTime']  or '?' in Dope.DB[run]['totalSize']  or '?' in Dope.DB[run]['nFiles'] or '?' in Dope.DB[run]['lastModified'] or not  Dope.DB[run]['lastModified'] == ami.DB[int(run)]['lastModified']:
                    msg.printDebug(" Run " + str(run) + " need and update from AMI for:")
                    msg.printDebug("   - The amiStatus")
                    msg.printDebug("   - The totalEvents")
                    msg.printDebug("   - The creation time")
                    msg.printDebug("   - The totalSize")
                    msg.printDebug("   - The nFiles")
                    msg.printDebug("   - The last modification time")
                    if '?' not in  ami.DB[int(run)]['amiStatus'] and 'amiStatus' in  ami.DB[int(run)]:
                        Dope.add_element(run, 'amiStatus', ami.DB[int(run)]['amiStatus'])
                    else:
                        msg.printDebug("The amiStatus for run " +str(run) + " is not available in AMI")
                    if '?' not in  ami.DB[int(run)]['totalEvents'] and 'totalEvents' in  ami.DB[int(run)]:
                        Dope.add_element(run, 'totalEvents', ami.DB[int(run)]['totalEvents'])
                    else:
                        msg.printDebug("The events for run " +str(run) + " is not available in AMI")
                    if '?' not in  ami.DB[int(run)]['created'] and 'created' in  ami.DB[int(run)]:
                        Dope.add_element(run, 'creationTime', ami.DB[int(run)]['created'])
                    else:
                        msg.printDebug("The creation time for run " +str(run) + " is not available in AMI")
                    if '?' not in  ami.DB[int(run)]['totalSize'] and 'totalSize' in  ami.DB[int(run)]:
                        Dope.add_element(run, 'totalSize', ami.DB[int(run)]['totalSize'])
                    else:
                        msg.printDebug("The total size for run " +str(run) + " is not available in AMI")
                    if '?' not in  ami.DB[int(run)]['nFiles'] and 'nFiles' in  ami.DB[int(run)]:
                        Dope.add_element(run, 'nFiles', ami.DB[int(run)]['nFiles'])
                    else:
                        msg.printDebug("The nFiles for run " +str(run) + " is not available in AMI")
                    if '?' not in  ami.DB[int(run)]['lastModified'] and 'lastModified' in  ami.DB[int(run)]:
                        Dope.add_element(run, 'lastModified', ami.DB[int(run)]['lastModified'])
                        thisRunInfoWasUpdated = True
                    else:
                        msg.printDebug("The time of last modification for run " +str(run) + " is not available in AMI")

            # check if date was set for runs in problematic_runs
            if ("problematic_runs" in abspath[i]):
                Dope.append_to_list('runsWithDateMissing',run)
                path = "%s/%s" %(abspath[i], run)
                Dope.append_to_list('runDate',(run, time.strftime("%d/%b/%Y",time.localtime(os.stat(path)[8]))))
                msg.printDebug("      --> DB key 'run' set for run: " +  run + str(Dope.listOfRuns['runsWithDateMissing']) +str( Dope.listOfRuns['runDate']))
                for element in Dope.listOfRuns['runDate']:
                    if (element[0] == run):
                        Dope.add_element(run, "date",element[1])
                        thisRunInfoWasUpdated = True
                msg.printDebug( "    --- UPDATE --- run[%s]['date']= %s" %(run, Dope.DB[run]['date']))
                
            if (thisRunInfoWasUpdated):
                Dope.add_element(run, "thisdbrecordtimestamp",time.localtime(time.time()))
                msg.printInfo(" runinfo timestamp: "+ str(Dope.DB[run]['thisdbrecordtimestamp']))

            #Dope.add_element(run, "monitoringFileIter1",'?') #for test

        ## End of loop over runListInTestFolder ##
                   
            msg.printGreen("=======================================================================")
            Dope.print_DB_values(run)
            msg.printGreen("=======================================================================")

        #
        # Now, store the runinfo data into the DB file
        #
        if (len(Dope.listOfRuns['RunsWithNewData'])>0): # we only store the data if there is something to be stored
            if msg.getDebugLevel() == 0: msg.printBold("Store the data from DB into the %s file" % (config.server + config.runInfoDBfile))
            msg.printInfo("=======================================================================")
            msg.printInfo("== dumping runInfo data on DB file: "+ config.runInfoDBfile)
            msg.printInfo("== runs in folder: " + abspath[i])
            msg.printInfo("=======================================================================")
            try:
                pickle.dump(Dope.DB,open(config.server + config.runInfoDBfile, 'w'))
                msg.printBold("Storing information from runs" + str(Dope.listOfRuns['RunsWithNewData']) +" into " + str(config.runInfoDBfile) +" --> SUCCESS!")
            except:
                msg.printError("something fishy happened while pickle.dump to " + config.server + config.runInfoDBfile)                 
        else:
            # touch runInfoDBfile -> web page will show a new time.
            config.Touch(config.server + config.runInfoDBfile)
            msg.printInfo("The modification date of %s has been updated!" % (config.server + config.runInfoDBfile))
    return


# =================================================================================
#  __main__
# =================================================================================
if __name__ == '__main__':
  main(sys.argv[1:])

