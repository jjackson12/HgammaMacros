from ROOT import *
from WgParameters import *
from testpy import getWRangesDict
import sys 
from getMCbgWeights import *
import re
import os
from numpy import linspace,sqrt


nBins = 75
histRanges = {}
histRanges["ph_pt"] = (0, 1200)
histRanges["jetAK8_pt"] = (0, 1500)
histRanges["ph_eta"] = (-3.,3.)
#histRanges["ph_phi"] = (-3.14,3.14)
histRanges["jetAK8_eta"] = (-3.,3.)
#histRanges["jetAK8_phi"] = (-3.14,3.14)
histRanges["jetAK8_puppi_softdrop_mass"] = (0,300)
bkgDir = "../MC/Background/smallified"



#TODO: Somewhere below; the bottom range of the top plot is being covered by the ratio plot





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






def plotComparison():
    
    prefixMap = {}
    prefixMap["Preselected"] = "preSelected_smallified"
    prefixMap["DD"] = "selected"
    prefixMap["Small3s"] = "smallified"

    treeMap = {}
    treeMap["Preselected"] = "Wgam"
    treeMap["DD"] = "Wgam"
    treeMap["smallified"] = "ntuplizer/tree"

    #getBackgroundHist(observable, baseCut)

    ####HACKACK
    #Import bkgHist 
    bkgFileDict = {}
    bkgHists = {}
    cans = {}
    outputFiles = {}
    iterTrees = {}
    for bkgFile in os.listdir(bkgDir):
      bkg = re.search(r'(.*)smallified_(.*).root',bkgFile).groups()[1]
      print("processing background: %s\n" % bkgFile)
      bkgFileDict[bkg] = TFile("%s/%s" % (bkgDir, bkgFile))

      iterTrees[bkg] = bkgFileDict[bkg].Get("ntuplizer/tree")
      for observable in histRanges.keys():

        histLabel = "%s_%s" % (bkg, observable)
        bkgHists["%s_%s"%(bkg,observable)]=TH1F(histLabel, histLabel, nBins, histRanges[observable][0], histRanges[observable][1])



        iterTrees[bkg].Draw('%s>>%s' % (observable, histLabel))
        #iterTrees[bkg].Draw(observable)
        outputFileName = "mcWTF_%s_%s"%(bkg,observable)
        cans[outputFileName] = TCanvas(outputFileName,outputFileName, 800, 800)
        cans[outputFileName].cd()
        bkgHists["%s_%s"%(bkg,observable)].Draw()
        outputFiles[outputFileName] = TFile("%s.root"%outputFileName, "RECREATE")
        outputFiles[outputFileName].cd()
        cans[outputFileName].Write()
        cans[outputFileName].Print("%s.png"%outputFileName)
        outputFiles[outputFileName].Close()






plotComparison()

