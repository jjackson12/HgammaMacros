from ROOT import *
import sys 
from getMCbgWeights import *
import re
import os


bkgDir = "../MC/Background/smallified"
signalDir = "../MC/Signal"
dataDir = "../HgammaCondor/smallified/smallified_singlePhoton2016.root"


nBins = 1000


histRanges = {}
histRanges["ph_pt"] = (0, 1200)
histRanges["jetAK8_pt"] = (0, 1500)
histRanges["ph_eta"] = (-3.,3.)
histRanges["ph_phi"] = (-3.14,3.14)
histRanges["jetAK8_eta"] = (-3.,3.)
histRanges["jetAK8_phi"] = (-3.14,3.14)
histRanges["jetAK8_puppi_softdrop_mass"] = (0,500)
histRanges["tau21"] = (0,1)

signalMasses = [600, 800,1000,2000,3500]


#weight calculation
weightDict = getMCbgWeightsDict(bkgDir)



observables = ["tau21", "ph_pt","jetAK8_pt","jetAK8_puppi_softdrop_mass"]#TODO, ADD: costheta*, John's poor-man's verson, think of others
observablesToTry = ["cosThetaStar","phPtoverMWgamma","jetAK8_puppi_softdrop_eta","leadingJet_eta","leadingPh_eta","phJetDeltaR","Ht"] #Ht = total hadronic energy in event
# See ph_eta cuts for ECAL endcap/barrel transition, 1.44 < eta < 1.57
#TODO: Make sure tau21 is taking from LEADING jets

def calcTau21Hist(sourceTree, histLabel):
    targetHist = TH1F(histLabel, histLabel, nBins, histRanges["tau21"][0], histRanges["tau21"][1])
    tempHist = targetHist.clone("tempHist")
    tempHist.SetTitle("tempHist")
    sourceTree.Draw('%s>>%s' % ("jetAK8_tau2", histLabel))
    sourceTree.Draw('%s>>%s' % ("jetAK8_tau1", "tempHist"))
    targetHist.Divide(tempHist)
    return targetHist



def getSignalHist(mass, observable):

    #sigFileDict = {}

    #sigHists = {}

    fileName = "%s/smallified_WGammaSig_m%s.root"%(signalDir,mass)
    sigFile = TFile(fileName)

    name = "signal_m" + str(mass)
#    iterTrees[name] = sigFileDict[name].Get("ntuplizer/tree")
    sigTree = sigFile.Get("ntuplizer/tree")
    histLabel = "%s_%s" % (name, observable)
	
    sigHist=TH1F(histLabel, histLabel, nBins, histRanges[observable][0], histRanges[observable][1])
    #iterTree.Draw('%s>>%s' % (observable, histLabel), str(weight))

    if(observable == "tau21"):
        sigHist = calcTau21Hist(iterTrees[name], histLabel)
    else:
        sigTree.Draw('%s>>%s' % (observable, histLabel))

    return sigHist

def getBackgroundHistStack(observable):
	bkgFileDict = {}
	bkgHists = {}
	iterTrees = {}

	for bkgFile in os.listdir(bkgDir):
	    print("processing background: %s\n" % bkgFile)
	    bkg = re.search(r'(.*)smallified_(.*).root',bkgFile).groups()[1]
	    bkgFileDict[bkg] = TFile("%s/%s" % (bkgDir, bkgFile))
	    iterTrees[bkg] = bkgFileDict[bkg].Get("ntuplizer/tree")
	    histLabel = "%s_%s" % (bkg, observable)
	    bkgHists[bkg]=TH1F(histLabel, histLabel, nBins, histRanges[observable][0], histRanges[observable][1])
	    #iterTree.Draw('%s>>%s' % (observable, histLabel), str(weight))
	    iterTrees[bkg].Draw('%s>>%s' % (observable, histLabel))
	    efficiency = iterTrees[bkg].GetEntries()/bkgFileDict[bkg].Get("ntuplizer/hCounter").GetBinContent(1)
	    weight =  weightDict["%s.root"%bkg][0]
	    bkgHists[bkg].Scale(weightDict["%s.root"%bkg][0])
	    #bkgHists[bkg].Scale(weight)
	    bkgHists[bkg].Sumw2()
	
	histStack = THStack()
	colors = [kRed,kBlue,kBlack,kGreen,kOrange,kYellow,kBlue-1,kRed+1,kGreen+2,kPink,kViolet,kAzure,kTeal,kTeal+3]
	for bkgHist in bkgHists.itervalues():
	    #bkgHist.Sumw2()
	    color = colors.pop()
	    bkgHist.SetLineColor(color)
	    bkgHist.SetFillColor(color)
	    histStack.Add(bkgHist)
	return histStack



def getDataHist(observable):

	dataFile = TFile(dataDir)
	data = dataFile.Get("ntuplizer/tree")
	
	dataHist = TH1F("dataHist", "dataHist", nBins, histRanges[observable][0], histRanges[observable][1])
	if(observable != "tau21"):
		data.Draw("%s>>dataHist" % observable)
	else:
		dataHist = calcTau21Hist(data,"dataHist")
	return dataHist



#NOTE: Different sets of cuts could yield better s/rtB when put together than isolated... Maybe later, try constructing sliding possible cuts for every observable, and running over every possible configuration
for observable in observables:
	print("plotting all for %s"%observable)


	cans = {}
	for sigMass in signalMasses:
	    print("\nplotting signal mass %s\n"%sigMass)
	    cans[sigMass] = TCanvas("can","Signal overlay on Data",800,800)
	    cans[sigMass].cd()
	    signal = getSignalHist(sigMass, observable)
	  
	    signal.SetLineColor(kRed)
	    #Normalize to data to find relative peaks. Remove to verify signal is beneath data before fine-tuning
	    '''
	    if(signal.GetSumOfWeights() != 0):
	        signal.Scale(dataHist.GetSumOfWeights()/signal.GetSumOfWeights())
	    else:
		#signal.Scale(1000)
	        print("WARNING: Zero sum of weights")
	    '''
	    signal.Draw()
	    dataHist.Draw("SAME")
	    leg = TLegend(0.7,0.7,0.9,0.9)
	    leg.AddEntry(signal,"signal")
	    leg.AddEntry(dataHist,"data")
	    leg.Draw("SAME")
	    cans[sigMass].SetLogy()
	    
	    printName = 'signalOverlays/%s/signal_m%s_%s.png'%(observable,str(sigMass), observable)
	    cans[sigMass].Print(printName,'png')

	    outFile = TFile("signalOverlays/%s/signal_m%s_%s.root"%(observable,str(sigMass), observable),"RECREATE")
	    outFile.cd()
	    cans[sigMass].Write()
	    outFile.Close()

