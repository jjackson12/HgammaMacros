#from os import listdir
from os.path import isfile, join, exists, basename
from sys import argv
from optparse import OptionParser
from glob import glob
from natsort import natsorted


parser = OptionParser()
parser.add_option("-i", "--inDir", dest="inDir",
                  help = "the input directory")
parser.add_option("-o", "--outFile", dest="outFile", default="sigsPlot.pdf",
                  help = "the filename for the output plot")
parser.add_option("-n", "--plotEvery", dest="plotEvery", default=1,
                  help = "this will scale down the number of masses drawn by the factor given")
parser.add_option("-f", "--form", dest="form", default="tuple",
                  help = "the format of the input histos: either 'workspace' from the DisplaySignalFits macro, or 'tuple' from the readHgamma macro")
parser.add_option("-k", "--kind", dest="kind", default="interpolated",
                  help = "the kind of signals in inDir: either 'interpolated' or 'fullsim'")
parser.add_option("-c", "--category", dest="category", default="antibtag",
                  help = "if there are btag as well as antibtag signals in your inDir, select the category")

(options, args) = parser.parse_args()

if options.inDir is None:
  print "please pick an input directory with the -i option"
  exit(1)

argv=[]

from ROOT import * 
gROOT.SetBatch()
inFiles=[]
inFileNames=natsorted(glob(join("%s"%options.inDir, "*.root")))
print inFileNames
for inF in inFileNames:
  inFiles.append(TFile(inF))

can = TCanvas()
can.cd()

canvases=[]

first=True
index=0
pdfsList=[]
framesList=[]
for inFile in inFiles:
  for key in inFile.GetListOfKeys():
    print " found key %s in file %s" % (key.GetName(), inFile.GetName())
    print "key.GetName(): ", key.GetName()
    if "distribs_X__x" == key.GetName() and options.form == "tuple" and options.kind == "interpolated" :
      if first:
        print "adding %s to the plot" % inFile.GetName()
        inFile.Get(key.GetName()).Draw()
        first=False
        index +=1
      else:
        if index%int(options.plotEvery) == 0:
          print "adding %s to the plot" % inFile.GetName()
          inFile.Get(key.GetName()).Draw("SAME")
        index+=1
    if  ( options.form == "workspace" and options.kind == "fullsim"):
      rooWS = inFile.Get("Vg")
      xVar = rooWS.var("x")
      framesList.append(xVar.frame())
      pdfs = rooWS.allPdfs()
      it = pdfs.iterator()
      pdf = it.Next()
      while pdf:
        print "found pdf %s in workspace %s of file %s" % (pdf.GetName(), rooWS.GetName(), inFile.GetName())
        if "signal_fixed" in pdf.GetName() and options.category in pdf.GetName():
          print " --> this one will be added to the plots"
          pdfsList.append(pdf.Clone())
          pdfsList[-1].plotOn(framesList[-1])
          canvases.append(TCanvas())
          canvases[-1].cd()
          framesList[-1].Draw()
        pdf = it.Next()
        
      
outFile = TFile(options.outFile, "RECREATE")
outFile.cd()
can.Write()  
outFile.Close()


print "--> plot of signals is: %s" % options.outFile
