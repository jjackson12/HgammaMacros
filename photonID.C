#define photonID_cxx
#include "photonID.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void photonID::Loop()
{
    TH1F* noCutEbHist          = new TH1F("noCutEbHist"          , "noCutEbHist"          , 1000, 0, 5000);
    TH1F* diphotonCutsEbHist   = new TH1F("diphotonCutsEbHist"   , "diphotonCutsEbHist"   , 1000, 0, 5000);
    TH1F* cutbasedLooseEbHist  = new TH1F("cutbasedLooseEbHist"  , "cutbasedLooseEbHist"  , 1000, 0, 5000);
    TH1F* cutbasedMediumEbHist = new TH1F("cutbasedMediumEbHist" , "cutbasedMediumEbHist" , 1000, 0, 5000);
    TH1F* cutbasedTightEbHist  = new TH1F("cutbasedTightEbHist"  , "cutbasedTightEbHist"  , 1000, 0, 5000);
    TH1F* mvaEbHist            = new TH1F("mvaEbHist"            , "mvaEbHist"            , 1000, 0, 5000);
    TH1F* noCutEeHist          = new TH1F("noCutEeHist"          , "noCutEeHist"          , 1000, 0, 5000);
    TH1F* diphotonCutsEeHist   = new TH1F("diphotonCutsEeHist"   , "diphotonCutsEeHist"   , 1000, 0, 5000);
    TH1F* cutbasedLooseEeHist  = new TH1F("cutbasedLooseEeHist"  , "cutbasedLooseEeHist"  , 1000, 0, 5000);
    TH1F* cutbasedMediumEeHist = new TH1F("cutbasedMediumEeHist" , "cutbasedMediumEeHist" , 1000, 0, 5000);
    TH1F* cutbasedTightEeHist  = new TH1F("cutbasedTightEeHist"  , "cutbasedTightEeHist"  , 1000, 0, 5000);
    TH1F* mvaEeHist            = new TH1F("mvaEeHist"            , "mvaEeHist"            , 1000, 0, 5000);

    fChain->SetBranchStatus("*"                   ,  0);
    fChain->SetBranchStatus("ph_pt"               ,  1);
    fChain->SetBranchStatus("ph_eta"              ,  1);
    fChain->SetBranchStatus("ph_phi"              ,  1);
    fChain->SetBranchStatus("ph_rho"              ,  1);
    fChain->SetBranchStatus("ph_superCluster_eta" ,  1);
    fChain->SetBranchStatus("ph_superCluster_phi" ,  1);
    fChain->SetBranchStatus("ph_sigmaIetaIeta"    ,  1);
    fChain->SetBranchStatus("ph_hOverE"           ,  1);
    fChain->SetBranchStatus("ph_isoGamma"         ,  1);
    fChain->SetBranchStatus("ph_isoCh"            ,  1);
    fChain->SetBranchStatus("ph_passEleVeto"      ,  1);
    fChain->SetBranchStatus("ph_passLooseId"      ,  1);
    fChain->SetBranchStatus("ph_passMediumId"     ,  1);
    fChain->SetBranchStatus("ph_passTightId"      ,  1);
    fChain->SetBranchStatus("ph_mvaCat"           ,  1);
    fChain->SetBranchStatus("ph_mvaVal"           ,  1);
    fChain->SetBranchStatus("genParticle_pdgId"   ,  1);
    fChain->SetBranchStatus("genParticle_eta"      ,  1);
    fChain->SetBranchStatus("genParticle_px"      ,  1);
    fChain->SetBranchStatus("genParticle_py"      ,  1);
    fChain->SetBranchStatus("genParticle_pz"      ,  1);
    fChain->SetBranchStatus("genParticle_mother"  ,  1);

   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      float bestPt = -1.;
      float bestDeltaR = 999;
      int bestIph = -1;
      TVector3 matchedGenPho = TVector3(0,0,0);
      TVector3 recoPho = TVector3(0,0,0);
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      for (int iGen=0; iGen<genParticle_pdgId->size(); ++iGen) {
        if (genParticle_pdgId->at(iGen) == 22 && (genParticle_mother->at(iGen)[0] == 25) ) { 
          //cout << "genparticle mother has pdgid = " << genParticle_mother->at(iGen)[0] <<cout;
          matchedGenPho.SetXYZ(genParticle_px->at(iGen),  genParticle_py->at(iGen),  genParticle_pz->at(iGen));  
        }
      }
      for (int iPh=0; iPh<(int)ph_pt->size(); ++iPh) {
        recoPho.SetPtEtaPhi(ph_pt->at(iPh), ph_eta->at(iPh), ph_phi->at(iPh));
        if (recoPho.DeltaR(matchedGenPho)<0.3) {
          if (std::abs(ph_eta->at(iPh)) < 1.4442) {
            if (std::abs(matchedGenPho.Eta())<1.4442){
              if (recoPho.DeltaR(matchedGenPho)<bestDeltaR) { 
                bestDeltaR = recoPho.DeltaR(matchedGenPho);
                bestPt = ph_pt->at(iPh);
                bestIph = iPh;
              }
            }
          }
        }
      }
      if (std::abs(recoPho.Eta()) < 1.4442) {
        if (std::abs(matchedGenPho.Eta())<1.4442){
          noCutEbHist            ->Fill(bestPt);
          if (bestIph>-1) {
              map<string, bool> diphotonIDdecisions = diphotonIDmap( ph_superCluster_eta ->at(bestIph) ,
                                                                     ph_superCluster_phi ->at(bestIph) ,
                                                                     ph_sigmaIetaIeta    ->at(bestIph) ,
                                                                     ph_hOverE           ->at(bestIph) ,
                                                                     ph_isoGamma         ->at(bestIph) ,
                                                                     ph_isoCh            ->at(bestIph) ,
                                                                     ph_rho              ->at(bestIph) ,
                                                                     ph_pt               ->at(bestIph) ,
                                                                     ph_passEleVeto      ->at(bestIph)   );
            if( diphotonIDdecisions["allCuts"]                           ) diphotonCutsEbHist   ->  Fill(bestPt);
            if( ph_passLooseId->at(bestIph) && ph_passEleVeto->at(bestIph) == 1  ) cutbasedLooseEbHist  ->  Fill(bestPt);
            if( ph_passMediumId->at(bestIph)&& ph_passEleVeto->at(bestIph) == 1  ) cutbasedMediumEbHist ->  Fill(bestPt);
            if( ph_passTightId->at(bestIph) && ph_passEleVeto->at(bestIph) == 1  ) cutbasedTightEbHist  ->  Fill(bestPt);
            if( ph_mvaCat->at(bestIph)==0 && ph_mvaVal->at(bestIph)>=0.374   && ph_passEleVeto->at(bestIph) == 1    ) mvaEbHist            ->  Fill(bestPt);
          }
        }
      }
   }
      // if (Cut(ientry) < 0) continue;
   TFile* outFile = new TFile("outfile.root","RECREATE");

   noCutEbHist           -> Write();
   diphotonCutsEbHist    -> Write();
   cutbasedLooseEbHist   -> Write();
   cutbasedMediumEbHist  -> Write();
   cutbasedTightEbHist   -> Write();
   mvaEbHist             -> Write();
   noCutEeHist           -> Write();
   diphotonCutsEeHist    -> Write();
   cutbasedLooseEeHist   -> Write();
   cutbasedMediumEeHist  -> Write();
   cutbasedTightEeHist   -> Write();
   mvaEeHist             -> Write();
}

map<string, bool> photonID::diphotonIDmap(float eta, float phi, float sigmaIetaIeta, float hOverE, float isoGamma, float isoCh, float rho, float pT, bool eleVeto) {
  map<string, bool> decisions;
  float isoGammaBar;

  decisions[ "eleVeto"] = eleVeto;
  decisions[ "hOverE" ] = ( hOverE < 5e-2 );
  decisions[ "isoCh"  ] = ( isoCh  < 5.   );
  if (std::abs(eta)<1.4442) {
    //Category 1:
    if (std::abs(eta)<0.9) {
      isoGammaBar = 2.5 + isoGamma - rho*0.17 - 4.5e-3*pT;
    }
    //Category 2:
    else {
      isoGammaBar = 2.5 + isoGamma - rho*0.14 - 4.5e-3*pT;
    }
    decisions[ "sigmaIEtaIEta" ] = ( sigmaIetaIeta < 0.0105 );
    decisions[ "isoGammaBar"   ] = ( isoGammaBar   < 2.75   );
  }
  else if ( std::abs(eta)>1.566 && std::abs(eta)<2.5 ) {
    //Category 3:
    if ( std::abs(eta)<2.0) {
      isoGammaBar = 2.5 + isoGamma - rho*0.11 - 4.5e-3*pT;
    }
    //Category 4:
    else if ( std::abs(eta)<2.2 ) {
      isoGammaBar = 2.5 + isoGamma - rho*0.14 - 3e-3*pT;
    }
    //Category 5:
    else {
      isoGammaBar = 2.5 + isoGamma - rho*0.22 - 3e-3*pT;
    }
    decisions[ "sigmaIEtaIEta" ] = ( sigmaIetaIeta < 0.028 );
    decisions[ "isoGammaBar"   ] = ( isoGammaBar   < 2.0   );
  }
  decisions[ "allCuts" ] = (decisions["hOverE"] && decisions["isoCh"] && decisions["isoGammaBar"] && decisions["sigmaIEtaIEta"] && decisions["eleVeto"]);
  return decisions;
}
