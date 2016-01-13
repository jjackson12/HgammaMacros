#define treeChecker_cxx
#include <iostream>
#include <iomanip>
#include "treeChecker.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLorentzVector.h>

using namespace std;

void treeChecker::Loop(string outputFileName)
{
  // Flags for running this macro
  bool debugFlag                    = false ;  // If debugFlag is false, the trigger checking couts won't appear and the loop won't stop when it reaches entriesToCheck
  bool checkTrigger                 = false ;
  int  entriesToCheck               = -1    ;  // If debugFlag = true, stop once the number of checked entries reaches entriesToCheck
  int  reportEvery                  = 500    ;

  
  // Photon MVA id cut values
  float endcap_phoMVAcut            = 0.336 ;  // See https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariatePhotonIdentificationRun2#Recommended_MVA_recipes_for_2015
  float barrel_phoMVAcut            = 0.374 ;  // These should change once we move to CMSSW_7_4_16
  float WZmassCutLow                =   65. ;  // Z mass +- 15 GeV
  float WZmassCutHigh               =  105. ;

  // Variables calculated using events
  bool  phoIsTight                  = false ; 
  bool  eventHasTightPho            = false ; 
  bool  eventHasMatchedRawJet       = false ; 
  TLorentzVector matchedJet_raw             ;
  bool  eventHasMatchedPrunedJet    = false ; 
  TLorentzVector matchedJet_pruned          ;
  bool  eventHasMatchedSoftdropJet  = false ; 
  TLorentzVector matchedJet_softdrop        ;
  int   eventsWithTightPho          =    0  ;
  int   eventsWithLooseJet          =    0  ;
  int   eventsWtightPhoAndLooseJet  =    0  ;
  int   eventsWithJetInWZmassCuts   =    0  ;
  int   eventsPassingFinalSelection =    0  ;
  TLorentzVector leadingPhoton              ;
  float leadingJetPt                =    0. ;
  float leadingJetE                 =    0. ;
  float leadingJetM                 =    0. ;
  float leadingJetPrunedM           =    0. ; 
  float leadingJetSoftdropM         =    0. ;
  float HT                          =    0. ;
  float leadingJetTau1              = -999. ;
  float raw_matchedJetTau1          = -999. ;
  float pruned_matchedJetTau1       = -999. ;
  float softdrop_matchedJetTau1     = -999. ;
  float leadingJetTau2              = -999. ;
  float raw_matchedJetTau2          = -999. ;
  float pruned_matchedJetTau2       = -999. ;
  float softdrop_matchedJetTau2     = -999. ;
  float leadingJetTau3              = -999. ;
  float raw_matchedJetTau3          = -999. ;
  float pruned_matchedJetTau3       = -999. ;
  float softdrop_matchedJetTau3     = -999. ;
  float leadingPhPt                 =    0. ;
  float leadingPhE                  =    0. ;
  float leadingPhMVA                =    0. ;
  float leadingPhCat                =    0. ;
  TLorentzVector sumVector                  ;
  
  // Output histograms
  TH1F*  leadingPhPtHist            = new TH1F( "leadingPhPtHist"            , "Leading photon pT"                    ,  700 ,      0 ,  7000 );
  TH1F*  leadingJetPtHist           = new TH1F( "leadingJetPtHist"           , "Leading AK8 jet pT"                   ,  700 ,      0 ,  7000 );
  TH1F*  HThist                     = new TH1F( "HThist"                     , "Scalar sum of jet PT"                 ,  700 ,      0 ,  7000 );
  TH1F*  leadingJetTau1Hist         = new TH1F( "leadingJetTau1Hist"         , "Leading jet #tau_{1}"                 ,  110 ,  -0.05 ,  1.05 );
  TH1F*  leadingJetTau2Hist         = new TH1F( "leadingJetTau2Hist"         , "Leading jet #tau_{2}"                 ,  110 ,  -0.05 ,  1.05 );
  TH1F*  leadingJetTau3Hist         = new TH1F( "leadingJetTau3Hist"         , "Leading jet #tau_{3}"                 ,  110 ,  -0.05 ,  1.05 );
  TH1F*  leadingJetT2T1             = new TH1F( "leadingJetT2T1"             , "Leading jet #tau_{2}/#tau_{1}"        ,  110 ,  -0.05 ,  1.05 );
  TH1F*  leadingJetT3T2             = new TH1F( "leadingJetT3T2"             , "Leading jet #tau_{3}/#tau_{2}"        ,  110 ,  -0.05 ,  1.05 );
  TH1F*  leadingPhMVAhist_endcap    = new TH1F( "leadingPhMVAhist_endcap"    , "Leading photon MVA"                   ,  210 ,  -1.05 ,  1.05 );
  TH1F*  leadingPhMVAhist_barrel    = new TH1F( "leadingPhMVAhist_barrel"    , "Leading photon MVA"                   ,  210 ,  -1.05 ,  1.05 );
  TH1F*  leadingJetMassHist         = new TH1F( "leadingJetMassHist"         , "Leading AK8 jet inv. mass"            ,  700 ,      0 ,  7000 );
  TH1F*  leadingJetPrunedMassHist   = new TH1F( "leadingJetPrunedMassHist"   , "Leading AK8 pruned jet inv. mass"     ,  700 ,      0 ,  7000 );
  TH1F*  leadingJetSoftdropMassHist = new TH1F( "leadingJetSoftdropMassHist" , "Leading AK8 softdrop jet inv. mass"   ,  700 ,      0 ,  7000 );
  TH1F*  leadingPhMassHist          = new TH1F( "leadingPhMassHist"          , "Leading photon inv. mass"             ,  700 ,      0 ,  7000 );
  TH1F*  phJetInvMassHist_raw       = new TH1F( "phJetInvMassHist_raw"       , "Photon+Jet invariant mass (raw)"      ,  700 ,      0 ,  7000 );
  TH1F*  phJetInvMassHist_pruned    = new TH1F( "phJetInvMassHist_pruned"    , "Photon+Jet invariant mass (pruned)"   ,  700 ,      0 ,  7000 );
  TH1F*  phJetInvMassHist_softdrop  = new TH1F( "phJetInvMassHist_softdrop"  , "Photon+Jet invariant mass (softdrop)" ,  700 ,      0 ,  7000 );

  TFile* outputFile                 = new TFile(outputFileName.c_str(), "RECREATE");

  // Branches from EXOVVNtuplizer tree
  fChain->SetBranchStatus( "*"                     ,  0 );  // disable all branches
  fChain->SetBranchStatus( "HLT_isFired"           ,  1 );  // activate select branches
  fChain->SetBranchStatus( "ph_pt"                 ,  1 );  
  fChain->SetBranchStatus( "ph_e"                  ,  1 );  
  fChain->SetBranchStatus( "ph_eta"                ,  1 );  
  fChain->SetBranchStatus( "ph_phi"                ,  1 );  
  fChain->SetBranchStatus( "ph_mvaVal"             ,  1 );
  fChain->SetBranchStatus( "ph_mvaCat"             ,  1 );
  fChain->SetBranchStatus( "jetAK8_pt"             ,  1 );  
  fChain->SetBranchStatus( "jetAK8_mass"           ,  1 );  
  fChain->SetBranchStatus( "jetAK8_e"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_eta"            ,  1 );  
  fChain->SetBranchStatus( "jetAK8_phi"            ,  1 );  
  fChain->SetBranchStatus( "jetAK8_pruned_mass"    ,  1 );
  fChain->SetBranchStatus( "jetAK8_softdrop_mass"  ,  1 );  
  fChain->SetBranchStatus( "jetAK8_tau1"           ,  1 );  
  fChain->SetBranchStatus( "jetAK8_tau2"           ,  1 );  
  fChain->SetBranchStatus( "jetAK8_tau3"           ,  1 );  
  fChain->SetBranchStatus( "jetAK8_IDLoose"        ,  1 );  

  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;

  // Loop over all events
  for (Long64_t jentry=0; jentry<nentries;++jentry) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;


    leadingPhPt                = 0.    ;
    leadingPhE                 = 0.    ;
    leadingJetPt               = 0.    ;
    leadingJetE                = 0.    ;
    leadingJetM                = 0.    ;
    leadingJetPrunedM          = 0.    ;
    leadingJetSoftdropM        = 0.    ;
    leadingJetTau1             = -999. ;
    leadingJetTau2             = -999. ;
    leadingJetTau3             = -999. ;
    eventHasMatchedPrunedJet   = false ;
    eventHasMatchedSoftdropJet = false ;
    raw_matchedJetTau1         = -999. ;
    raw_matchedJetTau2         = -999. ;
    raw_matchedJetTau3         = -999. ;
    pruned_matchedJetTau1      = -999. ;
    pruned_matchedJetTau2      = -999. ;
    pruned_matchedJetTau3      = -999. ;
    softdrop_matchedJetTau1    = -999. ;
    softdrop_matchedJetTau2    = -999. ;
    softdrop_matchedJetTau3    = -999. ;
    HT                         = 0.    ;
    phoIsTight                 = false ;
    eventHasTightPho           = false ;
    eventHasMatchedRawJet      = false ;
    leadingPhMVA               = -999. ;
    leadingPhCat               = -999. ;

    leadingPhoton       .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    matchedJet_raw      .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    matchedJet_pruned   .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    matchedJet_softdrop .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sumVector           .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    // Print out trigger information
    if (jentry%reportEvery==0) {
      cout << fixed << setw(5) << setprecision(3) << (float(jentry)/float(nentries))*100 << "% done: Scanned " << jentry << " events." << endl;
    }
    if (debugFlag) cout << "\n\nIn event number " << jentry << ":" << endl;
    if (debugFlag && checkTrigger) {
      cout << "     Trigger info for entry number " << jentry << ":" << endl;
      for(map<string,bool>::iterator it = HLT_isFired->begin(); it != HLT_isFired->end(); ++it) {
        if (debugFlag && checkTrigger) { 
          cout << it->first << " = " << it->second << endl;
        }
      }
    }
    
    // Loop over photons
    for (uint iPh = 0; iPh<ph_pt->size() ; ++iPh) { 
      if (debugFlag) {
        cout << "    Photon " << iPh << " has pT " << ph_pt->at(iPh)  << ", eta =" << ph_eta->at(iPh) << ", ph_mvaVal = " << ph_mvaVal->at(iPh) << ", ph_mvaCat = " << ph_mvaCat->at(iPh) << endl;
      }
      // Check if this event has a photon passing ID requirements
      phoIsTight = (ph_mvaCat->at(iPh)==0 && ph_mvaVal->at(iPh)>=barrel_phoMVAcut) || (ph_mvaCat->at(iPh)==1 && ph_mvaVal->at(iPh)>=endcap_phoMVAcut);
      eventHasTightPho |= phoIsTight;      
      // Fill the leading photon variables, requiring the photon to pass the ID requirements
      if (ph_pt->at(iPh) > leadingPhPt && phoIsTight ) {
        leadingPhPt  = ph_pt     ->  at(iPh) ;
        leadingPhE   = ph_e      ->  at(iPh) ;
        leadingPhMVA = ph_mvaVal ->  at(iPh) ;
        leadingPhCat = ph_mvaCat ->  at(iPh) ;
        leadingPhoton.SetPtEtaPhiE(ph_pt->at(iPh), ph_eta->at(iPh), ph_phi->at(iPh), ph_e->at(iPh));
      }
    }
    if (debugFlag && eventHasTightPho) cout << "    This event has a tight photon." << endl;
    leadingPhPtHist->Fill(leadingPhPt);
    if (leadingPhCat == 0) {
      leadingPhMVAhist_barrel->Fill(leadingPhMVA);
    }
    else if (leadingPhCat == 1) {
      leadingPhMVAhist_endcap->Fill(leadingPhMVA);
    }

    // Loop over jets
    for (uint iJet = 0; iJet<jetAK8_pt->size() ; ++iJet) { 
      if (debugFlag) cout << "    AK8 Jet " << iJet << " has pT " << jetAK8_pt->at(iJet) << endl;
      if (debugFlag) cout << "    jetAK8_IDLoose[" << iJet << "] is : " << jetAK8_IDLoose->at(iJet) << endl;
 
      if (jetAK8_IDLoose->at(iJet) == 1) { 
      // Get leading jet variables, requiring loose jet ID
        if (jetAK8_pt->at(iJet) > leadingJetPt) {
          leadingJetPt   = jetAK8_pt->at(iJet);
          //if (leadingJetE > jetAK8_e->at(iJet)) cout << "A leading jet (highest pT) had lower energy than another jet.";
          leadingJetE          = jetAK8_e             ->  at(iJet) ;
          leadingJetM          = jetAK8_mass          ->  at(iJet) ;
          leadingJetTau1       = jetAK8_tau1          ->  at(iJet) ;
          leadingJetTau2       = jetAK8_tau2          ->  at(iJet) ;
          leadingJetTau3       = jetAK8_tau3          ->  at(iJet) ;
        }
        if (jetAK8_mass->at(iJet) > WZmassCutLow  && jetAK8_mass->at(iJet) < WZmassCutHigh && !eventHasMatchedRawJet) {
          if(debugFlag) {
            cout << "    raw matched AK8 jet e is: "    << jetAK8_e    -> at(iJet) << endl ;
            cout << "    raw matched AK8 jet mass is: " << jetAK8_mass -> at(iJet) << endl ;
            cout << "    raw matched AK8 jet eta is: "  << jetAK8_eta  -> at(iJet) << endl ;
            cout << "    raw matched AK8 jet phi is: "  << jetAK8_phi  -> at(iJet) << endl ;
            cout << "    raw matched AK8 jet pt is: "   << jetAK8_pt   -> at(iJet) << endl ;
          }
          eventHasMatchedRawJet = true;
          matchedJet_raw.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
          raw_matchedJetTau1 = jetAK8_tau1 ->  at(iJet) ;
          raw_matchedJetTau2 = jetAK8_tau2 ->  at(iJet) ;
          raw_matchedJetTau3 = jetAK8_tau3 ->  at(iJet) ;
        }
        if (jetAK8_pruned_mass->at(iJet) > WZmassCutLow  && jetAK8_pruned_mass->at(iJet) < WZmassCutHigh && !eventHasMatchedPrunedJet) {
          if(debugFlag) {
            cout << "    pruned matched AK8 jet e is: "    << jetAK8_e->at(iJet)    << endl ;
            cout << "    pruned matched AK8 jet mass is: " << jetAK8_mass->at(iJet) << endl ;
            cout << "    pruned matched AK8 jet eta is: "  << jetAK8_eta->at(iJet)  << endl ;
            cout << "    pruned matched AK8 jet phi is: "  << jetAK8_phi->at(iJet)  << endl ;
            cout << "    pruned matched AK8 jet pt is: "   << jetAK8_pt->at(iJet)   << endl ;
          }
          eventHasMatchedPrunedJet = true;
          matchedJet_pruned.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
          pruned_matchedJetTau1 = jetAK8_tau1 ->  at(iJet) ;
          pruned_matchedJetTau2 = jetAK8_tau2 ->  at(iJet) ;
          pruned_matchedJetTau3 = jetAK8_tau3 ->  at(iJet) ;
        }
        if (jetAK8_softdrop_mass->at(iJet) > WZmassCutLow  && jetAK8_softdrop_mass->at(iJet) < WZmassCutHigh && !eventHasMatchedSoftdropJet) {
          if(debugFlag) {
            cout << "    softdrop matched AK8 jet e is: "    << jetAK8_e->at(iJet)    << endl ;
            cout << "    softdrop matched AK8 jet mass is: " << jetAK8_mass->at(iJet) << endl ;
            cout << "    softdrop matched AK8 jet eta is: "  << jetAK8_eta->at(iJet)  << endl ;
            cout << "    softdrop matched AK8 jet phi is: "  << jetAK8_phi->at(iJet)  << endl ;
            cout << "    softdrop matched AK8 jet pt is: "   << jetAK8_pt->at(iJet)   << endl ;
          }
          eventHasMatchedSoftdropJet = true;
          matchedJet_softdrop.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
          softdrop_matchedJetTau1 = jetAK8_tau1 ->  at(iJet) ;
          softdrop_matchedJetTau2 = jetAK8_tau2 ->  at(iJet) ;
          softdrop_matchedJetTau3 = jetAK8_tau3 ->  at(iJet) ;
        }
        HT+=jetAK8_pt->at(iJet);
     } 
    }
    leadingJetPtHist->Fill(leadingJetPt);
    HThist->Fill(HT);

    if (debugFlag) {  // Print some checks
      cout << "    eventHasTightPho is: " <<  eventHasTightPho  << endl;
      cout << "    leadingJetPt is: "     <<  leadingJetPt      << endl;
    }
 
    // Fill histograms with events that have a photon passing ID and a loose jet
    if (eventHasTightPho) {
      if (leadingJetPt > 0) {
        leadingJetTau1Hist         ->  Fill(leadingJetTau1)                   ;
        leadingJetTau2Hist         ->  Fill(leadingJetTau2)                   ;
        leadingJetTau3Hist         ->  Fill(leadingJetTau3)                   ;
        leadingJetT2T1             ->  Fill(leadingJetTau2/leadingJetTau1)    ;
        leadingJetT3T2             ->  Fill(leadingJetTau3/leadingJetTau2)    ;
        leadingJetMassHist         ->  Fill(leadingJetM)                      ;
        leadingJetPrunedMassHist   ->  Fill(leadingJetPrunedM)                ;
        leadingJetSoftdropMassHist ->  Fill(leadingJetSoftdropM)              ;
        leadingPhMassHist          ->  Fill(leadingPhE)                       ;
      }
      if(eventHasMatchedRawJet && matchedJet_raw.Pt() > 0) {
        sumVector = leadingPhoton + matchedJet_raw;
        if (debugFlag) cout << "    using matching with raw,      sumvector E is: " << sumVector.E() << endl;
        if (debugFlag) cout << "                                  sumvector M is: " << sumVector.M() << endl;
        if (debugFlag) cout << "                                    tau2/tau1 is: " << raw_matchedJetTau2/raw_matchedJetTau1 << endl;
        if (raw_matchedJetTau2/raw_matchedJetTau1<0.5) phJetInvMassHist_raw->Fill(sumVector.M());
      }
      if(eventHasMatchedPrunedJet && matchedJet_pruned.Pt() > 0) {
        sumVector = leadingPhoton + matchedJet_pruned;
        if (debugFlag) cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
        if (debugFlag) cout << "                                  sumvector M is: " << sumVector.M() << endl;
        if (debugFlag) cout << "                                    tau2/tau1 is: " << pruned_matchedJetTau2/pruned_matchedJetTau1 << endl;
        if (pruned_matchedJetTau2/pruned_matchedJetTau1<0.5) phJetInvMassHist_pruned->Fill(sumVector.M());
      }
      if(eventHasMatchedSoftdropJet && matchedJet_softdrop.Pt() > 0) {
        sumVector = leadingPhoton + matchedJet_softdrop;
        if (debugFlag) cout << "    using matching with softdrop, sumvector E is: " << sumVector.E() << endl;
        if (debugFlag) cout << "                                  sumvector M is: " << sumVector.M() << endl;
        if (debugFlag) cout << "                                    tau2/tau1 is: " <<softdrop_matchedJetTau2/softdrop_matchedJetTau1 << endl;
        if (softdrop_matchedJetTau2/softdrop_matchedJetTau1<0.5) phJetInvMassHist_softdrop->Fill(sumVector.M());
      }
    }
    if (debugFlag && entriesToCheck == jentry) break; // when debugFlag is true, break the event loop after reaching entriesToCheck 
  }


  outputFile->cd();

  leadingPhPtHist            -> Write();
  leadingJetPtHist           -> Write();
  HThist                     -> Write();
  leadingJetTau1Hist         -> Write();
  leadingJetTau2Hist         -> Write();
  leadingJetTau3Hist         -> Write();
  leadingJetT2T1             -> Write();
  leadingJetT3T2             -> Write();
  leadingPhMVAhist_endcap    -> Write();
  leadingPhMVAhist_barrel    -> Write();
  leadingJetMassHist         -> Write();
  leadingJetPrunedMassHist   -> Write();
  leadingJetSoftdropMassHist -> Write();
  leadingPhMassHist          -> Write();
  phJetInvMassHist_raw       -> Write();
  phJetInvMassHist_pruned    -> Write();
  phJetInvMassHist_softdrop  -> Write();
  outputFile->Close();
}
