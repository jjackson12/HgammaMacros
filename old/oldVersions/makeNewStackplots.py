from ROOT import *
from pyrootTools import * 
from getMCbgWeights import *
from HgParameters import *
from HgCuts import *
  
sampleDirs = getSamplesDirs()
weightsDict = getWeightsDict(sampleDirs["small3sDir"])
pre = getFilePrefix()



for key in weightsDict.keys():
  sampleName = key
  fullFileName = sampleDirs["ddDir"]+pre+sampleName
  tfile = TFile(fullFileName)
  tree = tfile.Get("higgs") 

  nEntries = tree.Draw("phJetInvMass_pruned_higgs")#, getAntiBtagComboCut())
  if nEntries != 0:
    hist = TH1F(key, key, 3250, 0, 13000)
    tree.Draw("phJetInvMass_pruned_higgs>> hist%s"%sampleName)#, getAntiBtagComboCut())
    outFile = TFile("st_%s"%key, "RECREATE")
    outFile.cd()
    hist.Write()
    outFile.Close()
  
    
    

