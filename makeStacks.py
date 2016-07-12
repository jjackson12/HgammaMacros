from ROOT import *
from testpy import getRangesDict, getHiggsRangesDict, getSidebandRangesDict, makeAllHists
from HgParameters import getSamplesDirs
from getMCbgWeights import getWeightsDict

histsDir = "~/WZgammaMacros/weightedMCbgHists/"
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
mcBgWeights = getWeightsDict(sampleDirs["small3sDir"])
print mcBgWeights
treekey="higgs"
for cutName in ["btag", "antibtag", "nobtag"]:
  nonEmptyFilesDict = makeAllHists(cutName)
  print nonEmptyFilesDict
  thstacks=[]
  cans=[]
  hists=[]
  tfiles=[]
  for varkey in higgsRangesDict.keys():
  #for varkey in [higgsRangesDict.keys()[0]]:
    cans.append(TCanvas())
    thstacks.append(THStack())
    for filekey in mcBgWeights.keys():
      filename = varkey+"_"+treekey+"_"+filekey
      if nonEmptyFilesDict["weightedMCbgHists_%s/%s" % (cutName, filename)] == "nonempty":
        tfiles.append(TFile(histsDir + filename))
        hists.append(tfiles[-1].Get("hist_%s" % filename))
        thstacks[-1].Add(hists[-1])
    outfileName = "testcans/%s_stack_%s.root"%(cutName, varkey)
    outfile=TFile(outfileName, "RECREATE")
    outfile.cd()
    #thisStack.Write()
    cans[-1].cd()
    thstacks[-1].Draw()
    cans[-1].Write()
    outfile.Close()
  print""
  print "thstacks:"
  print thstacks
  print""
  print "cans"
  print cans
