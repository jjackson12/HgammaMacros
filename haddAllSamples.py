from glob import glob
from pprint import pprint

def parseConfigs(show = False):
  configFiles =  glob("../VgammaTuplizer/Ntuplizer/crabconfigs/*.ini")
  configsDict={}

  from ConfigParser import RawConfigParser
  parsers = []
  for configFile in configFiles:
    parsers.append(RawConfigParser())
    parsers[-1].optionxform = str
    parsers[-1].read(configFile)
    values = dict(parsers[-1].items('ShortNames')).values()
    configsDict[configFile] = values
  if show:
    pprint(configsDict)
  return configsDict

def findAllMatches(show=False):
  datasetsDict = parseConfigs()
  for key in datasetsDict:
    if "ext" in key:
      del datasetsDict[key]
  matchingFiles = {}
  for datasetsArray in datasetsDict.values():
    for dataset in datasetsArray:
      if not "ext" in dataset:
        if "qcd" in dataset: ## fixme
          dataset = dataset.replace("qcdHT", "qcd")
        matchingFiles[dataset] = glob("../HgammaCondor/smallified_%s*.root" % dataset)
  if show:
    pprint(matchingFiles)
  return matchingFiles
  
def haddTogetherAllDatasets(outDir, show = False): 
  from commands import getoutput
  filesDict = findAllMatches()
  for dataset in filesDict:
    if filesDict[dataset]:
      incantation = "hadd %s/smallified_%s.root %s" % (outDir, dataset, " ".join(filesDict[dataset]))
      if show:
        print incantation
      pprint(getoutput(incantation))
    

if __name__ == "__main__":
  haddTogetherAllDatasets("smallifications_May1", True)
