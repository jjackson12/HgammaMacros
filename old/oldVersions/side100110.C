#define side100110_cxx
#include "side100110.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>

void side100110::Loop()
{
//   In a ROOT session, you can do:
//      root> .L side100110.C
//      root> side100110 t
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;

   uint nSidebandJets = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;
      cout << "sideLowFourPrunedJetCorrMass: " << sideLowFourPrunedJetCorrMass << endl;
      ++nSidebandJets;

   }
   cout << "Total number of sideband jets: " << nSidebandJets << endl;
}
