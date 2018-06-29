from ROOT import *
from WgCuts import *
from WgParameters import *
from testpy import getWRangesDict
import sys 
from getMCbgWeights import *
import re
import os
from numpy import linspace,sqrt


sampleDirs = getSamplesDirs()
bkgDir =  sampleDirs["bkgDDdir"]
signalDir = sampleDirs["sigDDdir"]
dataDir = sampleDirs["dataDDdir"]


nBins = 1000

histRanges = getWRangesDict()
#histRanges["ph_pt"] = (0, 1200)
#histRanges["jetAK8_pt"] = (0, 1500)
#histRanges["ph_eta"] = (-3.,3.)
#histRanges["ph_phi"] = (-3.14,3.14)
#histRanges["jetAK8_eta"] = (-3.,3.)
#histRanges["jetAK8_phi"] = (-3.14,3.14)
#histRanges["jetAK8_puppi_softdrop_mass"] = (0,500)
#histRanges["tau21"] = (0,1)

signalMasses = [600,800,1000,2000,3500]


weightDict = getWeightsDict(sampleDirs["bkgSmall3sDir"])
varKeys = getVarKeys()
#cutVars = ["Tau21", "ph_pt","jetAK8_pt","jetAK8_puppi_softdrop_mass"]
#cutVarsToTry = ["cosThetaStar","phPtoverMWgamma","leadingJet_eta","leadingPh_eta","phJetDeltaR","Ht","WJet_Tau21"] #Ht = total hadronic energy in event
# See ph_eta cuts for ECAL endcap/barrel transition, 1.44 < eta < 1.57



def getSoverRootB(bkg, sig, start, stop,scale):
  bb=0.
  ss=0.
  for iBin in range(bkg.FindBin(start), bkg.FindBin(stop)):
      bb+=bkg.GetBinContent(iBin)
      #print("bb += %s"%bkg.GetBinContent(iBin))
      ss+=sig.GetBinContent(iBin)
      #print("ss += %s"%sig.GetBinContent(iBin))
  if bb != 0:
    return ss*scale/sqrt(bb*scale)
  else:
    return "b=0"



#UNUSED
def getSignalHist(mass, cutVar, cut, scaleTo):


    name = "m" + str(mass)
    sigFileName = "%s/selected_flatTuple_WGammaSig_%s.root" % (signalDir, name)
    sigFile = TFile(sigFileName)
    #print "Grabbed file: ", sigFileName
#    iterTrees[name] = sigFileDict[name].Get("ntuplizer/tree")
    sigTree = sigFile.Get("Wgam")
    histLabel = "%s_%s" % (name, cutVar)
	
    sigHists[sigMass]=TH1F(histLabel, histLabel, nBins, histRanges[cutVar][0][0], histRanges[cutVar][0][1])

    sigTree.Draw('%s>>%s' % (cutVar, histLabel), cut)
    sigHists[sigMass].Scale(scaleTo/sigHists[sigMass].GetSumOfWeights())

    return sigHists[sigMass]





#UNUSED
def getBackgroundHistStack(cutVar,cut):
	bkgFileDict = {}
	bkgHists = {}
	iterTrees = {}
        
	for bkgFile in os.listdir(bkgDir):
	    #print("processing background: %s\n" % bkgFile)
	    bkg = re.search(r'(.*)selected_(.*).root',bkgFile).groups()[1]
	    bkgFileDict[bkg] = TFile("%s/%s" % (bkgDir, bkgFile))
	    histLabel = "%s_%s" % (bkg, cutVar)
	    bkgHists[bkg]=TH1F(histLabel, histLabel, nBins, histRanges[cutVar][0][0], histRanges[cutVar][0][1])

	    iterTrees[bkg] = bkgFileDict[bkg].Get("Wgam")
	    iterTrees[bkg].Draw('%s>>%s' % (cutVar, histLabel),cut)
            weight = weightDict["%s.root"%bkg]
	    bkgHists[bkg].Scale(weight[0])
	    #bkgHists[bkg].Scale(weight)
	    bkgHists[bkg].Sumw2()
	
	histStack = THStack()
        #TODO: Assign colors in coordination with type of background
	colors = [kRed,kBlue,kBlack,kGreen,kOrange,kYellow,kBlue-1,kRed+1,kGreen+2,kPink,kViolet,kAzure,kTeal,kTeal+3]
	for bkgHist in bkgHists.itervalues():
	    #bkgHist.Sumw2()
	    color = colors.pop()
	    bkgHist.SetLineColor(color)
	    bkgHist.SetFillColor(color)
	    histStack.Add(bkgHist)
        #TODO: This is failing;correctly gets histogram here, but when passing it, the hist is destroyed
        #histLabel = "finalHist"
        #bkgHists[histLabel]=TH1F(histLabel, histLabel, nBins, histRianges[cutVar][0][0], histRanges[cutVar][0][1])
        fullHist = histStack.GetStack().Last().Clone()
        fullHist.SetDirectory(0)
        return  fullHist




#TODO: Update
def getDataHist(cutVar):

	#dataFile = TFile(dataDir)
	#data = dataFile.Get("ntuplizer/tree")
	#
	#dataHist = TH1F("dataHist", "dataHist", nBins, histRanges[cutVar][0], histRanges[cutVar][1])
	#if(cutVar != "tau21"):
	#	data.Draw("%s>>dataHist" % cutVar)
	#else:
	#	dataHist = calcTau21Hist(data,"dataHist")
	#return dataHist
        return 0


#NOTE: Different sets of cuts could yield better s/rtB when put together than isolated... Maybe later, try constructing sliding possible cuts for every cutVar, and running over every possible configuration







def plotOpt(baseCut,cutVar,nSteps=50):
    
    #TODO: Need better way to optimize on ALL signal masses; they need to be considered together to some extent, such as combining them into the map


    print("\noptimizing on %s"%cutVar)
    #TODO: Sort backgrounds intoo qcd, gJets, and others
    #getBackgroundHist(cutVar, baseCut)

    ####HACKACK
    #Import bkgHist 
    bkgFileDict = {}
    bkgHists = {}
    iterTrees = {}
    print("processing backgrounds...")
    for bkgFile in os.listdir(bkgDir):
        #print("processing background: %s\n" % bkgFile)
        bkg = re.search(r'(.*)selected_(.*).root',bkgFile).groups()[1]
        bkgFileDict[bkg] = TFile("%s/%s" % (bkgDir, bkgFile))
        histLabel = "%s_%s" % (bkg, cutVar)
        bkgHists[bkg]=TH1F(histLabel, histLabel, nBins, histRanges[cutVar][0][0], histRanges[cutVar][0][1])
    
        iterTrees[bkg] = bkgFileDict[bkg].Get("Wgam")
        iterTrees[bkg].Draw('%s>>%s' % (cutVar, histLabel),baseCut)
        weight = weightDict["%s.root"%bkg]
        bkgHists[bkg].Scale(weight[0])
        #bkgHists[bkg].Scale(weight)
        bkgHists[bkg].Sumw2()
    
    bkgHistStack = THStack()
    #TODO: Assign colors in coordination with type of background
    colors = [kRed,kBlue,kBlack,kGreen,kOrange,kYellow,kBlue-1,kRed+1,kGreen+2,kPink,kViolet,kAzure,kTeal,kTeal+3]
    for bkgHist in bkgHists.itervalues():
        #bkgHist.Sumw2()
        color = colors.pop()
        bkgHist.SetLineColor(color)
        bkgHist.SetFillColor(color)
        bkgHistStack.Add(bkgHist)
    #histLabel = "finalHist"
    #bkgHists[histLabel]=TH1F(histLabel, histLabel, nBins, histRianges[cutVar][0][0], histRanges[cutVar][0][1])
    bkgHist = bkgHistStack.GetStack().Last().Clone()
    ####HACKHACK
    #End Import bkgHist

    outputFiles = {}
    cans = {}


    #TEST-TEMPORARY

    outputFileName="backgroundHistStackOnly_%s"%cutVar
    cans[outputFileName] = TCanvas(outputFileName,outputFileName)
    cans[outputFileName].cd()
    bkgHistStack.Draw()

    outputFiles[outputFileName] = TFile("%s.root"%outputFileName, "RECREATE")
    outputFiles[outputFileName].cd()
    cans[outputFileName].Write()
    cans[outputFileName].Print("%s.pdf"%outputFileName)
    outputFiles[outputFileName].Close()

    #TEST-TEMPORARY

    #bkgScale = bkgHist.GetSumOfWeights()
    
    varRange = histRanges[cutVar]
    upperBound = varRange[0][1]
    lowerBound = varRange[0][0]
    #TODO: Check if /10 is okay
    nSplits = bkgHist.GetNbinsX()/10
    #nSplits = nSteps

    varRangeList = linspace(lowerBound,upperBound,nSplits)


    sigFiles = {}
    sigTrees = {}
    sigHists = {}



    sRtBMaps = {}

 
    for sigMass in signalMasses:
      print("\nplotting signal mass %s\n"%sigMass)
      
      # HACK HACK
      # Import sigHists[sigMass]
      name = "m" + str(sigMass)
      sigFileName = "%s/selected_flatTuple_WGammaSig_%s.root" % (signalDir, name)
      sigFiles[sigMass] = TFile(sigFileName)
      sigTrees[sigMass] = sigFiles[sigMass].Get("Wgam")
      histLabel = "%s_%s" % (name, cutVar)
  	
      sigHists[sigMass]=TH1F(histLabel, histLabel, nBins, histRanges[cutVar][0][0], histRanges[cutVar][0][1])
      sigTrees[sigMass].Draw('%s>>%s' % (cutVar, histLabel), baseCut)
      #sigHists[sigMass].Scale(bkgScale/sigHists[sigMass].GetSumOfWeights())


      #TEST-TEMPORARY

      outputFileName="signalOnly_%s_%s"%(name,cutVar)
      cans[outputFileName] = TCanvas(outputFileName,outputFileName)
      cans[outputFileName].cd()
      sigHists[sigMass].Draw()

      outputFiles[outputFileName] = TFile("%s.root"%outputFileName, "RECREATE")
      outputFiles[outputFileName].cd()
      cans[outputFileName].Write()
      cans[outputFileName].Print("%s.pdf"%outputFileName)
      outputFiles[outputFileName].Close()

      #TEST-TEMPORARY

      #TEST-TEMPORARY

      outputFileName="signalOverlay_%s_%s"%(name,cutVar)
      cans[outputFileName] = TCanvas(outputFileName,outputFileName)
      cans[outputFileName].cd()
      bkgHistStack.Draw()
      sigHists[sigMass].Draw("SAME")
      leg = TLegend(0.7,0.7,0.9,0.9)
      leg.AddEntry(sigHists[sigMass],"signal")
      leg.AddEntry(bkgHistStack,"background (MC)")
      leg.Draw("SAME")

      outputFiles[outputFileName] = TFile("%s.root"%outputFileName, "RECREATE")
      outputFiles[outputFileName].cd()
      cans[outputFileName].Write()
      cans[outputFileName].Print("%s.pdf"%outputFileName)
      outputFiles[outputFileName].Close()

      #TEST-TEMPORARY






      bkgScale = 0
      sigScale = 0
      for bkgBin in range (1, bkgHist.GetXaxis().GetNbins()+1):
        bkgScale+=bkgHist.GetBinContent(bkgBin) 
        sigScale+=sigHists[sigMass].GetBinContent(bkgBin)
      sigScaleFactor = 1/sigScale
      bkgScaleFactor = 1/bkgScale
      scaleFactor = bkgScale/sigScale

      for sigBin in range (1, sigHists[sigMass].GetXaxis().GetNbins()+1):
        #sigHists[sigMass].SetBinContent(sigBin, sigHists[sigMass].GetBinContent(sigBin)*sigScaleFactor) 
        #bkgHist.SetBinContent(sigBin, bkgHist.GetBinContent(sigBin)*bkgScaleFactor) 
        sigHists[sigMass].SetBinContent(sigBin, sigHists[sigMass].GetBinContent(sigBin)*scaleFactor) 
  
      # Hack Hack
      # Import sigHists[sigMass]

      if not (sigHists[sigMass].GetNbinsX() == bkgHist.GetNbinsX() and (sigHists[sigMass].GetSumOfWeights() - bkgHist.GetSumOfWeights()) < (0.05*bkgHist.GetSumOfWeights())):
        print "bkg sum = %s\nsig sum = %s"%(bkgHist.GetSumOfWeights(), sigHists[sigMass].GetSumOfWeights())
        print "nonmatching histograms!"
        quit()

      directionMap = getDirections()
      directionWord = directionMap[varKeys[cutVar]]
      if directionWord in "both":
        directions = ["up","down"]
        bounds = varRangeList
      else:
        directions = [directionWord]
        if directionWord in "up":
          bounds = [upperBound]
        elif directionWord in "down":
          bounds = [lowerBound]

      # dict mapping cut ranges to s/rt(b) calculations
      sRtBcuts = {}
      
      lowBoundList = []
      highBoundList = []
      sRtBList = []
  
      optimalCut = ([0,0],-1)



      #Loop over ranges
      for boundPoint in bounds:
        for start in varRangeList:
          for direction in directions:
            #TODO: Fix conditions; giving b=0 always
            if direction in "up":
              if(boundPoint > start):
                cutRange = (start,boundPoint)
              else:
                continue

            if direction in "down":
              if(boundPoint < start):
                cutRange = (boundPoint,start)
              else:
                continue
            

            sRtB = getSoverRootB(bkgHist,sigHists[sigMass], cutRange[0], cutRange[1], 1/bkgScale)

            if(isinstance(sRtB,str)):
              continue
            #print("in range %s, s/rt(b) = %s"%(cutRange,sRtB))
            sRtBcuts[cutRange] = sRtB
            if(sRtB > optimalCut[1]):
              optimalCut = (cutRange, sRtB)
            lowBoundList.append(cutRange[0])
            sRtBList.append(sRtB)
            highBoundList.append(cutRange[1])
 


      print "############################\noptimal cut range for %s in mass range %s looks to be %s, with s/rt(b) = %s\n#############################\n"%(cutVar,sigMass,optimalCut[0],optimalCut[1])
      outputName = "sRtBMaps/sRtBMap_%s_%s"%(cutVar,sigMass)
      #TODO: REPLACE WIH TGRAPHS AND SOME SORT OF HEATMAPS
      if directionWord in "both":
        sRtBMaps[sigMass] = TGraph2D(len(sRtBList))
        for i in range(len(sRtBList)):
          sRtBMaps[sigMass].SetPoint(i,lowBoundList.pop(0),highBoundList.pop(0),sRtBList.pop(0))
      if directionWord in "up":
        sRtBMaps[sigMass] = TGraph(len(sRtBList))
        for  i in range(len(sRtBList)):
          x = lowBoundList.pop(0)
          y = sRtBList.pop(0)
          sRtBMaps[sigMass].SetPoint(i,x,y)
      
      if directionWord in "down":
        sRtBMaps[sigMass] = TGraph(len(sRtBList))
        for  i in range(len(sRtBList)):
          x = highBoundList.pop(0)
          y = sRtBList.pop(0)
          sRtBMaps[sigMass].SetPoint(i,x,y)
        #sRtBMaps[sigMass] = TGraph(len(sRtBList),highBoundList,sRtBList)
      cans[sigMass] = TCanvas(outputName,outputName)
      #pad = TPad()
      #pad.cd()
      cans[sigMass].cd()
      if directionWord in "both":
        gStyle.SetPalette(1)
        sRtBMaps[sigMass].Draw("surf1")
      else:
        sRtBMaps[sigMass].Draw()
      sRtBMaps[sigMass].GetXaxis().SetLimits(lowerBound, upperBound)
      sigHists[sigMass].GetXaxis().SetLimits(lowerBound, upperBound)

      sigHists[sigMass].GetYaxis().SetLimits(0,1.7)

      if not directionWord in "both":
        graphScale = sRtBMaps[sigMass].Integral(0,len(sRtBList)-1)
        for hist in bkgHistStack.GetStack():
          hist.GetXaxis().SetLimits(lowerBound, upperBound)
          hist.Scale(graphScale/bkgScale)
          hist.GetYaxis().SetLimits(0,1.7)
        sigHists[sigMass].Scale(graphScale/sigScale)
        bkgHistStack.Draw("SAME")
        sigHists[sigMass].Draw("SAME")
        leg = TLegend(0.7,0.7,0.9,0.9)
        leg.AddEntry(sigHists[sigMass],"signal")
        leg.AddEntry(bkgHistStack,"background")
        leg.AddEntry(sRtBMaps[sigMass],"s/rt(b) calculation")
        leg.Draw("SAME")
      #pad.SetBottomMargin(0.18)
      #pad.SetBorderSize(0)
      #cans[sigmass].cd()
      #pad.Draw()
      outputFileName=outputName
      outputFiles[sigMass] = TFile("%s.root"%outputFileName, "RECREATE")
      outputFiles[sigMass].cd()
      cans[sigMass].Write()
      cans[sigMass].Print("%s.pdf"%outputFileName)
      outputFiles[sigMass].Close()



for var in ["WJetTau21","phPtOverMgammaj","WJetPtOverMgammaj"]:#"cosThetaStar",
  plotOpt(getPreselectionComboCut(),var)


'''
if(signal.GetSumOfWeights() != 0):
signal.Scale(dataHist.GetSumOfWeights()/signal.GetSumOfWeights())
else:
#signal.Scale(1000)
print("WARNING: Zero sum of weights")
signal.Draw()
	    dataHist.Draw("SAME")
	    leg = TLegend(0.7,0.7,0.9,0.9)
	    leg.AddEntry(signal,"signal")
	    leg.AddEntry(dataHist,"data")
	    leg.Draw("SAME")
	    cans[sigmass]s[sigMass].SetLogy()
	    
	    printName = 'signalOverlays/%s/signal_m%s_%s.png'%(cutVar,str(sigMass), cutVar)
	    cans[sigmass]s[sigMass].Print(printName,'png')

	    outputFiles[sigMass] = TFile("signalOverlays/%s/signal_m%s_%s.root"%(cutVar,str(sigMass), cutVar),"RECREATE")
	    outputFiles[sigMass].cd()
	    cans[sigmass]s[sigMass].Write()
	    outputFiles[sigMass].Close()
'''
