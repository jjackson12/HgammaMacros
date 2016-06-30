import copy
from ROOT import *
from pyrootTools import *
from HgParameters import *
from HgCuts import getDefaultCuts, combineCuts

samplesDirs = getSamplesDirs()
dataFileName = samplesDirs["dataDir"]

cuts = getDefaultCuts()

btagCuts = copy.deepcopy(cuts)
btagCuts.pop("antibtag")
btagComboCut = combineCuts(btagCuts)
print btagComboCut

antibtagCuts = copy.deepcopy(cuts)
antibtagCuts.pop("btag")
antibtagComboCut = combineCuts(antibtagCuts)
print antibtagComboCut

notagCuts = copy.deepcopy(btagCuts)
notagCuts.pop("btag")
notagComboCut = combineCuts(notagCuts)
print notagComboCut

dataFile = TFile(dataFileName)
print "datafile %s:" % dataFileName,
print dataFile
higgsTree = dataFile.Get("higgs")
print "higgsTree: ",
print higgsTree
drawWithCutInNewCanvas(higgsTree, "phJetInvMass_pruned_higgs", notagComboCut,    "notag")
drawWithCutInNewCanvas(higgsTree, "phJetInvMass_pruned_higgs", antibtagComboCut, "antibtag")
drawWithCutInNewCanvas(higgsTree, "phJetInvMass_pruned_higgs", btagComboCut,     "btag")

