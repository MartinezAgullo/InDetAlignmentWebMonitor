def drawPlotRes(run):
    import os.path
    from ROOT import TCanvas
    from ROOT import TFile
    from ROOT import TH1F
    from ROOT import gPad
    from ROOT import TLegend
    import math
    import time
    try:
        import cPickle as pickle
    except:
        import pickle

    Color = [1, 2]
    try:
        server = "/var/vhost/atlas-alignment/database/"
        calibLoop = "/afs/cern.ch/user/a/atlidali/w0/calibLoop/web/database/"
        database = pickle.load(open(server + "server_runinfo2015.db",'r'))
    except:
        database = pickle.load(open(calibLoop + "server_runinfo2015.db",'r'))

    monFilePath = []
    Iter = []
    
    monpath0 = database[int(run)]['monitoringFile']
    monpath1 = database[int(run)]['monitoringFileIter1']
    
    if os.path.isfile(monpath0):
        if "Iter0" in monpath0:
            monFilePath.append(monpath0)
            Iter.append(0)
        elif "Iter1" in monpath0:
            monpath0 = monpath0.replace("Iter1","Iter0")
            if os.path.isfile(monpath0):
                monFilePath.append(monpath0)
                Iter.append(0)
        else:
            print "nothing to do"

    if os.path.isfile(monpath1):
        if "Iter1" in monpath1:
            monFilePath.append(monpath1)
            Iter.append(1)
        elif "Iter0" in monpath1:
            monpath1 = monpath1.replace("Iter0","Iter1")
            if os.path.isfile(monpath1):
                monFilePath.append(monpath1)
                Iter.append(1)

    PlotRes = {}    
    canvasname = ['pix','sct','d0vsphi0']
    results = []
    results.append(['pix_eca_xresvsmodphi','pix_eca_yresvsmodphi','pix_ecc_xresvsmodphi','pix_ecc_yresvsmodphi'])
    results.append(['sct_eca_xresvsmodphi','sct_ecc_xresvsmodphi'])
    results.append(['D0bsVsPhi0_Barrel','D0bsVsPhi0_ECA','D0bsVsPhi0_ECC'])
    plotsnames = []
    #pathfiles = "/afs/cern.ch/work/l/lbarranc/athena/20.1.0.3/InnerDetector/InDetMonitoring/InDetAlignmentWebMonitor/WebPage/constant/"
    pathfiles = "/var/vhost/atlas-alignment/secure/constant/"
    for k in range (len(canvasname)):
        legend = {}
        histos = {}
        monFile = {}
        PlotRes[k] = TCanvas(canvasname[k],canvasname[k])

        if canvasname[k] == 'sct':
            PlotRes[k].Divide(1,2)
        if canvasname[k] == 'pix':
            PlotRes[k].Divide(2,2)
        if canvasname[k] == 'd0vsphi0':
            PlotRes[k].SetCanvasSize(900,300)
            PlotRes[k].Divide(3,1)
        
        for i in range(len(Iter)):
           
            histos[i] = {}
            monFile[i] = TFile(monFilePath[i])
            for j in range(len(results[k])):

                PlotRes[k].cd(j + 1)
                if i == 0 and canvasname[k] != 'd0vsphi0':
                    legend[j] = TLegend(0.85,0.85,1.,1.)
                if i == 0 and canvasname[k] == 'd0vsphi0':
                    legend[j] = TLegend(0.7,0.80,1.,0.9)
                    
                if canvasname[k] != 'd0vsphi0':
                    
                    histos[i][j] = monFile[i].Get('IDAlignMon/AlignTracks_all/Residuals/%s' %(results[k][j]))
                    histos[i][j].GetYaxis().SetRangeUser(-0.035,0.035)
                    


                if canvasname[k] == 'd0vsphi0':
                    
                    temphist = monFile[i].Get('IDAlignMon/AlignTracks_all/GenericTracks/%s' %(results[k][j]))
                    tempprof = temphist.ProfileX()
                    tempprof.Draw()
                    histos[i][j] = TH1F(canvasname[k],results[k][j],tempprof.GetNbinsX(), 0, 2.*math.pi )
                    for bins in range(histos[i][j].GetNbinsX()):
                        histos[i][j].SetBinContent(bins +1,tempprof.GetBinContent(bins +1))
                        histos[i][j].SetBinError(bins +1,tempprof.GetBinError(bins +1))
                    histos[i][j].GetYaxis().SetRangeUser(-0.015,0.015)
                    histos[i][j].GetYaxis().SetTitle("d0_{bs} (mm)")

                histos[i][j].SetMarkerStyle(7)
                histos[i][j].SetMarkerColor(Color[i])
                histos[i][j].SetMarkerSize(0.7)
                histos[i][j].SetLineColor(Color[i])
                histos[i][j].SetFillColor(Color[i])
                histos[i][j].SetFillStyle(1001)
                histos[i][j].SetStats(False)
                if i == 0:
                    histos[i][j].DrawCopy('')
                    legend[j].AddEntry(histos[i][j], "%s Iter %s" %(run, Iter[i]),"p")
                    legend[j].SetTextSize(0.03)
                else:
                    histos[i][j].DrawCopy('same')
                    legend[j].AddEntry(histos[i][j], "%s Iter %s" %(run, Iter[i]),"p")
                    legend[j].SetTextSize(0.03)

                gPad.SetGridx()
                gPad.SetGridy()
                legend[j].Draw()

            gPad.Update()
        plotsnames.append("%s_%f_%s" %(canvasname[k], time.time(),canvasname[k]))
        PlotRes[k].SaveAs("%s%s.eps" %(pathfiles, plotsnames[k]),"eps")
        PlotRes[k].SaveAs("%s%s.png" %(pathfiles, plotsnames[k]),"png")



    return plotsnames
