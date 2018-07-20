from ROOT import *
from WgParameters import *
from WgCuts import *
from testpy import getWRangesDict
import sys 
from getMCbgWeights import *
import re
import os
import argparse
from numpy import linspace,sqrt


runOn = "Preselected"#OR DD

sampleDirs = getSamplesDirs()
sampleDirs["bkgPreselecteddir"] = "preSelectedBkg"
sampleDirs["sigPreselecteddir"] = "preSelectedSignal"
sampleDirs["dataPreselectedFile"] = "preSelected_singlePhoton2016.root"
sampleDirs["dataPreselecteddir"] = "."

bkgDir =  sampleDirs["bkg%sdir"%runOn]
signalDir = sampleDirs["sig%sdir"%runOn]
dataDir = sampleDirs["data%sdir"%runOn]
dataFileName = sampleDirs["data%sFile"%runOn]


nBins = 50

histRanges = {}
histRanges["Preselected"] = {}
histRanges["DD"] = {}
histRanges["DD"]["ph_pt"] = (0, 1200)
histRanges["DD"]["jetAK8_pt"] = (0, 1500)
histRanges["DD"]["ph_eta"] = (-3.,3.)
histRanges["DD"]["ph_phi"] = (-3.14,3.14)
histRanges["DD"]["jetAK8_eta"] = (-3.,3.)
histRanges["DD"]["jetAK8_phi"] = (-3.14,3.14)
histRanges["DD"]["jetAK8_puppi_softdrop_mass"] = (0,300)

histRanges["Preselected"]["leadingPhPt"] = (0, 1200)
histRanges["Preselected"]["WJet_puppi_pt"] = (0, 1500)
histRanges["Preselected"]["leadingPhEta"] = (-3.,3.)
histRanges["Preselected"]["leadingPhPhi"] = (-3.14,3.14)
histRanges["Preselected"]["WJet_puppi_eta"] = (-3.,3.)
histRanges["Preselected"]["WJet_puppi_phi"] = (-3.14,3.14)
histRanges["Preselected"]["WPuppi_softdropJetCorrMass"] = (0,500)

weightDict = getWeightsDict(sampleDirs["bkgSmall3sDir"])



#TODO: Somewhere below; the bottom range of the top plot is being covered by the ratio plot





#TODO: Update
def getDataHist(observable):

	#dataFile = TFile(dataDir)
	#data = dataFile.Get("ntuplizer/tree")
	#
	#	data.Draw("%s>>dataHistogram" % observable)
	#else:
	#	dataHistogram = calcTau21Hist(data,"dataHistogram")
	#return dataHistogram
        return 0






def plotComparison(observable, sideband, windowEdges=[70,90]):
    
    varDict = getVariableDict()
    if sideband:
      sbTitleTag = "in %s < %s < %s"%(windowEdges[0],varDict["WPuppi_softdropJetCorrMass"],windowEdges[1])
    else:
      sbTitleTag = "(no sideband)" 
    titleTxt = "%s %s"%(varDict[observable],sbTitleTag)

    prefixMap = {}
    prefixMap["Preselected"] = "preSelected_smallified"
    prefixMap["DD"] = "selected"
    prefixMap["Small3s"] = "smallified"

    treeMap = {}
    treeMap["Preselected"] = "Wgam"
    treeMap["DD"] = "Wgam"
    treeMap["smallified"] = "ntuplizer/tree"
    print("\n\nplotting %s, sideband = %s, with windowEdges - %s\n\n"%(observable, sideband, windowEdges))

    #getBackgroundHist(observable, baseCut)

    dataCut = getPreselectionComboCut(False,sideband,windowEdges)
    print("dataCut = %s"%dataCut)

    # Import dataHistogram
    #dataFileName = "%s/smallified_singlePhoton2016.root" % dataDir
    dataFile = TFile(dataFileName)
    dataTree = dataFile.Get(treeMap[runOn])
    histLabel = "dataHistogram"
	
    dataHistogram=TH1F(histLabel, varDict[observable] , nBins, histRanges[runOn][observable][0], histRanges[runOn][observable][1])
    dataTree.Draw('%s>>%s' % (observable, histLabel),dataCut)
    dataHistogram.SetLineColor(kBlack)

    dataScale = dataHistogram.GetSumOfWeights()

    ####HACKACK
    #Import bkgHist 
    bkgFileDict = {}
    bkgHists = {}
    iterTrees = {}
    print("processing backgrounds...")
    leg = TLegend(0.75,0.5,0.95,0.75)
    bkgHistStack = THStack()
    #colors = [kRed,kBlue,kBlack,kGreen,kOrange,kYellow,kBlue-1,kRed+1,kGreen+2,kPink,kViolet,kAzure,kTeal,kTeal+3]
    iQCD = 0
    igJets = 0
    iOther = 0
    for bkgFile in os.listdir(bkgDir):
        print("processing background: %s\n" % bkgFile)

        bkgEdges = []
        if sideband:
          bkgEdges = [70,90]
        bkgCut = getPreselectionComboCut(False,False,bkgEdges)
        print(bkgCut)
        bkg = re.search(r'(.*)%s_(.*).root'%prefixMap[runOn],bkgFile).groups()[1]
        bkgFileDict[bkg] = TFile("%s/%s" % (bkgDir, bkgFile))
        #print "%s/%s"%(bkgDir,bkgFile), bkgFileDict[bkg]
        histLabel = "dataHistogram"
        bkgHists[bkg]=TH1F(histLabel,"", nBins, histRanges[runOn][observable][0], histRanges[runOn][observable][1])


        iterTrees[bkg] = bkgFileDict[bkg].Get(treeMap[runOn])
        #print iterTrees[bkg]
        iterTrees[bkg].Draw('%s>>%s' % (observable, histLabel),bkgCut)
        weight = weightDict["%s.root"%bkg]
        bkgHists[bkg].Scale(weight[0])
        #bkgHists[bkg].Scale(weight)
        bkgHists[bkg].Sumw2()
    


        if "qcd" in bkg:
            color = kSpring + iQCD
            iQCD+=1
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



    fullBkgHist = bkgHistStack.GetStack().Last() 

    if(not(scaleSet)):
      bkgScale = fullBkgHist.GetSumOfWeights()
      scaleFactor = dataScale/bkgScale
    print("scaling all backgrounds by %s to match data"%scaleFactor)
    if(abs((scaleFactor - 1)) > 0.3):
      print("\n\nWARNING: scale factor very large: SF = %si\n\n"%scaleFactor)
    for bkgHist in bkgHistStack.GetStack():
      #Scale to data hist    
      bkgHist.Scale(scaleFactor)
    



    ####HACKHACK
    #End Import bkgHist

    outputFiles = {}
    cans = {}


    #sigHists[sigMass].Scale(bkgScale/sigHists[sigMass].GetSumOfWeights())


    # Make Comparison Plot

    if(sideband):
      outputDir = "mcBkgChecksSideband_%s-%s"%(windowEdges[0],windowEdges[1])
      outputFileName="mcBkgCheck_%s_%s-%s"%(observable,windowEdges[0],windowEdges[1])

    else:
      outputFileName="mcBkgCheck_%s"%observable
      outputDir = "mcBkgChecks"
    if(not(os.path.isdir(outputDir))):
      os.makedirs(outputDir)	





    cans[outputFileName] = TCanvas(titleTxt,titleTxt, 800, 800)
    # TODO: Add titles, labels
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    #		pad1.SetBottomMargin(0) 
    #pad1.SetGridx() 
    if ("Phi" not in observable and "phi" not in observable):
      pad1.SetLogy()
    else:
      dataHistogram.SetMinimum(0)
    pad1.cd() 
    #bkgHistStack.SetStats(0)        

    dataHistogram.SetLineWidth(2) 
    dataHistogram.GetYaxis().SetTitle("Events")
 
   # # Y axis h1 plot settings
    dataHistogram.GetYaxis().SetTitleSize(20) 
    dataHistogram.GetYaxis().SetTitleFont(43) 
    dataHistogram.GetYaxis().SetTitleOffset(1.55) 
    dataHistogram.GetXaxis().SetTitle(varDict[observable])
    dataHistogram.SetName("%s (data)"%varDict[observable])

    dataHistogram.Draw()
    bkgHistStack.Draw("hist SAME")
    dataHistogram.Draw("SAME")
    leg.AddEntry(dataHistogram,"data")
    leg.Draw("SAME")

    #dataHistogram.SetTitle("data vs MC Background")
    #dataHistogram.GetYaxis().SetLabelSize(0.)
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.29) 
    #		pad2.SetTopMargin(0) 
    #pad2.SetBottomMargin(0.2) 
    #pad2.SetGridx()  # vertical grid
    #		pad2.Draw() 
    pad2.cd()        # pad2 becomes the current pad
 
    # Define the ratio plot
    rPlot = dataHistogram.Clone("rPlot") 
    rPlot.Divide(fullBkgHist) 
    rPlot.SetLineColor(kBlack) 
    rPlot.SetTitle("")
    rPlot.SetMinimum(0.5)
    rPlot.SetMaximum(1.5)
    #rPlot.SetStats(0)   
    rPlot.SetMarkerStyle(21) 
    rPlot.Sumw2() 
    #rPlot.Rebin(10,"rPlot",linspace(histRanges[runOn][observable][0],histRanges[runOn][observable][1],11)) 
    #rPlot.Rebin(100)
    rPlot.Draw("ep")
 
    # h1 settings

 
 
    # Ratio plot (rPlot) settings
    rPlot.SetTitle("")  # Remove the ratio title
 
    # Y axis ratio plot settings
    rPlot.GetYaxis().SetTitle("data/MC") 
    rPlot.GetYaxis().SetNdivisions(7) 
    rPlot.GetYaxis().SetTitleSize(20) 
    rPlot.GetYaxis().SetTitleFont(43) 
    rPlot.GetYaxis().SetTitleOffset(1.55) 
    rPlot.GetYaxis().SetLabelFont(43)  # Absolute font size in pixel (precision 3)
    rPlot.GetYaxis().SetLabelSize(15) 
 
    # X axis ratio plot settings
    rPlot.GetXaxis().SetTitleFont(43) 
    rPlot.GetXaxis().SetTitleOffset(4.) 
    rPlot.GetXaxis().SetLabelFont(43)  # Absolute font size in pixel (precision 3)
    rPlot.GetXaxis().SetLabelSize(15) 

    cans[outputFileName].cd()           # Go back to the main canvas before defining pad2
    pad1.Draw()
    pad2.Draw()
    outputFiles[outputFileName] = TFile("%s/%s.root"%(outputDir,outputFileName), "RECREATE")
    outputFiles[outputFileName].cd()
    cans[outputFileName].Write()
    cans[outputFileName].Print("%s/%s.png"%(outputDir,outputFileName))
    outputFiles[outputFileName].Close()



from optparse import OptionParser
parser = OptionParser()
parser.add_option("-s","--sideband",action="store",type="string", dest="sideband",
                  help="use this to select sideband range"  )
(options, args) = parser.parse_args()



scaleSet = False
for ob in  ["leadingPhPt"]:# histRanges[runOn].keys():
  if options.sideband:
    sideWindows = [float(options.sideband.split("-")[0]),float(options.sideband.split("-")[1])]
    plotComparison(ob, True, sideWindows)
  else:
    plotComparison(ob,False,[])
#plotComparison("jetAK8_puppi_softdrop_mass")
