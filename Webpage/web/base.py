#
# base.py
#
import os, commands, datetime

#check with environment variable if server runs as local test 
runLocalTest = False
try:
    runLocalTest = os.getenv('RUNLOCALTEST', False)
except:
    runLocalTest = False

# set year for server_runinfoYEAR.db
server = "%s/database/" % (str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
print server
print "Creating a symbolic link to database"
os.system("ln -fs %s ." % server)

theYear = datetime.datetime.today().year
if not os.path.isfile("%s/server_runinfo%d.db" % (server, theYear)):
    year_arr = commands.getoutput('ls -r %s | grep .db' % server).splitlines()
    max = int(year_arr[0].replace('server_runinfo', '').replace('.db', ''))
    for iyear in year_arr:
        iyear = int(iyear.replace('server_runinfo', '').replace('.db', ''))
        if iyear > max: max = iyear
    theYear = max
# print 'theYear',theYear
# print os.getenv('ALIGNWEBYEAR')
os.environ["ALIGNWEBYEAR"] = "%d" % theYear
# print os.getenv('ALIGNWEBYEAR')

# fix runLocalTest
# print runLocalTest
    
# =================================================================================
#  class Skeleton
# =================================================================================
class Skeleton:

    # =================================================================================
    #  Thestart
    # =================================================================================
    def Thestart(self):
    
        self.start="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml">
<head>  
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> <!-- bootstrap is optimized for mobile -->
    
  <title>ID Alignment</title>
  
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
  <link rel="stylesheet" media="screen" href="./static/css/style.css" />			    <!-- MINE -->
  <link rel="icon" href="./static/images/logo.gif" />  									<!-- MINE -->
  <link href='https://fonts.googleapis.com/css?family=Open Sans' rel='stylesheet'>
  <script src="https://kit.fontawesome.com/a076d05399.js"></script>
  <script type="text/javascript" src="./static/js/jquery-latest.js"></script>  		    <!-- MINE -->
  <script type="text/javascript" src="./static/js/jquery.tablesorter.js"></script>      <!-- MINE -->
  <script type="text/javascript" id="js">
  
  $(document).ready(function()
  {
	$("table").tablesorter();
  }
  );
 		
  </script>
  
  <script>
  $(".show-all").on("click", function() {
  $("tbody > tr", $(this).prev()).show();
	});
	
	#runTable.show-all > tbody > tr {
	display: table-row;
	}
  </script>
  
</head>
<body>

	<!--<div class="container"> <!-- The container is the main element for using Bootstrap -->
"""
        return self.start

    # =================================================================================
    #  Theheader
    # =================================================================================
    def Theheader(self,string):
        self.header="""
			<div id="header">
            </div>
            """
        return self.header %(string)

    # =================================================================================
    #  TheNavBar
    # =================================================================================
    def TheNavBar(self):
		self.navbar='''
			 <!-- <div class="jumbotron"> -->
				<nav class="navbar navbar-expand-lg bg-dark text-white"> 

					<!-- <a class="navbar-brand" href="../webapp/"><img src="ATLAS.png"></a>  -->
                    <a class="navbar-brand" href="../webapp/"></a>
					<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
						<span style="color: #bbb" class="navbar-toggler-icon"> <i class="fas fa-bars"></i> </span>
					</button>

					<div class="collapse navbar-collapse" id="navbarSupportedContent">
						<ul class="navbar-nav mr-auto">
						
							<li class="nav-item active">
								<a class="nav-link" href="/webapp/"> <i class="fas fa-home"></i> Home</a>
							</li>


							<li class="nav-item dropdown">
								<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
								<i class="fas fa-toolbox"></i> Utils
								</a>
								<div class="dropdown-menu" aria-labelledby="navbarDropdown">
									<a style="color:#276ca3" class="nav-link" href="../webapp/bshandshake/HandShake_log_%s.txt"> <i class="far fa-handshake"></i> BS Hand shake</a>
									<a style="color:#276ca3" class="nav-link" href="https://tzcontzole01.cern.ch/run2/tasklister/"> <i class="fas fa-table"></i> TZ Task Lister </a>
									<a style="color:#276ca3" class="nav-link" href="https://atlas.web.cern.ch/Atlas/GROUPS/DATABASE/project/catrep/nemo/live.html"> <i class="fas fa-server"></i> Upload DB folder status</a>
								</div>
							</li>
						
							<li class="nav-item dropdown">
								<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
								<i class="far fa-file"></i> Documentation
								</a>
								<div class="dropdown-menu" aria-labelledby="navbarDropdown">
									<a style="color:#276ca3" class="dropdown-item" href="https://twiki.cern.ch/twiki/bin/view/AtlasComputing/AlignmentWebDisplayHowTo"> <i class="fas fa-book"></i> Twiki</a>
									<a style="color:#276ca3" class="dropdown-item" href="https://www.overleaf.com/read/xtyhycgbtdtv"> <i class="far fa-file-pdf"></i> Notes</a>
									<a style="color:#276ca3" class="nav-link" href="../webapp/Plots"><i class="fas fa-chart-bar"> </i> Plots</a>
									<div class="dropdown-divider"></div>
									<a style="color:#276ca3" class="nav-link" href="https://atlas.web.cern.ch/Atlas/Collaboration//"> <i class="fas fa-globe"></i> ATLAS</a>
									<div class="dropdown-divider"></div> 
									<a style="color:#276ca3" class="dropdown-item" href="/webapp/About">About the monitoring</a>
								</div>
							</li>
							
							<li class="nav-item">
								<a class="nav-link" href="https://gitlab.cern.ch/atlas-idalignment/InDetAlignmentWebMonitor/tree/master"> <i class="fas fa-code"></i> Source code</a>
							</li>	
							
							<li class="nav-item active">
								<a class="nav-link" href="/webapp/Contact"> <i class="fas fa-envelope"></i> Contact</a>
							</li>
							
						
						
						<!-- search button -->	
						<!--   
						</ul>
						<form class="form-inline my-2 my-lg-0">
							<input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
							<button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
						</form>
						--> 
						
					</div>
				</nav>
			 <!-- </div> --> <!-- nav bar jumbotron -->
			 
			 <!--</div>-->  <!-- nav bar container -->	
			
		<!-- <div class="container"> --> <!-- container for the body starts over the navbar)-->
		<div class="shadow"> 	<!-- shadow for the body -->
		<div class="jumbotron" style="border-radius: 0px 0px 0px 0px; margin-bottom: 0px;"> <!-- jumbotron start  for the body-->
		'''
		return self.navbar

    # =================================================================================
    #  Thefooter
    # =================================================================================
    def Thefooter(self):
        self.footer="""
			
		</div> <!-- jumbotron end -->
	</div> <!-- shadow -->

		
		<div id="footer" >
				<p class="copyright twocol"> ATLAS ID alignment team - The ATLAS Experiment &#169; 2019 CERN - all rights reserved</p>
		</div><!-- #footer -->
		
		<!--Inserting jQuery dependency of Bootstrap-->
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
		<!--Compiled js file -->
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
		
		<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
		
		<script>    <!-- SERCH ELEMMENTS IN TABLE (only shows row) -->
			function mySearcher() {
				var input, filter, table, tr, td, i, txtValue;
				input = document.getElementById("myInput");
				filter = input.value.toUpperCase();
				table = document.getElementById("runTable");
				tr = table.getElementsByTagName("tr");
				for (i = 0; i < tr.length; i++) {
					tr[i].style.display = "none";
					td = tr[i].getElementsByTagName("td");
					for (var j = 0; j < td.length; j++) {
						cell = tr[i].getElementsByTagName("td")[j];
						if (cell){
							txtValue = cell.textContent || cell.innerText;
								if (txtValue.toUpperCase().indexOf(filter) > -1) {
								tr[i].style.display = "";
							}
						}
					}
				}
			}
		</script>
		
		
		
		<script>    <!-- DISPLAY  RUNS RANGE (only shows row) -->
			function my_Limits() {
				var input_LOW, input_UP, run, table, tr, td, i;
				document.getElementById("demo").innerHTML = document.getElementById("myInput_lim");
				String input = document.getElementById("myInput_lim")
				display(input)
				input_LOW = input.split("-")[0]
				input_UP = input.split("-")[1]
				
				table = document.getElementById("runTable");
				tr = table.getElementsByTagName("tr");
				for (i = 0; i < tr.length; i++) {
					tr[i].style.display = "none";
					td = tr[i].getElementsByTagName("td");
					run = tr[i].getElementsByTagName("td")[0];
					if (run >= input_LOW && run <= input_UP){
							tr[i].style.display = "";
					}
				}
			}
		</script>
		
		
		
		<script> <!-- SORT ELEMMENTS IN TABLE COLUMN (Sorter alphabetic)-->
			function sortTable_Alph(n) {
				var table, rows, switching, i, x, y, shouldSwitch;
				table = document.getElementById("runTable");
				switching = true;
				//Set the sorting direction to ascending:
				dir = "asc";
				/*Make a loop that will continue until no switching has been done:*/
				while (switching) {
					//start by saying: no switching is done:
					switching = false;
					rows = table.rows;
					/*Loop through all table rows (except the first, which contains table headers):*/
					for (i = 1; i < (rows.length - 1); i++) {
						//start by saying there should be no switching:
						shouldSwitch = false;
						/*Get the two elements you want to compare,
						one from current row and one from the next:*/
						x = rows[i].getElementsByTagName("TD")[n];
						y = rows[i + 1].getElementsByTagName("TD")[n];
						//check if the two rows should switch place:
						
						if (dir == "asc") {
							if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
								//if so, mark as a switch and break the loop:
									shouldSwitch= true;
									break;
							}
						}
						else if (dir == "desc") {
							if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
								//if so, mark as a switch and break the loop:
								shouldSwitch = true;
								break;
							}
						}
					}
					if (shouldSwitch) {
						/*If a switch has been marked, make the switch and mark that a switch has been done:*/
						rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
						switching = true;
						//Each time a switch is done, increase this count by 1:
						switchcount ++; 
						}
					else {
						/*If no switching has been done AND the direction is "asc",
						set the direction to "desc" and run the while loop again.*/
						if (switchcount == 0 && dir == "asc") {
							dir = "desc";
							switching = true;
							}
						}
					}
				}
		</script>
		

		<script> <!-- SORT ELEMMENTS IN TABLE COLUMN (Sorter numeric)-->
			function sortTable_num(n){
				var table, rows, switching, i, x, y, shouldSwitch;
				table = document.getElementById("runTable");
				dir = "asc";
				switching = true;
				/*Make a loop that will continue until no switching has been done:*/
				while (switching) {
					//start by saying: no switching is done:
					switching = false;
					rows = table.rows;
					/*Loop through all table rows (except the first, which contains table headers):*/
					for (i = 1; i < (rows.length - 1); i++) {
						//start by saying there should be no switching:
						shouldSwitch = false;
						/*Get the two elements you want to compare,
						one from current row and one from the next:*/
						x = rows[i].getElementsByTagName("TD")[n];
						y = rows[i + 1].getElementsByTagName("TD")[n];
						//check if the two rows should switch place:
						if (dir == "asc") {
							if (Number(x.innerHTML) > Number(y.innerHTML)) {
								//if so, mark as a switch and break the loop:
								shouldSwitch = true;
								break;
								}
							}
						if (dir == "des"){
							if (Number(x.innerHTML) < Number(y.innerHTML)) {
								//if so, mark as a switch and break the loop:
								shouldSwitch = true;
								break;
								}
							}
					}
					if (shouldSwitch) {
						/*If a switch has been marked, make the switch and mark that a switch has been done:*/
						rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
						switching = true;
						//Each time a switch is done, increase this count by 1:
						switchcount ++; 
						}
					else {
						/*If no switching has been done AND the direction is "asc",
						set the direction to "desc" and run the while loop again.*/
						if (switchcount == 0 && dir == "asc") {
							dir = "desc";
							switching = true;
							}
						}	
						
				}
		</script>
		
		</body>
		</html>"""
        return self.footer
        
    # =================================================================================
    #  Thebody
    # ================================================================================= 
    def Thebody(self, n, left, right):
        import os, time
        server = "/var/vhost/atlas-alignment/database/"
        runLocalTest = True
        if runLocalTest == True:
			base_dir = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) 
			server = base_dir + "/database/"

        # print '****************** theYear', theYear
        print "****************** os.getenv('ALIGNWEBYEAR')", os.getenv('ALIGNWEBYEAR')
            
        theYear = os.getenv('ALIGNWEBYEAR')
        print " <Thebody> theYear = %s" % theYear        
        runInfoDBfile = "server_runinfo%s.db" % theYear
        self.body=""" 
        """

        if (not os.path.isfile(server + runInfoDBfile)):
            self.body="""
            <!-- starts body (NOT PATH) -->
            <div id="wrapper">
				<div id="content">%s File %s does not exist </div>
				<div id="searchs">%s</div> 
            </div> <!-- wrpper -->""" % (left, runInfoDBfile, right)
        else:
            print "runInfoDBfile checked" 
            try:
                accesstime = time.strftime("%a, %d/%b/%y %H:%M:%S", time.localtime(os.stat(server + runInfoDBfile)[8]))
                nRunsInList = int(n)
                self.body="""
                <!-- starts body (DISPLAY TABLE) -->
 
                <div class="align_left">
					<p>Runs <span class="badge badge-pill"> %s </span></p>
					<span style="float:left;">
						<p>Last update of <a href="https://gitlab.cern.ch/atlas-idalignment/InDetAlignmentWebMonitor/tree/master/database" style:"text-decoration: none;"> <span class="badge badgelink badge-pill">   %s  </span> </a> was on <span class="badge badge-pill badge-info"> %s </span></p>
					</span>
				</div>
				
                <div id="wrapper">
					<!--  <div id="content">  ->   <!-- content (old format) -->
						<!-- TABLE STARTS HERE -->
						 <align="right">  </> %s  
						<!-- TABLE ENDS HERE -->
						
					 <!-- </div> -> <!-- content (old format) -->
					 <!-- <div id="searchs">  (fix)  %s</div> -->
				</div> <!-- wrpper -->
                """ % (nRunsInList, runInfoDBfile, accesstime, left, right)

            except:

                if n == "Find":
                    self.body="""
                    <!-- starts body (FIND) -->
                    <div id="wrapper">
						<div id="content"><h2>Runs matched</h2>%s</div>
						<div id="searchs">%s</div>
                    </div> <!-- wrpper -->""" % (left,right)

                elif n == "RTT":
                    self.body="""
                    <!-- starts body (RTT) -->
                    <div id="wrapper">
						<div id="content"><h2>RTT</h2> < /br> %s</div>
						<div id="searchs">
						%s
						</div> <!-- searchs -->
                    </div> <!-- wrpper -->""" % (left,right)

                elif n == "Plots":
                    self.body="""
                    <!-- starts body (PLOTS) -->
                    <div id="wrapper">
						<div id="content_table">%s</div>
						
                    </div> <!-- wrpper -->
                    <!-- end body (PLOTS) -->
                    """ % (left)

        return self.body
        
    # =================================================================================
    #  Comments
    # =================================================================================
    def Comments(self):
        self.comment = """
		<h2>You can plot:</h2>
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
        
# =================================================================================
#  class contact
# =================================================================================
class contact:
    # =================================================================================
    #  contacts_page
    # =================================================================================
	def contacts_page(self, AligmentResponsable, WebResponsable):
		self.contact_page = """
		<div class="entry">
			<header class="entry-header">
				<h1 class="entry-title">Contacts</h1>
				<!-- Here we could write some subtitle -->
			</header><!-- .entry-header -->
						
			<div class="entry-content">
				<p>Please send any support request to <a href="https://e-groups.cern.ch/e-groups/Egroup.do?egroupId=126698/">hn-atlas-IDAlignment</a> mailing list .</p>
				<p>You can also contact the <strong>current maintainer</strong> of the package writing to: <a href="mailto:%s"> %s</a>. </p>
				<p>Web mantainer:  <a href="mailto:%s"> %s</a>.</p>
				
				<div class="clear"></div>
			</div><!-- .entry-content -->
		</div><!-- .entry -->
		"""
		return self.contact_page %(AligmentResponsable, AligmentResponsable, WebResponsable, WebResponsable)

    # =================================================================================
    #  AboutThisPage
    # =================================================================================
	def AboutThisPage(self):
		self.aboutMonitor = """
		<div class="entry">
			<header class="entry-header">
				<h1 class="entry-title">About</h1>
				<!-- Here we could write some subtitle -->
			</header><!-- .entry-header -->
						
			<div class="entry-content">
				<p> 
						The <a href="https://atlasalignment.cern.ch/webapp/">web-based online monitoring</a>  of the track-based alignment of the ATLAS ID tracker monitors the alignment results obtained at the calibration loop.
						It helps to evaluate the computed alignment correction as well as many plots related with the performance.
				</p>
				
				<div class="clear"></div>
			</div><!-- .entry-content -->
		</div><!-- .entry -->
		"""
		return self.aboutMonitor 
		
# =================================================================================
#  class Tables
# =================================================================================
class Tables:
    
    # =================================================================================
    #  __init__
    # =================================================================================
    def __init__(self):
        self.tablehead=""
        self.tablerow=""
        self.tableend=""

    # =================================================================================
    #  Thetablehead
    # =================================================================================
    def Thetablehead(self,string1,string2,string3,string4, string5): # adding the string name
        self.tablehead="""
        <div id="TheTable">  <!-- test pablo -->
        
        <div class="align_right">
        <form style="width: 500 px; margin: 0 auto;">
        <filedset style="background: #fff; border-radius: 3px; padding: 5px 5px 5px 5px;">
        <button style="border: none;" disabled>
          <i class="fas fa-search"></i>
        </button>
        <input type="text" id="myInput" onkeyup="mySearcher()" placeholder="Filter table..." title="Type in a Run number">
        </filedset>
        </form>
        </div>

        <table cellspacing="2" class="table-responsive text-nowrap tableFixHead tablesorter" id="runTable">
			<thead>
				<tr>
				 <th scope="col" onclick="sortTable_num(0)">%s</th> 
				 <th scope="col">%s</th>
				 <th scope="col">%s</th>
				 <th scope="col">%s</th>
				 <th scope="col">%s</th>
				 <th scope="col">Alignment results </th>
				 <th scope="col"> DB upload </th>
				 <th scope="col"> BS Handshake </th>
				</tr>
			</thead>
			<tbody>
		"""

        #return self.tablehead %(string1,string2,string3,string4,string5,string6)
        #return self.tablehead %(string1,string2,string3,string4)
        print("string1,string2,string3,string4,string5 => 1:" + str(string1)+ ". 2:" + str(string2) + ". "+ str(string3) + ". 4:"+ str(string4) + ". 5:"+ str(string5)  )
        return self.tablehead %(string1,string2,string3,string4,string5) # adding the string name

    # =================================================================================
    #  Thetablerow
    # =================================================================================
    def Thetablerow(self,string1,string2,string3,stringProject,stringStream,stringDate,stringTime,stringBSHandshake,stringBSHSAuthor, stringL11Results, myL16Results, myDBTimeStamp, myAnalysisFile, theConstantsFile,string8): 
        
        #print "Test <Thetablerow> : string1(nrun) = " + str(string1) +", string2(period) = " + str(string2) +", string3(subperiod) = " + str(string3) 
           
        import cPickle
        runLocalTest = True
        if runLocalTest == True:
			server = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
			theYear = os.getenv('ALIGNWEBYEAR')
			detailedplots_path = server + "/WebPage/detailed_plots/" +str(theYear) + "/plots"+str(theYear)+".db"
			detailedplots = cPickle.load(open(detailedplots_path,'r'))
        else:
            theYear = os.getenv('ALIGNWEBYEAR')

        if (False):
            # this lists period and subperiod    
            self.tablerow="""
            <tr>
				<td><a href="http://atlas-runquery.cern.ch/query.py?q=find+run+%(nrun)i+/+show+all+/+nodef">%(nrun)i</a></td>
				<td><a href="http://atlas-runquery.cern.ch/query.py?q=find+run+period%(period)s+/+show+all+/+nodef">%(period)s</a><a href="http://atlas-runquery.cern.ch/query.py?q=find+run+period%(subperiod)s+/+show+all+/+nodef">%(subperiod)s</a></td><td> %(mydate)s %(mytime)s </td><td>%(myproject)s </td>
				<td> %(mystream)s  </td>
				"""
        else:
            # this lists only the subperiod
            self.tablerow="""
            <tr>
				<td><a href="http://atlas-runquery.cern.ch/query.py?q=find+run+%(nrun)i+/+show+all+/+nodef">%(nrun)i</a></td>
				<td> <a href="http://atlas-runquery.cern.ch/query.py?q=find+run+period%(subperiod)s+/+show+all+/+nodef">%(subperiod)s</a></td>
				<td> %(mydate)s %(mytime)s </td>
				<td>%(myproject)s </td>
				<td> %(mystream)s </td>
				"""

        if theConstantsFile == "No":
            self.tablerow += """
				<td><font color="red">%(constantsFile)s</td> """
        else:
            self.tablerow += """
				<td><a href="/webapp/Plotting?nruns=%(nrun)i&idtracks=0&minruns=0&maxruns=0&periods=&subperiods=&olddata=FALSE"> Draw constants</a> """
            if os.path.exists(str(server)+"/WebPage/alignlogfiles/2018/ONLINE/00"+str(int(string1))+"/alignlogfileIter0.txt") == True:
				self.tablerow += """| <a href="/webapp/alignlogfiles/2018/ONLINE/00%(nrun)i/alignlogfileIter0.txt"> View L11 </a> 
				"""
            else:
				self.tablerow += """| <a title="L11 not available"> View L11 </a> 
				"""
            self.tablerow += """| <a href="/webapp/PlotMonitoring?nruns=%s"> Monitoring  </a>  </td>""" %(str(int(string1)))	


        self.tablerow += """
				 <!-- <a href="/webapp/PlotMonitoring?nruns=%(nrun)i&plotsType=%(resplots)s"> Residuals </a> -->"""
        self.tablerow += """<!-- | <a href="/webapp/PlotMonitoring?nruns=%(nrun)i&plotsType=%(hitsplots)s"> Hits </a> -->"""
        self.tablerow += """<!-- | <a href="/webapp/PlotMonitoring?nruns=%(nrun)i&plotsType=%(hitmaps)s"> Hit Maps </a> -->"""
        self.tablerow += """<!-- | <a href="/webapp/PlotMonitoring?nruns=%(nrun)i&plotsType=%(iblres)s"> IBL Res. </a> -->"""
        self.tablerow += """<!-- | <a href="/webapp/PlotMonitoring?nruns=%(nrun)i&plotsType=%(resmaps)s"> Residual Maps </a> -->"""
        #self.tablerow += """<a href="/webapp/PlotMonitoring?nruns=%s"> Monitoring  </a> """ %(str(int(string1)))
        self.tablerow += """
				 """
        
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


    # =================================================================================
    #  Thetableend
    # =================================================================================
    def Thetableend(self):
        self.tableend="""
			</tbody>
        </table>
        <!-- <a class="btn btn-white btn-animated" href="../webapp/"> Show all </a> -->
       </div>  <!-- TheTable test pablo -->
        """
        return self.tableend

# =================================================================================
#  class Formulary
# =================================================================================
class Formulary:

    # =================================================================================
    #  __init__
    # =================================================================================
    def __init__(self):
        self.form = """ """
        
    # =================================================================================
    #  Theform
    # =================================================================================
    def Theform(self, database_files, theYear):
        print ' -*--> theYear',theYear
        # os.environ["ALIGNWEBYEAR"] = "%d" % theYear
        html_form = '''

        <div class="align_center">
        <h1 class="heading-primary">
        <span class="heading-primary-main"> <a href="../webapp/"> ID Alignment </a> </span>
        <span class="heading-primary-sub"> Inner Detector Alignment Monitoring Web Display</span>
        </h1>
        </div>

        <div class="align_right">
		<form>
			<select name="theYear" class="custom-select" style="width:208px; height:30px; border: none;" onchange='this.form.submit()'> '''
        html_form += '''
        <option selected disabled>Year</option>
        '''
        for filename in database_files:
			yearOption = filename.rstrip(".db")
			yearOption = yearOption.strip('server_runinfo')
			# print (yearOption)
			html_form += ''' 
				<option>%s</option> ''' %(str(yearOption))			
        html_form += '''
			</select>
		</form>
        </div>
		'''
        self.form = html_form
        return self.form
    
# =================================================================================
#  class FormularyPlot
# =================================================================================
class FormularyPlot:

    # =================================================================================
    #  QuickDisplay
    # =================================================================================
    def QuickDisplay(self):
        from searchpickle import LastRuns
        a = LastRuns(100)
        print " <base.QucikDisplay> a = lastRuns(100) = ",a
        minmaxruns = a.LastN()
        print " <base.QucikDisplay> minmaxruns = ",minmaxruns
        return minmaxruns 

    # =================================================================================
    #  Theform
    # =================================================================================
    def Theform(self):
        self.form = """ """
        return self.form 

# =================================================================================
#  class Error
# =================================================================================
class Error:
    
    # =================================================================================
    #  error1
    # =================================================================================
    def error1(self):
        error = """<h3>Oops!! There is an error (error1) </h3>
                <p>Remember, Run must be an integer</p>
                <p>Period must be a letter</p>
                <p>Events must be an integer</p>
                <p>ID Tracks must be an integer</p>"""
        return error

    # =================================================================================
    #  error2
    # =================================================================================
    def error2(self):
        error = """<h3>Oops!! There is an error (error2) Error code: 2 </h3>
                <p> Salva --> Remember, run, min. run and max. run must be an integer</p>
                <p>If you want a range of plots displayed, you have to put both, the min. run and the max. run</p>
                <p>If you want several periods/subperiods, you have to put the periods/subperiods separated by comma, without blanks</p>"""
        return error

    # =================================================================================
    #  error3
    # =================================================================================
    def error3(self):
        error = """<h3>Oops!! There is a VIE, very important error</h3>
                <p>Can not be found the environment file, please, send an email</p>"""
        return error

    # =================================================================================
    #  error4
    # =================================================================================
    def error4(self):
        error = """<h3>Oops!! There is an error (error4)</h3>
                <p>Remember, run, min. run and max. run must be an integer</p>
                <p>If you want a range of plots displayed, you have to put both, the min. run and the max. run</p>
                <p>If you want several periods/subperiods, you have to put the periods/subperiods separated by comma, without blanks</p>"""
        return error

    # =================================================================================
    #  error5
    # =================================================================================
    def error5(self):
        error = """<h3>Oops!! There is an error (error5)</h3>
                <p>Remember, run, min. run and max. run must be an integer</p>
                <p>If you want a range of plots displayed, you have to put both, the min. run and the max. run</p>
                <p>If you want several periods/subperiods, you have to put the periods/subperiods separated by comma, without blanks</p>"""
        return error

    # =================================================================================
    #  error6
    # =================================================================================
    def error6(self):
        error = """<h3>Oops!! There is an error (error6)</h3>
                <p>Remember, run, min. run and max. run must be an integer</p>
                <p>If you want a range of plots displayed, you have to put both, the min. run and the max. run</p>
                <p>If you want several periods/subperiods, you have to put the periods/subperiods separated by comma, without blanks</p>"""
        return error
