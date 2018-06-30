from ROOT import *
from WgParameters import *
from testpy import getWRangesDict
import sys 
from getMCbgWeights import *
import re
import os
from numpy import linspace,sqrt


sampleDirs = getSamplesDirs()
bkgDir =  sampleDirs["bkgSmall3sDir"]
dataDir = sampleDirs["dataSmall3sDir"]


nBins = 1000

histRanges = {}
histRanges["ph_pt"] = (0, 1200)
histRanges["jetAK8_pt"] = (0, 1500)
histRanges["ph_eta"] = (-3.,3.)
histRanges["ph_phi"] = (-3.14,3.14)
histRanges["jetAK8_eta"] = (-3.,3.)
histRanges["jetAK8_phi"] = (-3.14,3.14)
histRanges["jetAK8_puppi_softdrop_mass"] = (0,500)


weightDict = getWeightsDict(sampleDirs["bkgSmall3sDir"])


print(weightDict)







#TODO: Update
def getDataHist(observable):

	#dataFile = TFile(dataDir)
	#data = dataFile.Get("ntuplizer/tree")
	#
	#	data.Draw("%s>>dataHist" % observable)
	#else:
	#	dataHist = calcTau21Hist(data,"dataHist")
	#return dataHist
        return 0






def plotComparison(observable):
    

    print("\nplotting %s"%observable)
    #getBackgroundHist(observable, baseCut)

    ####HACKACK
    #Import bkgHist 
    bkgFileDict = {}
    bkgHists = {}
    iterTrees = {}
    print("processing backgrounds...")
    leg = TLegend(0.7,0.7,0.9,0.9)
    bkgHistStack = THStack()
    #colors = [kRed,kBlue,kBlack,kGreen,kOrange,kYellow,kBlue-1,kRed+1,kGreen+2,kPink,kViolet,kAzure,kTeal,kTeal+3]
    iQCD = 0
    igJets = 0
    iOther = 0
    for bkgFile in os.listdir(bkgDir):
        print("processing background: %s\n" % bkgFile)
        bkg = re.search(r'(.*)smallified_(.*).root',bkgFile).groups()[1]
        bkgFileDict[bkg] = TFile("%s/%s" % (bkgDir, bkgFile))
        print bkgFileDict[bkg]
        histLabel = "%s_%s" % (bkg, observable)
        bkgHists[bkg]=TH1F(histLabel, histLabel, nBins, histRanges[observable][0], histRanges[observable][1])
        iterTrees[bkg] = bkgFileDict[bkg].Get("ntuplizer/tree")
        print iterTrees[bkg]
        iterTrees[bkg].Draw('%s>>%s' % (observable, histLabel))
        weight = weightDict["%s.root"%bkg]
        bkgHists[bkg].Scale(weight[0])
        #bkgHists[bkg].Scale(weight)
        bkgHists[bkg].Sumw2()
    

        if "qcd" in bkg:
            color = kSpring + iQCD
            iQCD+=2
        elif "gJets" in bkg:
            color = kPink + igJets
            igJets+=1
        else:
            color = kAzure + iOther
            iOther+=1
        bkgHists[bkg].SetLineColor(color)
        bkgHists[bkg].SetFillColor(color)
        bkgHistStack.Add(bkgHists[bkg])
        leg.AddEntry(bkgHists[bkg],bkg)
    
    #histLabel = "finalHist"
    #bkgHists[histLabel]=TH1F(histLabel, histLabel, nBins, histRianges[observable][0][0], histRanges[observable][0][1])
    fullBkgHist = bkgHistStack.GetStack().Last().Clone()
    ####HACKHACK
    #End Import bkgHist

    outputFiles = {}
    cans = {}


    # Import dataHist
    dataFileName = "%s/smallified_singlePhoton2016.root" % dataDir
    dataFile = TFile(dataFileName)
    dataTree = dataFile.Get("ntuplizer/tree")
    histLabel = "dataHist"
	
    dataHist=TH1F(histLabel, histLabel, nBins, histRanges[observable][0], histRanges[observable][1])
    dataTree.Draw('%s>>%s' % (observable, histLabel))
    dataHist.SetLineColor(kBlack)
    #sigHists[sigMass].Scale(bkgScale/sigHists[sigMass].GetSumOfWeights())


    # Make Comparison Plot
    outputDir = "mcBkgChecks"
    outputFileName="mcBkgCheck_%s"%observable
    cans[outputFileName] = TCanvas(outputFileName,outputFileName, 800, 800)
    # TOOD: Add titles, labels
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0) 
    pad1.SetGridx() 
    pad1.SetLogy()
    pad1.Draw()
    pad1.cd() 
    #bkgHistStack.SetStats(0)        
    bkgHistStack.Draw("hist")
    dataHist.Draw("SAME")
    leg.AddEntry(dataHist,"data")
    leg.Draw("SAME")
    dataHist.SetTitle("data vs MC Background")
    dataHist.GetYaxis().SetLabelSize(0.)
    #axis = TGaxis(histRanges[observable][0], 0, histRanges[observable][1], , 20,220,510,"")
    #axis.SetLabelFont(43)
    #axis.SetLabelSize(15)
    #axis.Draw()
    cans[outputFileName].cd()           # Go back to the main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3) 
    pad2.SetTopMargin(0) 
    pad2.SetBottomMargin(0.2) 
    #pad2.SetGridx()  # vertical grid
    pad2.Draw() 
    pad2.cd()        # pad2 becomes the current pad
 
    # Define the ratio plot
    rPlot = dataHist.Clone("rPlot") 
    rPlot.SetLineColor(kBlack) 
    rPlot.SetMinimum(0.8)
    rPlot.SetMaximum(1.35)
    rPlot.Sumw2() 
    rPlot.SetStats(0)   
    rPlot.Divide(fullBkgHist) 
    rPlot.SetMarkerStyle(21) 
    #rPlot.Rebin(10,"rPlot",linspace(histRanges[observable][0],histRanges[observable][1],11)) 
    #rPlot.Rebin(100)
    rPlot.Draw("ep")
 
    # h1 settings
    dataHist.SetLineWidth(2) 
 
    # Y axis h1 plot settings
    dataHist.GetYaxis().SetTitleSize(20) 
    dataHist.GetYaxis().SetTitleFont(43) 
    dataHist.GetYaxis().SetTitleOffset(1.55) 
 
 
    # Ratio plot (rPlot) settings
    rPlot.SetTitle("")  # Remove the ratio title
 
    # Y axis ratio plot settings
    rPlot.GetYaxis().SetTitle("ratio data / MC Background ") 
    rPlot.GetYaxis().SetNdivisions(5) 
    rPlot.GetYaxis().SetTitleSize(20) 
    rPlot.GetYaxis().SetTitleFont(43) 
    rPlot.GetYaxis().SetTitleOffset(1.55) 
    rPlot.GetYaxis().SetLabelFont(43)  # Absolute font size in pixel (precision 3)
    rPlot.GetYaxis().SetLabelSize(15) 
 
    # X axis ratio plot settings
    rPlot.GetXaxis().SetTitleSize(20)

    rPlot.GetXaxis().SetTitleFont(43) 
    rPlot.GetXaxis().SetTitleOffset(4.) 
    rPlot.GetXaxis().SetLabelFont(43)  # Absolute font size in pixel (precision 3)
    rPlot.GetXaxis().SetLabelSize(15) 

    outputFiles[outputFileName] = TFile("%s/%s.root"%(outputDir,outputFileName), "RECREATE")
    outputFiles[outputFileName].cd()
    cans[outputFileName].Write()
    cans[outputFileName].Print("%s/%s.png"%(outputDir,outputFileName))
    outputFiles[outputFileName].Close()







#for ob in histRanges.keys():
  #plotComparison(ob)

plotComparison("ph_pt")
