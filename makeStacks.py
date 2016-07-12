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
nonEmptyFilesDict = makeAllHists()
print nonEmptyFilesDict
for varkey in higgsRangesDict.keys():
  thisStack = THStack()
  for filekey in mcBgWeights.keys():
    filename = varkey+"_"+treekey+"_"+filekey
    if nonEmptyFilesDict["weightedMCbgHists/" + filename]=="nonempty":
      tfile = TFile(histsDir + filename)
      hist = tfile.Get("hist_%s" % filename)
      thisStack.Add(hist)
  outfileName = "stack_%s.root"%varkey
  outfile=TFile("outfileName", "RECREATE")
  outfile.cd()
  thisStack.Write()
  outfile.Close()

