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


#NOTE: Different sets of cuts could yield better s/rtB when put together than isolated... Maybe later, try constructing sliding possible cuts for every observable, and running over every possible configuration







def plotComparison(observable):
    
    #TODO: Need better way to optimize on ALL signal masses; they need to be considered together to some extent, such as combining them into the map


    print("\nplotting %s"%observable)
    #getBackgroundHist(observable, baseCut)

    ####HACKACK
    #Import bkgHist 
    bkgFileDict = {}
    bkgHists = {}
    iterTrees = {}
    print("processing backgrounds...")
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
    
    bkgHistStack = THStack()
    #colors = [kRed,kBlue,kBlack,kGreen,kOrange,kYellow,kBlue-1,kRed+1,kGreen+2,kPink,kViolet,kAzure,kTeal,kTeal+3]
    iQCD = 0
    igJets = 0
    iOther = 0
    for bkgHist in bkgHists.itervalues():
        if "qcd" in bkg:
            color = kAzure + iQCD
            iQCD+=1
        elif "gJets" in bkg:
            color = kSpring + igJets
            igJets+=1
        else:
            color = kViolet - iOther
            iOther+=1
        bkgHist.SetLineColor(color)
        bkgHist.SetFillColor(color)
        bkgHistStack.Add(bkgHist)
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
    dataTree = sigFile.Get("ntuplizer/tree")
    histLabel = "dataHist"
	
    dataHist=TH1F(histLabel, histLabel, nBins, histRanges[observable][0], histRanges[observable][1])
    dataTree.Draw('%s>>%s' % (observable, histLabel))
    #sigHists[sigMass].Scale(bkgScale/sigHists[sigMass].GetSumOfWeights())


    # Make Comparison Plot
    outputFileName="mcBkgCheck_%s"%(name,observable)
    can = TCanvas(outputFileName,outputFileName)
    can.cd()
    bkgHistStack.Draw()
    dataHist.Draw("SAME")
    leg = TLegend(0.7,0.7,0.9,0.9)
    leg.AddEntry(dataHist,"data")
    leg.AddEntry(bkgHistStack,"background (MC)")
    leg.Draw("SAME")
    can.SetLogy()
    outputFiles[outputFileName] = TFile("%s.root"%outputFileName, "RECREATE")
    outputFiles[outputFileName].cd()
    cans[outputFileName].Write()
    cans[outputFileName].Print("%s.pdf"%outputFileName)
    outputFiles[outputFileName].Close()

    #TODO: Ratio


























for ob in histRanges.keys():
  plotComparison(ob)
