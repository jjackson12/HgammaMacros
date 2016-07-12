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
thstacks=[]
cans=[]
for varkey in higgsRangesDict.keys():
#for varkey in [higgsRangesDict.keys()[0]]:
  cans.append(TCanvas())
  thstacks.append(THStack())
  for filekey in mcBgWeights.keys():
    filename = varkey+"_"+treekey+"_"+filekey
    if nonEmptyFilesDict["weightedMCbgHists/" + filename]=="nonempty":
      tfile = TFile(histsDir + filename)
      hist = tfile.Get("hist_%s" % filename)
      thstacks[-1].Add(hist)
  #outfileName = "stack_%s.root"%varkey
  #outfile=TFile("outfileName", "RECREATE")
  #outfile.cd()
  #thisStack.Write()
  #outfile.Close()
  cans[-1].cd()
  thstacks[-1].Draw()

