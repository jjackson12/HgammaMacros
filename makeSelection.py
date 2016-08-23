import copy
from ROOT import *
from pyrootTools import *
from HgParameters import *
from HgCuts import getDefaultCuts, combineCuts

# macro for plotting post-selection for H(bb)gamma
# John Hakala 7/13/16

samplesDirs = getSamplesDirs()
#dataFileName = samplesDirs["dataDir"]
sampleFileName="testSilver.root" 

cuts = getDefaultCuts("higgs")

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

sampleFile = TFile(sampleFileName)
print "sampleFileName %s:" % sampleFileName,
print sampleFile
higgsTree = sampleFile.Get("higgs")
print "higgsTree: ",
print higgsTree
drawWithCutInNewCanvas(higgsTree, "phJetInvMass_pruned_higgs", notagComboCut,    "notag")
drawWithCutInNewCanvas(higgsTree, "phJetInvMass_pruned_higgs", antibtagComboCut, "antibtag")
drawWithCutInNewCanvas(higgsTree, "phJetInvMass_pruned_higgs", btagComboCut,     "btag")

