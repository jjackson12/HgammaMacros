from os import path, makedirs
from ROOT import *
from pyrootTools import getSortedDictKeys, drawInNewCanvas
from testpy import getRangesDict, getHiggsRangesDict, getSidebandRangesDict, makeAllHists
from HgParameters import getSamplesDirs
from getMCbgWeights import getWeightsDict, getMCbgWeightsDict, getMCbgColors, getMCbgOrderedList, getMCbgLabels
from tcanvasTDR import TDRify

# new script to make all stackplots.
# John Hakala 7/14/16

printNonempties = False
printFileNames  = False

sampleDirs = getSamplesDirs()

rangesDict = getRangesDict()
print ""
print "getRangesDict:"
print rangesDict

higgsRangesDict = getHiggsRangesDict()
print ""
print "getHiggsRangesDict:"
print higgsRangesDict

#for sideband in ['100110','5070']:
#  SidebandRangesDict = getSidebandRangesDict(sideband)
#  print ""
#  print "getSidebandRangesDict('%s')" % sideband
#  print SidebandRangesDict


print ""
print ""
print "getMCbgWeights(): "
mcBgWeights = getMCbgWeightsDict(sampleDirs["small3sDir"])
print mcBgWeights
treekey="higgs"
#for cutName in ["btag", "antibtag", "nobtag", "preselection"]:
for cutName in ["preselection"]:
  histsDir = "~/WZgammaMacros/weightedMCbgHists_%s/"%cutName
  nonEmptyFilesDict = makeAllHists(cutName)
  print "done making all histograms."
  thstacks=[]
  cans=[]
  hists=[]
  tfiles=[]
  datahists=[]
  datafiles=[]
  legendLabels = getMCbgLabels()

  #for varkey in [higgsRangesDict.keys()[0]]:
  for varkey in higgsRangesDict.keys():
    cans.append(TCanvas())
    thstacks.append(THStack())
    integralsDict={}
    namesDict={}
    for filekey in mcBgWeights.keys():
      filename = varkey+"_"+treekey+"_"+filekey
      if printNonempties:
        print "The nonempty files dict is:"
        print nonEmptyFilesDict
      thisFileName = "weightedMCbgHists_%s/%s" % (cutName, filename)
      if nonEmptyFilesDict[thisFileName] == "nonempty":
        if printFileNames:
          print thisFileName
        tfiles.append(TFile(histsDir + filename))
        hists.append(tfiles[-1].Get("hist_%s" % filename))
        hists[-1].SetFillColor(getMCbgColors()[filekey])
        drawInNewCanvas(hists[-1])
        integralsDict[hists[-1].Integral()] = hists[-1] 
        namesDict[hists[-1].GetName()] = hists[-1]
    for mcBG in getMCbgOrderedList():
      for key in namesDict:
        if mcBG in key:
          #print "adding %s to stackplot; it has integral %f" % (integralsDict[key], key)
          thstacks[-1].Add(namesDict[key])
    dataFileName = varkey+"_"+treekey+"_SilverJson.root"
    datafiles.append(TFile("weightedMCbgHists_%s/%s"%(cutName, dataFileName)))
    datahists.append(datafiles[-1].Get("hist_%s"%dataFileName))

    outDirName = "stackplots_%s" % cutName
    if not path.exists(outDirName):
      makedirs(outDirName)
    outfileName = "%s/%s_stack_%s.root"%(outDirName, cutName, varkey)
    outfile=TFile(outfileName, "RECREATE")
    outfile.cd()
    #thisStack.Write()
    cans[-1].cd()
    thstacks[-1].Draw()
    datahists[-1].SetMarkerStyle(20)
    datahists[-1].Draw("APE SAME")

    cans[-1].SetLogy()
    cans[-1].BuildLegend()
    for prim in cans[-1].GetListOfPrimitives():
      if "TLegend" in prim.IsA().GetName():
        for subprim in prim.GetListOfPrimitives():
          for key in legendLabels:
            if key in subprim.GetLabel():
              subprim.SetLabel(legendLabels[key])
            elif "SilverJson" in subprim.GetLabel():
              subprim.SetLabel("data")
    TDRify(cans[-1])
    cans[-1].Write()
    outfile.Close()
  print""
  print "thstacks:"
  print thstacks
  print""
  print "cans"
  print cans
