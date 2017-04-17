import copy
from ROOT import *
from pyrootTools import *
from HgParameters import *
from HgCuts import getDefaultCuts, combineCuts

# macro for plotting post-selection for H(bb)gamma
# John Hakala 7/13/16

samplesDirs = getSamplesDirs()
#dataFileName = samplesDirs["dataDir"]
mass = "1000"
print "using samples directory: %s" % samplesDirs
sampleFileName="%s/ddTree_Hgamma_data27fb-1.root" % (samplesDirs["ddDir"])
#sampleFileName="testSilver.root"

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
print "\nall cuts, btag cat\n   "
print higgsTree.Draw("phJetInvMass_pruned_higgs", btagComboCut)
#print "\nall cuts, antibtag cat\n   "
#print higgsTree.Draw("phJetInvMass_pruned_higgs", antibtagComboCut)
#print "\nno btag cut\n   "
#print higgsTree.Draw("phJetInvMass_pruned_higgs", notagComboCut)

notagCuts.pop("ptOverM")
notagComboCut = combineCuts(notagCuts)
#print "\nno pT/M cut\n   "
#print higgsTree.Draw("phJetInvMass_pruned_higgs", notagComboCut)
#
#
#notagCuts.pop("phEta")
#notagComboCut = combineCuts(notagCuts)
#print "\nno phEta cut\n   "
#print higgsTree.Draw("phJetInvMass_pruned_higgs", notagComboCut)
#
#
#notagCuts.pop("jetEta")
#notagComboCut = combineCuts(notagCuts)
#print "\nno jetEta cut\n   "
#print higgsTree.Draw("phJetInvMass_pruned_higgs", notagComboCut)
#
#notagCuts.pop("deltaR")
#notagComboCut = combineCuts(notagCuts)
#print "\nno deltaR cut\n   "
#print higgsTree.Draw("phJetInvMass_pruned_higgs", notagComboCut)
#
#notagCuts.pop("turnon")
#notagComboCut = combineCuts(notagCuts)
#print "\nno turnon cut\n   "
#print higgsTree.Draw("phJetInvMass_pruned_higgs", notagComboCut)
#
#
#
#
#print notagComboCut
#
