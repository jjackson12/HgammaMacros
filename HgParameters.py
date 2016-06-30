# functions to centrally store Hgamma parameters
# John Hakala -  May 16, 2016
from ROOT import *

def getSamplesDirs():
  response = {}
  response["HgammaFlatTuples"] = "~/physics/nTuplizerStep/Hgamma_flatTuples"
  response["small3sDir"]       = "~/physics/nTuplizerStep/small3s"
  response["ddDir"]            = "~/physics/treeCheckerStep/newDDs_June29/"
  response["dataDir"]          = "~/physics/treeCheckerStep/newDDs_June29/ddTree_june29_small3_SilverJson.root"
  return response

def getNormalizations():
  normalizations = {}
  normalizations["750"]  = 1.0
  normalizations["1000"] = 0.8
  normalizations["2000"] = 0.1
  normalizations["3000"] = 0.1  
  return normalizations

def getMassWindows():
  massWindows = {}
  massWindows[750]  = [700,   800]
  massWindows[1000] = [900,  1100]
  massWindows[2000] = [1850, 2150]
  massWindows[3000] = [2200, 4000]
  return massWindows

def getSigNevents():
  sigNevents = {}
  for mass in getNormalizations().keys():
    flattuple = TFile("%s/flatTuple_Hgamma_m%s.root"%(getSamplesDirs()["HgammaFlatTuples"], mass))
    hCounter = flattuple.Get("ntuplizer/hCounter")
    sigNevents[mass] = hCounter.GetEntries()
  return sigNevents


