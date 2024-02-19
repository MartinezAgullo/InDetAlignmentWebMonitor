import commands,collections
import pyAMI.client, pyAMI.atlas.api, pyAMI.atlas.utils
#import pyAMI.query

from InDetAlignmentWebMonitor.MsgHelper import msgServer

# =====================================================================
#  amiServer
# =====================================================================
class amiServer:
    def __init__(self, year, debugLevel):
        
        self.msg = msgServer('amiServer', debugLevel)
        self.year = int(year)

        # pyAMI client (https://ami.in2p3.fr/pyAMI/pyAMI5_atlas_api.html)
        self.client = pyAMI.client.Client('atlas')
        pyAMI.atlas.api.init()
        self.msg.printInfo("pyAMI client loaded successfully!")

        if debugLevel == 0: self.getUserInfo()

        # print list of commands
        # print pyAMI.atlas.api.list_commands(self.client)

        self.DB = {}

        # initialize levelDB()
        self.levelDB = {}
        self.initialize_levelDB()

    # =====================================================================
    # getUserInfo
    # =====================================================================
    def getUserInfo(self):
        try:
            username = commands.getoutput("whoami")
            command = ['GetUserInfo', '-amiLogin=%s' % username ]
            for i in self.client.execute(command, format = 'dict_object').get_rows():
                if 'projectName' in str(i) or 'bookmark' in str(i): continue
                for key, value in i.items(): self.msg.printInfo("UserInfo from AMI :: %s = %s" % (key, value))
        except pyAMI.exception.Error:
            self.msg.printWarning("No user information is found for %s" % username)
            exit()

    # =====================================================================
    # getListOfDataPeriods
    # =====================================================================
    def getListOfDataPeriods(self, level):
        try: return pyAMI.atlas.api.list_dataperiods(self.client, level, self.year)
        except pyAMI.exception.Error:
            self.msg.printWarning("No information about periods can be retrieved from AMI for %s" % self.year)

    # =====================================================================
    # getListOfDataRuns
    # =====================================================================
    def getListOfDataRuns(self):
        try: return pyAMI.atlas.api.list_runs(self.client, self.year, data_periods="A")
        except pyAMI.exception.Error:
            self.msg.printWarning("No information from any run can be retrieved from AMI for %s" % self.year)

    # =====================================================================
    # getDatasetInfo
    # =====================================================================
    def getDatasetInfo(self, runnumber, dataProjectName, dataStreamName):
        if '_backup' in runnumber:
            runnumber = runnumber.rstrip('_backup')
        runnumber = int(runnumber)
        datasetName = '%s.%08d.%s.merge.RAW' % (dataProjectName, runnumber, dataStreamName)
        self.msg.printDebug("Looking for information about %s in AMI..." % datasetName)

        # command = ['GetDatasetInfo', '-logicalDatasetName=%s' % 'data18_13TeV.00362297.calibration_IDTracks.merge.RAW' ]
        # print self.client.execute(command, format = 'dict_object')
        try: dsInfo = pyAMI.atlas.api.get_dataset_info(self.client, datasetName)[0]
        except pyAMI.exception.Error:
            self.msg.printWarning("No information about dataset %s" % datasetName)
            return

        # print dsInfo
        # for key, value in dsInfo.items(): print key, value


        self.DB[runnumber].update({'amiStatus' : dsInfo['amiStatus']})
        self.DB[runnumber].update({'nFiles' : dsInfo['nFiles']})
        self.DB[runnumber].update({'totalEvents' : dsInfo['totalEvents']})
        self.DB[runnumber].update({'totalSize' : dsInfo['totalSize']}) # in GB
        self.DB[runnumber].update({'streamName' : dsInfo['streamName']})
        self.DB[runnumber].update({'created' : dsInfo['created']})
        self.DB[runnumber].update({'lastModified' : dsInfo['lastModified']})

        for key, value in self.DB[runnumber].items():
            if key == 'totalSize': self.msg.printInfo(str(key) + ' = ' + str(value) + " B")
            else: self.msg.printInfo(str(key) + ' = ' + str(value))

    # =====================================================================
    # getDataPeriodsForRunFromAMI                        
    # =====================================================================
    def getDataPeriodsForRunFromAMI(self, runnumber):
        # self.msg.printDebug("In getDataPeriodsForRunFromAMI()")
        command = ['AMIGetDataPeriodsForRun -runNumber=%d' % runnumber]
        try: return self.client.execute(command, format = 'dict_object').get_rows()        
        except (pyAMI.exception.Error, KeyError):
            self.msg.printWarning("No information from run number %d can be retrieved from AMI for %s" % (runnumber, self.year))
            return []
        
    # =====================================================================
    #  initialize_levelDB
    # =====================================================================
    def initialize_levelDB(self):
        self.msg.printDebug("Initializing levelDB dictionary...")
        for i in [1,2,3]: self.initialize_level_in_levelDB(i)

    # =====================================================================
    #  initialize
    # =====================================================================
    def initialize_level_in_levelDB(self, level):
        default_value = '?'
        default_options = [ 'period', 'project', 'description', 'periodLevel', 'status' ]
        options_dict = {}
        for opt in default_options: options_dict[opt] = default_value
        self.levelDB[level] = { default_options[0] : options_dict[default_options[0]] } # creates first entry for level
        for option in default_options: self.levelDB[level][option] = options_dict[option] # fill self.levelDB[level]
        self.msg.printDebug("levelDB[" + str(level) + "] -> default value set: " + str(self.levelDB[level]))

    # =====================================================================
    #  add_element
    # =====================================================================
    def add_element(self, DB, key, parameterName, parameterValue):
        parameterValue = parameterValue.replace('\n', '')
        if parameterName != 'runNumber':
            # self.msg.printDebug("TEST.     ParameterValue = %s.   ParamenterName = %s" %(parameterName,parameterValue))
            DB[key][parameterName] = parameterValue
            #self.msg.printDebug('   * ' + parameterName + ': ' + str(DB[key][parameterName]))
    
    # =====================================================================
    #  getDataPeriodsForRun
    # =====================================================================
    def getDataPeriodsForRun(self, runnumber):
        runnumber = int(runnumber)
        level = 3
        self.msg.printDebug("Retrieving information in AMI for run number %d..." % runnumber)
        #self.msg.printDebug("getDataPeriodsForRunFromAMI: "+ str(self.getDataPeriodsForRunFromAMI(runnumber)))
        for i in self.getDataPeriodsForRunFromAMI(runnumber):# getDataPeriodsForRunFromAMI returns a list
            #self.msg.printDebug("* level : %d" % level)
            if level == 0:
                self.msg.printDebug("If level == 0 we skip the loop")
                continue
            for key, value in i.items():
                # print level, " :: ", key, "=", value
                self.add_element(self.levelDB, level, key, value)
            level -= 1
        self.DB[runnumber] = { 'level1' : self.levelDB[1], 'level2' : self.levelDB[2], 'level3' : self.levelDB[3] }


    # =====================================================================
    #  printAmiDB
    # =====================================================================
    def printAmiDB(self, runnumber):
        self.msg.printDebug( " - Information of ami.DB["+str(int(runnumber))+"] - ")
        for element in self.DB[int(runnumber)].keys():
            if type(self.DB[int(runnumber)][element])== dict:
                self.msg.printDebug( " "+str(element))
                for level in self.DB[int(runnumber)][element].keys():
                    self.msg.printDebug( "   " + str(element) + "[" + str(level) + "] : " + str(self.DB[int(runnumber)][element][level]))
            else:
                if element == 'totalSize' : self.msg.printDebug( " "+str(element) + " : " + str(self.DB[int(runnumber)][element]) + " B")
                else:                self.msg.printDebug( " "+str(element) + " : " + str(self.DB[int(runnumber)][element]))
        self.msg.printDebug( " - ---------  - ")
