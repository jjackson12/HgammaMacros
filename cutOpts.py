from ROOT import *
from WgCuts import *
from WgParameters import *
from testpy import getWRangesDict
import sys 
from getMCbgWeights import *
import re
import os
from numpy import linspace,sqrt






#####Hardcoded params#####
runOn = "Preselected"#OR DD
manOrAutoCut = "man"#ual
analyzeCutRates = True
nBins = 100
varDict = getVariableDict()
histRanges = getWRangesDict()
sampleDirs = getSamplesDirs()
sampleDirs["bkgPreselecteddir"] = "preSelectedBkg"
sampleDirs["sigPreselecteddir"] = "preSelectedSignal"
sampleDirs["dataPreselectedFile"] = "preSelected_singlePhoton2016.root"
sampleDirs["dataPreselecteddir"] = "."
bkgDir =  sampleDirs["bkg%sdir"%runOn]
signalDir = sampleDirs["sig%sdir"%runOn]
dataDir = sampleDirs["data%sdir"%runOn]
dataFileName = sampleDirs["data%sFile"%runOn]
signalMasses = [600,800,1000,2000,3500]
cuts = {}
cuts["leadingPhAbsEta"]=1.4442
cuts["WJetTau21"] = 0.6
cuts["phPtOverMgammaj"] = 0.47
varKeys = getVarKeys()
weightDict = getWeightsDict(sampleDirs["bkgSmall3sDir"])
##########################






def getSoverRootB(bkg, sig, start, stop):
  bb=0.
  ss=0.
  for iBin in range(bkg.FindBin(start), bkg.FindBin(stop)):
      bb+=bkg.GetBinContent(iBin)
      #print("bb += %s"%bkg.GetBinContent(iBin))
      ss+=sig.GetBinContent(iBin)
      #print("ss += %s"%sig.GetBinContent(iBin))
  if bb != 0:
    return ss/sqrt(bb)
  else:
    return "b=0"

def analyzeCutRate(sig, start, stop, tag):
  initEvents = sig.GetSumOfWeights()
  ss=0.
  for iBin in range(sig.FindBin(start), sig.FindBin(stop)):
      ss+=sig.GetBinContent(iBin)
  if ss != 0:
    print "for %s %s, cutting from %s to %s removes %s percent of signal" % (tag, sig.GetName(), start, stop, 100*(1 - ss/initEvents))





def plotOpt(withTrigger,sideband,cutVar):
    


    print("\noptimizing on %s, sideband is %s"%(cutVar,sideband))
    #getBackgroundHist(cutVar, baseCut)
    prefixMap = {}
    prefixMap["Preselected"] = "preSelected_smallified"
    prefixMap["DD"] = "selected"
    prefixMap["Small3s"] = "smallified"

    treeMap = {}
    treeMap["Preselected"] = "Wgam"
    treeMap["DD"] = "Wgam"
    treeMap["smallified"] = "ntuplizer/tree"

    leg = TLegend(0.78,0.5,0.98,0.765)
    if sideband:
      print "running on sideband 50-70"
      dataCut = getPreselectionComboCut(withTrigger,sideband,[50,70])
      print("dataCut = %s"%dataCut)

      # Import dataHistogram
      #dataFileName = "preSelected_singlePhoton2016.root"
      dataFile = TFile(dataFileName)
      dataTree = dataFile.Get(treeMap[runOn])
      histLabel = "dataSideband"
          
      dataSideband=TH1F(histLabel, "" , nBins, histRanges[cutVar][0][0], histRanges[cutVar][0][1])
      dataTree.Draw('%s>>%s' % (cutVar, histLabel),dataCut)
      dataSideband.SetLineColor(kBlack)
      leg.AddEntry(dataSideband,"sideband (50-70 GeV)")

      bkgScale = dataSideband.GetSumOfWeights()
      print("sideband has %s events"%bkgScale)
      fullBkgHist = dataSideband
    else:
      ####HACKACK
      #Import fullBkgHist 
      fullBkgHistStack = THStack()

      bkgFileDict = {}
      fullBkgHists = {}
      iterTrees = {}
      iQCD = 0
      igJets = 0
      iOther = 0 
      bkgCatColors = {}
      bkgCatColors["QCD"] = kBlack
      bkgCatColors["Jet + gamma"] = kGray
      bkgCatColors["Others"] = kGray + 2
      histLabel = "MC_Bkgs"
      bkgCatHists = {}
      bkgCatHists["QCD"] = TH1F("qcd%s"%cutVar,"qcd%s"%cutVar, nBins, histRanges[cutVar][0][0], histRanges[cutVar][0][1])
      bkgCatHists["Others"] = TH1F("others%s"%cutVar,"others%s"%cutVar, nBins, histRanges[cutVar][0][0], histRanges[cutVar][0][1])
      bkgCatHists["Jet + gamma"] = TH1F("gJets%s"%cutVar,"gJets%s"%cutVar, nBins, histRanges[cutVar][0][0], histRanges[cutVar][0][1])


      histList = {}
      histList["QCD"]=TList()
      histList["Jet + gamma"]=TList()
      histList["Others"]=TList()
      for bkgFile in os.listdir(bkgDir):
          print("processing background: %s\n" % bkgFile)
  
          bkgEdges = [70,90]
          bkgCut = getPreselectionComboCut(withTrigger,False,bkgEdges)
          #print(bkgCut)
          bkg = re.search(r'(.*)%s_(.*).root'%prefixMap[runOn],bkgFile).groups()[1]
          bkgFileDict[bkg] = TFile("%s/%s" % (bkgDir, bkgFile))
          #print "%s/%s"%(bkgDir,bkgFile), bkgFileDict[bkg]
          histLabel = "MCbkgHistogram"
          fullBkgHists[bkg]=TH1F(histLabel,"", nBins, histRanges[cutVar][0][0], histRanges[cutVar][0][1])
  
  
          iterTrees[bkg] = bkgFileDict[bkg].Get(treeMap[runOn])
          #print iterTrees[bkg]
          iterTrees[bkg].Draw('%s>>%s' % (cutVar, histLabel),bkgCut)
          weight = weightDict["%s.root"%bkg]
          fullBkgHists[bkg].Scale(weight[0])
          #fullBkgHists[bkg].Scale(weight)
          fullBkgHists[bkg].Sumw2()
  
  
          if "qcd" in bkg:
              histList["QCD"].Add(fullBkgHists[bkg])
              #color = kSpring + iQCD
              #iQCD+=1
          elif "gJets" in bkg:
              histList["Jet + gamma"].Add(fullBkgHists[bkg])
              #color = kPink + igJets
              #igJets+=1
          else:
              histList["Others"].Add(fullBkgHists[bkg])
              #color = kAzure + iOther
              #iOther+=1



      for bkgCat in ["QCD","Jet + gamma","Others"]:
        bkgCatHists[bkgCat].Merge(histList[bkgCat])
        bkgCatHists[bkgCat].SetLineColor(bkgCatColors[bkgCat])
        bkgCatHists[bkgCat].SetFillColor(bkgCatColors[bkgCat])
        fullBkgHistStack.Add(bkgCatHists[bkgCat])
        leg.AddEntry(bkgCatHists[bkgCat],bkgCat)
      fullBkgHist = fullBkgHistStack.GetStack().Last().Clone()
    ####HACKHACK
    #End Import fullBkgHist

    outputFiles = {}
    cans = {}


#    #TEST-TEMPORARY
#
#    outputFileName="backgroundHistStackOnly_%s"%cutVar
#    cans[outputFileName] = TCanvas(outputFileName,outputFileName)
#    cans[outputFileName].cd()
#    fullBkgHistStack.Draw()
#
#    outputFiles[outputFileName] = TFile("%s.root"%outputFileName, "RECREATE")
#    outputFiles[outputFileName].cd()
#    cans[outputFileName].Write()
#    cans[outputFileName].Print("%s.pdf"%outputFileName)
#    outputFiles[outputFileName].Close()
#
#    #TEST-TEMPORARY

    #bkgScale = fullBkgHist.GetSumOfWeights()
    
    varRange = histRanges[cutVar]
    upperBound = varRange[0][1]
    lowerBound = varRange[0][0]
    nSplits = fullBkgHist.GetNbinsX()
    #nSplits = nSteps

    varRangeList = linspace(lowerBound,upperBound,nSplits)


    sigFiles = {}
    sigTrees = {}
    sigHists = {}

    sRtBMaps = {} 

    idealCutsMap = {}

 
    for sigMass in signalMasses:
      print("\nplotting signal mass %s\n"%sigMass)
      
      # HACK HACK
      # Import sigHists[sigMass]
      name = "m" + str(sigMass)
      sigFileName = "%s/preSelected_smallified_flatTuple_WGammaSig_%s.root" % ("preSelectedSignal", name)
      sigFiles[sigMass] = TFile(sigFileName)
      sigTrees[sigMass] = sigFiles[sigMass].Get("Wgam")
      histLabel = "%s_%s" % (name, cutVar)
      sigCut = getPreselectionComboCut(False,sideband,[50,70])

      sigHists[sigMass]=TH1F(histLabel, histLabel, nBins, histRanges[cutVar][0][0], histRanges[cutVar][0][1])
      sigTrees[sigMass].Draw('%s>>%s' % (cutVar, histLabel), sigCut)
      #sigHists[sigMass].Scale(bkgScale/sigHists[sigMass].GetSumOfWeights())
      print("sig %s has %s events" % (name,sigHists[sigMass].GetSumOfWeights()))


     # #TEST-TEMPORARY

     # outputFileName="signalOnly_%s_%s"%(name,cutVar)
     # cans[outputFileName] = TCanvas(outputFileName,outputFileName)
     # cans[outputFileName].cd()
     # sigHists[sigMass].Draw()

     # outputFiles[outputFileName] = TFile("%s.root"%outputFileName, "RECREATE")
     # outputFiles[outputFileName].cd()
     # cans[outputFileName].Write()
     # cans[outputFileName].Print("%s.pdf"%outputFileName)
     # outputFiles[outputFileName].Close()

     # #TEST-TEMPORARY

     # #TEST-TEMPORARY

     # outputFileName="signalOverlay_%s_%s"%(name,cutVar)
     # cans[outputFileName] = TCanvas(outputFileName,outputFileName)
     # cans[outputFileName].cd()
     # fullBkgHistStack.Draw()
     # sigHists[sigMass].Draw("SAME")
     # leg = TLegend(0.7,0.7,0.9,0.9)
     # leg.AddEntry(sigHists[sigMass],"signal")
     # leg.AddEntry(fullBkgHistStack,"background (MC)")
     # leg.Draw("SAME")

     # outputFiles[outputFileName] = TFile("%s.root"%outputFileName, "RECREATE")
     # outputFiles[outputFileName].cd()
     # cans[outputFileName].Write()
     # cans[outputFileName].Print("%s.pdf"%outputFileName)
     # outputFiles[outputFileName].Close()

     # #TEST-TEMPORARY






    #  bkgScale = 0
    #  sigScale = 0
    #  for bkgBin in range (1, fullBkgHist.GetXaxis().GetNbins()+1):
    #    bkgScale+=fullBkgHist.GetBinContent(bkgBin) 
    #    sigScale+=sigHists[sigMass].GetBinContent(bkgBin)
    #  sigScaleFactor = 1/sigScale
    #  bkgScaleFactor = 1/bkgScale
    #  scaleFactor = bkgScale/sigScale

     # for sigBin in range (1, sigHists[sigMass].GetXaxis().GetNbins()+1):
     #   #sigHists[sigMass].SetBinContent(sigBin, sigHists[sigMass].GetBinContent(sigBin)*sigScaleFactor) 
     #   #fullBkgHist.SetBinContent(sigBin, fullBkgHist.GetBinContent(sigBin)*bkgScaleFactor) 
     #   sigHists[sigMass].SetBinContent(sigBin, sigHists[sigMass].GetBinContent(sigBin)*scaleFactor) 



      #sigHists[sigMass].Scale(scaleFactor)





      # Hack Hack
      # Import sigHists[sigMass]

      if not (sigHists[sigMass].GetNbinsX() == fullBkgHist.GetNbinsX()):# and (sigHists[sigMass].GetSumOfWeights() - fullBkgHist.GetSumOfWeights()) < (0.05*fullBkgHist.GetSumOfWeights())):
        print "bkg sum = %s\nsig sum = %s"%(fullBkgHist.GetSumOfWeights(), sigHists[sigMass].GetSumOfWeights())
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
            

            sRtB = getSoverRootB(fullBkgHist,sigHists[sigMass], cutRange[0], cutRange[1])

            if(isinstance(sRtB,str)):
              continue
            #print("in range %s, s/rt(b) = %s"%(cutRange,sRtB))
            sRtBcuts[cutRange] = sRtB
            if(sRtB > optimalCut[1]):
              optimalCut = (cutRange, sRtB)
            lowBoundList.append(cutRange[0])
            sRtBList.append(sRtB)
            highBoundList.append(cutRange[1])
 
      sRtBNBins = len(sRtBList)
      sRtBMaps[sigMass] = TGraph(len(sRtBList))
      sRtBMaps[sigMass].GetXaxis().SetLimits(lowerBound,upperBound)
      if directionWord in "both":
        sRtBMaps[sigMass] = TGraph2D(len(sRtBList))
        for i in range(len(sRtBList)):
          sRtBMaps[sigMass].SetPoint(i,lowBoundList.pop(0),highBoundList.pop(0),sRtBList.pop(0))
      if directionWord in "up":
        for  i in range(len(sRtBList)):
          x = lowBoundList.pop(0)
          y = sRtBList.pop(0)
          sRtBMaps[sigMass].SetPoint(i,x,y)
      
      if directionWord in "down":
        for  i in range(len(sRtBList)):
          x = highBoundList.pop(0)
          y = sRtBList.pop(0)
          sRtBMaps[sigMass].SetPoint(i,x,y)
      sRtBMapTitle = "s/rt(b) optimal cut limit(cumulative)"
      sRtBMaps[sigMass].SetTitle(sRtBMapTitle)
      sRtBMaps[sigMass].GetYaxis().SetTitle("sig/sqrt(bkg) events")
      #sRtBMaps[sigMass].SetName(sRtBMapTitle)
      idealCutsMap[sigMass] = optimalCut
      print "############################\noptimal cut range for %s in mass range %s looks to be %s, with s/rt(b) = %s\n#############################\n"%(cutVar,sigMass,optimalCut[0],optimalCut[1])

    #TODO: Get rid of "both" variables
    outputFileName = "sRtBMap_%s"%cutVar

      #sRtBMaps[sigMass] = TGraph(len(sRtBList),highBoundList,sRtBList)
    cans[outputFileName] = TCanvas(outputFileName,outputFileName,800,1100)
    pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
    #		pad1.SetBottomMargin(0) 
    #pad1.SetGridx() 
    pad1.SetLogy()
    pad1.cd() 
    #fullBkgHistStack.SetStats(0)        

    #HACKHACK Just to set axis titles
    tempHist = fullBkgHist.Clone("tempHist")
    tempHist.SetLineColor(kWhite) 
    tempHist.SetFillColor(kWhite)
    tempHist.GetYaxis().SetTitle("Events")
    tempHist.GetXaxis().SetTitle(varDict[cutVar])
    tempHist.SetTitle(varDict[cutVar]) 
    tempHist.SetName(varDict[cutVar]) 
    tempHist.Draw()
    



    if cutVar in cuts.keys():
      if "man" in manOrAutoCut:
        finalCut = cuts[cutVar]
      elif "auto" in manOrAutoCut: 
        finalCut = sum(idealCutsMap.values())/len(idealCutsMap.values())
      cutLine = TLine(finalCut,0,finalCut,1.4*fullBkgHist.GetMaximum())
      cutLine.SetLineColor(6)
      cutLine.SetLineWidth(5)
      cutLine.SetLineStyle(8)
      leg.AddEntry(cutLine,"proposed Cut")



    sbTag = ""
    if sideband:

      fullBkgHist.Draw("SAME")
      sbTag = "against sideband (50-70)"
      leg.AddEntry(fullBkgHist,"sideband (50-70)")
      #if "Eta" in cutVar:
        #fullBkgHist.Scale(0.5)
        #fullBkgHist.SetMinimum(0)
    else:
      #fullBkgHist.Draw()
      fullBkgHistStack.Draw("hist SAME")
      sbTag = "against MC"
 
    colors=[kBlue,kRed,kOrange,kGreen,kAzure+10]
    for sigMass in signalMasses:
      #for hist in fullBkgHistStack.GetStack():
      #  hist.GetXaxis().SetLimits(lowerBound, upperBound)
      #  //hist.Scale(graphScale/bkgScale)
      #  hist.GetYaxis().SetLimits(0,1.7)
      #sigHists[sigMass].Scale(graphScale/sigScale)
      sigHists[sigMass].GetYaxis().SetTitle("Events")
      sigHists[sigMass].GetXaxis().SetTitle(varDict[cutVar])
      sigHists[sigMass].SetLineColor(colors.pop())
      sigHists[sigMass].SetLineStyle(9)
      sigHists[sigMass].SetLineWidth(3)
      if "Eta" in cutVar:
        sigHists[sigMass].Scale(20)
      sigHists[sigMass].Draw("SAME")
      leg.AddEntry(sigHists[sigMass],"Wgamma %s"%sigMass)


    if cutVar in cuts.keys():
      cutLine.Draw("SAME")
    leg.Draw("SAME")

    #dataHistogram.SetTitle("data vs MC Background")
    #dataHistogram.GetYaxis().SetLabelSize(0.)
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.39) 
    #		pad2.SetTopMargin(0) 
    #pad2.SetBottomMargin(0.2) 
    #pad2.SetGridx()  # vertical grid
    #		pad2.Draw() 
    pad2.cd()        # pad2 becomes the current pad

    pad2Max = 9
    #pad2Max = max(map(lambda x: x.GetMaximum(),sRtBMaps.values()))

    dummyHist = TH1F(sRtBMapTitle,sRtBMapTitle,sRtBNBins,lowerBound,upperBound)
    dummyHist.GetYaxis().SetTitle("sig/sqrt(bkg) events")
    dummyHist.SetMaximum(pad2Max)
    dummyHist.Draw()

    colors=[kBlue,kRed,kOrange,kGreen,kAzure+10]
    First = True
    for sigMass in reversed(signalMasses):
      if analyzeCutRates and cutVar in cuts.keys():
        if "up" in direction:
          analyzeCutRate(sigHists[sigMass],finalCut,upperBound,"signal")
          analyzeCutRate(fullBkgHist,finalCut,upperBound,"background")
        elif "down" in direction:
          analyzeCutRate(sigHists[sigMass], lowerBound, finalCut,"signal")
          analyzeCutRate(fullBkgHist,finalCut,upperBound,"background")

      sRtBMaps[sigMass].SetLineColor(colors.pop())
      #if First:
      #  sRtBMaps[sigMass].Draw()
      #else:
      #  sRtBMaps[sigMass].Draw("SAME")
      sRtBMaps[sigMass].Draw("SAME")
      First = False
    
    if cutVar in cuts.keys():
      cutLine2 = TLine(finalCut,0,finalCut,pad2Max)
      cutLine2.SetLineColor(6)
      cutLine2.SetLineWidth(5)
      cutLine2.SetLineStyle(8)
      cutLine2.Draw("SAME")

  
 
    cans[outputFileName].cd()
    pad1.Draw()
    pad2.Draw()

    outputDir = "sRtBMaps"
    if sideband:
      outputDir += "Sideband"
    if withTrigger:
      outputDir += "WithTrigger" 


    if(not(os.path.isdir(outputDir))):
      os.makedirs(outputDir)  


    outputFiles[outputFileName] = TFile("%s/%s.root"%(outputDir,outputFileName), "RECREATE")
    outputFiles[outputFileName].cd()
    cans[outputFileName].Write()
    cans[outputFileName].Print("%s/%s.png"%(outputDir,outputFileName))
    outputFiles[outputFileName].Close()
    return idealCutsMap

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-s","--sideband",action="store_true", dest="sbOpt",default=False,
                  help="use this to select sideband"  )
parser.add_option("-t","--trigger",action="store_true", dest="trigOpt",default=False,
                  help="use this to select sideband range"  )
(options, args) = parser.parse_args()

if(options.trigOpt): print "doing triggers"
if(options.sbOpt): print "using sideband"


idealMaps = {}
#TODO: Fix eta problem
for var in ["leadingPhAbsEta", "WJetTau21","phPtOverMgammaj","cosThetaStar"]:
  idealMaps[var] = plotOpt(options.trigOpt,options.sbOpt,var)

print "\n\n######################################\nIdeal Cuts\n#####################################\n"
for key in idealMaps.keys():
  print "\nideals for %s"%key
  for keyMass in idealMaps[key].keys():
    print "sigMass: %s   |   range: %s   |   sRtB: %s"%(keyMass,idealMaps[key][keyMass][0],idealMaps[key][keyMass][1])
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
