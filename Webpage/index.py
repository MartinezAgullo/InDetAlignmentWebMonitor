import os, time, sys, commands, datetime
import cherrypy
from cherrypy.lib.static import serve_file
from web.base import Skeleton, Tables, Formulary, FormularyPlot, Error, contact
from web.searchpickle import Searches, LastRuns, FileBrowser, Plotpreparation
try: import cPickle as pickle
except: import pickle
from optparse import OptionParser
from python.MsgHelper import msgServer

# =================================================================================
#  options
# =================================================================================
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default=datetime.datetime.today().year, type="int",
                      help="set which year you want to retrieve [default: %default]", metavar="YEAR")
parser.add_option("-d", "--debugLevel", dest="debugLevel", default=0, type="int",
                      help="set debug level (DEBUG=0, INFO=1, WARNING=2, ERROR=3, FATAL=4) [default: %default]", metavar="LEVEL")
parser.add_option("-t", "--localtest", action="store_true", dest="localtest", default=False,
                      help="run a local test [default: %default]")
#parser.add_option("-w", "--workdir", dest="workingDir", default=os.environ['PWD'],
#                      help="set the working directory [default: %default]", metavar="DIR")
(options, args) = parser.parse_args()

global msg
msg = msgServer('index.py', options.debugLevel)
if options.debugLevel == 0: doDebug = True
else: doDebug = False

current_dir = os.path.dirname(os.path.abspath(__file__))

doDebug = False
_skeleton = Skeleton()
_tables = Tables()
_form = Formulary()
_formplot = FormularyPlot()
_contact = contact()
n = 199 #number of runs displayed
_processing = "hip5TeV"

# check with environment variable if server runs as local test 
runLocalTest = options.localtest

# test of reading the server_runinfo file
runinfoDB_index = {}
runInfoDBfile  = ""

# read the runinfo db
server = "/var/vhost/atlas-alignment/database/"
parent_dir = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print parent_dir

if runLocalTest == True: 
    server = "%s/database/" % (parent_dir)
    print server
    msg.printDebug("Running a local test")
    msg.printDebug("Creating a symbolic link to detailed_plots")
    os.system("ln -fs %s/run/Monitor/detailed_plots ." % str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
    msg.printDebug("Creating a symbolic link to alignlogfiles")
    os.system("ln -fs %s/run/WebPage/alignlogfiles ." % str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
    msg.printDebug("Creating a symbolic link to bshandshake")
    os.system("ln -fs %s/run/WebPage/bshandshake ." % str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
    msg.printDebug("Creating a symbolic link to runanalysislog")
    os.system("ln -fs %s/run/WebPage/runanalysislog ." % str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

# set year for server_runinfoYEAR.db
global theYear
# print os.getenv('ALIGNWEBYEAR')
theYear = int(os.getenv('ALIGNWEBYEAR'))

if theYear != options.year:
    if os.path.isfile("%s/server_runinfo%d.db" % (server, options.year)):
        theYear = options.year
        os.environ["ALIGNWEBYEAR"] = "%d" % theYear
# print theYear
# print os.getenv('ALIGNWEBYEAR')

runInfoDBfile = "server_runinfo%s.db" % (theYear)
print " __main__ server = " + str(server)
print " __main__ server_runinfo.db = " + str(runInfoDBfile)

database_files = []
for mydbfile in commands.getoutput('ls -r %s | grep .db' % server).splitlines():
    database_files.append(mydbfile)
print "list of DB files: " + str(database_files)

runinfoDB_index = pickle.load(open(server + runInfoDBfile,'r'))
# msg.printDebug(runinfoDB_index.keys()) #runs displayed

# =================================================================================
#  Web
# =================================================================================
class Web:
    def __init__(self, year):
        self.alignWebYear = year

        msg.printDebug("year = " +str(year))
        msg.printDebug("alignWebYear = " +str(self.alignWebYear))

    # =================================================================================
    #  index
    # =================================================================================
    @cherrypy.expose
    def index(self, theYear = None):
        print " <index> - START - theYear = ",theYear," -- "
        cherrypy.log("<index> - START - theYear = %s -- " % theYear, traceback=False)

        #print 'self.alignWebYear',self.alignWebYear
        print 'theYear?',theYear
        #print "os.getenv('ALIGNWEBYEAR')",os.getenv('ALIGNWEBYEAR')
        # theYear = os.getenv('ALIGNWEBYEAR')
        
        if theYear is not None:
            os.environ["ALIGNWEBYEAR"] = "%s" % str(theYear)
            self.alignWebYear = str(theYear)
            print "os.getenv('ALIGNWEBYEAR')",os.getenv('ALIGNWEBYEAR')
            theYear = int(os.getenv('ALIGNWEBYEAR'))
            
        msg.printGreen("Test: theYear = " + str(theYear))
        msg.printGreen("Test: alignWebYear = " + str(self.alignWebYear))	
        Runs = LastRuns(n)
        rows = Runs.RunDisplayed(self.alignWebYear)#rows = Runs.RunDisplayed(theYear)
        # first part of the table with the run and data info
        druns = _tables.Thetablehead("Run "+str(self.alignWebYear),"Period", "Run record date", "Project", "Stream")
        druns += rows[0]
        druns += _tables.Thetableend()
		# end of table
        html = [_skeleton.Thestart()]

        print theYear
        print theYear
        print theYear
        print theYear
        
		#html.append(_skeleton.Theheader("ID Alignment"))
        html.append(_skeleton.TheNavBar())
        html.append(_form.Theform(database_files, theYear))
        html.append(_skeleton.Thebody( rows[1], druns, _form.Theform(database_files, theYear))) # rows[1] = number of runs. druns = code for table. _form.Theform() = the formulary for searches
        html.append(_skeleton.Thefooter())

        print " <index> - COMPLETED - "
        return html

    # =================================================================================
    #  Find
    # =================================================================================
    @cherrypy.expose
    def Find(self,nrun,string,nevents,nidtracks):

        Search = Searches(nrun,string,nevents,nidtracks)

        request_table = _tables.Thetablehead("Run","Period","Date","Events","ID Tracks")
        request_table += Search.Request()
        request_table += _tables.Thetableend()

        html2 = [_skeleton.Thestart()]
        #html2.append(_skeleton.Theheader("ID Alignment"))
        html2.append(_skeleton.TheNavBar())
        html2.append(_skeleton.Thebody("Find",request_table,_form.Theform()))
        html2.append(_skeleton.Thefooter())

        return html2

    # =================================================================================
    #  Plots
    # =================================================================================
    @cherrypy.expose
    def Plots(self):

        html4 = [_skeleton.Thestart()]
        # html4.append(_skeleton.Theheader("ID Alignment"))
        html4.append(_skeleton.TheNavBar())
        html4.append(_skeleton.Thebody("Plots",_skeleton.Comments(),_formplot.Theform()))
        html4.append(_skeleton.Thefooter())

        return html4

    # =================================================================================
    #  Plotting
    # =================================================================================
    @cherrypy.expose
    def Plotting(self, nruns, idtracks, minruns, maxruns, periods, subperiods, olddata):
        print " <Plotting> start "
        images = ""
        run = nruns.split(',')
        tracks = int(idtracks)
        minrun = int(minruns)
        maxrun = int(maxruns)
        period = periods.upper().split(',')
        subperiod = subperiods.upper().split(',')

        theYear = self.alignWebYear
        
        # drawing mode
        # - one may be plotting the alignment constats corrections for a single run
        SINGLERUN = 1
        # - or the evolution of the aligment corrections for many runs
        MANYRUNS = 2
        # - default is single run
        drawingMode = SINGLERUN
        
        if (minrun < maxrun):
            drawingMode = MANYRUNS
                
        if "" in olddata.upper():
            cmd =current_dir + '/environment.sh'
        if not os.path.exists(cmd):
            error=Error()
            html5 = [_skeleton.Thestart()]
            #html5.append(_skeleton.Theheader("ID Alignment"))
            html5.append(_skeleton.TheNavBar())
            html5.append(_skeleton.Thebody("Plots",error.error3(),_formplot.Theform()))
            html5.append(_skeleton.Thefooter())
            return html5
        if (doDebug): 
            images += "<p><h2> Debugging </h2></p>"
            images += "<p><h3> input: nruns: " + nruns + "</h3></p>"
            images += "<p><h3>     idtracks: " + idtracks + "</h3></p>"
            images += "<p><h3>      minruns: " + minruns + "</h3></p>"
            images += "<p><h3>      maxruns: " + maxruns + "</h3></p>"
            images += "<p><h3>         year: " + self.alignWebYear +"</h3></p>"
        if int(run[0]) != 0:
            r = ""
            for i in run:
                if i != "":
                    r += "%s," %(i)

            cmd += ' -n ' + r

        elif minrun != 0 and maxrun != 0:
            cmd += ' -r %i,%i -t %i' %(minrun, maxrun, tracks)

        elif period[0] != "":
            per = ""
            for p in sorted(period):
                per += "%s," %(p)

            cmd += ' -p %s -t %i' %(per, tracks)

        elif subperiod[0] != "":
            subper = ""
            for p in sorted(subperiod):
                subper += "%s," %(p)

            cmd += ' -s %s -t %i'  %(subper, tracks)

        # the year
        cmd += ' -y %s' % theYear
        print " <Plotting> theYear ", theYear 
        
        import commands
        (status, output) = commands.getstatusoutput(cmd)
        
        if (doDebug): 
            print " <Plotting> Command: %s " %cmd
            images += "<p> Command: %s </p>" %(cmd)
            images += "<p> command status: %d <p>" %(status)
            images += "<p> command output: %s <p>" %(output)
            
        count = int(output.find("{"))
        string1 = output[count:]
        count = int(string1.find("["))
        results = string1[count:].split("'")
        corrections = string1[:count].split("'")
        vectorcorr=[]
        vectorres=[]
        listOfCorrectionPlotsPNG = []
        listOfEvolutionPlotsPNG  = []
        listOfCorrectionPlotsPDF = []
        listOfEvolutionPlotsPDF  = []
        listOfL11EvolutionPlotsPNG = []
        listOfL11EvolutionPlotsPDF = []
        listOfL16EvolutionPlotsPNG = []
        listOfL16EvolutionPlotsPDF = []
        
        for l in corrections :
            #images += "<p> " + l + "</p>"
            if len(l)>15: # this is a file
                vectorcorr.append(l)
            if ("correction" in l and "png" in l):
                listOfCorrectionPlotsPNG.append(l)
            if ("correction" in l and "pdf" in l):
                listOfCorrectionPlotsPDF.append(l)
            if ("evolution" in l and "png" in l):
                listOfEvolutionPlotsPNG.append(l)
            if ("evolution" in l and "pdf" in l):
                listOfEvolutionPlotsPDF.append(l)
            if ("evolution" in l and "L11" in l and "png" in l):
                listOfL11EvolutionPlotsPNG.append(l)
            if ("evolution" in l and "L11" in l and "pdf" in l):
                listOfL11EvolutionPlotsPDF.append(l)
            if ("evolution" in l and "L16" in l and "png" in l):
                listOfL16EvolutionPlotsPNG.append(l)
            if ("evolution" in l and "L16" in l and "pdf" in l):
                listOfL16EvolutionPlotsPDF.append(l)

        for l in results :
            if len(l)>10:
                vectorres.append(l)

        print " <Plotting> step 1 " 
        if (doDebug):        
            images += "<p><h2> list of output files: " + str(len(vectorcorr)) + "</h2>"
            for myfig in vectorcorr:
                images += "<p> " + myfig + "</p>"

            images += "<p><h2> list of Correction (png) files: " + str(len(listOfCorrectionPlotsPNG)) + "</h2>"
            for myfig in listOfCorrectionPlotsPNG:
                images += "<p> png: " + myfig + "</p>"

            images += "<p><h2> list of Correction (pdf) files: " + str(len(listOfCorrectionPlotsPDF)) + "</h2>"
            for myfig in listOfCorrectionPlotsPDF:
                images += "<p> pdf: " + myfig + "</p>"

            images += "<p><h2> list of Evolution (png) files: " + str(len(listOfEvolutionPlotsPNG)) + "</h2>"
            for myfig in listOfEvolutionPlotsPNG:
                images += "<p> png: " + myfig + "</p>"

            images += "<p><h2> list of Evolution (pdf) files: " + str(len(listOfEvolutionPlotsPDF)) + "</h2>"
            for myfig in listOfEvolutionPlotsPDF:
                images += "<p> pdf: " + myfig + "</p>"

            images += "<p><h2> list of L11 Evolution (png) files: " + str(len(listOfL11EvolutionPlotsPNG)) + "</h2>"
            for myfig in listOfL11EvolutionPlotsPNG:
                images += "<p> png: " + myfig + "</p>"

            images += "<p><h2> list of L16 Evolution (png) files: " + str(len(listOfL16EvolutionPlotsPNG)) + "</h2>"
            for myfig in listOfL16EvolutionPlotsPNG:
                images += "<p> png: " + myfig + "</p>"
        # end of debug print
        
        # adding the plots now
        # First L11
        try:
            if (drawingMode == SINGLERUN): 
                images += ("<p><h2>Level 11 Alignment Corrections for run " +str(nruns) + "  (year: " + theYear +") </h2></p>")
                if (doDebug):images += "<p> drawing mode SINGLERUN </p>"
            if (drawingMode == MANYRUNS): 
                images += "<p><h2>Level 11 Alignment Corrections Evolution from run "+str(minruns) +" to run " +str(maxruns)+ " </h2></p>" 
                if (doDebug): images += "<p> drawing mode MANYRUNS </p>"

            if (len(listOfCorrectionPlotsPNG)>0 and drawingMode == SINGLERUN):
                if (doDebug): images += "<p> mode 1 - correction plots - single run - </p>"
                # Level 11
                for i in range(7):
                    images += """<p><image src="../webapp/constant/%s"/> <input type="button" value="pdf file" onclick="window.open('../webapp/constant/%s')" /></p>""" %(listOfCorrectionPlotsPNG[i], listOfCorrectionPlotsPDF[i])

            # now try with the new L11
            try:
                images += "<p><h2>Level 11 Alignment Corrections evolution </h2></p>"
                if (len(listOfL11EvolutionPlotsPNG)>0 and drawingMode == SINGLERUN):
                    # find the index to the Bx evolution plot with all IBL staves in. 
                    # - first Bx file --> all IBL staves in one plot (called evolution_dofs)
                    # - second Bx file --> evolution of the Bx for each IBL stave 
                    theFileIndex = 0
                    for myfig in listOfL11EvolutionPlotsPNG:
                        if (doDebug): 
                            images += """<p> """ + listOfL11EvolutionPlotsPNG[theFileIndex] + """</p> """
                        images += """<p><image src="../webapp/constant/%s"/> <input type="button" value="pdf file" onclick="window.open('../webapp/constant/%s')" /></p>""" %(listOfL11EvolutionPlotsPNG[theFileIndex], listOfL11EvolutionPlotsPDF[theFileIndex])
                        theFileIndex += 1
                if (len(listOfL11EvolutionPlotsPNG)==0 and drawingMode == SINGLERUN):
                    images += """<p>  Old scheme. L11 with No LB group splitting (or may be just only one group) </p> """
            except:
                images += "<p><h2>Level 11 Alignment Corrections (new method 26/September/2016) NOT WORKING </h2></p>" 

            if (len(listOfEvolutionPlotsPNG)>0 and drawingMode == MANYRUNS):
                if (doDebug): images += "<p> mode 2 - evolution plots - many runs - </p>"
                # Level 11
                for i in range(min(len(listOfEvolutionPlotsPNG), 7)):
                    if (doDebug): images += "<p> " + listOfEvolutionPlotsPNG[i] + "</p>"
                    images += """<p><image src="../webapp/constant/%s"/> <input type="button" value="pdf file" onclick="window.open('../webapp/constant/%s')" /></p>""" %(listOfEvolutionPlotsPNG[i], listOfEvolutionPlotsPDF[i])

                    
            try:
                images += "<p><h2>Level 16 Alignment Corrections </h2></p>"

                if (len(listOfL16EvolutionPlotsPNG)>0 and drawingMode == SINGLERUN):
                    images += """<p><h3> Evolution of Bx per LB group for run """ + str(nruns) + """</h3></p>"""
                    # find the index to the Bx evolution plot with all IBL staves in. 
                    # - first Bx file --> all IBL staves in one plot (called evolution_dofs)
                    # - second Bx file --> evolution of the Bx for each IBL stave 
                    theFileIndex = 0
                    for myfig in listOfL16EvolutionPlotsPNG:
                        if (doDebug): 
                            images += """<p> """ + listOfL16EvolutionPlotsPNG[theFileIndex] + """</p> """
                        images += """<p><image src="../webapp/constant/%s"/> <input type="button" value="pdf file" onclick="window.open('../webapp/constant/%s')" /></p>""" %(listOfL16EvolutionPlotsPNG[theFileIndex], listOfL16EvolutionPlotsPDF[theFileIndex])
                        theFileIndex += 1
                     
                if (len(listOfEvolutionPlotsPNG)>0 and drawingMode == MANYRUNS):
                    images += "<p><h3> Evolution of Bx per LBGroup from run "+str(minruns) +" to run " +str(maxruns)+ " </h3></p>"
                    # find the index to the Bx evolution plot with all IBL staves in. 
                    # - first Bx file --> L11 (not interested)
                    # - second Bx file --> all IBL staves in one plot
                    # - third Bx file --> evolution of the Bx for each IBL stave
                    bxcount = 0
                    filecount = 0
                    bxevolplot = 0
                    bxevolbydof = 0
                    for myfig in listOfEvolutionPlotsPNG:
                        filecount += 1 
                        if ("Bx" in myfig):
                            bxcount += 1
                            if (bxcount == 2): bxevolplot = filecount-1  
                            if (bxcount == 3): bxevolbydof = filecount-1  
                    if (doDebug): 
                        images += """<p> """ + listOfEvolutionPlotsPNG[bxevolplot] + """</p> """
                    images += """<p><image src="../webapp/constant/%s"/> <input type="button" value="pdf file" onclick="window.open('../webapp/constant/%s')" /></p>""" %(listOfEvolutionPlotsPNG[bxevolplot], listOfEvolutionPlotsPDF[bxevolplot])
                    images += "<p><h3> Evolution of Bx per LBGroup from run "+str(minruns) +" to run " +str(maxruns)+ " (per IBL stave) </h3></p>"
                    if (doDebug): 
                        images += """<p> """ + listOfEvolutionPlotsPNG[bxevolbydof] + """</p> """
                    images += """<p><image src="../webapp/constant/%s"/> <input type="button" value="pdf file" onclick="window.open('../webapp/constant/%s')" /></p>""" %(listOfEvolutionPlotsPNG[bxevolbydof], listOfEvolutionPlotsPDF[bxevolbydof])


            except:
                print "No level 16 available"

                
        except:
            error = Error()
            html5 = [_skeleton.Thestart()]
            #html5.append(_skeleton.Theheader("ID Alignment"))
            html5.append(_skeleton.TheNavBar())
            html5.append(_skeleton.Thebody("Plots", cmd + output,_formplot.Theform()))
            if (doDebug): html5.append(_skeleton.Thebody("Plots", images,_formplot.Theform()))
            html5.append(_skeleton.Thebody("Plots", error.error2(),_formplot.Theform()))
            html5.append(_skeleton.Thefooter())
            return html5

        print " <Plotting> step 2 " 
        html5 = [_skeleton.Thestart()]
        #html5.append(_skeleton.Theheader("ID Alignment"))
        print " <Plotting> step 3 " 
        #html5.append(_skeleton.Thebody("Plots", cmd + output,_formplot.Theform()))
        html5.append(_skeleton.TheNavBar())
        html5.append(_skeleton.Thebody("Plots", images,_formplot.Theform()))
        html5.append(_skeleton.Thefooter())

        print " <Plotting> Completed "
        return html5
    #################################################################

    # =================================================================================
    #  PlotMonitoring
    # =================================================================================
    @cherrypy.expose
    def PlotMonitoring(self,nruns):
        #import os

        thisRun = "00"+str(nruns)
        images = ""
        html6 = [_skeleton.Thestart()]
        #html6.append(_skeleton.Theheader("ID Alignment"))
        html6.append(_skeleton.TheNavBar())

        theYear = os.getenv("ALIGNWEBYEAR",str(self.alignWebYear))
        theProcessing = _processing
        try: 
            theProcessing = runinfoDB_index[thisRun]['processing']
        except:
            theProcessing = _processing
            
        print "Test: theProcessing = " + str(theProcessing)
        
        
        images += '''<h2>MONITORING PLOTS FOR RUN 00%s</h2>

					<div id="myBtnContainer">
						<button class="btn active" onclick="filterSelection('all')"> Show all</button>
						<button class="btn" onclick="filterSelection('RESID')"> Residuals</button>
						<button class="btn" onclick="filterSelection('HITS')"> Hits</button>
						<button class="btn" onclick="filterSelection('HITMAPS')"> Hit Maps</button>
						<button class="btn" onclick="filterSelection('IBLRES')"> IBL Res.</button>
						<button class="btn" onclick="filterSelection('RESMAPS')"> Residual Maps</button>
					</div>''' %(str(nruns))
            
        #form the images with the monitoring plots of this run
        textForHeader = " Monitoring plots: Run  %ss  (%s)" %(thisRun, theProcessing)
        #images += "<p><h2> "+textForHeader+" </h2></p>"
        
        # we may need to change this in the final version
        parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        msg.printFatal("parentdir = " + str(parentdir))
        folderWithMonitoringFiles = " %s/%s/%s/%s/%08d" %(parentdir, "WebPage/detailed_plots",theYear, theProcessing, int(thisRun))
        ##
        
        msg.printBlue(str(folderWithMonitoringFiles)) #test
        #folderWithMonitoringFiles = " %s/%s/%s/%s/s" %(current_dir, "detailed_plots",theYear, theProcessing, thisRun)
        

        if (doDebug or False): images += "<p> server: %s"   %(server)
        if (doDebug or False): images += "<p> runinfoDB file: %s"   %(runInfoDBfile)
        if (doDebug or False): images += "<p> processing flavour: %s"   %(runinfoDB_index)
       
		#We loop for all plot types
        MonitoringTypes = ['RESID', 'HITS', 'HITMAPS', 'IBLRES', 'RESMAPS']
         
        # Start of the grid
        images += ''' 
           <!-- Portfolio Gallery Grid -->
        '''  
            
        # Grid presentation of images (before opening)
        images += ''' 
            <div class="row"> <!--  lightbox row start -->
        '''
        i = 0
        for plotsType in MonitoringTypes:        
            listOfMonitoringFiles = os.popen("ls %s/%s*" %(folderWithMonitoringFiles,plotsType)).readlines()
            if (len(listOfMonitoringFiles)>0):                
                for element in listOfMonitoringFiles:
						element = element.split("/")
						plotName = element[-1]
						i = i+1
						images += '''  
						<div class="column %s"> <!-- Column start -->
							<div class="content">
								<img src="../webapp/detailed_plots/%s/%s/%s/%s" title="%s"''' %(plotsType, str(theYear), theProcessing, thisRun, plotName, plotName.replace('.png', ' '))
						images += '''style="width:95%" '''
						images += '''onclick="openModal();currentSlide(%s)" class="hover-shadow cursor">
							</div>
						</div>	<!-- Column end -->
						''' %(str(i))
            if not (len(listOfMonitoringFiles)>0):
				images += "<p><h3> Monitoring plots for run %s will appear soon </h3></p>" %(thisRun)
				images += "<p> checking folder: %s"   %(folderWithMonitoringFiles)	
				break		
        images += ''' 
						</div> <!--  lightbox row end -->
					<!-- end Gallery Grid -->
			
					<div id="myModal" class="modal">  <!--  lightbox modal start -->
					<span class="close cursor" onclick="closeModal()">&times;</span>
					<div class="modal-content">
					''' 
            
        # Slide / Big picture (opened images)
        i = 0
        for plotsType in MonitoringTypes:
            typename = "Plot"
            if plotsType ==  'RESID': typename = "Residuals"
            if plotsType ==  'HITS': typename = "Hits"
            if plotsType ==  'HITMAPS': typename = "Hit Maps"
            if plotsType ==  'IBLRES': typename = "IBL Res."
            if plotsType ==  'RESMAPS': typename = "Res. Maps"
            listOfMonitoringFiles = os.popen("ls %s/%s*" %(folderWithMonitoringFiles,plotsType)).readlines()
            if not (len(listOfMonitoringFiles)>0):
                break
            j=0
            for element in listOfMonitoringFiles:
                element = element.split("/")
                plotName = element[-1]
                i = i+1
                j=j+1
                images += '''
						<div class="mySlides"> 
						<center>
							<div class="numbertext"> %s/%s| %s </div>
							<img src="../webapp/detailed_plots/%s/%s/%s/%s" alt="%s"
				'''%(str(j), str(len(listOfMonitoringFiles)),typename , str(theYear), theProcessing, thisRun, plotName, plotName.replace('.png', ' '))
                images += '''> <!--  width when clicked -->
						</center>
								</div>'''
        images += '''
							<a class="prev" onclick="plusSlides(-1)"> <i class="fas fa-chevron-left"></i> prev </a>
							<a class="next" onclick="plusSlides(1)"> next <i class="fas fa-chevron-right"></i> </a> 
				
							<div class="caption-container">
								<p id="caption"></p>
							</div>
							'''

                                                        
        images += ''' 
				</div> <!--  lightbox modalcontent end -->
			</div> <!--  lightbox modal end -->
			'''
			
			
			
			# Functions for tabed gallery
        images+= '''
			<script> <!--  Functions for the tabed gallery -->
				filterSelection("all")
				function filterSelection(c) {
					var x, i;
					x = document.getElementsByClassName("column");
					if (c == "all") c = "";
					for (i = 0; i < x.length; i++) {
						w3RemoveClass(x[i], "show");
						if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show");
					}
				}
				
				
				function w3AddClass(element, name) {
					var i, arr1, arr2;
					arr1 = element.className.split(" ");
					arr2 = name.split(" ");
					for (i = 0; i < arr2.length; i++) {
						if (arr1.indexOf(arr2[i]) == -1) {element.className += " " + arr2[i];}
					}
				}
				
				
				function w3RemoveClass(element, name) {
					var i, arr1, arr2;
					arr1 = element.className.split(" ");
					arr2 = name.split(" ");
					for (i = 0; i < arr2.length; i++) {
						while (arr1.indexOf(arr2[i]) > -1) {
							arr1.splice(arr1.indexOf(arr2[i]), 1);     
						}
					}
					element.className = arr1.join(" ");
				}
				
				
				// Add active class to the current button (highlight it)
				var btnContainer = document.getElementById("myBtnContainer");
				var btns = btnContainer.getElementsByClassName("btn");
				for (var i = 0; i < btns.length; i++) {
					btns[i].addEventListener("click", function(){
						var current = document.getElementsByClassName("active");
						current[0].className = current[0].className.replace(" active", "");
						this.className += " active";
					});
				}
			</script>'''
              
            #Function to show the slides
        images += '''
            <script> <!--  Functions for the slide view -->
				function openModal() {
				document.getElementById("myModal").style.display = "block";
				}
				
				function closeModal() {
				document.getElementById("myModal").style.display = "none";
				}
				
				var slideIndex = 1;
				showSlides(slideIndex);
				
				function plusSlides(n) {
				showSlides(slideIndex += n);
				}
				
				function currentSlide(n) {
				showSlides(slideIndex = n);
				}
				
				function showSlides(n) {
				var i;
				var slides = document.getElementsByClassName("mySlides");
				var dots = document.getElementsByClassName("demo");
				var captionText = document.getElementById("caption");
				if (n > slides.length) {slideIndex = 1}
				if (n < 1) {slideIndex = slides.length}
				for (i = 0; i < slides.length; i++) {
					slides[i].style.display = "none";
				}
				for (i = 0; i < dots.length; i++) {
					dots[i].className = dots[i].className.replace(" active", "");
				}
				slides[slideIndex-1].style.display = "block";
				dots[slideIndex-1].className += " active";
				captionText.innerHTML = dots[slideIndex-1].alt;
				}
			</script>
            '''
            
        images += '''
			<script>
				function leftArrowPressed() {
					plusSlides(-1)
				}
					
				function rightArrowPressed() {
					plusSlides(1)
				}
				
				function EscPressed() {
					closeModal()
				}
					
				document.onkeydown = function(evt) {
					evt = evt || window.event;
					switch (evt.keyCode) {
						case 37:
							leftArrowPressed();
							break;
						case 39:
							rightArrowPressed();
							break;
						case 27:
							EscPressed();
							break;
						}
					};
						
							
			</script>
            '''
                        
        

        
        html6.append(_skeleton.Thebody("Plots", images,_formplot.Theform()))
        html6.append(_skeleton.Thefooter())
        return html6 

    # =================================================================================
    #  Contact
    # =================================================================================
    @cherrypy.expose
    def Contact(self):
       	html7 = [_skeleton.Thestart()]
       	#html7.append(_skeleton.Theheader("ID Alignment"))
       	html7.append(_skeleton.TheNavBar())
       	msg.printGreen("Accessing to: contacts_page")
       	html7.append(_contact.contacts_page("salvador.marti@cern.ch", "pablo.martinez.agullo@cern.ch"))
       	html7.append(_skeleton.Thefooter())
       	return html7 

    # =================================================================================
    #  About
    # =================================================================================
    @cherrypy.expose
    def About(self):
       	html8 = [_skeleton.Thestart()]
       	#html8.append(_skeleton.Theheader("ID Alignment"))
       	html8.append(_skeleton.TheNavBar())
       	html8.append(_contact.AboutThisPage())
       	html8.append(_skeleton.Thefooter())
       	return html8 

# =================================================================================
#  PrintRunInfo
# =================================================================================    
def PrintRunInfo(theRunInfoDB):
    import cPickle
    listOfRuns = theRunInfoDB.keys()
    print " <PrintRunInfo> List of runs in DB file: ",listOfRuns

    '''
    runcount = 0
    for run_char in listOfRuns:
        run = int(run_char)
        runcount += 1
        print " "
        print " =============================================================== " 
        print " =================  run: %6d (%3d/%3d)  ===================== " %(run, runcount, len(listOfRuns))
        print " =============================================================== " 
        listOfKeys = readdatabase[run].keys()
        print " number of keys for this run: ",len(listOfKeys)
        for keyName in listOfKeys:
            listOfValues = readdatabase[run][keyName]
            if ('list' in type(listOfValues).__name__):
                for i in range(len(listOfValues)):
                    print " [%d][%s][%d]  =  %s" %(run, keyName, i, listOfValues[i]) 
            else:
                print " [%d][%s]  =  %s " %(run, keyName, readdatabase[run][keyName])
      '''                  

#################################################################
#################################################################
#################################################################

# =================================================================================
#  __name__
# =================================================================================
application_conf = {
   '/' : {'tools.staticdir.on': True,
          'tools.staticdir.dir': current_dir},
       }

root = Web(theYear)

# -- local test --
if __name__=='__main__':

    if (runLocalTest):
        conf={
            '/': {
                'tools.sessions.on':True,
                'tools.staticdir.root':os.path.dirname(os.path.abspath(__file__))
            },
            '/static' : {						# Servig the entire static directory
                'tools.staticdir.on':True,
                'tools.staticdir.dir':'./static'
            }
            }
            
        msg.printGreen("---")
        msg.printGreen("Debug: '/' : tools.staticdir.root  = " + os.path.dirname(os.path.abspath(__file__)))
        msg.printGreen("Debug: '/static' : tools.staticdir.root  = " + './static')
        msg.printGreen("---")
            
        cherrypy.tree.mount(root,'/webapp',config=application_conf) # Tree is used to host several applications in the server
        cherrypy.quickstart(root,'/',conf) #cherrypy.quickstart(app root, script name, config)
    # -- end of local test --  

# =================================================================================
#  setup_server
# =================================================================================
def setup_server():

    cherrypy.tree.mount(root, '/webapp', config=application_conf)
