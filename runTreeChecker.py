# Macro to check a tree in the WZgamma ntuples
# This macro takes two arguments
# The first argument is the input file, the tree that will be checked is the "ntuplizer/tree" tree
# The second argument is the output file
# Example: 
# python runTreeChecker.py myWZgammaNtuple.root myOutputFile.root

from ROOT import *
import os, subprocess
from sys import argv

# function to compile a C/C++ macro for loading into a pyroot session
if len(argv) != 3:
        print "please supply two arguments to the macro: the input ntuple and the output filename."	
        exit(1)
def compileMacro(macroName):
        # remove the previously compiled libraries
	if os.path.exists(macroName+"_C_ACLiC_dict_rdict.pcm"):
    		os.remove(macroName+"_C_ACLiC_dict_rdict.pcm")
	if os.path.exists(macroName+"_C.d"):
    		os.remove(macroName+"_C.d")
	if os.path.exists(macroName+"_C.so"):
    		os.remove(macroName+"_C.so")
        # compile the macro using g++
	macro = macroName + ".C++g"
	subprocess.call(["root", "-l", "-q", macro])

# get the tree specified by argument 1

# call the compiling function to compile the treeChecker, then run its Loop() method
compileMacro("treeChecker")
gSystem.Load('treeChecker_C')
file = TFile(argv[1])
tree = file.Get("ntuplizer/tree")
checker = treeChecker(tree)
checker.Loop(argv[2])
