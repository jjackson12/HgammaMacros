# Macro to analyze a VgammaTuplizer flatTuple
# This macro takes three options
# The option "i" is the input file, containing the tree named "ntuplizer/tree" 
# The "-o" option is the output filename
# The optional "-l" will ask to load the macro from a compiled library, rather than compiling it from source
# Example: 
# python runTreeChecker.py -i myVgammaNtuple.root -o myOutputFile.root -l
# John Hakala 1/15/2016

import os
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-l", dest="load", action="store_true", default=False,
                  help="use this if you want to load the macro from a compiled library"  )
parser.add_option("-i",  dest="inputFileName",
                  help="the input file name"                                             )
parser.add_option("-o",  dest="outputFileName",
                  help="the output file name"                                            )
(options, args) = parser.parse_args()


from ROOT import *


if options.inputFileName is None:
  print "\nPlease specify the input file with the -i option."
  exit(1)
elif options.outputFileName is None:
  print "\nPlease specify the output filename with the -o option."
  exit(1)
elif not os.path.isfile(options.inputFileName):
  print "\nThe input file specified was not found: %s" % options.inputfileName
  exit(1)

def deleteLibs(macroName):
  # remove the previously compiled libraries
  if os.path.exists(macroName+"_C_ACLiC_dict_rdict.pcm"):
     os.remove(macroName+"_C_ACLiC_dict_rdict.pcm")
  if os.path.exists(macroName+"_C.d"):
     os.remove(macroName+"_C.d")
  if os.path.exists(macroName+"_C.so"):
     os.remove(macroName+"_C.so")

print "\nInput file is %s\n" % options.inputFileName
presentTense = "load" if options.load else "compile"
pastTense  = "loaded" if options.load else "compiled"
print "\nAttempting to %s HgammaSelector.\n" % presentTense

# call the compiling function to compile the HgammaSelector, then run its Loop() method
if presentTense=="compile":
   deleteLibs("HgammaSelector")
   # compile the macro using g++ and check compilation status
   exitCode = gSystem.CompileMacro("HgammaSelector.C", "gOck")
   success=(exitCode==1)
elif presentTense=="load":
   exitCode = gSystem.Load('HgammaSelector_C')
   success=(exitCode>=-1)
if not success:
   print "\nError... HgammaSelector failed to %s. :-("%presentTense
   print "Make sure you're using an up-to-date version of ROOT by running cmsenv in a 7_4_X>=16 CMSSW area."
   exit(1)

print "\nHgammaSelector %s successfully."%pastTense
if presentTense=="compile":
   gSystem.Load('HgammaSelector_C')
inputFile = TFile(options.inputFileName)

# get the ntuplizer/tree tree from the file specified by argument 1
tree = inputFile.Get("ntuplizer/tree")
instance = HgammaSelector(tree)
# run the HgammaSelector::Loop method
instance.Loop(options.outputFileName)

