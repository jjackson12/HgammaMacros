from ROOT import *
from pyrootTools import instance

sigWindowTreeName = "higgs"  # just keep the name from TTree::MakeClass(), don't give it a special name

dataFileName = "may5_tagging/small3_SilverJson_may5.root"
dataFile = TFile(dataFileName)
sigWindowTree = dataFile.Get(sigWindowTreeName)

instance(sigWindowTreeName, [dataFileName, "test.root", "compile"])

sigWindowData = higgs(sigWindowTree)
nSignalWindowEventsInData = sigWindowData.Loop()
"Number of signal window events in data is: %i" % nSignalWindowEventsInData


