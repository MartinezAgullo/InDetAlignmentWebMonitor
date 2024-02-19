#!/usr/bin/env python
import os, sys, commands, datetime, threading
try: import cPickle as pickle
except: import pickle
from optparse import OptionParser

from InDetAlignmentWebMonitor.ConfigServer import configServer
from InDetAlignmentWebMonitor.MsgHelper import msgServer
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
    parser.add_option("-r", "--rebuild", action="store_true", dest="rebuild", default=False,
                      help="rebuild the merging of the monitoring ROOT files [default: %default]")
    parser.add_option("-d", "--debugLevel", dest="debugLevel", default=0, type="int",
                      help="set debug level (DEBUG=0, INFO=1, WARNING=2, ERROR=3, FATAL=4) [default: %default]", metavar="LEVEL")
    parser.add_option("-t", "--localtest", action="store_true", dest="localtest", default=False,
                      help="run a local test [default: %default]")
    (options, args) = parser.parse_args()

    global msg
    msg = msgServer('make_plots', options.debugLevel)

    global config
    config = configServer(options.year, options.configfile, options.workingDir, options.localtest, options.debugLevel)
    config.printConfig()
    
    # rebuild the merged file with all monitoring files from the LB groups
    global rebuild
    rebuild = options.rebuild

    global utilities
    utilities = utils(options.debugLevel)

    # create the monitoring directory
    utilities.createDir(config.monitoringFolderName)

    # check if the athena release is well configured
    utilities.checkAthenaRelease()

    # prepare RUNlist
    if options.RUNlist == '': options.RUNlist = []
    else: options.RUNlist = options.RUNlist.replace(' ','').split(',')

    # update runs for the InDetAlignmentWebMonitor package
    MakePlots(options.RUNlist, options.debugLevel)
    config.endBanner()

# =================================================================================
#  MakePlots
# =================================================================================
def MakePlots(RUNlist, debugLevel):
    msg.printDebug('In MakePlots()')

    # read the database file (server_runinfo20XX.db) that is generated by update_runs.py
    try:
        runinfo_database = pickle.load(open(config.server + config.runInfoDBfile, 'r'))
        msg.printBold("Run info file %s succesfully read!" % config.runInfoDBfile)

        # for key in runinfo_database: # Uncomment these lines to see  runinfo_databas
        #     #msg.printDebug("Run: " + str(key))
        #     if key == 354359 or key == '00354359':
        #         msg.printInfo("Viewing information of run " + str(key))
        #         for value in runinfo_database[key]:
        #             print value + ':' + str(runinfo_database[key][value])
        # exit()
        
    except IOError:
        msg.printFatal("Run info file %s not found!" % config.runInfoDBfile)
        exit()

    # create directory for plots
    utilities.createDir(config.detailed_plots)
    msg.printInfo("Directory %s succesfully created!" % config.detailed_plots)
    plotsDBFile = config.detailed_plots + "plots" + config.year +".db"
    msg.printGreen("Information about the plots will be saved in: " + str(plotsDBFile))
    try:
        plotdatabase = pickle.load(open(plotsDBFile, 'r'))
        msg.printBold(" + PlotsDB file %s --> loaded successfully!" % plotsDBFile)
        if rebuild:
            if (options.RUNlist) == 0: msg.printWarning(" -> PlotsDB will be rebuilt for all runs stored in %s!" % config.runInfoDBfile)
            else:
                msg.printWarning(" -> PlotsDB will be rebuilt for runs: %s" % str(options.RUNlist))

        #for key in plotsDBFile: # Uncommet these lines to see the plotdatabase
        #    if key == 354359 or key == '00354359':
        #        print "---- Checking that the info is properly stored ----"
        #        msg.printInfo(key)
        #        for value in plotsDBFile[key]:
        #            msg.printDebug(str(value) + ":" + str(plotsDBFile[key][value]))
        #exit()
                 
    except:
        plotdatabase = {}
        msg.printInfo(" + New PlotsDB file is created: %s" % plotsDBFile)

    k = 0
    nRunsProcessed = 0 #initialization
    updates = []
    maxFilesAcceptedByMonitoring = 9
    maxNrunsToBeProcessed = 999
    maxRun = 999999
    
    msg.printDebug("Max number of runs to be processed: %d" %(maxNrunsToBeProcessed))

    trackCollection = "ExtendedTracks_alignSelection"
    msg.printDebug("Track collection used in monitoring: %s" %(trackCollection))
    
    # markers
    # The color and shape of markers must be defined to an integer becuase utilites.py only understands this type of variable
    global markerList
    markerList = ["kOpenTriangleDown", "kOpenCross", "kOpenCross", "kOpenSquare"] # markers for Iter0, Iter1, Iter2 and Iter 3
    markerList = [32, 28, 28, 25] # This redefiniton of markerList is done using the name-integer correspondence
    global colorList
    colorList = ["kGray+3", "kAzure+2", "kAzure+2", "kRed"] # colors for Iter0, Iter1, Iter2 and Iter3
    colorList = [923, 862, 862, 632] # This redefiniton of the color is done using the name-integer correspondence

    # database keys
    # msg.printDebug("plotdatabase.keys() list=" + str(plotdatabase.keys()))

    if len(RUNlist) == 0: msg.printDebug( "All runs in %s will be processed within the make_plots.py loop: " % config.runInfoDBfile)
    else: msg.printDebug( "List of runs to be processed within the make_plots.py loop: " + str(RUNlist))

    ################ loop over runs to create folders ###########
    msg.printInfo("==================================================================================================")
    msg.printInfo("==                                  Monitoring plots                                            ==")
    msg.printInfo("==================================================================================================")
    for run in sorted(runinfo_database, reverse=True):
        if len(RUNlist) > 0 and str(run) not in RUNlist and str(int(run)) not in RUNlist:
            msg.printDebug( " - run number to be ignored: %s" % (run))
            continue
        else:
            if len(RUNlist) > 0:
                msg.printDebug( " - run number to be used in the plotter: %s" % (run))

        try:
            maxRunTester = int(run) # The reprocesed runs are strings that cannot be converted to integer
            if maxRunTester > maxRun:
                msg.printDebug("Run "+str(run) + " > max run: continue")
                continue
        except:
            msg.printDebug("The run " + str(run) + " is a reporcessed run.") #That is why we could not convert it to an integer
        nRunsProcessed += 1

        #if debugLevel == 0:
        #    for key in runinfo_database: # Uncomment these lines to see  runinfo_databas
        #        msg.printGreen("------")
        #        msg.printDebug(" Run: " + str(key))
        #        msg.printInfo(" Viewing information of run " + str(key))
        #        for value in sorted(runinfo_database[key]):
        #            print "  +" + str(value) + ' : ' + str(runinfo_database[key][value])
        #        msg.printGreen("------")
        #exit()

        if nRunsProcessed <= maxNrunsToBeProcessed:
            msg.printBlue("%02d. Processing run: %s" % (nRunsProcessed, str(run)))

            msg.printDebug("=======================================================================")
            msg.printDebug("Information stored in the database (" + config.runInfoDBfile + ") about the run " + str(run) + ':')
            for key, value in runinfo_database[run].iteritems(): msg.printDebug(" + DB." + key + ": " + str(value))
            msg.printDebug("=======================================================================")
                
            # create a directory/folder to store the png files
            # add processing name (logical name) and then check
            # add run number and then check
            folderForThisRun = "%s%s/%s" %(config.detailed_plots, runinfo_database[run]['processing'] ,run)
            msg.printInfo(" + Directory %s succesfully created!" % folderForThisRun)
            utilities.createDir(folderForThisRun)

            # loop over runs to merge LB group files plots
            msg.printDebug (" + %02d. Merging monitoring files for run: %s" % (nRunsProcessed, str(run)))

            # create folder to store merged monitoring files
            mergedFilesFolder = "%s/%s/%s" %(config.mergedFilesFolder, runinfo_database[run]['year'], runinfo_database[run]['processing'])
            utilities.createDir(mergedFilesFolder)
            msg.printInfo(" + Directory %s succesfully created!" % mergedFilesFolder)

#            # merge all the different LB group monitoring files in just one for the entire run
#            doMultiThreading = True
#            if doMultiThreading:
#                threads = list()
#                for i in [0, 2, 3]:
#                    t = threading.Thread(target=mergeLBGroupMonitoringFiles, args=(runinfo_database,run, i))
#                    threads.append(t)
#                
#                # start all threads
#                for t in threads: t.start()
#                
#                msg.printInfo("Merging ROOT monitoring files with differnt LB... please be patient!")
#                
#                # wait for all of them to finish
#                for t in threads: t.join()
#            else:
#                msg.printInfo("Merging ROOT monitoring files with differnt LB... please be patient!")
#                iter0Status, iter0MergedFile = mergeLBGroupMonitoringFiles(runinfo_database, run, 0) # Iter0 --> initial
#                iter2Status, iter2MergedFile = mergeLBGroupMonitoringFiles(runinfo_database, run, 2) # Iter2 --> After L11
#                iter3Status, iter3MergedFile = mergeLBGroupMonitoringFiles(runinfo_database, run, 3) # Iter3 --> After L16

            # produce monitoring plots
            msg.printBlue(" + %d. Producing monitoring plots for run: %s" % (nRunsProcessed, str(run)))

            # check the status of this run in the plots database
            plotsOfThisRunAlreadyDone = True
            try:
                msg.printDebug("Keys in: " + plotsDBFile + " = "+ str(plotdatabase.keys()))
                msg.printDebug("Values in " + plotsDBFile + " for " + str(run) + " = "+ str(plotdatabase[run]))

                # check if there is some circumstance for plots to be reapeated
                msg.printDebug(" + Cheking if there is any circumstance for the plots to be repeated)")
                if (plotdatabase[run]['iter0'] == 0): plotsOfThisRunAlreadyDone = False 
                if (plotdatabase[run]['iter2'] == 0): plotsOfThisRunAlreadyDone = False
                if (plotdatabase[run]['iter3'] == 0): plotsOfThisRunAlreadyDone = False
                if (plotdatabase[run]['residuals']>0): plotsOfThisRunAlreadyDone = False
                if (plotdatabase[run]['hits']>0): plotsOfThisRunAlreadyDone = False
                if (plotdatabase[run]['hitmaps']>0): plotsOfThisRunAlreadyDone = False
                if (plotdatabase[run]['iblres']>0): plotsOfThisRunAlreadyDone = False
                if (plotdatabase[run]['resmaps']>0): plotsOfThisRunAlreadyDone = False
                if rebuild == True: plotsOfThisRunAlreadyDone = False
                #print "plotsOfThisRunAlreadyDone = " + str(plotsOfThisRunAlreadyDone) #test
            except:
                msg.printDebug(" + There is no information in %s about run %s yet!" % (plotsDBFile, str(run)))
                plotsOfThisRunAlreadyDone = False
            
            if plotsOfThisRunAlreadyDone: # plotsOfThisRunAlreadyDone is a boolean
                msg.printDebug (" + Monitoring plots for run %s already exist!" % str(run))
                continue # If we already have this plots for this run we do not create the again
            
            # file1 <- Initial LB group
            # file2 <- AfterL11 LB group
            # file3 <- AfterL16 LB group

            file1 = runinfo_database[run]["monitoringFileIter0"] # Iter0 
            file2 = []
            file2.append(runinfo_database[run]["monitoringFileIter1"][0]) # Iter1 :: for the AfterL11  we only use one LB (we take the first LB of the list)
            file3 = runinfo_database[run]["monitoringFileIter3"] # Iter3
            #The file 1 is used to later define the input files. We must notice that currently we are using the '/afs/cern.ch/user/atlidali' files, which are not the files we merged.
      
            #msg.printDebug("Run = " + str(run))  # Checker: Uncoment to see this run information
            #for entrada in runinfo_database[run]:
            #    msg.printDebug(str(entrada)+" : "+ str(runinfo_database[run][entrada]))

            msg.printDebug(" len(file1) = " +  str(len(file1)) + " --> " + str(file1))               
            msg.printDebug(" len(file2) = " +  str(len(file2)) + " --> " + str(file2))
            msg.printDebug(" len(file3) = " +  str(len(file3)) + " --> " + str(file3))

            # - third step: build the options to pass them to MakeMajorAlignMonPlots.py

            # this superseedes all the above for the new IDAlignment scheme at tier 0 with split LB even at L1
            # the code needs some clean up (Salva, 22/September/2016)
            # Pablo: The func SampleTheMonitoringFiles needs to be fixed (comments about it in the fuction itself) 
            (listOfInputFiles, listOfMarkers, listOfColors, listOfLabels,nMonitoringFilesUsed) = SampleTheMonitoringFiles(file1, file2, file3)
            listOfText = " --canvasText 'IDAlignCalibLoop Run_%s %s'" %(str(run), trackCollection)

            msg.printDebug("============== SUMMARY ================================================")
            msg.printDebug(" nMonitoringFilesUsed = " + str(nMonitoringFilesUsed))
            msg.printDebug(" list of markers: " + str(listOfMarkers))
            msg.printDebug(" list of colors: " + str(listOfColors))
            msg.printDebug(" list of labels: " + str(listOfLabels))
            msg.printDebug(" list of text "+ str(listOfText))
            msg.printDebug("=======================================================================")

            # basic string with MakeMajorAlignMonPlots options
            if "_backup" in run:
                stringOptions = str(listOfInputFiles) + str(listOfMarkers) + str(listOfColors) + str(listOfLabels) + str(listOfText)
                stringOptions += " --inputFolder run_"+str(run)+"  --inputTrackCollection "+str(trackCollection)+" --outputFolder "+str(folderForThisRun)
            else:
                stringOptions = str(listOfInputFiles) + str(listOfMarkers) + str(listOfColors) + str(listOfLabels) + str(listOfText)
                stringOptions += " --inputFolder run_"+str(int(run))+"  --inputTrackCollection "+str(trackCollection)+" --outputFolder "+str(folderForThisRun)
                
            # if config.localtest == False: stringOptions += " --WebMonitoring"
            stringOptions += " --WebMonitoring"

            common_cmd = 'python ' + 'MakeMajorAlignMonPlots.py '
            
            residuals_stringOptions = stringOptions + " --Residuals --Extended --Prefix RESIDUALS_ "
            residuals_cmd = common_cmd + residuals_stringOptions
               
            hits_stringOptions = stringOptions + " --Hits --Prefix HITS_ "
            hits_cmd = common_cmd + hits_stringOptions
            
            hitmaps_stringOptions = stringOptions + " --HitMaps --Prefix HITMAPS_ "
            hitmaps_cmd = common_cmd + hitmaps_stringOptions
            
            iblres_stringOptions = stringOptions + " --IBLresiduals --Extended --Prefix IBLRES_ "
            iblres_cmd = common_cmd + iblres_stringOptions
            
            resmaps_stringOptions = stringOptions + " --ResidualMaps --Prefix RESMAPS_ "
            resmaps_cmd = common_cmd + resmaps_stringOptions

            # run the macro that makes the plots
            residuals_status = 256 # this means failed or plots not done
            hits_status = 256
            hitmaps_status = 256
            iblres_status = 256
            resmaps_status = 256
            hitmaps_output = "Not run"
            iblres_output = "Not run"
            resmaps_output = "Not run"
            
            msg.printInfo("Let's make the plots...")
    
            # change to the directory
            os.chdir(config.getInDetAlignmentMonitoringPath())

            msg.printGreen("=======================================================================")
            msg.printGreen("===                     Residuals                                   ===")
            msg.printGreen("=======================================================================")
            msg.printDebug(" residuals_cmd = " + str(residuals_cmd))
            (residuals_status, residuals_output) = commands.getstatusoutput(residuals_cmd)
            msg.printDebug("status from MakeMajorAlignMonPlots with residuals = " + str(residuals_status))
            msg.printDebug("residuals_output")
            print residuals_output

            msg.printGreen("=======================================================================")
            msg.printGreen("===                     Hits                                        ===")
            msg.printGreen("=======================================================================")
            msg.printDebug(" hits_cmd = " + str(hits_cmd))
            (hits_status, hits_output) = commands.getstatusoutput(hits_cmd)
            msg.printDebug("status from MakeMajorAlignMonPlots with hits = " + str(hits_status))
            msg.printDebug("hits_output")
            print hits_output

            msg.printGreen("=======================================================================")
            msg.printGreen("===                     Hits Maps                                   ===")
            msg.printGreen("=======================================================================")
            msg.printDebug("hitmaps_cmd = " + str(hitmaps_cmd))
            (hitmaps_status, hitmaps_output) = commands.getstatusoutput(hitmaps_cmd)
            msg.printDebug(" status from MakeMajorAlignMonPlots with hit maps = " +str(hitmaps_status))
            msg.printDebug("hitmaps_output")
            print hitmaps_output
            
            msg.printGreen("=======================================================================")
            msg.printGreen("===                     IBL Residuals                               ===")
            msg.printGreen("=======================================================================")
            msg.printDebug(" iblres_cmd = " + str(iblres_cmd))
            (iblres_status, iblres_output) = commands.getstatusoutput(iblres_cmd)
            msg.printDebug(" status from MakeMajorAlignMonPlots with IBL residuals = " + str(iblres_status))
            msg.printDebug("iblres_output")
            print iblres_output
 
            msg.printGreen("=======================================================================")
            msg.printGreen("===                     Residual Maps                               ===")
            msg.printGreen("=======================================================================")
            msg.printDebug(" resmaps_cmd = " + str(resmaps_cmd))
            (resmaps_status, resmaps_output) = commands.getstatusoutput(resmaps_cmd)
            msg.printDebug(" status from MakeMajorAlignMonPlots with residual maps = " + str(resmaps_status))
            msg.printDebug("resmaps_output")
            print resmaps_output
            
            msg.printGreen("Plots done!")
            
            # go back to the alignWebRoot directory
            os.chdir(config.workingDir)

            # report status
            msg.printGreen("=======================================================================")
            msg.printGreen("===                     Status report                               ===")
            msg.printGreen("=======================================================================")
            k += 1
            #msg.printDebug("residuals_status: "+str(residuals_status)) #Test
            residuals_status = 0 #test
            #msg.printDebug("hitmaps_status: "+str(hitmaps_status))      #Test
            #msg.printDebug("hits_status: "+str(hits_status))            #Test
            #msg.printDebug("resmaps_status: "+str(resmaps_status))      #Test
            #msg.printDebug("iblres_status: "+str(iblres_status))        #Test
            if (residuals_status !=0 or hits_status != 0 or hitmaps_status != 0 or iblres_status !=0 or resmaps_status !=0 ):
                msg.printWarning(" something went wrong producing the plots")
                if (hitmaps_status !=0):
                    msg.printWarning(" PROBLEMS producing HIT MAPS. Full output follows:")
                    msg.printWarning(str(hitmaps_output))
                if (iblres_status !=0):
                    msg.printWarning(" PROBLEMS producing IBL RESIDUALS. Full output follows:")
                    msg.printWarning(str(iblres_output))
                if (resmaps_status !=0):
                    msg.printWarning(" PROBLEMS producing RESIDUAL MAPS. Full output follows:")
                    msg.printWarning( str(resmaps_output))
            else:
                msg.printDebug(" monitoring plots for run:" + str(run) + " --> SUCCESFULLY created ")
                    
            # the record for the plots db -> 
            msg.printDebug(" going to fill run variables plotdatabase[%s][xxx]" %(str(run)))
            updates.append(run)
            plotdatabase[run] = {}
            # plotdatabase[run]['output'] = output
            plotdatabase[run]['folder'] = folderForThisRun
            plotdatabase[run]['residuals'] = residuals_status
            plotdatabase[run]['hits'] = hits_status
            plotdatabase[run]['hitmaps'] = hitmaps_status
            plotdatabase[run]['iblres'] = iblres_status
            plotdatabase[run]['resmaps'] = resmaps_status
            # default values for number of files used
            plotdatabase[run]['iter0'] = 0
            plotdatabase[run]['iter2'] = 0
            plotdatabase[run]['iter3'] = 0
            # fill with number of iles in run
            if ('list' in type(file1).__name__): 
                plotdatabase[run]['iter0'] = len(file1)
            else:
                if ('?' not in file1):
                    plotdatabase[run]['iter0'] = 1

            if ('list' in type(file2).__name__): 
                plotdatabase[run]['iter2'] = len(file2)
            else:
                if ('?' not in file2):
                    plotdatabase[run]['iter2'] = 1
                    
            if ('list' in type(file3).__name__): 
                plotdatabase[run]['iter3'] = len(file3)
            else:
                if ('?' not in file3):
                    plotdatabase[run]['iter3'] = 1
            
        msg.printGreen("-----------  End of loop over run "+str(run)+" -----------")
                
    msg.printGreen("-----------  End of loop over all runs   -----------")

    ################ loop on runs to produce monitoring plots ###########
    #StepHeader(4)  #STEP 4
    msg.printGreen("Loop over runs to update " + str(plotsDBFile) + " if necessary")
    #msg.printInfo(" Closing...")
    if k == 0:
        msg.printInfo(" - nothing to update")
    if k != 0: 
        msg.printInfo(" - Number of runs to update: " + str(k) + " --> " + str(updates))
        for run in updates :
            msg.printInfo(" Plots for run %s have been updated" %(str(run)))
            listOfKeys = plotdatabase[run].keys()
            msg.printDebug("                 - number of keys for this run: " + str(len(listOfKeys)))
            for key in listOfKeys:
                msg.printDebug("       plotdatabase[%s][%s] = %s" %(str(run),key,plotdatabase[run][key]))
                
        pickle.dump(plotdatabase, open(plotsDBFile, 'w'))
        msg.printInfo("Info updated and sanved in : " + str(plotsDBFile))

    msg.printInfo(" Completed")


# =================================================================================
#  mergeLBGroupMonitoringFiles
# =================================================================================
def mergeLBGroupMonitoringFiles(runinfo_database, run, theIter=0):
    msg.printDebug('In mergeLBGroupMonitoringFiles()')
   
    rebuildFile = rebuild
    hadd_status = 0
    hadd_output = "xx"
    
    # check if monitor folder is writeable
    if (not os.access(config.monitoringFolderName, os.W_OK)):
        msg.printError(" Monitor folder is not writable: %s. STOP execution. " % config.detailedPlotsRoot)
        exit()

    # define name of the merged monitoring file
    mergedFilesFolder = "%s/%s/%s" %(config.mergedFilesFolder, runinfo_database[run]['year'], runinfo_database[run]['processing'])
    thisIterMergedMonitoringFile = "%s/%s%d%s%s%s" %(mergedFilesFolder, "Iter", theIter, "_Merged_Run", str(run), ".root")
    msg.printInfo(" + Output merged file: %s" % thisIterMergedMonitoringFile)

    # check if this file exists
    if os.path.exists(thisIterMergedMonitoringFile):
        if rebuild: msg.printWarning(" + Merged file " + str(thisIterMergedMonitoringFile) + " is going to be rebuilt!")
        else: msg.printInfo(" + Merged file " + str(thisIterMergedMonitoringFile) + " already exists!")

    # set the list of monitoring files to be merged   
    listOfMonitoringFilesToAdd = ""
    keyName = "%s%d" % ("monitoringFileIter", theIter)
    monitoringFiles = runinfo_database[run][keyName]
    # msg.printDebug("monitoringFileIter: %s" % monitoringFiles)

    if ('list' in type(monitoringFiles).__name__):
        for i in range(0,len(monitoringFiles)):
            listOfMonitoringFilesToAdd += (monitoringFiles[i] + " ")

    if len(monitoringFiles) == 0: msg.printWarning(" + No input files available for run: " +str(run))

    # check if merged file exists and rebuilt it just if the rebuild option is set to true
    if os.path.exists(thisIterMergedMonitoringFile) and not rebuild: return 1,thisIterMergedMonitoringFile

    msg.printDebug(" + Merging files... " + str(thisIterMergedMonitoringFile))

    hadd_status = 1
    if len(monitoringFiles) == 1:
        hadd_command = "cp -f "
        hadd_command += listOfMonitoringFilesToAdd + " " + thisIterMergedMonitoringFile
        msg.printDebug(" + cp_command = " + str(hadd_command))
        os.system(hadd_command)
    else:
        hadd_command = "hadd -f " # hadd is used to merge histograms
        hadd_command += thisIterMergedMonitoringFile + " " + listOfMonitoringFilesToAdd
        msg.printDebug(" + hadd_command = " + str(hadd_command))
        hadd_status, hadd_output = commands.getstatusoutput(hadd_command)
        msg.printDebug(" + hadd_status = " + str(hadd_status))
        if hadd_status != 0: msg.printError(" + hadd_output = %s" % hadd_output)

    return thisIterMergedMonitoringFile

# =================================================================================
#  SampleTheMonitoringFiles
# =================================================================================
def SampleTheMonitoringFiles(Iter0Files, Iter2Files, Iter3Files):
    # Of all the monitoring files for each LB group, use just a sample of 3, for the initial, middle and last LB groups
    msg.printDebug('In SampleTheMonitoringFiles()')
     
    #if ('list' in type(file1).__name__ and ):
    #    for i in range(0,len(file1)):
 
    # msg.printDebug("type(Iter0Files).__name__ = " +str(type(Iter0Files).__name__ ))
    # msg.printDebug("type(Iter2Files).__name__ = "+str(type(Iter2Files).__name__ ))
    # msg.printDebug("type(Iter3Files).__name__ = "+str(type(Iter3Files).__name__ ))

    Iter0LBGroup = [0, 0, 0] # index pointing to the initial, middle and last
    Iter2LBGroup = [0, 0, 0]
    Iter3LBGroup = [0, 0, 0]

    nIter0LBgroups = 0
    
    if ('list' in type(Iter0Files).__name__):
        # check the number of LB groups: 
        nIter0LBgroups = len(Iter0Files)
        # msg.printDebug("<SampleTheMonitoringFiles> nIter0LBgroups = " +str(nIter0LBgroups))
        Iter0LBGroup[0] = 0 # points to first one
        # msg.printDebug("<SampleTheMonitoringFiles> Iter0LBGroup[0] = "+ str(Iter0LBGroup[0]))
        if (nIter0LBgroups>1): Iter0LBGroup[2] = nIter0LBgroups-1 # points to last one
        # msg.printDebug("<SampleTheMonitoringFiles> Iter0LBGroup[2] = "+str(Iter0LBGroup[2]))
        if (Iter0LBGroup[2]-Iter0LBGroup[0] > 1): 
            # msg.printDebug("<SampleTheMonitoringFiles> Iter0LBGroup[2] - Iter0LBGroup[0]= "+str(Iter0LBGroup[2]-Iter0LBGroup[0]))
            Iter0LBGroup[1] = int(Iter0LBGroup[0] + (Iter0LBGroup[2]-Iter0LBGroup[0])/2)
            # msg.printDebug("<SampleTheMonitoringFiles> Iter0LBGroup[1] = "+str(Iter0LBGroup[1]))
    else:
        # no action needed
        # msg.printDebug("type(Iter0Files).__name__ = "+ str(type(Iter0Files).__name__ )+" --> no list of LB groups")
        Iter0LBGroup = [0, 0, 0]
    msg.printDebug("Iter0LBGroup = " + str(Iter0LBGroup))
        
    if ('list' in type(Iter2Files).__name__):
        # check the number of LB groups: 
        nIter2LBgroups = len(Iter2Files)
        Iter2LBGroup[0] = 0 # points to first one
        if (nIter2LBgroups>1): Iter2LBGroup[2] = nIter2LBgroups-1 # points to last one
        if (Iter2LBGroup[2]-Iter2LBGroup[0] > 1): 
            Iter2LBGroup[1] = int(Iter2LBGroup[0] + (Iter2LBGroup[2]-Iter2LBGroup[0])/2)
    else:
        # no action needed
        msg.printDebug("type(Iter2Files).__name__ = "+str(type(Iter2Files).__name__)+" --> no list of LB groups") 
        Iter2LBGroup = [0, 0, 0]
    msg.printDebug("Iter2LBGroup= " +str(Iter2LBGroup))

    if ('list' in type(Iter3Files).__name__):
        # check the number of LB groups: 
        nIter3LBgroups = len(Iter3Files)
        # msg.printDebug("<SampleTheMonitoringFiles> nIter3LBgroups = " +str(nIter3LBgroups))
        Iter3LBGroup[0] = 0 # points to first one
        # msg.printDebug("<SampleTheMonitoringFiles> Iter3LBGroup[0] = "+str(Iter3LBGroup[0]))
        if (nIter3LBgroups>1): Iter3LBGroup[2] = nIter3LBgroups-1 # points to last one
        # msg.printDebug("<SampleTheMonitoringFiles> Iter3LBGroup[2] = "+str(Iter3LBGroup[2]))
        if (Iter3LBGroup[2]-Iter3LBGroup[0] > 1): 
            Iter3LBGroup[1] = int(Iter3LBGroup[0] + (Iter3LBGroup[2]-Iter3LBGroup[0])/2)
    else:
        # no action needed
        msg.printDebug("type(Iter3Files).__name__ = "+str(type(Iter3Files).__name__)+" --> no list of LB groups" )
        Iter3LBGroup = [0, 0, 0]
    msg.printDebug("Iter3LBGroup= " + str(Iter3LBGroup))

    # Now, let's make the list of files, markers, etc.
    listOfInputFiles = " --inputFiles  '" # header and opening '
    listOfMarkers = " --inputMarkers '" 
    listOfColors = " --inputColors '"
    listOfLabels = " --inputLabels '"
    nMonitoringFilesUsed = 0 # count the files because there is a hard coded limit in MakeMajorAlignMonPlots

    # Initial reconstruction (Iter0): 
    for i in range(0, len(Iter0LBGroup)):
        if ((i==0) or i>0 and Iter0LBGroup[i]>0):
            # msg.printDebug("Iter0> Iter0 group: "+str(i))
            listOfInputFiles += (Iter0Files[Iter0LBGroup[i]] + " ")
            listOfMarkers += ("%s" %(markerList[0]) + " ")
            listOfColors += ("%s" %(str(colorList[0]+i)) + " ")
            listOfLabels += ("Initial_LBgroup_%02d " %(Iter0LBGroup[i]))
            nMonitoringFilesUsed += 1

    # After L1 alignment (Iter2):
    for i in range(0, len(Iter2LBGroup)):
        if ((i==0) or i>0 and Iter2LBGroup[i]>0):
            # msg.printDebug("Iter2> Iter2 group: "+str(i))
            listOfInputFiles += (Iter2Files[Iter2LBGroup[i]] + " ")
            listOfMarkers += ("%s" %(markerList[2]) + " ")
            listOfColors += ("%s" %(colorList[2]) + " ")
            listOfLabels += ("AfterL11_LBgroup_%02d " %(Iter2LBGroup[i]))
            nMonitoringFilesUsed += 1

    # After L16 alignment (Iter3): 
    for i in range(0, len(Iter3LBGroup)):
        if ((i==0) or i>0 and Iter3LBGroup[i]>0): 
            # msg.printDebug("Iter3> Iter3 group: "+str(i))
            listOfInputFiles += (Iter3Files[Iter3LBGroup[i]] + " ")
            listOfMarkers += ("%s" %(markerList[3]) + " ") 
            listOfColors += ("%s" %(str(colorList[3]+i)) + " ") 
            listOfLabels += ("AfterL16_LBgroup_%02d " %(Iter3LBGroup[i]))
            nMonitoringFilesUsed += 1
                
    listOfInputFiles += "'" # closing character
    listOfMarkers += "'" 
    listOfColors += "'" 
    listOfLabels += "'"
    
    return listOfInputFiles, listOfMarkers, listOfColors, listOfLabels, nMonitoringFilesUsed

# =================================================================================
#  __main__
# =================================================================================
if __name__ == '__main__':
    main(sys.argv[1:])