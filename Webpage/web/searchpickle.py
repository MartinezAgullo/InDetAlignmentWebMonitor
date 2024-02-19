#!/usr/bin/env python
#
# searchpickle.py
#
import os, sys
from time import mktime
from datetime import datetime

#from plot.fileutils import readConstants
#from plot.drawutils import *
#from ROOT import *

# TEST Pablo - Start -
try:
	path_to_index = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
	print "path_to_index = " +str(path_to_index)	
	print "sys.path = " + str(sys.path)
	sys.path.append = path_to_index
	from index_salva import theYear # Here I am trying to inform searchpickle.py 
	from index_salva import runLocalTest # about the year and if we are in localtest
except:
	print "Fail loading the options from index.py into searchpickle.py "
# TEST Pablo -  End  -

try:
    import cPickle as pickle
except:
    import pickle

from cherrypy.lib.static import serve_file
from base import Tables, Error


#check with environment variable if server runs as local test 
runLocalTest = True
#try:
#    stringRunLocalTest = os.getenv('RUNLOCALTEST', False)
#    if ("True" in stringRunLocalTest): #interpret the string returned by getenv into a boolean
#        runLocalTest = True
#except:
#    runLocalTest = False

        
# pointer to the folder when the server resides   
alignWebRoot = ""
try:
    alignWebRoot = os.getenv('ALIGNWEBROOT',"")
except:
    alignWebRoot = ""    

printLevel = 10


##################################
# definition of folders and basic files
webFolderName = "WebPage/"

root_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

if (runLocalTest):
    if (len(alignWebRoot)==0):
        alignWebRoot = root_dir
    else:
        if (printLevel >=10): print " <serverManageOutputs2017> user defined ALIGNWEBROOT: ",alignWebRoot
else:
    if (len(alignWebRoot)==0):
        alignWebRoot = "/var/vhost/atlas-alignment/"
        webFolderName = "secure/"

# make sure that the last character of alignWebRoot is a slash
if (alignWebRoot[-1] is not "/"):
    alignWebRoot += "/"
    if (printLevel >=10): print "  <serverManageOutputs2017> ALIGNWEBROOT needs a '/' --> ", alignWebRoot 
    

# the year
# pointer to the folder when the server resides   
alignWeYear = "2018"
try:
    alignWebYear = os.getenv('ALIGNWEBYEAR',"2018")
except:
    alignWebYear = "2018"


#        
server = alignWebRoot + "database/"
server_alignfiles = alignWebRoot + webFolderName + "alignlogfiles/" + alignWebYear + "/"
bsHandshakeFolder = alignWebRoot + webFolderName + "bshandshake/"
runAnalysisLogFolder = alignWebRoot + webFolderName + "runanalysislog/" + alignWebYear + "/"
    
calibLoop = "/afs/cern.ch/user/a/atlidali/w0/calibLoop/web/database/"
analysisLogFilesFolder = "/afs/cern.ch/user/a/atlidali/w0/calibLoop/checker/log_forEachRun/"
extendedPlots = alignWebRoot + webFolderName + "detailed_plots/"+ alignWebYear + "/"

runInfoDBfile = "server_runinfo%s.db" % alignWebYear


##########################################################################
    
try:
    database = pickle.load(open(server + runInfoDBfile,'r')) 
except:
    database = ""

try:
    detailedPlots = pickle.load(open(extendedPlots + 'plots' + alignWebYear +'.db','r'))
except:
    #detailedPlots = pickle.load(open(extendedPlots + 'plots' + alignWebYear +'.db','r'))
    detailedPlots = {}

_Row = Tables()


class Searches:

    def __init__(self,nrun,string,nevents,nidtracks):

            self.runNumber = nrun
            self.Period = string.upper()
            self.Events = nevents
            self.Idtracks = nidtracks
            self.request = ""


    def Request(self):

        try:
            self.runNumber = int(self.runNumber)
            self.Events = int(self.Events)
            self.Idtracks = int(self.Idtracks)

            if self.runNumber != 0:
                try:
                    self.request =""
                    self.request += _Row.Thetablerow(self.runNumber,database[self.runNumber]['period'],database[self.runNumber]['subperiod'],database[self.runNumber]['date'],database[self.runNumber]['events'],database[self.runNumber]['idtracks'])

                except:
                    self.request = "<h3>No runs matched</h3>"


            elif self.Period == "" and self.Events !=0 and self.Idtracks == 0:
                self.request =""
                for nrun in sorted(database) :
                    if database[nrun]['events']>=self.Events:
                        self.request += _Row.Thetablerow(nrun,database[nrun]['period'],database[nrun]['subperiod'],database[nrun]['date'],database[nrun]['events'],database[nrun]['idtracks'])
                if self.request == "":
                    self.request = "<h3>No runs matched</h3>"


            elif self.Period == "" and self.Events ==0 and self.Idtracks != 0:
                self.request =""
                for nrun in sorted(database) :
                    if database[nrun]['idtracks']>=self.Idtracks:
                        self.request += _Row.Thetablerow(nrun,database[nrun]['period'],database[nrun]['subperiod'],database[nrun]['date'],database[nrun]['events'],database[nrun]['idtracks'])
                if self.request == "":
                    self.request = "<h3>No runs matched</h3>"


            elif self.Period != "" and self.Events ==0 and self.Idtracks == 0:
                self.request =""
                for nrun in sorted(database) :
                    if database[nrun]['period'] == self.Period :
                        self.request += _Row.Thetablerow(nrun,database[nrun]['period'],database[nrun]['subperiod'],database[nrun]['date'],database[nrun]['events'],database[nrun]['idtracks'])
                if self.request == "":
                    self.request = "<h3>No runs matched</h3>"


            elif self.Period == "" and self.Events !=0 and self.Idtracks != 0:
                self.request =""
                for nrun in sorted(database) :
                    if database[nrun]['events'] >= self.Events and database[nrun]['idtracks'] >= self.Idtracks :
                        self.request += _Row.Thetablerow(nrun,database[nrun]['period'],database[nrun]['subperiod'],database[nrun]['date'],database[nrun]['events'],database[nrun]['idtracks'])
                if self.request == "":
                    self.request = "<h3>No runs matched</h3>"


            elif self.Period != "" and self.Events !=0 and self.Idtracks == 0:
                self.request =""
                for nrun in sorted(database) :
                    if database[nrun]['events'] >= self.Events and database[nrun]['period'] == self.Period :
                        self.request += _Row.Thetablerow(nrun,database[nrun]['period'],database[nrun]['subperiod'],database[nrun]['date'],database[nrun]['events'],database[nrun]['idtracks'])
                if self.request == "":
                    self.request = "<h3>No runs matched</h3>"


            elif self.Period != "" and self.Events ==0 and self.Idtracks != 0:
                self.request =""
                for nrun in sorted(database) :
                    if database[nrun]['period'] == self.Period and database[nrun]['idtracks'] >= self.Idtracks :
                        self.request += _Row.Thetablerow(nrun,database[nrun]['period'],database[nrun]['subperiod'],database[nrun]['date'],database[nrun]['events'],database[nrun]['idtracks'])
                if self.request == "":
                    self.request = "<h3>No runs matched</h3>"


            elif self.Period != "" and self.Events !=0 and self.Idtracks != 0:
                self.request =""
                for nrun in sorted(database) :
                    if database[nrun]['events'] >= self.Events and database[nrun]['idtracks'] >= self.Idtracks and database[nrun]['period'] == self.Period:
                        self.request += _Row.Thetablerow(nrun,database[nrun]['period'],database[nrun]['subperiod'],database[nrun]['date'],database[nrun]['events'],database[nrun]['idtracks'])
                if self.request == "":
                    self.request = "<h3>No runs matched</h3>"

            return self.request

        except:
            error = Error()
            return error.error1()
####################################################
####################################################
####################################################


class Plotpreparation:
    
    def __init__(self,nruns, minruns, maxruns, periods, subperiods):
        self.period = periods.upper().split(',')
        self.subperiod = subperiods.upper().split(',')
        self.minrun = minruns
        self.maxrun = maxruns
        self.run = nruns

    def Plotting(self):
        print " <seachpickle.PlotPreparation.Plotting> minrun=", self.minrun,"  maxrun=",self.maxrun 
        try:
            self.minrun = int(self.minrun)
            self.maxrun = int(self.maxrun)
            self.run = int(self.run)
        except:
            error=Error()
            return error.error4()

        rootSetup()	
        calibLoop = "/afs/cern.ch/user/a/atlidali/w0/calibLoop"

        if self.period[0] != "" :

            try:

                detector = {}
            
                for p in sorted(self.period):
                    for nrun in sorted(database):
                        if database[nrun]['period']== p:
                            file = os.path.join(calibLoop, database[nrun]['constantsFile'].replace('EigenAnaOutput.root','alignlogfile.txt'))
                            newnrun = "%i %s" %(nrun,database[nrun]['subperiod'])
                            detector[newnrun] = readConstants(file)

                links = drawAllCorr(detector)

                return links

            except:
                error=Error()
                return error.error4()

        if self.subperiod[0] != "" :

            try:
                detector = {}

                for p in sorted(self.subperiod):
                    for nrun in sorted(database):
                        if database[nrun]['subperiod']== p:
                            file = os.path.join(calibLoop, database[nrun]['constantsFile'].replace('EigenAnaOutput.root','alignlogfile.txt'))
                            newnrun = "%i %s" %(nrun,p)
                            detector[newnrun] = readConstants(file)

                links = drawAllCorr(detector)

                return links

            except:
                error=Error()
                return error.error4()


        if self.minrun != 0 or self.maxrun != 0 :

            try:

                detector = {}

                for nrun in sorted(database):
                    if self.minrun <= nrun <= self.maxrun:
                        file = os.path.join(calibLoop, database[nrun]['constantsFile'].replace('EigenAnaOutput.root','alignlogfile.txt'))
                        newnrun = "%i %s" %(nrun,database[nrun]['subperiod'])
                        detector[newnrun] = readConstants(file)

                links = drawAllCorr(detector)

                return links

            except:
                error=Error()
                return error.error4()


        if self.run != 0:

            try:
                detector = {}
                file = os.path.join(calibLoop, database[self.run]['constantsFile'].replace('EigenAnaOutput.root','alignlogfile.txt'))
                newnrun = "%i %s" %(self.run,database[self.run]['subperiod'])
                detector[newnrun] = readConstants(file)
                links = drawAllCorr(detector)

                return links

            except:
                error=Error()
                return error.error4()


        else:
            error = Error()
            return error.error4()
    ####################################################
    def PlotMonitoring(self):
        " hola "
        print " <seachpickle.PlotPreparation.PlotMonitoring> hola"

####################################################
####################################################
####################################################


class LastRuns:

    def __init__(self,n):
        self.runs = int(n)

#################################################    
    def RunDisplayed(self, theYear):
        print " <RunsDisplayed> - START - theYear = "+str(theYear)

        runInfoDBfile = "server_runinfo"+str(theYear)+".db"
		
	
	#print "test: runInfoDBfile = " + str(runInfoDBfile)
	#print "test: server = " + str(server)
	
		
        try:
            print "Trying to read " +str(server + runInfoDBfile)
            database = pickle.load(open(server + runInfoDBfile,'r'))
            print "Reading of "  +str(server + runInfoDBfile) + " was successful"
        except:
            database = ""
            print " <RunsDisplayed> problems reading %s%s " %(server,runInfoDBfile)
            
            
        #print "database["+str(nrun)+"]"
        #for key in database[nrun]:
		#	print " - " + str(key) + " = " + str(database[nrun][key])
        #exit()     
        
        lrTable = ""
        i = 0
        for nrun in sorted(database, reverse=True):
            if database[nrun]['constantsFile'] != "?":
                constantsFile = "Yes"
            else:
                constantsFile = "No"

            try:
                detailedPlots[nrun]
                detailed_plots = "Yes"
            except KeyError:
                detailed_plots = "No"

            #lrTable += _Row.Thetablerow(nrun,database[nrun]['period'],database[nrun]['subperiod'],constantsFile,detailed_plots)
            thePeriod = database[nrun]['period']
            theSubPeriod = database[nrun]['subperiod']

            theProject = "PROJECT"
            try: 
                if (database[nrun]['project']): theProject = database[nrun]['project']
            except:
                theProject = "PROJECT"
                
            theStream = "STREAM"
            try: 
                if (database[nrun]['stream']): theStream = database[nrun]['stream']
            except:
                theStream = "STREAM"
            
              
            theDate = "DATE"
            if 'date' in database[nrun].keys():
		    theDate = database[nrun]['date']
	    if 'runRecordDate' in database[nrun].keys():
		    theDate = database[nrun]['runRecordDate']
            
           # print "--------_"
           # print database[nrun]['thisdbrecordtimestamp']
           # dt = str(datetime.fromtimestamp(mktime(database[nrun]['thisdbrecordtimestamp'])))
           # print "..."
           # print dt
           # print "--------_"
           # print "."  esto estaria bien arreglarlo
            theTime = "TIME"   
            if (database[nrun]['thisdbrecordtimestamp']): theTime = " " # need to fix "String index is out of range" error when using db_timestamp_hour 
            theBShandshake = "BSHandShake"
            if (database[nrun]['bshandshake']): theBShandshake = database[nrun]['bshandshake']
            theBSauthor = "BSAUTHOR"
            if (database[nrun]['bshsauthor']): theBSauthor = database[nrun]['bshsauthor']
            theL11Results = database[nrun]['L11Results']
            if (database[nrun]['L11Results']): theL11Results = database[nrun]['L11Results']
            theL16Results = database[nrun]['L16Results']
            if (database[nrun]['L16Results']): theL16Results = database[nrun]['L16Results']
            theDBtimestamp = database[nrun]['DBtimestamp']
            if (database[nrun]['DBtimestamp']): theDBtimestamp = database[nrun]['DBtimestamp']
            
            #new elements
            if 'totalSize' in database[nrun].keys(): theRunSize = database[nrun]['totalSize']
            else: theRunSize = '?'
            
            if 'nFiles' in database[nrun].keys(): theNfiles = database[nrun]['nFiles']
            else: theNfiles = '?'
            
        
            
                
            lrTable += _Row.Thetablerow(nrun, thePeriod, theSubPeriod, theProject, theStream, theDate, theTime, theBShandshake, theBSauthor, theL11Results, theL16Results, theDBtimestamp, database[nrun]['analysisfile'], constantsFile, detailed_plots) # for 2016
            i += 1

        return lrTable, i
    
####################################################
    def LastN(self):
        print " - start - lastN - "
        j = 0
        minmaxruns = []
        for nrun in sorted(database, reverse=True):
            if j < self.runs:
                if j == 0:
                    minmaxruns.append("00"+str(int(nrun)))
                #if (j <= 9 and j>0):
                if (j>0):
                    minmaxruns.append("00"+str(int(nrun)))
                    print " append : ",j, " run: ",nrun
                j += 1
            else:
                break
        return minmaxruns
####################################################
####################################################
####################################################


class FileBrowser:

    def __init__(self, run):

        self.nrun = int(run)

    def Showfile(self):

        constantsPath = database[self.nrun]['constantsFile']
        monitoringPath = database[self.nrun]['monitoringFile']

        show = '<a href="../webapp/Download/?filepath=' + constantsPath + '">' + "Constants File</a> <br />"
        show += '<a href="../webapp/Download/?filepath=' + monitoringPath + '">' + "Monitoring File</a> <br />"
        return show
