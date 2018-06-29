from WgParameters import getSamplesDirs
import os

first = True
for bkgOrSignal in ["bkg","sig"]:
  sourceDir = getSamplesDirs()["%sSmall3sDir"%bkgOrSignal]
  outDir = getSamplesDirs()["%sDDdir"%bkgOrSignal]
  for srcFileName in os.listdir(sourceDir):
    srcFile = sourceDir +"/"+ srcFileName
    outFile = outDir +"/selected_"+ srcFileName.replace("smallified_","")

    if not first:
      load = "-l"
    else:
      load = ""
    cmd = "python runWgammaSelector.py -i %s -o %s %s"%(srcFile, outFile, load) 

    print "running %s, saving to %s\n cmd = %s"%(srcFile, outFile, cmd)
    runReport = os.system(cmd)
    print "returned: \n%s"%runReport
    first = False



