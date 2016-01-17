#WZgammaMacros
Macros for analyzing ntuples from the EXOVVNtuplizer: https://github.com/jhakala/EXOVVNtuplizerRunII
These instructions were tested on lxplus
##1) Get the code
Go to the directory where you want to check the code out and clone the code:
```
cd ~/my/example/dir
git clone git@github.com:jhakala/WZgammaMacros.git
```
##2) Use an up-to-date version of ROOT and python
ROOT 6.02 and python 2.7.6 is recommended to run these. On lxplus, the default versions are ROOT 5.32 and python 2.6.6. One way to get up-to-date versions is:
```
cd ~/other/example/dir
cmsrel CMSSW_7_4_16_patch1
cd CMSSW_7_4_16_patch1/src
cmsenv
```
##3) Create histograms using treeChecker.
The EXOVVNtuples are processed by the `treeChecker` class, defined in `treeChecker.C` and `treeChecker.h`. This class is compiled, loaded, and its `Loop` method to process the ntuple is called using the python script `runTreeChecker.py`. `runTreeChecker.py` requires two arguments: the input ntuple and a name for the output file.
```
python runTreeChecker.py myInputNtuple.root myHistograms.root
```

##4) Format histograms using the python scripts
The following python scripts format the histograms in the output from the last step into pretty pdfs which are placed into a directory named `output`:
* formatMVAvsEprofiles.py
* formatPreSelectionPlots.py
* formatSubjetVarsPlots.py
* makeTriggerTurnOnPlot.py
All of these take one argument, the input histograms file. For example:
```
python formatPreSelectionPlots.py myHistograms.root
```
Or, to suppress pyroot's crazy flashing plots:
```
python formatPreSelectionPlots.py myHistograms.root -b
```

The python script `makeAllPlots.py` will run all of the above scripts, and similarly it takes one argument, the histograms file:
```
python makeAllPlots.py myHistograms.root
```

