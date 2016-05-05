import os
from ROOT import *
# function to compile a C/C++ macro for loading into a pyroot session

def deleteLibs(macroName):
        # remove the previously compiled libraries
   if os.path.exists(macroName+"_C_ACLiC_dict_rdict.pcm"):
      os.remove(macroName+"_C_ACLiC_dict_rdict.pcm")
   if os.path.exists(macroName+"_C.d"):
      os.remove(macroName+"_C.d")
   if os.path.exists(macroName+"_C.so"):
      os.remove(macroName+"_C.so")
        # compile the macro using g++

def instance(macroName, args):
  # call the compiling function to compile the macro, then run its Loop() method
  #args: macro name, [input filename, output filename, load/compile]
  if len(args) != 3:
     print "please supply three arguments to the macro: the input ntuple, the output filename, and either 'load' or 'compile'."   
     exit(1)
  elif not (args[2]=="load" or args[2]=="compile"):
     print "for the third argument, please pick 'load' or 'compile'."
  else:
     print "\nInput file is %s\n" % args[0]
     print "\nAttempting to %s treeChecker.\n" % macroName
     pastTense = "loaded" if args[2]=="load" else "compiled"
  if args[2]=="compile":
     deleteLibs("%s"%macroName)
     exitCode = gSystem.CompileMacro("%s.C"%macroName, "gOck")
     success=(exitCode==1)
  elif args[3]=="load":
     exitCode = gSystem.Load('%s_C'%macroName)
     success=(exitCode>=-1)
  if not success:
     print "\nError... %s failed to %s. :-("%(macroName, args[2])
     print "Make sure you're using an up-to-date version of ROOT by running cmsenv in a 7_4_X>=16 CMSSW area."
     exit(1)
  else:
     print "\n%s %s successfully."%(macroName, pastTense)
     if args[2]=="compile":
        gSystem.Load('%s_C'%macroName)
