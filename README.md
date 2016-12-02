#HgammaMacros
Macros for analyzing ntuples from the [EXOVVNtuplizer](https://github.com/jhakala/EXOVVNtuplizerRunII)

These instructions were tested on lxplus.
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
cmsrel CMSSW_8_0_X # X > 19
cd CMSSW_8_0_X
cmsenv
```
##3) Create histograms for all sample using HbbGammaSelector.C
The EXOVVNtuples are processed by the `HbbGammaSelector` class, defined in [`HbbGammaSelector.C`](HbbGammaSelector.C) and [`HbbGammaSelector.h`](HbbGammaSelector.h). This class is compiled, loaded, and its `Loop` method to process the ntuple is called using the python script [`runHbbGammaSelector.py`](runHbbGammaSelector.py). [`runHbbGammaSelector.py`](runHbbGammaSelector.py) requires three arguments: the input ntuple, a name for the output file, and either `compile` or `load`, depending on whether you want the macro recompiled (e.g. if there were any changes made to the source) or whether it should be loaded from a previously compiled library (e.g. if doing batch processing). The bash scripts [`makeAllNewerDDs.sh`](makeAllNewerDDs.sh) and [`makeAllSigDDs.sh`](makeAllSigDDs.sh) give an example of processing many files at once. In this readme, the output files from HbbGammaSelector are called "DDs."
```
cd ~/my/example/dir/WZgammaMacros
./makeAllNewerDDs.sh 
```
##4) Make stackplots
Once signals, MC backgrounds, and the data are processed, the location of the input ntuples and the output DDs must be specified in [`HgParameters.py`](HgParameters.py). In that file as well as [`HgCuts.py`](HgCuts.py) and [`getMCbgWeights.py`](getMCbgWeights.py),  various settings for processing the data are defined, including sample names, cut values, and plotting details. Once these are specified accordingly, one can make stackplots of all variables for all samples using  [`makeStacks.py`](makeStacks.py). 
```
python makeStacks.py -b
```
##5) Make optimization plots
After making all the stackplots, optimization plots can be made using [`plotOpts.py`](plotOpts.py).
```
python plotOpts.py -b
```
