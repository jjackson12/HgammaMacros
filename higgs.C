#define higgs_cxx
#include <iostream>
#include <limits>
#include "TMath.h"
#include "higgs.h"
#include "treeChecker.h"

// Class for doing quick counting experiments on the "ddTrees" from the treeChecker macro.
// John Hakala, 5/11/2016

int higgs::Loop(std::string category, float HbbCutValue,  float pToverMcutValue, float deltaRcutValue, float jetEtaCutValue, float phoEtaCutValue, float jetMassLowerBound, float jetMassUpperBound, float lowerMassBound, float upperMassBound)
{
   if (fChain == 0) return -1;
   Long64_t nentries = fChain->GetEntriesFast();
   Long64_t nbytes = 0, nb = 0;

   uint nHiggsJets = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      if (  Cut( ientry,
                 category, 
                 HbbCutValue, 
                 pToverMcutValue,
                 deltaRcutValue,
                 jetEtaCutValue,
                 phoEtaCutValue
               ) < 0 
            || higgsPrunedJetCorrMass < jetMassLowerBound
            || higgsPrunedJetCorrMass > jetMassUpperBound
            || phJetInvMass_pruned_higgs < lowerMassBound 
            || phJetInvMass_pruned_higgs > upperMassBound 
         ) continue;
      //cout << runNo << " : " << lumiNo  << " : " << eventNo << endl;
      ++nHiggsJets;
   }
   return nHiggsJets;
}

Int_t higgs::Cut(Long64_t entry, std::string category, float HbbCutValue, float pToverMcutValue, float deltaRcutValue, float jetEtaCutValue, float phoEtaCutValue) {
  //LoadTree(entry);
  if (    
           leadingPhAbsEta          < phoEtaCutValue
       &&  higgsJet_pruned_abseta   < jetEtaCutValue
       &&  phJetDeltaR_higgs        > deltaRcutValue
       &&  phPtOverMgammaj          > pToverMcutValue
       &&  (     (category == "btag" && higgsJet_HbbTag >= HbbCutValue) 
              || (category == "antibtag" && higgsJet_HbbTag <= HbbCutValue)
              || category == "nobtag" 
           )
     ) return 1;

  else return -1;
}
