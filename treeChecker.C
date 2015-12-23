#define treeChecker_cxx
#include <iostream>
#include <iomanip>
#include "treeChecker.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

using namespace std;

void treeChecker::Loop()
{
  bool debugFlag       = true ;  // If debugFlag is false, the trigger checking couts won't appear and the loop won't stop when it reaches entriesToCheck
  bool checkTrigger    = false ;
  int  entriesToCheck  = 500   ;  // If debugFlag = true, stop once the number of checked entries reaches entriesToCheck

  //   In a ROOT session, you can do:
  //      root> .L treeChecker.C
  //      root> treeChecker t
  //      root> t.GetEntry(12); // Fill t data members with entry number 12
  //      root> t.Show();       // Show values of entry 12
  //      root> t.Show(16);     // Read and show values of entry 16
  //      root> t.Loop();       // Loop on all entries
  //

  //     This is the loop skeleton where:
  //    jentry is the global entry number in the chain
  //    ientry is the entry number in the current Tree
  //  Note that the argument to GetEntry must be:
  //    jentry for TChain::GetEntry
  //    ientry for TTree::GetEntry and TBranch::GetEntry
  //
  //       To read only selected branches, Insert statements like:
  // METHOD1:
  //    fChain->SetBranchStatus("*",0);  // disable all branches
  //    fChain->SetBranchStatus("branchname",1);  // activate branchname
  // METHOD2: replace line
  //    fChain->GetEntry(jentry);       //read all branches
  //by  b_branchname->GetEntry(ientry); //read only this branch
  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntriesFast();

  Long64_t nbytes = 0, nb = 0;
  for (Long64_t jentry=0; jentry<nentries;++jentry) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;

    // print out trigger information
    if (jentry%1000==0) {
      cout << fixed << setw(3) << setprecision(1) << (float(jentry)/float(nentries))*100 << "% done: Scanned " << jentry << " events." << endl;
    }
    if (debugFlag && checkTrigger) {
      cout << "\n \n Trigger info for entry number " << jentry << ":" << endl;
      for(map<string,bool>::iterator it = HLT_isFired->begin(); it != HLT_isFired->end(); ++it) {
        if (debugFlag && checkTrigger) { 
          cout << it->first << " = " << it->second << endl;

        }
      }
    }
    cout << "HLT_isFired[HLT_Photon175_v2] is: " << (*HLT_isFired)[string("HLT_Photon175_v2")] << endl;
    

    nb = fChain->GetEntry(jentry);   nbytes += nb;
    // if (Cut(ientry) < 0) continue;
    if (debugFlag && entriesToCheck == jentry) break;
  }
}
