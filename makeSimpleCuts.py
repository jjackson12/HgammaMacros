from ROOT import *
from WgCuts import getPreselectionComboCut
import sys

inputFileName = sys.argv[1]
outputFileName = sys.argv[2]

cut = getPreselectionComboCut("Wgam",False)

inputFile = TFile(inputFileName)
tree = inputFile.Get("Wgam")


