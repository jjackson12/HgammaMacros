#define photonID_cxx
#include "photonID.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include <iomanip>
#include <TVector3.h>

using namespace std;

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
    fChain->SetBranchStatus("genParticle_px"      ,  1);
    fChain->SetBranchStatus("genParticle_py"      ,  1);
    fChain->SetBranchStatus("genParticle_pz"      ,  1);
    fChain->SetBranchStatus("genParticle_mother"  ,  1);



   if (fChain == 0) return;

   bool debugFlag = false;
   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      TVector3 matchedGenPho = TVector3(0,0,0);
      TVector3 recoPho = TVector3(0,0,0);
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      for (int iGen=0; iGen<genParticle_pdgId->size(); ++iGen) {
        if (genParticle_pdgId->at(iGen) == 22 && (genParticle_mother->at(iGen)[0] ==35 || genParticle_mother->at(iGen)[0] ==36) ) { 
          matchedGenPho.SetXYZ(genParticle_px->at(iGen),  genParticle_py->at(iGen),  genParticle_pz->at(iGen));  
        }
      }
      for (int iPh=0; iPh<(int)ph_pt->size(); ++iPh) {
        recoPho.SetPtEtaPhi(ph_pt->at(iPh), ph_eta->at(iPh), ph_phi->at(iPh));
        if (recoPho.DeltaR(matchedGenPho)<0.3) {
          map<string, bool> diphotonIDdecisions = diphotonIDmap( ph_superCluster_eta ->at(iPh) ,
                                                                 ph_superCluster_phi ->at(iPh) ,
                                                                 ph_sigmaIetaIeta    ->at(iPh) ,
                                                                 ph_hOverE           ->at(iPh) ,
                                                                 ph_isoGamma         ->at(iPh) ,
                                                                 ph_isoCh            ->at(iPh) ,
                                                                 ph_rho              ->at(iPh) ,
                                                                 ph_pt               ->at(iPh) ,
                                                                 ph_passEleVeto      ->at(iPh)   );
          if (debugFlag) {
            cout << "\nIn event number " << jentry << ", value from decisions for photon " << iPh << " is:" << endl; 
            cout << "            hOverE: " <<  diphotonIDdecisions[ "hOverE"        ] << endl;
            cout << "             isoCh: " <<  diphotonIDdecisions[ "isoCh"         ] << endl;
            cout << "     sigmaIEtaIEta: " <<  diphotonIDdecisions[ "sigmaIEtaIEta" ] << endl;
            cout << "       isoGammaBar: " <<  diphotonIDdecisions[ "isoGammaBar"   ] << endl;
            cout << "           eleVeto: " <<  diphotonIDdecisions[ "eleVeto"       ] << endl;
            cout << "           allCuts: " <<  diphotonIDdecisions[ "allCuts"       ] << endl;
          }
          if (std::abs(ph_eta->at(iPh)) < 1.479) {
            noCutEbHist            ->Fill(ph_pt->at(iPh));
            if( diphotonIDdecisions["allCuts"]                      ) diphotonCutsEbHist   ->  Fill(ph_pt->at(iPh));
            if( ph_passLooseId->at(iPh)                             ) cutbasedLooseEbHist  ->  Fill(ph_pt->at(iPh));
            if( ph_passMediumId->at(iPh)                            ) cutbasedMediumEbHist ->  Fill(ph_pt->at(iPh));
            if( ph_passTightId->at(iPh)                             ) cutbasedTightEbHist  ->  Fill(ph_pt->at(iPh));
            if( ph_mvaCat->at(iPh)==0 && ph_mvaVal->at(iPh)>=0.374  ) mvaEbHist            ->  Fill(ph_pt->at(iPh));
          }
  
          if (std::abs(ph_eta->at(iPh)) < 2.4) {
            noCutEeHist            ->Fill(ph_pt->at(iPh));
            if( diphotonIDdecisions["allCuts"]                      ) diphotonCutsEeHist     ->Fill(ph_pt->at(iPh));
            if( ph_passLooseId->at(iPh)                             ) cutbasedLooseEeHist    ->Fill(ph_pt->at(iPh));
            if( ph_passMediumId->at(iPh)                            ) cutbasedMediumEeHist   ->Fill(ph_pt->at(iPh));
            if( ph_passTightId->at(iPh)                             ) cutbasedTightEeHist    ->Fill(ph_pt->at(iPh));
            if( ph_mvaCat->at(iPh)==1 && ph_mvaVal->at(iPh)>=0.336  ) mvaEeHist              ->Fill(ph_pt->at(iPh));
          }
        }
      }
      
   }

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
  //Category 3:
  else if ( std::abs(eta)>1.566 && std::abs(eta)<2.5 ) {
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
  decisions[ "allCuts" ] = (decisions["hOverE"] && decisions["isoCh"] && decisions["isoGammaBar"] && decisions["isoGammaBar"] && decisions["eleVeto"]);
  return decisions;
}
