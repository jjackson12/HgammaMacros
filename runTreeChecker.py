# Macro to check a tree in the WZgamma ntuples
# This macro takes either 0 or 1 arguments:
# With zero arguments, it will check hardcoded default tree
# With one argument, the tree that will be checked is the "ntuplizer/tree" tree
# in the root file specified in the argument
# Example: 
# python runTreeChecker.py myWZgammaNtuple.root

from ROOT import *
import os, subprocess
from sys import argv

# function to compile a C/C++ macro for loading into a pyroot session
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
if len(argv) > 1:
	file = TFile(argv[1])
	tree = file.Get("ntuplizer/tree")
        checker = treeChecker(tree)
else:
	checker = treeChecker()
checker.Loop()
