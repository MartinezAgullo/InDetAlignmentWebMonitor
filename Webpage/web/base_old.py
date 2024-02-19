#
# base.py
#
import os

#check with environment variable if server runs as local test 
runLocalTest = False
try:
    runLocalTest = os.getenv('RUNLOCALTEST', False)
except:
    runLocalTest = False

##############################################################
class Skeleton:

    
    def Thestart(self):
    
        self.start="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta charset="UTF-8"/>
  <title>ID Alignment</title>
  <link rel="stylesheet" media="screen" href="./static/css/style.css" />
  <link rel="icon" href="./static/images/logo.gif" />  
  <script type="text/javascript" src="./static/js/jquery-latest.js"></script> 
  <script type="text/javascript" src="./static/js/jquery.tablesorter.js"></script>
  <script type="text/javascript" id="js">
  $(document).ready(function()
  {
	$("table").tablesorter();
  }
  );
  </script>
</head>
<body>
"""
        return self.start


    def Thestart2(self):
    
        self.start="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta charset="UTF-8"/>
  <title>ID Alignment</title>
  <link rel="stylesheet" media="screen" href="./static/css/style.css" />
  <link rel="icon" href="./static/images/logo.gif" />  
</head>
<body>
"""


    def Theheader(self,string, theYear="2018"):
        self.header="""<div id="header">
  <abbr title="Atlas, the primordial Titan who supported the heavens"><img id="logo" src="./static/images/logo.png" /></abbr>
  <h1><a href="../webapp/">%s</a></h1>
  <ul>
    <li><a href="../webapp/Plots">Plots</a></li>
    <li><a href="https://atlas.web.cern.ch/Atlas/Collaboration//">ATLAS</a></li>
    <li><a href="https://tzcontzole01.cern.ch/run2/tasklister/">conTZole</a></li>
    <li><a href="https://twiki.cern.ch/twiki/bin/view/AtlasComputing/AlignmentWebDisplayHowTo">Documentation Twiki</a></li>
    <li><a href="https://svnweb.cern.ch/trac/atlasoff/browser/InnerDetector/InDetMonitoring/InDetAlignmentWebMonitor"> Source code </a></li>
    <li><a href="../webapp/bshandshake/HandShake_log_%s.txt"> BS Hand shake </a></li>
    <li><a href="https://atlas.web.cern.ch/Atlas/GROUPS/DATABASE/project/catrep/nemo/live.html"> Upload DB folder status </a></li>
    </ul>
</div>"""
        return self.header %(string, theYear)


    def Thefooter(self):
        self.footer="""<div id="footer">
    <a href="mailto:salvador.marti@cern.ch">Contact</a>
</div>
</body>
</html>"""
        return self.footer
        
    ###########################################################    
    def Thebody(self, n, left, right):
        import os, time
        server = "/var/vhost/atlas-alignment/database/"
        runLocalTest = True
        if runLocalTest == True:
			base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) 
			server = base_dir + "/database/"
			#server = "/Users/martis/projectes/atlas/alineament/webmonitoringtest/InDetAlignmentWebMonitor/trunk/database/"

        theYear = os.getenv('ALIGNWEBYEAR',"2018")
        print " <Thebody> theYear = %s" % theYear

        runInfoDBfile = "server_runinfo%s.db" % theYear
        self.body=""""""

        
        if (not os.path.isfile(server + runInfoDBfile)):
            self.body="""<div id="wrapper">
            <div id="content">%s File %s does not exist </div>
            <div id="searchs">%s</div>
            </div>""" % (left,runInfoDBfile,right)
        else:
            print "runInfoDBfile checked" 
            try:
                accesstime = time.strftime("%a, %d/%b/%y %H:%M:%S", time.localtime(os.stat(server + runInfoDBfile)[8]))
                nRunsInList = int(n)
                self.body="""<div id="wrapper">
                <div id="content"><h2>%s runs </h2><align="right">Last update of %s was %s </> %s</div>
                <div id="searchs">%s</div>
                </div>""" % (nRunsInList, runInfoDBfile, accesstime, left,right)

            except:

                if n == "Find":
                    self.body="""<div id="wrapper">
                    <div id="content"><h2>Runs matched</h2>%s</div>
                    <div id="searchs">%s</div>
                    </div>""" % (left,right)

                elif n == "RTT":
                    self.body="""<div id="wrapper">
                    <div id="content"><h2>RTT</h2> < /br> %s</div>
                    <div id="searchs">%s</div>
                    </div>""" % (left,right)

                elif n == "Plots":
                    self.body="""<div id="wrapper">
                    <div id="content">%s</div>
                    <div id="searchs">%s</div>
                    </div>""" % (left,right)

        return self.body
        
###################################        
    def Comments(self):

        self.comment = """<h2>You can plot:</h2>
<ul>
 <li>A period or several, just put in the form your desired periods or subperiods separated by ',' (e.g. k,l,m or k2,l1,m3)</li>
 <li>A range of runs, just put in the form the minimun run number and the maximun run number</li>
 <li>Just one run</li>
 </ul>
 <h2>Old data:</h2>
 <ul>
 <li>You can ask for old runs (2011 & 2012)</li>
 <li>Just remember to write the year of the required year in the old data button</li>
 </ul>
<h2>Results:</h2>
<ul>
 <li>You get two plots for each DoF (L11 & L2)</li>
 <li>For several runs/periods, it is represented correction vs run number</li>
 <li>For a particular run, it is represented correction vs element aligned</li>
 <li>You can download each plot in .eps</li>
 <li>Generate the plots may take a while, be patient please. If you find some issue, please contact me!!</li>
</ul>





"""
        return self.comment
        
##################################################################
##################################################################

class Tables:
    def __init__(self):
        self.tablehead=""
        self.tablerow=""
        self.tableend=""
####################################################################
    def Thetablehead(self,string1,string2,string3,string4, string5): # adding the string name
        #self.tablehead="""<table cellspacing="1" class="tablesorter">
#<thead>
#    <tr>
#        <th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>Plots</th><th>Extended plots</th>
#        <th>%s</th><th>Plots</th><Extended plots</th>
#    </tr>
#</thead>
#<tbody>"""
        self.tablehead="""<table cellspacing="1" class="tablesorter">
<thead>
    <tr>
        <th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>Alignment results </th><th> Monitoring plots </th> <th> DB upload </th> <th> BS Handshake </th>
    </tr>
</thead>
<tbody>"""

        #return self.tablehead %(string1,string2,string3,string4,string5,string6)
        #return self.tablehead %(string1,string2,string3,string4)
        return self.tablehead %(string1,string2,string3,string4,string5) # adding the string name

#############################################################################################
    def Thetablerow(self,string1,string2,string3,stringProject,stringStream,stringDate,stringTime,stringBSHandshake,stringBSHSAuthor, stringL11Results, myL16Results, myDBTimeStamp, myAnalysisFile, theConstantsFile,string8): 
        
        #print "Test <Thetablerow> : string1(nrun) = " + str(string1) +", string2(period) = " + str(string2) +", string3(subperiod) = " + str(string3) 
           
        import cPickle
        runLocalTest = True
        if runLocalTest == True:
			server = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
			theYear = os.getenv('ALIGNWEBYEAR',"2018")
			detailedplots_path = server + "/WebPage/detailed_plots/" +str(theYear) + "/plots"+str(theYear)+".db"
			detailedplots = cPickle.load(open(detailedplots_path,'r'))
        else:
            theYear = os.getenv('ALIGNWEBYEAR',"2018")

        if (False):
            # this lists period and subperiod    
            self.tablerow="""<tr>
<td><a href="http://atlas-runquery.cern.ch/query.py?q=find+run+%(nrun)i+/+show+all+/+nodef">%(nrun)i</a></td><td><a href="http://atlas-runquery.cern.ch/query.py?q=find+run+period%(period)s+/+show+all+/+nodef">%(period)s</a><a href="http://atlas-runquery.cern.ch/query.py?q=find+run+period%(subperiod)s+/+show+all+/+nodef">%(subperiod)s</a></td><td> %(mydate)s %(mytime)s </td><td>%(myproject)s </td><td> %(mystream)s </td>"""
        else:
            # this lists only the subperiod
            self.tablerow="""<tr>
<td><a href="http://atlas-runquery.cern.ch/query.py?q=find+run+%(nrun)i+/+show+all+/+nodef">%(nrun)i</a></td><td> <a href="http://atlas-runquery.cern.ch/query.py?q=find+run+period%(subperiod)s+/+show+all+/+nodef">%(subperiod)s</a></td><td> %(mydate)s %(mytime)s </td><td>%(myproject)s </td><td> %(mystream)s </td>"""

        if theConstantsFile == "No":
            self.tablerow += """<td><font color="red">%(constantsFile)s</td> """
        else:
            self.tablerow += """<td><a href="/webapp/Plotting?nruns=%(nrun)i&idtracks=0&minruns=0&maxruns=0&periods=&subperiods=&olddata=FALSE"> Draw constants</a> """
            self.tablerow += """| <a href="/webapp/alignlogfiles/2018/ONLINE/00%(nrun)i/alignlogfileIter0.txt"> View L11 </a> </td>"""


        self.tablerow += """<td> <a href="/webapp/PlotMonitoring?nruns=%(nrun)i&plotsType=%(resplots)s"> Residuals </a> """
        self.tablerow += """| <a href="/webapp/PlotMonitoring?nruns=%(nrun)i&plotsType=%(hitsplots)s"> Hits </a> """
        self.tablerow += """| <a href="/webapp/PlotMonitoring?nruns=%(nrun)i&plotsType=%(hitmaps)s"> Hit Maps </a> """
        self.tablerow += """| <a href="/webapp/PlotMonitoring?nruns=%(nrun)i&plotsType=%(iblres)s"> IBL Res. </a> """
        self.tablerow += """| <a href="/webapp/PlotMonitoring?nruns=%(nrun)i&plotsType=%(resmaps)s"> Residual Maps </a> """
        self.tablerow += """</td> """
        
        # the upload constants DB part
        if (theConstantsFile != "No"): # check that there exists alignment results
            if (stringL11Results == "Good"):
                self.tablerow += """<td> <font color="green"> L11 %(L11Results)s  <font color="black"> | """
            else :
                self.tablerow += """<td> <font color="red"> L11 %(L11Results)s <font color="black"> | """

            
            if (myL16Results == "Good"):
                self.tablerow += """ <font color="green"> L16 %(L16Results)s """
            else :
                self.tablerow += """ <font color="red"> L16 %(L16Results)s """
            
            self.tablerow += """ <font color="black"> |  %(DBTimeStamp)s """

            self.tablerow += """ | Summary File """
            if ('?' in myAnalysisFile):
                self.tablerow += """  None """
            else:
                self.tablerow += """ <a href="../webapp/runanalysislog/2018/%(AnalysisFile)s"> %(AnalysisFile)s </a>"""
        else:
            self.tablerow += """<td> No Alignment results """    
        # clsoe the current cell
        self.tablerow += """</td>"""

            
        # the upload constants DB part
        if ('?' in stringBSHandshake):
            self.tablerow += """<td> <strong><font color="orange"> PENDING  </strong></td></tr>"""
        else:
            self.tablerow += """<td> <font color="green"> %(bshandshake)s %(bshsauthor)s </td></tr>"""
                
        return self.tablerow %{"nrun": int(string1),"period":string2,"subperiod":string3,"mydate":stringDate,"myproject":stringProject,"mystream":stringStream,"constantsFile":theConstantsFile,"detailedPlots":string8,"resplots":"RESID","hitsplots":"HITS","hitmaps":"HITMAPS","iblres":"IBLRES","resmaps":"RESMAPS","bshandshake":stringBSHandshake,"bshsauthor":stringBSHSAuthor,"L11Results":stringL11Results, "L16Results":myL16Results, "DBTimeStamp":myDBTimeStamp, "AnalysisFile":myAnalysisFile, "mytime":stringTime}

#############################################################################################    
    def Thetableend(self):
        self.tableend="""</tbody></table>"""

        return self.tableend
##################################################################
##################################################################

class Formulary:

    def __init__(self):
        self.form = """ """

    def Theform(self, theYear = "2018"):
        self.form1 = """<form method="get" action="index" type="submit"><select name="theYear"><option>2019</option><option>2018</option><option>2017</option><option>2016</option><option>2015</option></select><button type="submit">Go!</button></form> """

        self.form ="""<form action="Find" method="GET">
Search
<table>
<tr>
<td><label for="run">Run:</label> <input type="text" value="0" maxlength="8" size="9" name="nrun" class="campo" /></td></tr>
<tr>
<td><label for="period">Period:</label> <input type="text" value="" maxlength="1" size="9"name="string" class="campo" /></td>
</tr>
<tr>
<td><label for="events">Min. number of Events:</label> <input type="text" value="0" maxlength="15" size="9" name="nevents" class="campo" /></td>
</tr>
<tr>
<td><label for="idtracks">Min. number of ID Tracks:</label> <input type="text" value="0" maxlength="15" size="9" name="nidtracks" class="campo" /></td>
</tr>
<tr>
<td><input value="submit" type="submit"></td>
</tr>
<tr>
<td><input value="reset" type="reset"></td>
</tr></table>"""
#</form>
#RTT
#<center><a href="/webapp/constant/RTT_control.png" align="center"><img src="/webapp/constant/RTT_control.png" width="80%"/></a></center>"""
        return self.form1 + self.form
################################################################
################################################################

class FormularyPlot:

    def QuickDisplay(self):
        from searchpickle import LastRuns
        a = LastRuns(100)
        print " <base.QucikDisplay> a = lastRuns(100) = ",a
        minmaxruns = a.LastN()
        print " <base.QucikDisplay> minmaxruns = ",minmaxruns
        return minmaxruns 
        
################################################################    
    def Theform(self):
        self.form ="""<form action="Plotting" method="GET">
<table>
<tr>
<td><b>Plots</b></td></tr><tr><td><input type="button" value="All runs" name="mySelection" onclick="window.open('../webapp/Plotting?nruns=0&idtracks=0&minruns=%i&maxruns=%i&periods=&subperiods=&olddata=FALSE')" /></td>
</tr>
<tr>        
<td><label for="nruns">Run:</label> <input type="text" value="0" maxlength="20" size="4" name="nruns" class="campo" /></td>
<td><label for="idtracks">Min. IDTracks:</label> <input type="text" value="0" maxlength="8" size="6" name="idtracks" class="campo" /></td>
</tr>
<tr>
<td><label for="minruns">Min. Run:</label> <input type="text" value="0" maxlength="8" size="4" name="minruns" class="campo" /></td>
<td><label for="maxruns">Max. Run:</label> <input type="text" value="0" maxlength="8" size="4" name="maxruns" class="campo" /></td>
</tr>
<tr>
<td><label for="periods">Period (e.g. j,l,m):</label> <input type="text" value="" maxlength="20" size="4" name="periods" class="campo" /></td>
<td><label for="subperiods">Suberiod (e.g. j2,l1):</label> <input type="text" value="" maxlength="20" size="4" name="subperiods" class="campo" /></td></tr>
<tr>
<td><label for="olddata">Old Data (2011 & 2012 available):</label><input type="text" value="" maxlength="4" size="7" name="olddata" class="campo" /></td>
<td><input value="Plot" type="submit"> <input value="reset" type="reset"></td>
</tr></table></form>"""
        last10 = self.QuickDisplay()
        print " <base.Theform> last 10: ",last10
        first = 0;
        last = 1;
        last = len(last10)-1
        if (len(last10) <= 1): last = 0
        print " <base.Theform> first= %s   last= %s:   From Run %s to %s" %(str(first), str(last), str(last10[last]), str(last10[first])) 
        print "last10[last] = " +str(last10[last])
        print "last10[first] = " +str(last10[first])
        theCommand = self.form %(int(last10[last]),int(last10[first]))
        print " <base.Theform> the Command = ", theCommand
        return self.form %(int(last10[last]),int(last10[first]))
    
################################################################
################################################################

class Error:
    def error1(self):
        
        error = """<h3>Oops!! There is an error (error1) </h3>
                <p>Remember, Run must be an integer</p>
                <p>Period must be a letter</p>
                <p>Events must be an integer</p>
                <p>ID Tracks must be an integer</p>"""
        return error

    def error2(self):
        
        error = """<h3>Oops!! There is an error (error2) Error code: 2 </h3>
                <p> Salva --> Remember, run, min. run and max. run must be an integer</p>
                <p>If you want a range of plots displayed, you have to put both, the min. run and the max. run</p>
                <p>If you want several periods/subperiods, you have to put the periods/subperiods separated by comma, without blanks</p>"""
        return error

    def error3(self):
        
        error = """<h3>Oops!! There is a VIE, very important error</h3>
                <p>Can not be found the environment file, please, send an email</p>"""
        return error

    def error4(self):
        error = """<h3>Oops!! There is an error (error4)</h3>
                <p>Remember, run, min. run and max. run must be an integer</p>
                <p>If you want a range of plots displayed, you have to put both, the min. run and the max. run</p>
                <p>If you want several periods/subperiods, you have to put the periods/subperiods separated by comma, without blanks</p>"""
        return error

    def error5(self):
        error = """<h3>Oops!! There is an error (error5)</h3>
                <p>Remember, run, min. run and max. run must be an integer</p>
                <p>If you want a range of plots displayed, you have to put both, the min. run and the max. run</p>
                <p>If you want several periods/subperiods, you have to put the periods/subperiods separated by comma, without blanks</p>"""
        return error
    
    def error6(self):
        error = """<h3>Oops!! There is an error (error6)</h3>
                <p>Remember, run, min. run and max. run must be an integer</p>
                <p>If you want a range of plots displayed, you have to put both, the min. run and the max. run</p>
                <p>If you want several periods/subperiods, you have to put the periods/subperiods separated by comma, without blanks</p>"""
        return error
