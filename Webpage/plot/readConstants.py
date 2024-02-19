#!/usr/bin/env python
import commands

global alignWebRoot

###############################################################
def files(options, args):
    doDebug = True
    if doDebug == True:
        print " ==========================================  "
        print " ======== readConstants.files ==== START ==  "
        print " == options == " + str(options)+ " ==  "
        print " == args == " + str(args)
        print " ==========================================  "
    
    minNtracks = int(options.tracks)

    if options.period != "" :

        detector = {}
        periods = options.period.split(',')
        for p in sorted(periods):
            for nrun in sorted(database):
                if database[nrun]['period']== p and database[nrun]['idtracks']>= minNtracks:
                    file = database["00"+str(nrun)]['constantsFile']
                    newnrun = "%i %s" %(nrun,database[nrun]['subperiod'])
                    try:
                        detector[newnrun] = readConstants(file)
                    except:
                        print "No det"
        links = drawAllCorr(detector)
        return links

    if options.subperiod != "" :
        detector = {}
        subperiods = options.subperiod.split(',')
        for p in sorted(subperiods):
            for nrun in sorted(database):
                if database[nrun]['subperiod']== p and database[nrun]['idtracks']>=minNtracks:
                    file = database["00"+str(nrun)]['constantsFile']
                    #if runLocalTest == True:
					#	file = str(file)
					#	file = file.rstrip("/afs/cern.ch/user/m/martinpa/work/alignment/webMonitoring/run/WebPage/")
					#	print file
                    newnrun = "%i %s" %(nrun,p) 
                    detector[newnrun] = readConstants(file)

        links = drawAllCorr(detector)
        return links

    if options.range != 0:
        minrun = int(options.range.split(',')[0])
        maxrun = int(options.range.split(',')[1])
        detector = {}
        detector2 = {}
        nsamples = 0
        labelList = []
        if (doDebug):
            print "  == readConstants.files == method 1 (activated for 'Last 10')"
            print "                      minrun: ", minrun, "    maxrun: ", maxrun
            print "  -- readConstants.files -- start loop on nrun in sorted(database) "
        for nrun in sorted(database):
            if (doDebug): print " -- readConstants.files -- testing run: ",nrun
            if (doDebug): print "                      run: ",nrun," is in range:",minrun," --> ",maxrun
            if minrun <= nrun <= maxrun and database[nrun]['idtracks']>= minNtracks:
                fileL11 = database[nrun]['constantsFile']
                if fileL11 != '?':
                    newnrun = "%i %s" %(nrun,database[nrun]['subperiod'])
                    #detector[newnrun] = readConstants(fileL11)
                    detector[nsamples] = readConstants(fileL11)
                    myLabel = "%i %s" %(nrun,database[nrun]['subperiod'])
                    labelList.append(myLabel)
                    nsamples += 1
                    
        if (doDebug): print " -- readConstants.files -- going to drawAllCorr(detector) with detector:",detector
        links = drawAllCorr(detector)
        
        if (doDebug): 
            print " -- readConstants.files -- going to drawCorrEvolution with ",detector
            print "                                                 labelList ",labelList
        linksL11 = drawCorrEvolution(detector, labelList, drawErrors=True, drawLine = True, whichdof=-1, outputFormat=2)
        # up to here for L11

        # for L16, one has to loop per run and use all LB groups of that run
        fileCounter = 0
        detectorL16 = {}
        labelList = []
        for nrun in sorted(database):
            if (doDebug): print " -- readConstants.files -- testing run for L16: ",nrun
            if (doDebug): print "                      run: ",nrun," is in range:",minrun," --> ",maxrun
            if minrun <= nrun <= maxrun and database[nrun]['idtracks']>= minNtracks: # run in range and with enough number of tracks
                lbGroupCount = 0 # reset LB group count for a new run
                fileL16 = database[nrun]['constantsFileIter2']
                if fileL16 != "?":
                    # check if it is just single file or a list of files:
                    LBGroupFiles = fileL16 #.split()
                    for LBGroupFile in LBGroupFiles:
                        print " --> run:",nrun, " LBGroup:", lbGroupCount," --> file:",LBGroupFile
                        mylabel = "%d_LB_%02d" %(nrun, lbGroupCount)
                        labelList.append(mylabel)  
                        detectorL16[fileCounter] = readConstants(LBGroupFile)
                        fileCounter += 1
                        lbGroupCount += 1
                else:
                    print " -- readConstants.files -- warning fileL16 = ? " 
        #up to here for L16
        linksL16 = drawCorrEvolution(detectorL16, labelList, drawErrors=True, drawLine = True, whichdof=-1, outputFormat=2)
        linksL16_2 = drawCorrEvolution(detectorL16, labelList, drawErrors=True, drawLine = True, whichdof=-1, outputFormat=3)

        # return the evolution plots for L11 and L16
        return (linksL11, linksL16, linksL16_2)

    # 
    # - this method works for a single run -  
    # 
    if int(options.run.split(',')[0]) != 0:
        #runs = options.run.split(',')
        runs = options.run.split(',')[0]
        if (doDebug):
            print " == readConstants.files == method 2 for run number ",runs, " == " 
        detector = {}
        detectorL11 = {}
        detectorL16 = {}
        runs = options.run.split(',')
        drawResults = {}
        links = {}
        labelList = ""
        k = 0
        for r in runs:
            if r != "":
                if (not str(r) == str(int(r))) and ('backup' not in str(r)):
                    nr = "00" + str(int(r))
                    print "The runnumber contains a 00"
                
                
                nr	= int(r)	
                fileL11 = database["00"+str(nr)]['constantsFile']
                fileL11_byLB = database["00"+str(nr)]['constantsFileIter0']
                fileL16 = database["00"+str(nr)]['constantsFileIter2']
                if (doDebug):
                    print " == readConstants.files.method 2 == run %d fileL11 = %s == " %(nr, fileL11)
                if (fileL11 != "?"):
					newnrun = "%i %s" %(nr,database["00"+str(nr)]['subperiod'])
					detector[newnrun] = readConstants(fileL11)
                if (len(fileL11_byLB)>1):
                    if (doDebug):
                        print " == readConstants.files.method 2 == run %d has %d L11 LBGroups == " %(nr, len(fileL11_byLB))
                        print " == readConstants.files.method 2 == run %d fileL11_byLB = %s == " %(nr, fileL11_byLB)
                    LBGroupFiles = fileL11_byLB 
                    fileCounter = 0
                    for LBGroupFile in LBGroupFiles:
                        if (doDebug): print " == L11 file: ",LBGroupFile, " == " 
                        detectorL11[fileCounter] = readConstants(LBGroupFile)
                        fileCounter += 1
                    

                if fileL16 != "?":
                    # check if it is just single file or a list of files:
                    LBGroupFiles = fileL16 #.split()
                    
                    fileCounter = 0
                    for LBGroupFile in LBGroupFiles:
                        if (doDebug): print " == L16 file: ",LBGroupFile, " == "
                        detectorL16[fileCounter] = readConstants(LBGroupFile)
                        fileCounter += 1
                        
                    #LBGroupFiles0 = fileL16[0]
                    #detector2[newnrun] = readConstants(LBGroupFiles0)
                    
                #drawResults[k] = drawPlotRes(nr)
                k += 1
        # link to the list of files with L11 results
        links[0] = drawSingleCorr(detector)

        # in case of L11 split by LB groups
        if (len(fileL11_byLB)>1):
            if (doDebug or True): print " == readConstants.files == len(fileL11_byLB) = ",len(fileL11_byLB), " =="
        
        if (len(fileL11_byLB)>1): 
            counter = 0
            labelList = []
            for mydet in fileL11_byLB:
                mylabel = "LBGroup_%02d" %counter
                labelList.append(mylabel)  
                counter += 1
            print " -counter: %d --- detector: %s --- " %(counter, mydet)
            links[1] = drawCorrEvolution(detectorL11, labelList, whichdof=0, drawErrors=True, outputFormat=1, userLabel="L11")
            links[2] = drawCorrEvolution(detectorL11, labelList, whichdof=1, drawErrors=True, outputFormat=1, userLabel="L11")
            links[3] = drawCorrEvolution(detectorL11, labelList, whichdof=2, drawErrors=True, outputFormat=1, userLabel="L11")
            links[4] = drawCorrEvolution(detectorL11, labelList, whichdof=3, drawErrors=True, outputFormat=1, userLabel="L11")
            links[5] = drawCorrEvolution(detectorL11, labelList, whichdof=4, drawErrors=True, outputFormat=1, userLabel="L11")
            links[6] = drawCorrEvolution(detectorL11, labelList, whichdof=5, drawErrors=True, outputFormat=1, userLabel="L11")
            links[7] = drawCorrEvolution(detectorL11, labelList, whichdof=6, drawErrors=True, outputFormat=1, userLabel="L11")

        # level 16 plots
        if fileL16 != "?":
            if (len(fileL16)>=1):
                # this draws corrections for LBgroups in a single plot 
                # --> links[1] = drawSingleCorr(detectorL16)
                # use this in production (28/APR/2016)
                links[8] = drawAllCorr(detectorL16)
                
                print " -- readConstants.files == going to drawCorrEvolution for L16 LB groups"
                counter = 0
                labelList = []
                for mydet in detectorL16:
                    mylabel = "LBGroup_%02d" %counter
                    labelList.append(mylabel)  
                    counter += 1
                    print " -counter: %d --- detector: %s --- " %(counter, mydet)
                print " --- labelList: ", labelList
                # save the IBL Bx in two styles, 
                # - all staves in one plot 
                links[9] = drawCorrEvolution(detectorL16, labelList, drawErrors=True, whichdof=6,  outputFormat=1, userLabel="L16")
                # - one stave per plot, but all in one page
                links[10] = drawCorrEvolution(detectorL16, labelList, drawErrors=True, whichdof=6,  outputFormat=3, userLabel="L16_stavebystave")
                # - one stave per plot, but all in one page
                # -> working on this (Salva 23/Sep/2016) 

                
    return links

###############################################
if __name__ == '__main__':
    #
    # readConstants.py
    #
    import os

    doDebug = True

    #check with environment variable if server runs as local test 
#    runLocalTest = False
#    try:
#        stringRunLocalTest = os.getenv('RUNLOCALTEST', False)
#        if ("True" in stringRunLocalTest): #interpret the string returned by getenv into a boolean
#            runLocalTest = True
#    except:
#        runLocalTest = False

#    runLocalTest = True
    
    
    # pointer to the folder when the server resides   
    global alignWebRoot; alignWebRoot = ""
 #   try:
 #       alignWebRoot = os.getenv('ALIGNWEBROOT',"")
 #   except:
 #       alignWebRoot = ""    

    try:
        import cPickle as pickle
    except:
        import pickle

    ##################################
    # definition of folders and basic files
    webFolderName = "WebPage/"
#    runLocalTest = True
#    if runLocalTest == True:
#        if (len(alignWebRoot)==0):
#            #alignWebRoot = "/Users/martis/projectes/atlas/alineament/webmonitoringtest/InDetAlignmentWebMonitor/trunk/"
#            #alignWebRoot = "/afs/cern.ch/user/m/martis/mywork/JPsi_20.7.3.8/InnerDetector/InDetMonitoring/InDetAlignmentWebMonitor/"
#            alignWebRoot = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
#            
#        else:
#            if (doDebug): print " - readConstants - user defined ALIGNWEBROOT: ",alignWebRoot
#    else:
#        if (len(alignWebRoot)==0):
#            alignWebRoot = "/var/vhost/atlas-alignment/"
#            webFolderName = "secure/"

    # make sure that the last character of alignWebRoot is a slash
#    if (alignWebRoot[-1] is not "/"):
#        alignWebRoot += "/"
#        if (doDebug): print "  <serverManageOutputs2016> ALIGNWEBROOT needs a '/' --> ", alignWebRoot


    alignWebRoot = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    print " - readConstants - user defined ALIGNWEBROOT: ",alignWebRoot


    # the year
    alignWebYear = "2016"
    try:
        alignWebYear = os.getenv('ALIGNWEBYEAR',"2018")
    except:
        alignWebYear = "2016"	
	
	

    print alignWebYear



    #        
    server = alignWebRoot + "/database/"

    
    #### continue
    import sys
    import re
    from fileutils import readConstants
    from drawutils import drawAllCorr, drawSingleCorr, AutoColors,drawCorrEvolution
    from plotresults import drawPlotRes

    qargv = []
    for s in sys.argv:
        if re.search('\s|\*|\?',s):
            if "'" in s:
                qargv.append('"%s"' % re.sub('"',"'",s))
            else:
                qargv.append("'%s'" % re.sub("'",'"',s))
        else:
            qargv.append(s)

    qcmd = ' '.join(qargv)

    if (doDebug): print " -readConstants- == START == "


    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option('-n', '--nrun', dest='run', default=0)
    parser.add_option('-r', '--range', dest='range', default=0)
    parser.add_option('-p', '--period', dest='period', default="")
    parser.add_option('-s', '--subperiod', dest='subperiod', default="")
    parser.add_option('-t', '--tracks', dest='tracks', default=0)
    parser.add_option('-y', '--year', dest='theYear', default=2018)
    (options, args) = parser.parse_args()

    if (doDebug): print " -readConstants- == CONTINUE == "

    alignWebYear = options.theYear
    if (doDebug): print " -- readConstants -- ALIGNWEBYEAR = %s -- " % alignWebYear
    if (doDebug):
        print " ======================================================= "
        print " == readConstants ==                                  == "
        #print " == runLocalTest :", runLocalTest
        print " == alignWebroot :", alignWebRoot
        print " == alignWebYear :", alignWebYear
        print " ======================================================== "
        print " == webFolderName:", webFolderName
        print " == server :", server
        print " ======================================================== "

    try:
        database = pickle.load(open(server + "server_runinfo"+alignWebYear+".db",'r'))
    except:
        database = pickle.load(open(server + "server_runinfo"+alignWebYear+".db",'r'))


    if (doDebug): print " <readConstants> ==  calling files(options, args) where plots are done == "

    thePlots = files(options, args)

    # this is the way to return the list of files, via printing "a" and searchpicle.py reads the output
    for element in thePlots:
        print " len(element): ", element

    print thePlots
    if (doDebug): print " <readConstants> == COMPLETED == "

