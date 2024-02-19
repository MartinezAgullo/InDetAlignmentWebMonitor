#
DoFStrings = ['Tx','Ty','Tz','Rx','Ry','Rz','Bx']
OutputLevel = 1

doDebug = True 
runWebMonitor = True
runLocalTest = True
    
def openFile(file):
    try:
        file = open(file)               # open file
    except:
        print "The file ", file, "doesn't exist"
    else:
        return file.read()
    
def writeCorr(outputfile, detector):
    alignOutput = open(outputfile,'w')
    text = "%6s %6s %6s %6s %6s %6s %6s %12s %12s %12s %12s %12s %12s %12s\n" % ("module",
    "Level","Det","Bec","Lay","Phi","Eta","Tx","Ty","Tz","Rx","Ry","Rz","Hits")
    alignOutput.write(text)
    alignOutput.write(detector.PrintValues())
    alignOutput.close()
    
def readConstants(file, useBarrels=True,  useEndCaps=True):
    import imp
    import os, commands

    doDebug = False
    #check with environment variable if server runs as local test 
    runLocalTest = False
    try:
        stringRunLocalTest = os.getenv('RUNLOCALTEST', False)
        if ("True" in stringRunLocalTest): #interpret the string returned by getenv into a boolean
            runLocalTest = True
    except:
        runLocalTest = False

    # pointer to the folder when the server resides   
    alignWebRoot = ""
    try:
        alignWebRoot = os.getenv('ALIGNWEBROOT',"")
    except:
        alignWebRoot = ""    

    # definition of folders and basic files
    webFolderName = "WebPage/"
    runLocalTest = True
    if runLocalTest == True:
        if (len(alignWebRoot)==0):
            #alignWebRoot = "/Users/martis/projectes/atlas/alineament/webmonitoringtest/InDetAlignmentWebMonitor/trunk/"
            #alignWebRoot = "/afs/cern.ch/user/m/martis/mywork/JPsi_20.7.3.8/InnerDetector/InDetMonitoring/InDetAlignmentWebMonitor/"
            alignWebRoot = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        else:
            if (doDebug): print " -fileutils- user defined ALIGNWEBROOT: ",alignWebRoot
    else:
        if (len(alignWebRoot)==0):
            alignWebRoot = "/var/vhost/atlas-alignment/"
            webFolderName = "secure/"

    # make sure that the last character of alignWebRoot is a slash
    if (alignWebRoot[-1] is not "/"):
        alignWebRoot += "/"
        if (doDebug): print " -fileutils- ALIGNWEBROOT needs a '/' --> ", alignWebRoot

    doDebug = True
    if doDebug == True:
        print " ======================================================= "
        print " == fileutils.readConstants == fileutils !!!!         == "
        print " == runLocalTest :", runLocalTest
        print " == alignWebroot :" +str( alignWebRoot) 
        # print " == alignWebYear :", alignWebYear
        print " ======================================================== "
        print " == webFolderName:", webFolderName
        #print " == server :", server
        print " == runWebMonitor:",runWebMonitor
        print " ======================================================== "


            
    #from module import Module
    #from module import Detector
    if (runWebMonitor):
        m_utils = imp.load_source('Module', alignWebRoot + webFolderName +'plot/module.py')
        m_utils = imp.load_source('Detector', alignWebRoot + webFolderName +'plot/module.py')

        if (doDebug): print " - fileutils - m_utils loaded :)" 
    else:
        m_utils = imp.load_source('Module', 'include/moduleutils.py')
        m_utils = imp.load_source('Detector', 'include/moduleutils.py')   

    if (doDebug): print  " = fileutils.readconstants = opening file:", file
    
    if runLocalTest == True:	
		
		if 'lxplus' not in commands.getoutput('hostname'):
			aux = str(file).split('WebPage')[-1]
			#aux = aux.rstrip('/afs/cern.ch/user/m/martinpa/work/alignment/webMonitoring/run')
			file_directory = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
			file = file_directory + '/WebPage' + str(aux)
			print "Vew file >>>>>>" + str(file)
			print "<<<<<<<"
			#file = file_directory + "/WebPage/alignlogfiles/2018/ONLINE/00364485/alignlogfileIter0.txt" #
			#print file

		
    if (os.path.isfile(file)):
        alignText = openFile(file).splitlines()
    else:
        if (doDebug or True): print " -fileutils.readconstants - == ERROR == file %s does not exist -- " %file
        exit()
        
    # initialize variables
    level, det, bec, layer, phi, eta = -999,-999,-999,-999,-999,-999
    Tx, Ty, Tz, Rx, Ry, Rz = 0,0,0,0,0,0
    counter = -1
    detector = m_utils.Detector()
    takeThisModule = True

    # print " useBarrels= ", not useBarrels
    
    for line in alignText:
        if "Alignment parameters for module" in line:
            line = line[33:]
            takeThisModule = True
            # reinitialize variables for each module
            Tx, Ty, Tz, Rx, Ry, Rz = 0,0,0,0,0,0
            ETx, ETy, ETz, ERx, ERy, ERz = 0,0,0,0,0,0
            Bx = 0 # IBL bowX degree of freedom
            EBx = 0 # its error/uncertainty
            
            if ("EndCap" in line and not useEndCaps):
                takeThisModule = False
                print " ** readConstants ** ** WARNING ** ** EndCap found ** ==> ", line 

            if ((not ("EndCap" in line) and (not useBarrels)) ):
                takeThisModule = False
                print " ** readConstants ** ** WARNING ** ** Barrel part found ** ==> ", line 

            if takeThisModule:
                counter = counter +1
                detector.addModule(m_utils.Module(counter,line))
                    
        elif "Number of hits seen" in line:
            if (counter >= 0):
                line = line[25:]
                detector.GetModule(counter).setHits(int(line))
        elif "Number of tracks passing" in line:
            if (counter >= 0):
                line = line[25:]
                if (doDebug and OutputLevel > 1): print " In Ntracks --> counter:", counter, "  Ntracks: ",line 
                detector.GetModule(counter).setTracks(int(line))
        elif "total time spent in solve" in line:
            if (doDebug): print " ** readConstants ** ** WARNING ** ** DISCARDING REST OF THE FILE ** after counter ", counter 
            break
        else:
            if "Number of hits too small" in line:
                detector.GetModule(counter).setHits(0)
            if (takeThisModule):
                if "Trans" in line or "Rot" in line or "Bow" in line:
                    if "TransX" in line:
                        Tx = float(line[10:23])
                        detector.GetModule(counter).setTx(Tx)
                        ETx = float(line[27:])
                        detector.GetModule(counter).setETx(ETx)
                        # if (counter < 10): print " Tx: ", Tx,"  ETx: ", ETx
                    elif "TransY" in line:
                        Ty = float(line[10:23])
                        detector.GetModule(counter).setTy(Ty)
                        ETy = float(line[27:])
                        detector.GetModule(counter).setETy(ETy)
                    elif "TransZ" in line:
                        Tz = float(line[10:23])
                        detector.GetModule(counter).setTz(Tz)
                        ETz = float(line[27:])
                        detector.GetModule(counter).setETz(ETz)
                    elif "RotX" in line:
                        Rx = float(line[10:23])
                        detector.GetModule(counter).setRx(1000*Rx)
                        ERx = float(line[27:])
                        detector.GetModule(counter).setERx(1000*ERx)
                    elif "RotY" in line:
                        Ry = float(line[10:23])
                        detector.GetModule(counter).setRy(1000*Ry)
                        ERy = float(line[27:])
                        detector.GetModule(counter).setERy(1000*ERy)
                    elif "RotZ" in line:
                        Rz = float(line[10:23])
                        detector.GetModule(counter).setRz(1000*Rz)
                        ERz = float(line[27:])
                        detector.GetModule(counter).setERz(1000*ERz)
                    elif "BowX" in line:
                        Bx = float(line[10:23])
                        detector.GetModule(counter).setBx(Bx)
                        EBx = float(line[27:])
                        detector.GetModule(counter).setEBx(EBx)

    if (doDebug): print " == fileutils.readconstants ==  reading input file. final Counter value = ", counter, "  (OutputLevel=",OutputLevel,")"
    if (doDebug and OutputLevel > 0):
        print detector.PrintValues()
    return detector

def saveConstants(detector,file):
    from ROOT import TFile
    from ROOT import TTree
    from ROOT import gROOT
    from ROOT import AddressOf
    f = TFile(file,'RECREATE')
    t = TTree('Corrections','Corrections')
    
    gROOT.ProcessLine(\
        "struct MyStruct{\
            Int_t index;\
            Int_t type;\
            Int_t bec;\
            Int_t layer;\
            Int_t sector;\
            Int_t ring;\
            Int_t hits;\
            Double_t tx;\
            Double_t ty;\
            Double_t tz;\
            Double_t rx;\
            Double_t ry;\
            Double_t rz;\
            Double_t etx;\
            Double_t ety;\
            Double_t etz;\
            Double_t erx;\
            Double_t ery;\
            Double_t erz;\
        };")
    from ROOT import MyStruct
    # Create branches in the tree
    s = MyStruct()
    t.Branch('index',AddressOf(s,'index'),'index/I')
    t.Branch('type',AddressOf(s,'type'),'type/I')
    t.Branch('bec',AddressOf(s,'bec'),'bec/I')
    t.Branch('layer',AddressOf(s,'layer'),'layer/I')
    t.Branch('sector',AddressOf(s,'sector'),'sector/I')
    t.Branch('ring',AddressOf(s,'ring'),'ring/I')
    t.Branch('hits',AddressOf(s,'hits'),'hits/I')
    t.Branch('tx',AddressOf(s,'tx'),'tx/D')
    t.Branch('ty',AddressOf(s,'ty'),'ty/D')
    t.Branch('tz',AddressOf(s,'tz'),'tz/D')
    t.Branch('rx',AddressOf(s,'rx'),'rx/D')
    t.Branch('ry',AddressOf(s,'ry'),'ry/D')
    t.Branch('rz',AddressOf(s,'rz'),'rz/D')
    t.Branch('etx',AddressOf(s,'etx'),'etx/D')
    t.Branch('ety',AddressOf(s,'ety'),'ety/D')
    t.Branch('etz',AddressOf(s,'etz'),'etz/D')
    t.Branch('erx',AddressOf(s,'erx'),'erx/D')
    t.Branch('ery',AddressOf(s,'ery'),'ery/D')
    t.Branch('erz',AddressOf(s,'erz'),'erz/D')
    t.SetMarkerStyle(20)
    #print detector
    for i in range(detector.nModules()):
        detector.GetModule(i)
        s.index = i
        if "Pixel" in detector.GetModule(i).Det:
            det = 1
        elif "SCT" in detector.GetModule(i).Det:
            det = 2
        elif "TRT" in detector.GetModule(i).Det:
            det = 3
        else:
            det = 0
        s.type = det
        
        if "Barrel" in detector.GetModule(i).BarrelEC:
            bec = 0
        elif "EndCapA" in detector.GetModule(i).BarrelEC or "EndcapA" in detector.GetModule(i).BarrelEC:
            bec = -1
        elif "EndCapC" in detector.GetModule(i).BarrelEC or "EndcapC" in detector.GetModule(i).BarrelEC:
            bec = 1
        else:
            bec = 999
        s.bec = bec 
        s.layer = int(detector.GetModule(i).Layer)
        s.sector = int(detector.GetModule(i).PhiModule)
        s.ring = int(detector.GetModule(i).EtaModule)
        s.hits = int(detector.GetModule(i).Hits)
        s.tx = detector.GetModule(i).Tx
        s.ty = detector.GetModule(i).Ty
        s.tz = detector.GetModule(i).Tz
        s.rx = detector.GetModule(i).Rx
        s.ry = detector.GetModule(i).Ry
        s.rz = detector.GetModule(i).Rz
        s.bx = detector.GetModule(i).Bx
        s.etx = detector.GetModule(i).ETx
        s.ety = detector.GetModule(i).ETy
        s.etz = detector.GetModule(i).ETz
        s.erx = detector.GetModule(i).ERx
        s.ery = detector.GetModule(i).ERy
        s.erz = detector.GetModule(i).ERz
        s.ebx = detector.GetModule(i).EBx
        t.Fill()
    f.Write()
    f.Close()
