import os, commands, tarfile, time 
from InDetAlignmentWebMonitor.MsgHelper import msgServer
#from InDetAlignmentWebMonitor.ConfigServer import configServer

# =====================================================================
#  runInfo
# =====================================================================
class runInfo:           
	# We define a class with all the info. In the previous version this was done using dictionaries.	
	def __init__(self,debugLevel):
		self.msg = msgServer('runInfo', debugLevel)

		# A dictionary that saves the information of every run
		# every run creates a new entry in this dictionary. Global dic. 
		# Works like the runinfo={} of the previous program	
		self.DB = {}		

		# This dictionary contains the different lists which classify the runs
		# it is filled using the functions "append_to_list" and "append_to_dictionary"
		self.listOfRuns = {}

		self.constantsFileIter = {}
		self.monitingFileIter = {}
	
		# auxilar dictionary
		self.options_dict = {}

		# default values
		self.default_value = '?'
		self.numOfIters = 4
		self.default_options = [
			'project',
			'stream',
			'year',
			'period',
			'subperiod',
			'creationTime',
			'amiStatus',
			'totalEvents',
			'lastModified',
			'nFiles',
			'totalSize',
			'processing',
			'L11Results',
			'L16Results',
			'DBsubmission',
			'DBtimestamp',
			'runRecordDate',
			'analysisfile',
			'bshandshake',
			'bshsauthor',
			'thisdbrecordtimestamp',
			'constantsFile',
			'constantsFileIter0',
			'constantsFileIter2',
			'monitoringFileIter0',
			'monitoringFileIter1',
			'monitoringFileIter2',
			'monitoringFileIter3'
			]
		for i in range(0, self.numOfIters): self.default_options += [ 'monitoringFileIter%d' % i ]
		
	# =====================================================================
	#  initialize
	# =====================================================================
	def initialize(self,runnumber):
		self.set_default_options()
		self.DB[runnumber] = { self.default_options[0] : self.options_dict[self.default_options[0]] } # creates first entry for runnumber
		for option in self.default_options: self.DB[runnumber][option] = self.options_dict[option] # fill DB[runnumber]
		# self.msg.printDebug("Default value set: " + str(self.DB[runnumber]))
		# self.print_DB_values(runnumber)


	# =====================================================================
	#  set_default_options
	# =====================================================================
	def set_default_options(self):
		for opt in self.default_options: self.options_dict[opt] = self.default_value


	# =====================================================================
	#  add_element
	# =====================================================================
	def add_element(self, runnumber, ParameterName, ParameterValue):
		if (not runnumber in self.DB.keys()):self.initialize(runnumber)

		if not ParameterName in self.default_options: #Protection
			self.msg.printFatal("ParameterName not recognized: " + str(ParameterName))
			exit()
	
		self.DB[runnumber][ParameterName] = ParameterValue
		self.msg.printDebug(" + For run " + str(runnumber) + " adding, '" + ParameterName + "': " + str( self.DB[runnumber][ParameterName]))


	# =====================================================================
	#  append_to_list
	# =====================================================================
	def append_to_list(self,NameOfList, WhatGoesIn): 
		# The entries in lists and dictionaries are not only the runnbers. They include more information
		if not NameOfList in self.listOfRuns.keys(): # Creating the list if it does not exist yet
			self.listOfRuns[NameOfList] = []
			self.msg.printInfo("New list created: " + str(NameOfList))
		if not WhatGoesIn in self.listOfRuns[NameOfList]:
			self.listOfRuns[NameOfList].append(WhatGoesIn)
			self.msg.printInfo("The information -> " + str(WhatGoesIn) + " <- has been added to the list " + str(NameOfList))
		else:
			self.msg.printInfo("The information -> " + str(WhatGoesIn) + " <- was already in list " + str(NameOfList))


	# =====================================================================
	#  append_to_dictionary
	# =====================================================================
	def append_to_dictionary(self, NameOfDictionary, runnumber, WhatGoesIn):
		if not NameOfDictionary in self.listOfRuns.keys(): # Creating the dictionary if it does not exist yet
			self.listOfRuns[NameOfDictionary] = {} #It is a dictionary
			self.msg.printInfo("New dictionary created: " + NameOfDictionary)
		if type(WhatGoesIn)== list or (not WhatGoesIn in self.listOfRuns[NameOfDictionary]):
			self.msg.printInfo(" The information:  " + str(WhatGoesIn) + " has been added to the dictionary: " + str(NameOfDictionary))
			self.listOfRuns[NameOfDictionary].update({runnumber : WhatGoesIn}) 
		else:
			self.msg.printInfo(" The run " + str(WhatGoesIn) + " was already in dictionary " + str(NameOfDictionary))
		

	# =====================================================================
	#  add_ConstantsFileIteration
	# =====================================================================
	def add_ConstantsFileIteration(self,iteration):         # Not done                                     
		 self.constantsFileIter.update({'iteration':"?"})                                              

	
	# =====================================================================
	#  add_MonitoringFileIteration
	# =====================================================================
	def add_MonitoringFileIteration(self,iteration):                                     
		 self.monitingFileIter.update({'iteration':"?"})                                        
		 # Not done  	
		

	# =================================================================================
	#  func_idalignmerge
	# =================================================================================
	def func_idalignmerge(self,ThingPath,Cardinal, runnumber, MonItMiss,MonItFiles):
		# ThingPag = things
		# Cardinal = 0,1,2 or 3 <- For the Iter
		# runnumber = run
		# MonItMiss = runsWithMonitoringIterXmissing (where X can be 0,1,2, or 3)
		# MonItFiles = monitoringFilesIterX
		# ClassObject = Dope

		if not MonItFiles in self.listOfRuns.keys(): self.listOfRuns[MonItFiles]={} #initialize
		if not MonItMiss in self.listOfRuns.keys(): self.listOfRuns[MonItMiss]=[]
		path = "%s/" % (ThingPath.rstrip())
		content = os.listdir(path) #Return a list containing the names of the entries in the directory given by path
		
		self.msg.printInfo("Run " + str(runnumber) + " Iter" + str(Cardinal)  + " --> number of monitoring files: " + str(len(content)))
		index=0; # starting at index 0 --> fisrt LB group
		TheListOfWhatGoesIn = []
		for file in content: #runs over the files in path
			if "idalignmerge" in file:
				TheListOfWhatGoesIn.append(path+file)
				#self.append_to_dictionary(MonItFiles,runnumber,path+file)
				if (runnumber not in self.listOfRuns[MonItMiss]):self.append_to_list(str(MonItMiss), runnumber)
				if ('RunsWithNewData' not in self.listOfRuns or runnumber not in self.listOfRuns['RunsWithNewData']): self.append_to_list('RunsWithNewData',runnumber)
			
				self.msg.printInfo( "   -- RUN " + runnumber + " Iter"  + str(Cardinal)  + " monitoring file for LBgroup "+ str(index) + "  --> LOADED in monitoringFilesIter" + str(Cardinal)  + runnumber)
				index +=1
		
		self.append_to_dictionary(MonItFiles,runnumber,TheListOfWhatGoesIn)

	# =====================================================================
	#  func_UpdateIterA
	# =====================================================================
	def func_UpdateIterA(self,runnumber, Cardinal,runsWithMonitoringIterXmissing,monitoringFileIterX, ExtractLBGroupFilesOput):
		self.msg.printDebug("Number of runs with monitoring file Iter"+str(Cardinal)+" missing: " + str(len(self.listOfRuns[runsWithMonitoringIterXmissing])))
		if (len(self.listOfRuns[runsWithMonitoringIterXmissing]) >0 ): self.msg.printDebug( "           is run %s in list? %s" %(runnumber, runnumber in self.listOfRuns[runsWithMonitoringIterXmissing]))
		if runnumber in self.listOfRuns[runsWithMonitoringIterXmissing] :
			self.add_element(runnumber, monitoringFileIterX,ExtractLBGroupFilesOput)
			self.msg.printDebug("    --- UPDATE --- Iter"+str(Cardinal)+" monitoring -- run["+runnumber+"]['monitoringFileIter"+ str(Cardinal) +"']= "+str(self.DB[runnumber][monitoringFileIterX]))
			return True
		else:
			return False


	# =====================================================================
	#  func_UpdateIterB
	# =====================================================================
	def func_UpdateIterB(self,runnumber, Cardinal,runsWithMonitoringIterXmissing,monitoringFileIterX, monitoringFilesIterX):
		self.msg.printDebug("Number of runs with monitoring file Iter"+str(Cardinal)+" missing:" + str(len(self.listOfRuns[runsWithMonitoringIterXmissing])))
		if (len(self.listOfRuns[runsWithMonitoringIterXmissing]) >0 ): self.msg.printDebug( "           is run %s in list? %s" %(runnumber, runnumber in self.listOfRuns[runsWithMonitoringIterXmissing]))
		if runnumber in self.listOfRuns[runsWithMonitoringIterXmissing] :
			#self.msg.printGreen("Test: Here the monitoringFileIter"+str(Cardinal)+" information for the run " +str(runnumber)+ " is gonna be updated with  self.listOfRuns[monitoringFilesIter"+str(Cardinal)+"]["+str(runnumber)+"] =" + str( self.listOfRuns[monitoringFilesIterX][runnumber]))
			self.add_element(runnumber, monitoringFileIterX, self.listOfRuns[monitoringFilesIterX][runnumber])
			self.msg.printDebug("    --- UPDATE --- Iter"+str(Cardinal)+" monitoring -- run["+runnumber+"]['monitoringFileIter"+ str(Cardinal) +"']= "+str(self.DB[runnumber][monitoringFileIterX]))
			# self.msg.printDebug("\n")
			return True
		else:
			return False


	# =====================================================================
	#  ExtractAlignLogFiles_A
	# =====================================================================
	def ExtractAlignLogFiles_A(self, runnumber,cardinal, CalibLoopDirectory, alignfiles,logicName,runsWithConstantsIterXmissing):
		runcontent2 = os.listdir(CalibLoopDirectory.rstrip())
		self.msg.printDebug("-new- PROCESSING  Iter"+str(cardinal)+" TAR_ALIGNFILES --> There is "+str(len(runcontent2))+" files --> runcontent2 = "+str(runcontent2))
		lbGroupIndex=-1; # starting at index 0 --> fisrt LB group
		for things2 in runcontent2:
			if ("idalignsolve.TAR_ALIGNFILES.Iter"+str(cardinal)) in things2 :
				path = "%s/%s" % (CalibLoopDirectory.rstrip(),things2.rstrip())
				alignfile_path = alignfiles + "%s/%s/" %(logicName,runnumber)
				# check if the folder to store the alignlogfiles already exists
				if (lbGroupIndex == 0): 
                                        try:
						os.mkdir(alignfile_path)
						self.msg.printDebug("Create a folder to store the alignlogfiles: %s" %(alignfile_path))
                                        except:
						self.msg.printDebug("Storing aliglogfiles in already existing folder: %s " %(alignfile_path))
                                        
				try: 
                                        self.msg.printInfo("Going to tar=tarfile.open(%s)" %(path))
					tar = tarfile.open(path)
                                        tar.extract("alignlogfile.txt",alignfile_path)
				except: 
                                        self.msg.printWarning("tarfile.open(%s) FAILED " %(path))
                                          
				lbGroupIndex +=1
				newfilename = "alignlogfileIter"+str(cardinal)+"_LBGroup%02d.txt" %(lbGroupIndex)
				string1 = "mv %salignlogfile.txt  %s%s" %(alignfile_path,alignfile_path,newfilename)
				cmd1 = string1
				(status1, output1) = commands.getstatusoutput(cmd1)
				tar.close()
				filetostore =  alignfile_path + newfilename
				self.append_to_list(('constantsFilesIter'+str(cardinal)),(runnumber, filetostore))
				if (runsWithConstantsIterXmissing not in self.listOfRuns or runnumber not in self.listOfRuns[runsWithConstantsIterXmissing]): self.append_to_list(runsWithConstantsIterXmissing, runnumber)
				self.msg.printInfo("   -new- -- RUN "+ str(runnumber) +" alignlogfileIter"+str(cardinal)+" LBGroup %s file was FOUND. Stored as: %s" %(lbGroupIndex, newfilename))
                                    

	# =====================================================================
	#  ExtractAlignLogFiles_B
	# =====================================================================
	def ExtractAlignLogFiles_B(self, runnumber, cardinal, CalibLoopDirectory, alignfiles, logicName, runsWithConstantsIterXmissing):

		#print runnumber
		#print cardinal
		#print CalibLoopDirectory
		#print alignfiles
		#print logicName
		#print runsWithConstantsIterXmissing

		# alignfinles= config.server_alignfiles
		# logicName = logicName[i]
		runcontent2 = os.listdir(CalibLoopDirectory.rstrip())

		# print runcontent2

		self.msg.printDebug(" Iter"+str(cardinal)+" TAR_ALIGNFILES found --> it has "+str(len(runcontent2))+" files --> runcontent2 = "+str(runcontent2) )
		for things2 in runcontent2:
			if ("idalignsolve.TAR_ALIGNFILES.Iter"+str(cardinal)) in things2 :
				path = "%s/%s" % (CalibLoopDirectory.rstrip(),things2.rstrip())
				alignfile_path = alignfiles + "%s/" %(logicName)  # add logic name to the store folder path, then check
				# check if the folder to store the alignlogfiles already exists
				try:
					os.mkdir(alignfile_path)
					self.msg.printDebug(" create a folder to store the alignlogfiles: %s" %(alignfile_path))
				except:
                                        self.msg.printDebug(" storing aliglogfiles in already existing folder: %s " %(alignfile_path))

				# add run number to the store folder path, then check
				alignfile_path = alignfile_path + "%s/" %(runnumber) 
				
				tar = tarfile.open(path)
				try: 
                                        tar.extract("alignlogfile.txt",alignfile_path)
				except: 
                                        self.msg.printFatal("Tarfile.open("+ str(path) +") FAILED ")

				string = "mv "+str(alignfile_path)+"alignlogfile.txt  "+alignfile_path+"alignlogfileIter"+str(cardinal)+".txt"
				cmd = string
				(status, output) = commands.getstatusoutput(cmd)
				tar.close()
				if (runnumber not in self.listOfRuns['RunsWithNewData']): self.append_to_list('RunsWithNewData',runnumber)
				self.append_to_dictionary('constantsFile',runnumber, alignfile_path+'alignlogfileIter'+str(cardinal)+'.txt') # this is to store Iter0 alignment constant
				self.msg.printInfo( "   -- RUN "+ str(runnumber) +" --> REGISTERED in the list of runs with new data (RunsWithNewData)")
				self.msg.printInfo("   -- RUN "+ str(runnumber) +" Iter"+ str(cardinal) +" alignlogfile --> LOADED in constantsFile["+ str(runnumber) +"]")
				if (runsWithConstantsIterXmissing not in self.listOfRuns or runnumber not in self.listOfRuns[runsWithConstantsIterXmissing]): self.append_to_list(runsWithConstantsIterXmissing, runnumber)
                                    
				# - let's extract the date of Iter0 
				self.append_to_list('runsWithDateMissing',runnumber)
				self.append_to_list('runDate',(runnumber, (time.strftime("%d/%b/%Y",time.localtime(os.stat(path)[8])))))
				self.msg.printInfo("   -- RUN "+ str(runnumber) +" Iter"+ str(cardinal) +" alignlogfile --> DATE: "+ str(time.strftime("%d/%b/%Y",time.localtime(os.stat(path)[8]))))
		return


	# =====================================================================
	#  print_DB_values
	# =====================================================================
	def print_DB_values(self, runnumber, color=''):
		if color == "red":
			self.msg.printRed("Information stored in the database about the run " + str(runnumber) + ':')
			for key, value in self.DB[runnumber].iteritems():
				self.msg.printRed(" + DB." + key + ": " + str(value))	    		
		else:
			self.msg.printBold("Information stored in the database about the run " + str(runnumber) + ':')
			# self.msg.printDebug("DB value set: " + str(self.DB[runnumber]))
			for key, value in self.DB[runnumber].iteritems():
				self.msg.printInfo(" + DB." + key + ": " + str(value))

	# =====================================================================
	#  print_ListOfRuns
	# =====================================================================
	def print_ListOfRuns(self):
		import json
		self.msg.printDebug("The lists are: ")
		print(json.dumps(self.listOfRuns.keys(), indent = 2))
		self.msg.printDebug("Shown recursively: ")
		print(json.dumps(self.listOfRuns, indent = 4))

	# =====================================================================
	#  print_a_List
	# =====================================================================
	def print_a_List(self,ListName):
		import json
		print(json.dumps(self.listOfRuns[ListName], indent = 2))
