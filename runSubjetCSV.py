# Macro to run the subjet csv demo
# This macro takes two arguments
# The first argument is the input file, the tree that will be checked is the "ntuplizer/tree" tree
# The second argument is the output file
# Example: 
# python runSubjetCSV.py myVgammaNtuple.root myOutputFile.root
# John Hakala 1/15/2016

from ROOT import *
import os, subprocess
from sys import argv

# function to compile a C/C++ macro for loading into a pyroot session
if len(argv) != 4:
   print "please supply three arguments to the macro: the input ntuple, the output filename, and either 'load' or 'compile'."   
   exit(1)
elif not (argv[3]=="load" or argv[3]=="compile"):
   print "for the third argument, please pick 'load' or 'compile'."
else:
   print "\nInput file is %s\n" % argv[1]
   print "\nAttempting to %s treeChecker.\n" % argv[3]
   pastTense = "loaded" if argv[3]=="load" else "compiled"

def deleteLibs(macroName):
        # remove the previously compiled libraries
   if os.path.exists(macroName+"_C_ACLiC_dict_rdict.pcm"):
      os.remove(macroName+"_C_ACLiC_dict_rdict.pcm")
   if os.path.exists(macroName+"_C.d"):
      os.remove(macroName+"_C.d")
   if os.path.exists(macroName+"_C.so"):
      os.remove(macroName+"_C.so")
        # compile the macro using g++

# call the compiling function to compile the treeChecker, then run its Loop() method
if argv[3]=="compile":
   deleteLibs("subjet_csv")
   exitCode = gSystem.CompileMacro("subjet_csv.C", "vgOck")
   success=(exitCode==1)
elif argv[3]=="load":
   exitCode = gSystem.Load('subjet_csv_C')
   success=(exitCode>=-1)
if not success:
   print "\nError... subjet_csv failed to %s. :-("%argv[3]
   print "Make sure you're using an up-to-date version of ROOT by running cmsenv in a 7_4_X>=16 CMSSW area."
   exit(1)
else:
   print "\nsubjet_csv %s successfully."%pastTense
   if argv[3]=="compile":
      gSystem.Load('subjet_csv_C')
   file = TFile(argv[1])
   
   # get the ntuplizer/tree tree from the file specified by argument 1
   tree = file.Get("ntuplizer/tree")
   checker = treeChecker(tree)
   checker.Loop(argv[2])
