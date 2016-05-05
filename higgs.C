#define higgs_cxx
#include <iostream>
#include "TMath.h"
#include "higgs.h"

int higgs::Loop(float cutValue, float lowerMassBound, float upperMassBound)
{
   if (fChain == 0) return -1;
   Long64_t nentries = fChain->GetEntriesFast();
   Long64_t nbytes = 0, nb = 0;

   uint nHiggsJets = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      if (  Cut(ientry) < 0 
         || higgsJet_HbbTag <= cutValue 
         || phJetInvMass_pruned_higgs < lowerMassBound 
         || phJetInvMass_pruned_higgs > upperMassBound ) continue;
      ++nHiggsJets;
   }
   return nHiggsJets;
}

Int_t higgs::Cut(Long64_t entry) {
  if (   cosThetaStar<-0.627*TMath::ATan((-0.005938*phJetInvMass_pruned_higgs)+3.427)
     &&  leadingPhAbsEta          < 1.4442
     &&  higgsJet_pruned_abseta   < 2.2
     &&  phJetDeltaR_higgs        > 1.1 ) return 1;

  else return -1;
}
