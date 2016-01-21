#WZgammaMacros
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
cmsrel CMSSW_7_4_16_patch1
cd CMSSW_7_4_16_patch1/src
cmsenv
```
##3) Create histograms for a sample using treeChecker
The EXOVVNtuples are processed by the `treeChecker` class, defined in [`treeChecker.C`](treeChecker.C) and [`treeChecker.h`](treeChecker.h). This class is compiled, loaded, and its `Loop` method to process the ntuple is called using the python script [`runTreeChecker.py`](runTreeChecker.py). [`runTreeChecker.py`](runTreeChecker.py) requires two arguments: the input ntuple and a name for the output file.
```
cd ~/my/example/dir/WZgammaMacros
python runTreeChecker.py myInputNtuple.root myHistograms.root
```

The WZgamma ntuples are stored on lxplus eos in the directory `/store/group/phys_b2g/WZgamma2016`. The easiest way to access them is:
```
mkdir ~/myEosMountpoint
eosmount ~/myEosMountpoint
# and for example:
root -l ~/myEosMountpoint/store/group/phys_b2g/WZgamma2016/WZgammaNtuples_zJetsToQQHT600toInf_Jan14/flatTuple_1.root
```
Since TChains are slow, I recommend processing a complete dataset by first using `hadd` to combine all the ntuples from a given dataset into a single giant ntuple. For example:
```
hadd myGJets100-200tuple.root ~/myEosMountpoint/store/group/phys_b2g/WZgamma2016/WZgammaNtuples_gJetsHT100to200_Jan13/*.root
python runTreeChecker.py myGJets100-200tuple.root myGJets100-200histos.root
```

##4) Format histograms using the python scripts
The following python scripts format the histograms in the output from the last step into pretty pdfs which are placed into a directory named `output`:
* [`formatMVAvsEprofiles.py`](formatMVAvsEprofiles.py)
* [`formatPreSelectionPlots.py`](formatPreSelectionPlots.py)
* [`formatSubjetVarsPlots.py`](formatSubjetVarsPlots.py)
* [`makeTriggerTurnOnPlot.py`](makeTriggerTurnOnPlot.py)

To run a formatting script, supply it one argument: the input histograms file. For example:
```
python formatPreSelectionPlots.py myHistograms.root
```
Or, to suppress pyroot's crazy flashing plots:
```
python formatPreSelectionPlots.py myHistograms.root -b
```
The python script [`makeAllPlots.py`](makeAllPlots.py) will run all of the above scripts, and similarly it takes one argument, the histograms file:
```
python makeAllPlots.py myHistograms.root
```
##5) Make a stackplot of all samples
Once you've done step 3 for all the samples, I recommend combining all the background MC histograms with their corresponding weights using `haddws`, which can be checked out from github here: https://github.com/hkaushalya/haddws
Follow the instructions there to combine the gJets and qcd background histograms.

Once you have combined the background samples by `haddws`ing them with appropriate weights, make a stack plot using [`makestackplot.py`](makestackplot.py). First, create a text file that defines your input files for the backgrounds, signals, and data: an example is in [`stackPlotInputs.tx`](stackPlotInputs.tx).

Then make the stackplot:
```
python makeStackPlot.py myStackPlotInputs.txt
```

