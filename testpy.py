from ROOT import *
from pyrootTools import *
from getMCbgWeights import *
from WgParameters import *
from WgCuts import *
from os import path

# John Hakala, 12/1/2016
# A poorly-named collection of functions that churns out all the possible histograms from DDtrees

printCuts = False


def getWRangesDict(fineBinning=False):
  # TODO: Play around with ranges
  rangesDict = {}
  rangesDict["cosThetaStar"]                 = [[0., 1.]]
  rangesDict["phPtOverMgammaj"]              = [[0., 1.2]]
  rangesDict["WJetPtOverMgammaj"]              = [[0., 1.2]]
  rangesDict["leadingPhPhi"]                 = [[-3.5, 3.5]]
  rangesDict["phPt"]                  = [[0., 3000.]]
  rangesDict["leadingPhAbsEta"]              = [[0.,2.5]]
  rangesDict["leadingPhEta"]                 = [[-2.8,2.8]]
  rangesDict["weightFactor"]                 = [[0.0, 2.0]]
  label = "W"
  rangesDict["%sJet_puppi_abseta"%label]=[[0., 3]]
  rangesDict["%sJet_puppi_eta"%label]       = [[-3., 3.]]
  rangesDict["%sJet_puppi_phi"%label]       = [[-3.5, 3.5]]
  rangesDict["%sJet_puppi_pt"%label]        = [[0., 4000.]]
  rangesDict["%sJetTau21"%label]              = [[0.0, 1.0]]
  #rangesDict["%sPrunedJetCorrMass"%label]    = [[0.,200.], [0.,1000.]]
  #rangesDict["%sPuppi_softdropJetCorrMass"%label]=[[50.,150.]]
  rangesDict["%sPuppi_softdropJetCorrMass"%label]    = [[0.,1000.]]
  rangesDict["phJetDeltaR_%s"%label]         = [[0.,6.]]
  if fineBinning:
    rangesDict["phJetInvMass_puppi_softdrop_%s"%label]=[[700., 4700.]]
  else:
    rangesDict["phJetInvMass_puppi_softdrop_%s"%label]=[[0., 10000.]]
  return rangesDict

## this is for making stackplots from the ddTrees
#def getSidebandRangesDict(sideband):
#  rangesDict = {}
#  if sideband == "100110":
#    index="Four"
#  elif sideband == "5070":
#    index="Three"
#  else:
#    print "Invalid sideband! Either 100110 or 5070."
#    quit()
#  label="sideLow%s"%index
#  rangesDict["cosThetaStar"] = [0., 1.]
#  rangesDict["phPtOverMgammaj"]=[0., 2.]
#  rangesDict["leadingPhPhi"]=[-3.5, 3.5]
#  rangesDict["leadingPhPt"]=[0., 2000.]
#  rangesDict["leadingPhAbsEta"]=[0.,2.5]
#  rangesDict["leadingPhEta"]=[-2.8,2.8]
#  rangesDict["%sJet_HbbTag"%label]=[-1. , 1.]
#  rangesDict["%sJet_puppi_softdrop_abseta"%label]=[0., 3]
#  rangesDict["%sJett2t1"%label]=[0, 1]
#  rangesDict["%sPuppi_softdropJetCorrMass"%label]=[0, 4000]
#  rangesDict["phJetDeltaR_%s"%label]=[0,6]
#  rangesDict["phJetInvMass_puppi_softdrop_%s"%label]=[0,4000]
#  return rangesDict

def getRangesDict(fineBinning=False):
  WRangesDict = getWRangesDict(fineBinning)
  return WRangesDict

#def makeHist(tree, hist, var, key, region):
#  nEntries = tree.Draw("%s>> hist"%var, getAntiBtagComboCut(region))
#  if nEntries == 0:
#    return False
#  else:
#    outFile = TFile("weightedMCbgHists/%s_%s_%s"%(key, region, var), "RECREATE")
#    outFile.cd()
#    for histBin in range (0,hist.GetXaxis().GetNbins()):
#      hist.SetBinContent(histBin, hist.GetBinContent(histBin)*weightsDict[key])
#    hist.Draw()
#    hist.Write()
#    outFile.Close()
#    return True

def makeAllHists(cutName, sideband=False, useScaleFactors=False, windowEdges=[70,90], fineBinning=False, useReweighting=False):
  if fineBinning != useReweighting:
    print "there was something funny happening... fineBinning and useReweighting were different..."
    exit(1)
  sampleDirs = getSamplesDirs()
  weightsDict = getWeightsDict(sampleDirs["bkgSmall3sDir"])
  #regions = ["higgs", "side100110", "side5070"]
  regions = ["Wgam"]
  rangesDict = getRangesDict(fineBinning)
  nonEmptyFilesDict={}
  #for key in getWeightsDict(getSamplesDirs()["bkgSmall3sDir"]).keys():
  for key in getMCWeightsDict(getSamplesDirs()["bkgSmall3sDir"]).keys():
    sampleType = getWeightsDict(getSamplesDirs()["bkgSmall3sDir"])[key][1]
    useTrigger = True
    if sampleType == "sig":
      useTrigger = False
    #print "making all histograms for: %s" % key
    #print "useTrigger is %r since sampleType is %s" % (useTrigger, sampleType)
    for region in regions:
      pre = getDDPrefix()
      tfile = TFile(path.join(sampleDirs["%sDDdir" % sampleType], pre+key))
      print "tfile is: ", tfile.GetName(), tfile
      tree = tfile.Get(region)
      varNames = []
      for branch in tree.GetListOfBranches():
        if not "csvValues" in branch.GetName() and not "subjetCut" in branch.GetName() and not "triggerFired" in branch.GetName() and not "mcWeight" in branch.GetName():
          varNames.append(branch.GetName())
      print varNames
      for var in varNames:
        iRange = 1
        firstRange = True
        for rng in rangesDict[var]:
          #TODO: Doesn't this have to have "preselection" in it?
          histName = "hist_%s_%s_%s"%(var, region, key)
          if not firstRange:
            histName = histName.replace(".root","")+"_%i.root"%iRange
          if fineBinning == True:
            nBins = 4000
          else:
            nBins = 100
          hist = TH1F(histName,histName,nBins,rng[0],rng[1])
          #TODO: Select Cuts here, maybe preselection?
          if cutName in "nMinus1":
            cut = getNminus1ComboCut(region, var, withBtag, useTrigger, sideband, windowEdges)
          elif cutName in "preselection":
            cut = getPreselectionComboCut(region, useTrigger, sideband, [30.0, 99999.9])
          else:
            print "Invalid category: %s" % cutName
            print "Must be btag, antibtag, nMinus1, or preselection."
            exit(1)
          if useTrigger:
            cut += makeTrigger()
            
          if cutName is "preselection":
            nEntries = tree.Draw("%s>> hist_preselection_%s_%s_%s"%(var, var, region, key), cut)
            filename = "weightedMCbgHists_%s/%s_%s_%s"%("preselection", var, region, key)
          #elif not preselection:
          #histName = "hist_%s_%s_%s"%(var, region, key)
          if useScaleFactors:
            if cutName in ["antibtag", "btag"]:
              cutString = "%sSF*(%s)" % (cutName, cut)
              if useReweighting:
                cutString = "weightFactor*(%s)"%cutString
            else:
              cutString = "1*(%s)" % (cut)
          else: #TODO: What is this syntax?
            if cutName in "preselection":
              cutString = "1*(%s)" % cut
            else:
              cutString = "1*(%s)" % (cut)
          print "cuts:", cutString
          nEntries = tree.Draw("%s>> %s"%(var, histName), cutString, "HIST")
          directory = ""
          bareDirectory = ""
          if cutName in "nMinus1":
            if withBtag:
                directory = "weightedMCbgHists_%s_withBtag"%cutName
                bareDirectory = directory
            else:
                directory = "weightedMCbgHists_%s_noBtag"%cutName
                bareDirectory = directory
          else:
            if useScaleFactors:
              directory = "weightedMCbgHists_%s"%cutName
              bareDirectory = directory
            else:
              directory = "weightedMCbgHists_%s"%cutName
              bareDirectory = directory
          if sideband:
            if not cutName in "preselection":
              directory += "_sideband%i%i" % (windowEdges[0], windowEdges[1])
          if useScaleFactors:
            directory += "_SF"
            bareDirectory += "_SF"
          if fineBinning and useReweighting:
            directory += "_vgMC"
            bareDirectory += "_vgMC"
          filename = "%s/%s_%s_%s"%(directory, var, region, key)
          hackFilename = "%s/%s_%s_%s"%(bareDirectory, var, region, key)
          if not os.path.exists(directory):
            os.makedirs(directory)
          if not nEntries == 0:
            if firstRange:
              outFile = TFile(filename, "RECREATE")
            else:
              outFile = TFile(filename.replace(".root","")+"_%i.root"%iRange, "RECREATE")
            outFile.cd()
            #print "applying weight %s to sample %s" % (weightsDict[key][0], filename )
            #print " weightsDict has keys: " 
            #print weightsDict.keys()
            #Scale hist
            for histBin in range(0,hist.GetXaxis().GetNbins()):
              hist.SetBinContent(histBin, hist.GetBinContent(histBin)*weightsDict[key][0])  
            hist.Write()
            outFile.Close()
            #print "closed outFile" , outFile.GetName()
            nonEmptyFilesDict[filename]="nonempty"
            nonEmptyFilesDict[hackFilename]="nonempty"
          else:
            nonEmptyFilesDict[filename]="empty"
            nonEmptyFilesDict[hackFilename]="empty"
            #print "the histogram %s was empty for" % histName, filename
          iRange += 1
          firstRange = False;
  return nonEmptyFilesDict
