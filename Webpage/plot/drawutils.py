def rootSetup():
    from ROOT import gStyle
    gStyle.SetStatColor(0)
    gStyle.SetFillColor(38)
    gStyle.SetCanvasColor(0)
    gStyle.SetPadColor(0)
    gStyle.SetPadBorderMode(0)
    gStyle.SetCanvasBorderMode(0)
    gStyle.SetFrameBorderMode(0)
    gStyle.SetOptStat(1110)
    gStyle.SetStatH(0.3)
    gStyle.SetStatW(0.3)
    
    gStyle.SetTitleFillColor(0)
    #gStyle.SetTitleY(1.)
    #gStyle.SetTitleX(.1)
    gStyle.SetTitleBorderSize(0)
    gStyle.SetHistLineWidth(2)
    gStyle.SetFrameFillColor(0)
    #gStyle.SetLineWidth(2)
    #gStyle.SetTitleColor(0)
    #gStyle.SetTitleColor(1)
    gStyle.SetLabelSize(0.04,"x")
    gStyle.SetLabelSize(0.04,"y")
    gStyle.SetLabelOffset(0.01,"y")
    gStyle.SetTitleOffset(1.3,"y")
    gStyle.SetTitleSize(0.04,"y")
    gStyle.SetPadRightMargin(0.09)
    gStyle.SetPadLeftMargin(0.10)


def  AutoColors(NFiles):
    Colors = {}
    doDebug = False

    #import settings.py
    #import imp
    #s_utils = imp.load_source('init', 'include/settings.py')
    #print " xxxyyyzzz ", s_utils.TestUseBarrel
    
    if NFiles > 2:
        ColorStep = 50./(NFiles-1)
    Color_i = 0;
    
    if NFiles is 1:
        Colors[0] = 920+3 #kGray
    
    elif NFiles is 2:
        Colors[0] = 632+1 #kRed+1
        Colors[1] = 920+3 #kGray+3

    elif NFiles is 3:
        Colors[0] = 632+1 #kRed+1
        Colors[1] = 920+2 #kGray+2
        Colors[2] = 860+1 #kAzure+1

    elif NFiles is 4:
        if (True):
            Colors[0] = 616 # IBL
            Colors[1] = 1   # Pixel 
            Colors[2] = 632 # SCT
            Colors[3] = 416 # TRT
        else:
            Colors[0] = 629 # SCT
            Colors[1] = 801   
            Colors[2] = 398 # TRT
            Colors[3] = 813 
            
    elif NFiles is 8:
        Colors[0] = 616 #kMagenta+2     #IBL
        Colors[1] = 1 #kBlack           #Pixel
        Colors[2] = 632 #kRed           #SCT
        Colors[3] = 629 #kRed+2
        Colors[4] = 801 #kOrange+7
        Colors[5] = 416 #          #TRT
        Colors[6] = 398 
        Colors[7] = 813 

    elif NFiles > 3:
        for i in range(0,NFiles):
            Color_i = int(51+i*ColorStep)
            if Color_i>100:
                Color_i = 100
            #print " File ", i,  " --> color ",Color_i
            Colors[i] = Color_i
        Colors[1] = 1    
            
    if (doDebug):        
        for i in range(NFiles):
            print " color ",i,"=", Colors[i]
            
    return Colors

def  AutoMarkers(NFiles):
    Markers = {}

    if NFiles is 8:
        Markers[0] = 20 #kFullCircle	#IBL
        Markers[1] = 20 #kFullCircle	#Pixel
        Markers[2] = 20 #kFullCircle	#SCT
        Markers[3] = 22 #kFullTriangleUp
        Markers[4] = 23 #kFullTriangleDown
        Markers[5] = 20 #kFullCircle	#TRT
        Markers[6] = 22 #kFullTriangleUp
        Markers[7] = 23 #kFullTriangleDown
        return Markers

    if NFiles is 16:
        Markers[0] = 20 #kFullCircle 		#IBL
        Markers[1] = 20 #kFullCircle		#Pixel Barrel
        Markers[2] = 20 #kFullCircle
        Markers[3] = 20 #kFullCircle
        Markers[4] = 22 #kFullTriangleUp	#Pixel ECA
        Markers[5] = 22 #kFullTriangleUp
        Markers[6] = 22 #kFullTriangleUp
        Markers[7] = 23 #kFullTriangleDown	#Pixel ECC
        Markers[8] = 23 #kFullTriangleDown
        Markers[9] = 23 #kFullTriangleDown
        Markers[10] = 20 #kFullCircle		#SCT Barrel
        Markers[11] = 20 #kFullCircle
        Markers[12] = 20 #kFullCircle
        Markers[13] = 20 #kFullCircle
        Markers[14] = 22 #kFullTriangleUp	#SCT EC
        Markers[15] = 23 #kFullTriangleDown
        return Markers

    else:
        for i in range(0,NFiles):
			Markers[i] = 20
	return Markers



#def drawAllCorr(detector):
#    import time
#    from ROOT import TCanvas
#    from ROOT import TH1F
#    from ROOT import gPad
#    from ROOT import TLegend
#    debug = False
    
#    Alldetector = {}
#    nUsedDofs = 6

#    if (debug): print " -- drawAllCorr -- starting for detector = ",detector
#    showErrors = True
#    Alldetector = TCanvas("AlignmentCorrections(All)","Alignment Corrections (All)")
#    Alldetector.Divide(3,2)
#    AllCorrections = {}
#    yrange = [0,0,0,0,0,0]
#    if (debug): print " -- drawAllCorr -- finding out histogram ranges... "
#    for i in range(nUsedDofs):
#        if (debug): print "  -- drawAllCorr -- extracting range for dof:",i
#        for det in detector:
#            for bin in range(detector[det].nModules()):
#                #print " ** drawutils ** drawAllCorr ** det:",det,"  nModules = ",detector[det].nModules()
#                if abs(detector[det].GetModule(bin).GetDoF(i)[1])>yrange[i]:
#                    yrange[i] = abs(detector[det].GetModule(bin).GetDoF(i)[1])
#        yrange[i] *= 1.1
        
#    if (debug): print " -- drawAllCorr -- finding out colors ..."
#    Color = AutoColors(len(detector))
#    #print "++++++++++++++++++++++++++++++++++++++"
#    #print "++++++++++++++++++++++++++++++++++++++"
#    #print "++++++++++++++++++++++++++++++++++++++"
#    #print detector
#    for det in detector:
#        for i in range(nUsedDofs):
#            Alldetector.cd(i+1)
#            AllCorrections[det]={}
#            name, value = detector[det].GetModule(0).GetDoF(i)
#            hname = 'All_%s_corrections_%s' % (name,det)
#            htitle = 'All %s Corrections_%s' % (name,det)
#            AllCorrections[det][name] = TH1F(hname,htitle, detector[det].nModules(),0,detector[det].nModules())
#            if name is 'Tx' or name is 'Ty' or name is 'Tz':
#                AllCorrections[det][name].SetYTitle("mm")
#            else:
#                AllCorrections[det][name].SetYTitle("mrad")
#                
#            for bin in range(detector[det].nModules()):
#                AllCorrections[det][name].SetBinContent(bin+1,detector[det].GetModule(bin).GetDoF(i)[1])
#                if showErrors:
#                    AllCorrections[det][name].SetBinError(bin+1,detector[det].GetModule(bin).GetDoFError(i)[1])

#                if detector[det].nModules()<35:
#                    AllCorrections[det][name].GetXaxis().SetBinLabel(bin+1,detector[det].GetModule(bin).GetName())
                    
#            #AllCorrections[det][name].SetMarkerStyle(20)
#            AllCorrections[det][name].SetMarkerColor(Color[det])
#            AllCorrections[det][name].SetLineColor(Color[det])
#            AllCorrections[det][name].SetFillColor(Color[det])
#            AllCorrections[det][name].SetFillStyle(1001)

#            AllCorrections[det][name].SetStats(False)
#            if det==0:
#                AllCorrections[det][name].GetYaxis().SetRangeUser(-yrange[i],yrange[i])
#                AllCorrections[det][name].DrawCopy()                        
#            else:
#                AllCorrections[det][name].DrawCopy('same')

#            gPad.SetGridx()
#            gPad.SetGridy() 
#            gPad.Update()
#    return Alldetector

#############################################################
def drawAllCorr(detector):

    import time
    from ROOT import TCanvas
    from ROOT import TH1F
    from ROOT import gPad
    from ROOT import TLegend
    import os
    #check with environment variable if server runs as local test 
    runLocalTest = False
    try:
        runLocalTest = os.getenv('RUNLOCALTEST', False)
    except:
        runLocalTest = False

    print " -- drawAllCorr -- START -- " 
    showErrors = True
    Alldetector = {}
    AllCorrections = {}
    #         Tx     Ty     Tz     Rx     Ry     Rz     Bx
    yrange = [0.005, 0.005, 0.010, 0.001, 0.001, 0.001, 0.005]
    finalName = ["","","","","","",""]
    plotfile = {}

    # pointer to the folder when the server resides   
    alignWebRoot = ""
    try:
        alignWebRoot = os.getenv('ALIGNWEBROOT',"/var/vhost/atlas-alignment/")
    except:
        alignWebRoot = "/var/vhost/atlas-alignment/"
    # make sure that the last character of alignWebRoot is a slash
    if (alignWebRoot[-1] is not "/"):
        alignWebRoot += "/"
    
    pathfiles = "/var/vhost/atlas-alignment/secure/constant/"
    if (runLocalTest): 
        #pathfiles = "/Users/martis/projectes/atlas/alineament/webmonitoringtest/InDetAlignmentWebMonitor/trunk/WebPage/constant/"
        pathfiles = alignWebRoot + "WebPage/constant/"

    leg = TLegend(0.9,0.50,1,1)
    for i in range(7):
        for det in detector:
            for bin in range(detector[det].nModules()):
                if abs(detector[det].GetModule(bin).GetDoF(i)[1])>yrange[i]:
                   yrange[i] = abs(detector[det].GetModule(bin).GetDoF(i)[1])
        yrange[i] *= 1.1

        Color = AutoColors(detector[det].nModules())
	Marker = AutoMarkers(detector[det].nModules())

    for i in range(7):
        name,value = detector[detector.keys()[0]].GetModule(0).GetDoF(i)
        Alldetector[i] = {}
        Alldetector[i] = TCanvas("Alignment_corrections_%s" %(name), "Alignment_corrections_%s" %(name))
        leg.Clear()
        for module in range(detector[det].nModules()):

            AllCorrections[module]={}

            hname = 'All_%s_corrections_%s' % (name,module)
            #htitle = 'All %s Corrections_%s' % (name,module)
            htitle = 'Evolution of %s Corrections' %(name)
            AllCorrections[module][name] = TH1F(hname,htitle, len(detector),0,len(detector))

            if name is 'Tx' or name is 'Ty' or name is 'Tz' or name is 'Bx':
                AllCorrections[module][name].SetYTitle("mm")
            else:
                AllCorrections[module][name].SetYTitle("mrad")

            j = 0 #
            for det in sorted(detector):
                AllCorrections[module][name].SetBinContent(j+1,detector[det].GetModule(module).GetDoF(i)[1])

                AllCorrections[module][name].SetBinError(j+1,detector[det].GetModule(module).GetDoFError(i)[1])

                AllCorrections[module][name].GetXaxis().SetBinLabel(j+1,"%s"%(det))
                j +=1
           
            AllCorrections[module][name].SetMarkerStyle(Marker[module])
            AllCorrections[module][name].SetMarkerSize(1)
            AllCorrections[module][name].SetMarkerColor(Color[module])
            AllCorrections[module][name].SetLineColor(Color[module])
            AllCorrections[module][name].SetLineWidth(2)
            AllCorrections[module][name].SetFillStyle(0)
            AllCorrections[module][name].SetStats(False)
            leg.AddEntry(AllCorrections[module][name],"%s" %(detector[detector.keys()[0]].GetModule(module).GetName()),"p")
            if module==0:
                AllCorrections[module][name].GetYaxis().SetRangeUser(-yrange[i],yrange[i])
                AllCorrections[module][name].Draw("P E0X0 L")

            else:
                AllCorrections[module][name].Draw("P E0X0 L SAME")

            gPad.SetGridx()
            gPad.SetGridy()

        t = time.time()
        leg.Draw()
        finalName[i] = "%f_correction_%s" %(t, name)
        Alldetector[i].SaveAs(pathfiles + finalName[i] + ".png", "png")
        Alldetector[i].SaveAs(pathfiles + finalName[i] + ".pdf", "pdf")
        Alldetector[i].SaveAs(pathfiles + finalName[i] + ".root", "root")

    plotfile['png']={0:finalName[0] + ".png",1:finalName[1] + ".png",2:finalName[2] + ".png",3:finalName[3] + ".png",4:finalName[4] + ".png",5:finalName[5] + ".png", 6:finalName[6] + ".png"}
    plotfile['pdf']={0:finalName[0] + ".pdf",1:finalName[1] + ".pdf",2:finalName[2] + ".pdf",3:finalName[3] + ".pdf",4:finalName[4] + ".pdf",5:finalName[5] + ".pdf", 6:finalName[6] + ".pdf"}

    print " -- drawAllCorr -- COMPLETED -- " 

    return plotfile

#############################################################
def drawCorrEvolution(detector, labelList, drawErrors=False, drawLine=True, whichdof=-1, outputFormat=1, userLabel=""):
    from ROOT import TCanvas
    from ROOT import TH1F
    from ROOT import gPad
    from ROOT import TLegend
    from ROOT import TLine
    import time
    import os

    doDebug = True
    #check with environment variable if server runs as local test 
    runLocalTest = False
    try:
        runLocalTest = os.getenv('RUNLOCALTEST', False)
    except:
        runLocalTest = False

    # pointer to the folder when the server resides   
    alignWebRoot = ""
    try:
        alignWebRoot = os.getenv('ALIGNWEBROOT',"/var/vhost/atlas-alignment/")
    except:
        alignWebRoot = "/var/vhost/atlas-alignment/"
    # make sure that the last character of alignWebRoot is a slash
    if (alignWebRoot[-1] is not "/"):
        alignWebRoot += "/"

    showErrors = True
    drawAllDofs = True
    nUsedDofs = 7

    if (whichdof != -1):
        drawAllDofs = False 
        if (whichdof > 5): nUsedDofs = 7 # 7/oct/2015 with the BowX we may have up to 7 dofs. Unless stated draw the ordinary 6.

    lowerDof = 0;
    upperDof = 6;

    if (not drawAllDofs):
        lowerDof = whichdof
        upperDof = whichdof

    # output formats
    ALLINONE = 1
    ONEBYONE = 2
    SPLITBYSTRUCT = 3

    Alldetector = {} # list of canvas 
    finalName = ["","","","","","",""] #name of the output files

    gridALLENTRIES = 1
    gridNEWRUN = 2
    xGridType = gridNEWRUN
    
    #    
    pathfiles = "/var/vhost/atlas-alignment/secure/constant/"
    if (runLocalTest): 
        #pathfiles = "/Users/martis/projectes/atlas/alineament/webmonitoringtest/InDetAlignmentWebMonitor/trunk/WebPage/constant/"
        pathfiles = alignWebRoot + "WebPage/constant/"

    plotfile = {}

    rootSetup()

    dofNameForOutputFile = "All"
    if (lowerDof == upperDof):
        if (lowerDof == 0): dofNameForOutputFile = "Tx"
        if (lowerDof == 1): dofNameForOutputFile = "Ty"
        if (lowerDof == 2): dofNameForOutputFile = "Tz"
        if (lowerDof == 3): dofNameForOutputFile = "Rx"
        if (lowerDof == 4): dofNameForOutputFile = "Ry"
        if (lowerDof == 5): dofNameForOutputFile = "Rz"
        if (lowerDof == 6): dofNameForOutputFile = "Bx"
    
    # -- start the body of the code --
    if (doDebug):    
        print "\n -- drawCorrEvolution -- START -- \n"
        print "              runLocalTest= ",runLocalTest
        print "                 pathfiles= ",pathfiles
        print "              outputFormat= ",outputFormat
    if (doDebug):
        print " ======================================================= "
        print " == drawCorrEvolution ==                              == "
        print " == runLocalTest :", runLocalTest
        print " ======================================================== "
        print " == pathfiles :",pathfiles
        print " == lowerDof --> upperDof: ", lowerDof," --> ",upperDof
        print " == drawErrors: ", drawErrors
        print " == drawLine: ", drawLine
        print " == outputFormat: ", outputFormat 
        print " == dofNameForOutputFile: ", dofNameForOutputFile
        print " == userLabel: ",userLabel
        print " ======================================================== "
        
    
    # list of the histograms 
    hCorrectionsEvol = {}
    hCorrectionsEvolStruct={}
    # min axis range for each dof
    #         Tx     Ty     Tz     Rx    Ry    Rz    Bx
    yrange = [0.002, 0.002, 0.002, 0.01, 0.01, 0.01, 0.002] # minimum is 0.001 (mm or mrad)

    # here detector = num of iterations
    numberOfSamples = len(detector)
    if (doDebug): print " -- drawCorrEvolution -- numberOfSamples=", numberOfSamples
    numOfAlignableStruct = detector[0].nModules()
    if (doDebug): print " numOfAlignableStructe=", numOfAlignableStruct
    EvolColor = AutoColors(numOfAlignableStruct)    
   
    # a canvas for all dofs
    ThisCanvas = TCanvas("AlignmentCorrectionsEvol","Evolution of alignment corrections (All)",920,600)
    if (drawAllDofs and outputFormat == ALLINONE): ThisCanvas.Divide(3,2)

        
    # find out range
    #for i in range(lowerDof, upperDof):
    for i in range (nUsedDofs):
        for iter in range(numberOfSamples):
            for bin in range(detector[iter].nModules()):
                thisValue = abs(detector[iter].GetModule(bin).GetDoF(i)[1])+ detector[iter].GetModule(bin).GetDoFError(i)[1]
                if abs(thisValue)>yrange[i]:
                    yrange[i] = thisValue
        yrange[i] *= 1.025
        if (doDebug): print " dof=",i," --> temp range: ",yrange[i]

    #                
    # Tx and Ty should have the same range
    if (yrange[0] > yrange[1]): 
        yrange[1] = yrange[0]
    else:
        yrange[0] = yrange[1]    
    # Tz range should be as minimum as Tx and Ty
    if (yrange[2] < yrange[0]): yrange[2] = yrange[0]    

    #Bx range --> keep it independent
    yrange[6] *= 1.05 # scale it a bit more
                
    # Rx and Ry should have the same range
    if (yrange[3] > yrange[4]): 
        yrange[4] = yrange[3]
    else:
        yrange[3] = yrange[4]  
         
    # Rz keep it independent

    # maximum range
    #  --- Y range of the plots --- cap the drawing range 
    maxTransRange = 0.1
    if (yrange[0]> maxTransRange): yrange[0] = maxTransRange       
    if (yrange[1]> maxTransRange): yrange[1] = maxTransRange       
    if (yrange[2]> maxTransRange): yrange[2] = maxTransRange       
    if (yrange[6]> maxTransRange): yrange[6] = maxTransRange #Bx       

    if (doDebug):    
        for i in range (nUsedDofs):
            print " dof=",i," --> final range: ",yrange[i]
            
    #
    # prepare the legend
    #
    myLegend = TLegend(0.90,0.80,0.99,0.99)
    myLegend.SetFillColor(0) # white
    # and a line to split the runs if xGridType = gridNEWRUN
    myGridLine = TLine()
    myGridLine.SetLineStyle(3);
    
    # loop dof by dof (Tx, Ty...) and fill a polyline with teh corrections for each iteration
    if (doDebug): 
        print " -- drawCorrEvolution -- going to draw form lowerDof=", lowerDof, " to upperDof = ", upperDof
        
    #for dof in range(nUsedDofs):
    for dof in range(lowerDof, upperDof+1):
        # extract dof name
        name = detector[0].GetModule(0).GetDoF(dof)[0]
        if (doDebug): 
            print "\n -- drawCorrEvolution -- going to draw dof= %d (%s)" %(dof,name)

        #dealing with canvases
        if (outputFormat == ALLINONE):   
            ThisCanvas.cd()
            if (drawAllDofs): 
                ThisCanvas.cd(dof+1)
        if (outputFormat == ONEBYONE):  
            Alldetector[dof] = {}
            Alldetector[dof] = TCanvas("AlignCorrectionsEvol_%s" %(name), "Alignment_corrections_evolution_%s" %(name), 920, 600)
            print " -- drawCorrEvolution -- new canvas declared %s" %Alldetector[dof].GetName()
        if (outputFormat == SPLITBYSTRUCT): 
            Alldetector[dof] = {}
            Alldetector[dof] = TCanvas("AlignCorrectionsEvol_%s_byDOF" %(name), "Alignment_corrections_evolution_%s_byDOF" %(name), 920, 600)
            if (numOfAlignableStruct >= 15):
                Alldetector[dof].Divide(5,3)
                print " -- drawCorrEvolution -- Divide (5x3)"
            print " -- drawCorrEvolution -- new canvas declared %s for %d structures" %(Alldetector[dof].GetName(), numOfAlignableStruct)

        # prepare the histogram that will store the corrections 
        hname = 'Dof_%s_corrections_Evol' % (name)
        htitle = 'Evolution of %s corrections' % (name)
        if (doDebug): 
            print " -- drawCorrEvolution -- dof= %d  hname= %s" %(dof, hname)
            print "                                 htitle= ", htitle

        # build the histogram that is the main frame to plot the corrections for this dof (evolution of dof for each sample)
        hCorrectionsEvol[dof] = TH1F(hname, htitle, numberOfSamples, -0.5, numberOfSamples*1.-0.5)

        # set the x axis labels
        hCorrectionsEvol[dof].GetXaxis().SetLabelSize(0.05)
        if (numberOfSamples > 8): # this is in case there are too many
            hCorrectionsEvol[dof].GetXaxis().SetLabelSize(0.04)
            hCorrectionsEvol[dof].GetXaxis().SetBit(18)
            if (numberOfSamples > 16): # reduce further the size
                hCorrectionsEvol[dof].GetXaxis().SetLabelSize(0.03)
            if (numberOfSamples > 24): # reduce further the size
                hCorrectionsEvol[dof].GetXaxis().SetLabelSize(0.02)
            
        for iter in range(numberOfSamples): 
            hCorrectionsEvol[dof].GetXaxis().SetBinLabel(iter+1,'Iter_%d' % (iter))
            if (len(labelList)>iter): # use label given by user
                hCorrectionsEvol[dof].GetXaxis().SetBinLabel(iter+1,labelList[iter])

        # label of the Y axis
        if name is 'Tx' or name is 'Ty' or name is 'Tz' or name is 'Bx':
            hCorrectionsEvol[dof].SetYTitle("mm")
        else:
            hCorrectionsEvol[dof].SetYTitle("mrad")

        # set the range     
        hCorrectionsEvol[dof].GetYaxis().SetRangeUser(-yrange[dof],yrange[dof])
        hCorrectionsEvol[dof].SetStats(False)
        # going to draw the frame 
        # -be ware, in case of drawing by structure need to change to the right pad
        if (outputFormat == ALLINONE or outputFormat == ONEBYONE):
            hCorrectionsEvol[dof].DrawCopy()
            gPad.SetGridy()
            if (xGridType == gridALLENTRIES): gridPad.SetGridx()

            
        # draw the frame
        #hCorrectionsEvol[dof].DrawCopy()
        #gPad.SetGridx()
        #gPad.SetGridy()

        #
        # once the frame is plotted, loop on every structure and fill a histogram and draw it
        #
        if (doDebug):
            print "  -- drawCorrEvolution --  dealing with", name, "corrections. Y range for this dof: (",dof,")   range: +-",yrange[dof]
            print "                           reminder: numOfAlignableStruct = ",numOfAlignableStruct

        for struct in range(numOfAlignableStruct):
            if (doDebug and False): print " >> looping on struct:", struct
            if (outputFormat == SPLITBYSTRUCT): 
                Alldetector[dof].cd(struct+1)
                # then draw frame
                hCorrectionsEvol[dof].DrawCopy()
                gPad.SetGridy()
                if (xGridType == gridALLENTRIES): gridPad.SetGridx()
            hCorrectionsEvolStruct[dof]={}
            hname = 'Dof_%s_corrections_Evol_struct_%d' % (name, struct)
            htitle = 'Corrections evolution for structure %s (struct %d)' % (name, struct)
            hCorrectionsEvolStruct[dof][struct] = TH1F(hname, htitle, numberOfSamples, -0.5, numberOfSamples*1.-0.5)
            #print " -- drawCorrEvolution -- hCorrectionsEvolStruct has ",hCorrectionsEvolStruct[dof][struct].GetNbinsX(), ' bins in X'
            hCorrectionsEvolStruct[dof][struct].SetLineColor(EvolColor[struct])
            hCorrectionsEvolStruct[dof][struct].SetStats(False)
            # once the histogram is created, fill it with the corrections of each iteration

            currentLabel = "000000" # dummy value
            for iter in range(numberOfSamples): 
                value = detector[iter].GetModule(struct).GetDoF(dof)[1]
                hCorrectionsEvolStruct[dof][struct].SetBinContent(iter+1, value)
                if (drawErrors): hCorrectionsEvolStruct[dof][struct].SetBinError(iter+1, detector[iter].GetModule(struct).GetDoFError(dof)[1])
                # check the label in case it needs to be marked
                if (xGridType == gridNEWRUN):
                    thisLabel = labelList[iter][0:6]
                    if (thisLabel != currentLabel or "LBGrou" in thisLabel):
                        # new run found
                        currentLabel = thisLabel
                        #print " thisLabel = ", thisLabel 
                        myGridLine.DrawLine(iter, -yrange[dof], iter, yrange[dof])
                
            # now draw the corrections for this structure
            if (drawErrors): 
                hCorrectionsEvolStruct[dof][struct].SetFillColor(EvolColor[struct])
                hCorrectionsEvolStruct[dof][struct].SetFillStyle(3354)
                # hCorrectionsEvolStruct[dof][struct].DrawCopy('same e3')
                # --> original hCorrectionsEvolStruct[dof][struct].DrawCopy('same e3')
                hCorrectionsEvolStruct[dof][struct].SetMarkerStyle(20)
                hCorrectionsEvolStruct[dof][struct].SetMarkerSize(0.5)
                hCorrectionsEvolStruct[dof][struct].SetMarkerColor(EvolColor[struct])
                hCorrectionsEvolStruct[dof][struct].DrawCopy('same p e3 x0')
                for iter in range(numberOfSamples):
                    hCorrectionsEvolStruct[dof][struct].SetBinError(iter+1, 0)
                hCorrectionsEvolStruct[dof][struct].SetFillStyle(0)
                hCorrectionsEvolStruct[dof][struct].DrawCopy('l x0 e3 same')

            else:
                myOption = "same"
                if (drawLine): 
                    myOption += " l"
                else:
                    myOption += " p"
                    hCorrectionsEvolStruct[dof][struct].SetMarkerStyle(20)
                    hCorrectionsEvolStruct[dof][struct].SetMarkerColor(EvolColor[struct])
                        
                hCorrectionsEvolStruct[dof][struct].DrawCopy(myOption)
            gPad.Update()
            #if (dof == 0 and True): 
            if (True): 
                myLegend.AddEntry(hCorrectionsEvolStruct[dof][struct],detector[0].GetModule(struct).GetName(), "l")
                myLegend.Draw()
                gPad.Update()    

        t = time.time()
        finalName[dof] = "%f_evolution_%s" %(t, name)
        gPad.Update()
        if (len(userLabel)>0):
            finalName[dof] = "%s_%s" %(finalName[dof], userLabel) 
        if (outputFormat == ONEBYONE or outputFormat == SPLITBYSTRUCT):
            Alldetector[dof].SaveAs(pathfiles + finalName[dof] + ".png", "png")
            Alldetector[dof].SaveAs(pathfiles + finalName[dof] + ".pdf", "pdf")
            Alldetector[dof].SaveAs(pathfiles + finalName[dof] + ".root", "root")

        if (outputFormat == ALLINONE):
            #t = time.time()
            myFinalName = "%f_evolution_%s" %(t, dofNameForOutputFile)
            
            if (doDebug): print " -SALVA- myFinalName = ",myFinalName,"  userLabel: ",userLabel, "  len(userLabel)=",len(userLabel)
            if (len(userLabel)>0):
                myFinalName = "%f_evolution_%s_%s" %(t, dofNameForOutputFile, userLabel)
            finalName[dof] = myFinalName
            ThisCanvas.SaveAs(pathfiles+myFinalName + ".png","png")
            ThisCanvas.SaveAs(pathfiles+myFinalName + ".pdf","pdf")
            plotfile['png']={0:myFinalName + ".png"}
            plotfile['pdf']={0:myFinalName + ".pdf"}
        
    if (outputFormat == ONEBYONE or outputFormat == SPLITBYSTRUCT):            
        plotfile['png']={0:finalName[0] + ".png", 1:finalName[1] + ".png", 2:finalName[2] + ".png", 3:finalName[3] + ".png", 4:finalName[4] + ".png", 5:finalName[5] + ".png", 6:finalName[6] + ".png"}
        plotfile['pdf']={0:finalName[0] + ".pdf", 1:finalName[1] + ".pdf", 2:finalName[2] + ".pdf", 3:finalName[3] + ".pdf", 4:finalName[4] + ".pdf", 5:finalName[5] + ".pdf", 6:finalName[6] + ".pdf"}

    return plotfile

#######################################################################
def drawCorrVsHits(detector):
    from ROOT import TCanvas
    from ROOT import TGraph
    from array import array
    from ROOT import gPad
    CorrVsHits = TCanvas("CorrVsHits", "Alignment Corrections vs hits")
    CorrVsHits.Divide(3,2)
    hCorrVsHits = {}
    Color = AutoColors(len(detector))
    for det in detector:
        hCorrVsHits[det] = {}
        for i in range(6):
            CorrVsHits.cd(i+1)
            name, value = detector[det].GetModule(0).GetDoF(i)
            hname = 'CorrVsHits_%s_corrections_%d' % (name,det)
            htitle = '%s Corrections vs hits_%d' % (name,det)
            xpoints = []
            ypoints = []
            for j in range(detector[det].nModules()):
                xpoints.append(detector[det].GetModule(j).Hits)
                ypoints.append(detector[det].GetModule(j).GetDoF(i)[1])
            x = array("f",xpoints)
            y = array("f",ypoints)
            hCorrVsHits[det][name] = TGraph(detector[det].nModules(),x,y)
            hCorrVsHits[det][name].SetTitle(htitle)
            hCorrVsHits[det][name].GetXaxis().SetTitle("Hits per module")
            hCorrVsHits[det][name].GetYaxis().SetTitle(name)
            if name is 'Tx' or name is 'Ty' or name is 'Tz' or name is 'Bx':
                hCorrVsHits[det][name].GetYaxis().SetTitle(name+" (mm)")
            else:
                hCorrVsHits[det][name].GetYaxis().SetTitle(name+" (mrad)")
            hCorrVsHits[det][name].SetMarkerStyle(4)
            hCorrVsHits[det][name].SetMarkerSize(0.5)
            hCorrVsHits[det][name].SetMarkerColor(Color[det])
            if det==0:
                hCorrVsHits[det][name].Draw("Ap")
            else:
                hCorrVsHits[det][name].Draw("psame")
            gPad.SetGridx()
            gPad.SetGridy()
            gPad.SetLogx()
    CorrVsHits.Update()
    return CorrVsHits, hCorrVsHits  
    
def drawPixBarrelCorrDistributions(detector):
    from ROOT import TCanvas
    from ROOT import TH1F
    from ROOT import gPad
    PixBarrelCorrDistributions = TCanvas("PixBarrelCorrDistributions","Pixel Barrel Corrections Distributions")
    PixBarrelCorrDistributions.Divide(3,2)
    hPixBarrelCorrDistributions = {}
    detname = "Pixel Barrel"
    Color = AutoColors(len(detector))
    for d in detector:
        hPixBarrelCorrDistributions[d] = {}
        for i in range(6):
            PixBarrelCorrDistributions.cd(i+1)
            name, value = detector[d].GetModule(0).GetDoF(i)
            hname = '%s_%sCorrections_%d' % (detname,name,d)
            htitle = '%s %s Corrections' % (detname,name)
            if name is 'Tx':
                hPixBarrelCorrDistributions[d][name] = TH1F(hname,htitle,50,-0.005,0.005)
            elif name is 'Ty':
                hPixBarrelCorrDistributions[d][name] = TH1F(hname,htitle,50,-0.02,0.02)
            else:
                hPixBarrelCorrDistributions[d][name] = TH1F(hname,htitle,50,-0.25,0.25)
            if name is 'Tx' or name is 'Ty' or name is 'Tz' or name is 'Bx':
                hPixBarrelCorrDistributions[d][name].GetXaxis().SetTitle(name+" (mm)")
            else:
                hPixBarrelCorrDistributions[d][name].GetXaxis().SetTitle(name+" (mrad)")    
            
            hPixBarrelCorrDistributions[d][name].GetYaxis().SetTitle("Modules")
            hPixBarrelCorrDistributions[d][name].SetLineColor(Color[d])
            for module in detector[d].ReturnPixelBarrelModules():
                hPixBarrelCorrDistributions[d][name].Fill(module.GetDoF(i)[1])
            if d == 0:
                hPixBarrelCorrDistributions[d][name].Draw()
            else:
                hPixBarrelCorrDistributions[d][name].Draw("Same")   
            gPad.SetGridx()
            gPad.SetGridy()
    PixBarrelCorrDistributions.Update()
    return PixBarrelCorrDistributions, hPixBarrelCorrDistributions  
    
def drawSctBarrelCorrDistributions(detector):
    from ROOT import TCanvas
    from ROOT import TH1F
    from ROOT import gPad
    SctBarrelCorrDistributions = TCanvas("SctBarrelCorrDistributions","SCT Barrel Corrections Distributions")
    SctBarrelCorrDistributions.Divide(3,2)
    hSctBarrelCorrDistributions = {}
    detname = "SCT Barrel"
    Color = AutoColors(len(detector))
    for d in detector:
        hSctBarrelCorrDistributions[d] = {}
        for i in range(6):
            SctBarrelCorrDistributions.cd(i+1)
            name, value = detector[d].GetModule(0).GetDoF(i)
            hname = '%s_%sCorrections_%d' % (detname,name,d)
            htitle = '%s %s Corrections' % (detname,name)
            if name is 'Tx':
                hSctBarrelCorrDistributions[d][name] = TH1F(hname,htitle,50,-0.005,0.005)
            elif name is 'Ty':
                hSctBarrelCorrDistributions[d][name] = TH1F(hname,htitle,50,-0.1,0.1)
            else:
                hSctBarrelCorrDistributions[d][name] = TH1F(hname,htitle,50,-0.25,0.25)
            if name is 'Tx' or name is 'Ty' or name is 'Tz' or nasme is 'Bx':
                hSctBarrelCorrDistributions[d][name].GetXaxis().SetTitle(name+" (mm)")
            else:
                hSctBarrelCorrDistributions[d][name].GetXaxis().SetTitle(name+" (mrad)")    
            
            hSctBarrelCorrDistributions[d][name].GetYaxis().SetTitle("Modules")
            hSctBarrelCorrDistributions[d][name].SetLineColor(Color[d])
            for module in detector[d].ReturnSctBarrelModules():
                hSctBarrelCorrDistributions[d][name].Fill(module.GetDoF(i)[1])
            if d == 0:
                hSctBarrelCorrDistributions[d][name].Draw()
            else:
                hSctBarrelCorrDistributions[d][name].Draw("Same")   
            gPad.SetGridx()
            gPad.SetGridy()
    SctBarrelCorrDistributions.Update()
    return SctBarrelCorrDistributions, hSctBarrelCorrDistributions
        
def drawL3CorrVsHits(detector,det,bec):
    from ROOT import TCanvas
    from ROOT import TGraph
    from array import array
    from ROOT import gPad       
    if det == 1:
        if bec == None:
            detname = "PIX"
        elif bec == 0:
            detname = "PIXBarrel"
        elif bec == -1:
            detname = "PIXECC"
        elif bec == 1:
            detname = "PIXECA"
        
    elif det == 2:
        if bec == None:
            detname = "SCT"
        elif bec == 0:
            detname = "SCTBarrel"
        elif bec == -1:
            detname = "SCTECC"
        elif bec == 1:
            detname = "SCTECA"
        
    L3CorrVsHits = TCanvas(detname+"CorrVsHits", detname+" Alignment Corrections vs hits")
    L3CorrVsHits.Divide(3,2)
    hCorrVsHits = {}
    Color = AutoColors(len(detector))
    for d in detector:
        hCorrVsHits[d] = {}
        for i in range(6):
            L3CorrVsHits.cd(i+1)
            name, value = detector[d].GetModule(0).GetDoF(i)
            hname = '%s_CorrVsHits_%s_corrections' % (detname,name)
            htitle = '%s %s Corrections vs hits' % (detname,name)
            xpoints = []
            ypoints = []
            for j in detector[d].ReturnModules(det,bec):
                xpoints.append(detector[d].GetModule(j).Hits)
                ypoints.append(detector[d].GetModule(j).GetDoF(i)[1])
            x = array("f",xpoints)
            y = array("f",ypoints)
            hCorrVsHits[d][name] = TGraph(len(x),x,y)
            hCorrVsHits[d][name].SetTitle(htitle)
            hCorrVsHits[d][name].GetXaxis().SetTitle("Hits per module")
            hCorrVsHits[d][name].GetYaxis().SetTitle(name)
            if name is 'Tx' or name is 'Ty' or name is 'Tz' or name is 'Bx':
                hCorrVsHits[d][name].GetYaxis().SetTitle(name+" (mm)")
            else:
                hCorrVsHits[d][name].GetYaxis().SetTitle(name+" (mrad)")
            hCorrVsHits[d][name].SetMarkerStyle(4)
            hCorrVsHits[d][name].SetMarkerSize(0.5)
            hCorrVsHits[d][name].SetMarkerColor(Color[d])
            if d == 0:
                hCorrVsHits[d][name].Draw("Ap")
            else:
                hCorrVsHits[d][name].Draw("Ap")
            
            gPad.SetGridx()
            gPad.SetGridy()
    L3CorrVsHits.Update()
    return L3CorrVsHits, hCorrVsHits    
    
    
def drawStavePlots(detector,det):   
    from ROOT import TCanvas
    from ROOT import TH1F
    from ROOT import gPad
    StavePlots = {}
    if det == 1:
        Lay = [0,1,2]
        Phi = [22,38,52]
        detname = "PIX"
    if det == 2:
        Lay = [0,1,2,3]
        Phi = [32,40,48,56]
        detname = "SCT"
    ncanvas = 0
    for lay in Lay:
        for phi in range(Phi[lay]):
            StavePlots[ncanvas] = TCanvas("Stave%sPlots_L%d_Phi%d" %(detname, lay,phi),"Stave Plots %s L%d Phi%d" %(detname,lay,phi))
            StavePlots[ncanvas].Divide(3,2)
            stavemodules = detector.ReturnModules(det,0,lay,phi)
            hStaveCorrections = {}
            for i in range(6):
                StavePlots[ncanvas].cd(i+1)
                name, value = detector.GetModule(0).GetDoF(i)
                hname = 'Stave_%s_L%d_Phi%d_%s_corrections' % (detname,lay,phi,name)
                htitle = 'Stave %s L%d Phi%d %s Corrections' % (detname,lay,phi,name)
                hStaveCorrections[name] = TH1F(hname,htitle, len(stavemodules),0,len(stavemodules))
                if name is 'Tx' or name is 'Ty' or name is 'Tz' or name is 'Bx':
                    hStaveCorrections[name].SetYTitle("mm")
                else:
                    hStaveCorrections[name].SetYTitle("mrad")
                bin = 1
                for mod in stavemodules:
                    hStaveCorrections[name].SetBinContent(bin,detector.GetModule(mod).GetDoF(i)[1])
                    bin = bin+1
    
                #hStaveCorrections[name].Draw()
                XAxis = hStaveCorrections[name].GetXaxis()
                XAxis.CenterLabels()
                bin = 1
                for mod in stavemodules:
                    XAxis.SetBinLabel(bin,str(detector.GetModule(mod).Eta))
                    bin = bin + 1
                hStaveCorrections[name].SetStats(False)
                hStaveCorrections[name].DrawCopy()
                gPad.SetGridx()
                gPad.SetGridy()
            ncanvas = ncanvas + 1
    return StavePlots
    
def drawStaves(detector):
    StavePlots = []
    if detector.CountModules(1,0) > 0:
        StavePlots.append(drawStavePlots(detector,1))
    if detector.CountModules(2,0) > 0:
        StavePlots.append(drawStavePlots(detector,2))
    return StavePlots


#######################################################################
def drawSingleCorr(detector):
    from ROOT import TCanvas
    from ROOT import TH1F
    from ROOT import gPad
    from ROOT import TLegend
    import time
    import os
    #check with environment variable if server runs as local test 
    runLocalTest = False
    try:
        runLocalTest = os.getenv('RUNLOCALTEST', False)
    except:
        runLocalTest = False

    # pointer to the folder when the server resides   
    alignWebRoot = ""
    try:
        alignWebRoot = os.getenv('ALIGNWEBROOT',"/var/vhost/atlas-alignment/")
    except:
        alignWebRoot = "/var/vhost/atlas-alignment/"
    # make sure that the last character of alignWebRoot is a slash
    if (alignWebRoot[-1] is not "/"):
        alignWebRoot += "/"
    
    pathfiles = "/var/vhost/atlas-alignment/secure/constant/"
    if (runLocalTest): 
        #pathfiles = "/Users/martis/projectes/atlas/alineament/webmonitoringtest/InDetAlignmentWebMonitor/trunk/WebPage/constant/"
        pathfiles = alignWebRoot + "WebPage/constant/"

    plotfile = {}
    Alldetector = {}
    AllCorrections = {}
    # minimum scale of the Tx, Ty... plots
    yrange = [0.005, 0.005, 0.010, 0, 0, 0, 0.002]
    finalName = ["","","","","","",""]
    nUsedDofs = 7
    
    for i in range(nUsedDofs):
        for det in detector:
            for bin in range(detector[det].nModules()):
                if abs(detector[det].GetModule(bin).GetDoF(i)[1])>yrange[i]:
                    yrange[i] = abs(detector[det].GetModule(bin).GetDoF(i)[1])
        yrange[i] *= 1.1

    Color = AutoColors(len(detector))
    #Color = AutoColors(detector[det].nModules())
    leg = TLegend(0.81,0.91,0.98,0.98)

    for i in range(nUsedDofs):
        Alldetector[i] = TCanvas("AlignmentCorrections(%s)" %(i),"Alignment Corrections (%s)" %(i), 900, 600)
        leg.Clear()
        count = 0
        for det in detector:
            
            AllCorrections[det]={}
            name, value = detector[det].GetModule(0).GetDoF(i)
            hname = '%s_corrections_%d' % (name,count)
            #htitle = '%s Corrections Iter %d' % (name,count)
            htitle = '%s Corrections' % (name)
            AllCorrections[det][name] = TH1F(hname,htitle, detector[det].nModules(),0,detector[det].nModules())
            
            if name is 'Tx' or name is 'Ty' or name is 'Tz' or name is 'Bx':
                AllCorrections[det][name].SetYTitle("mm")
            else:
                AllCorrections[det][name].SetYTitle("mrad")
            
            for bin in range(detector[det].nModules()):
                AllCorrections[det][name].SetBinContent(bin+1,detector[det].GetModule(bin).GetDoF(i)[1])
                AllCorrections[det][name].SetBinError(bin+1,detector[det].GetModule(bin).GetDoFError(i)[1])
                AllCorrections[det][name].GetXaxis().SetBinLabel(bin+1,detector[det].GetModule(bin).GetName())
            
            AllCorrections[det][name].SetMarkerStyle(20)
            AllCorrections[det][name].SetMarkerSize(1.2)
            AllCorrections[det][name].SetMarkerColor(Color[count])
            AllCorrections[det][name].SetLineColor(Color[count])
            AllCorrections[det][name].SetFillColor(Color[count])
            AllCorrections[det][name].SetFillStyle(1001)
            AllCorrections[det][name].SetStats(False)
            leg.AddEntry(AllCorrections[det][name],"%s" %(det), "pl")
            if count == 0:
                AllCorrections[det][name].GetYaxis().SetRangeUser(-yrange[i],yrange[i])
                AllCorrections[det][name].DrawCopy('')
            else:
                AllCorrections[det][name].DrawCopy('same')
            gPad.SetGridx()
            gPad.SetGridy()
            count += 1
        count = 0
        t = time.time()
        leg.Draw()
        finalName[i] = "%f_correction_%s" %(t, name)
        Alldetector[i].SaveAs(pathfiles + finalName[i] + ".png", "png")
        Alldetector[i].SaveAs(pathfiles + finalName[i] + ".pdf", "pdf")
    plotfile['png']={0:finalName[0] + ".png",1:finalName[1] + ".png",2:finalName[2] + ".png",3:finalName[3] + ".png",4:finalName[4] + ".png",5:finalName[5] + ".png",6:finalName[6] + ".png"}
    plotfile['pdf']={0:finalName[0] + ".pdf",1:finalName[1] + ".pdf",2:finalName[2] + ".pdf",3:finalName[3] + ".pdf",4:finalName[4] + ".pdf",5:finalName[5] + ".pdf",6:finalName[6] + ".pdf"}
    
    return plotfile



