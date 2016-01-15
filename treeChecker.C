#define treeChecker_cxx
#include "treeChecker.h"

using namespace std;

void treeChecker::Loop(string outputFileName)
{
  // Flags for running this macro
  bool debugFlag                    = false ;  // If debugFlag is false, the trigger checking couts won't appear and the loop won't stop when it reaches entriesToCheck
  bool checkTrigger                 = false ;
  bool dumpEventInfo                = false ;
  int  entriesToCheck               =   100 ;  // If debugFlag = true, stop once the number of checked entries reaches entriesToCheck
  int  reportEvery                  =  2000 ;

  // Photon id cut values
  float endcap_phoMVAcut            = 0.336 ;  // See https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariatePhotonIdentificationRun2#Recommended_MVA_recipes_for_2015
  float barrel_phoMVAcut            = 0.374 ;
  float phoEtaMax                   =   2.4 ;
  float phoEtaRanges[5]             = {0, 0.75, 1.479, 2.4, 3.0};

  // W/Z jet mass matching
  float WZmassCutLow                =   65. ;  // Z mass +- 15 GeV
  float WZmassCutHigh               =  105. ;

  TFile* outputFile                 = new TFile(outputFileName.c_str(), "RECREATE");


  // Create TProfiles
  char *profTitle = new char[15];
  for (uint iProf=0; iProf<sizeof(phMVAvsEProf)/sizeof(phMVAvsEProf[0]); ++iProf) { 
    sprintf(profTitle, "phMVAvsEProf%d", iProf);
    phMVAvsEProf[iProf] = new TProfile(profTitle, "Photon ID MVA value profile vs. E_{#gamma}", 400, 0, 4000);
  }

  // Branches from EXOVVNtuplizer tree
  fChain->SetBranchStatus( "*"                        ,  0 );  // disable all branches
  fChain->SetBranchStatus( "HLT_isFired"              ,  1 );  // activate select branches
  fChain->SetBranchStatus( "ph_pt"                    ,  1 );  
  fChain->SetBranchStatus( "ph_e"                     ,  1 );  
  fChain->SetBranchStatus( "ph_eta"                   ,  1 );  
  fChain->SetBranchStatus( "ph_phi"                   ,  1 );  
  fChain->SetBranchStatus( "ph_mvaVal"                ,  1 );
  fChain->SetBranchStatus( "ph_mvaCat"                ,  1 );
  fChain->SetBranchStatus( "jetAK8_pt"                ,  1 );  
  fChain->SetBranchStatus( "jetAK8_mass"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_pruned_massCorr"   ,  1 );
  fChain->SetBranchStatus( "jetAK8_softdrop_massCorr" ,  1 );  
  fChain->SetBranchStatus( "jetAK8_e"                 ,  1 );  
  fChain->SetBranchStatus( "jetAK8_eta"               ,  1 );  
  fChain->SetBranchStatus( "jetAK8_phi"               ,  1 );  
  fChain->SetBranchStatus( "jetAK8_tau1"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_tau2"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_tau3"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_IDLoose"           ,  1 );  

  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;

  cout << "\n\nStarting treeChecker::Loop().\n" << endl;
  // Loop over all events
  for (Long64_t jentry=0; jentry<nentries;++jentry) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;


    leadingPhPt                = 0.    ;
    leadingPhEta               = -999  ;
    leadingPhPhi               = -999  ;
    leadingPhPt_noID           = 0.    ;
    leadingPhE                 = 0.    ;
    leadingPhE_noID            = 0.    ;
    leadingPhEta_noID          = -999. ;
    leadingPhMVA_noID          = -999. ;
    leadingJetPt               = 0.    ;
    leadingJetE                = 0.    ;
    leadingJetEta              = -999. ;
    leadingJetPhi              = -999  ;
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
    phoEtaPassesCut            = false ;
    eventHasTightPho           = false ;
    eventHasMatchedRawJet      = false ;
    leadingPhMVA               = -999. ;
    leadingPhCat               = -999. ;
    triggerFired               = false ; 

    leadingPhoton       .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    matchedJet_raw      .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    matchedJet_pruned   .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    matchedJet_softdrop .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sumVector           .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    // Print out trigger information
    if (jentry%reportEvery==0) {
      cout << fixed << setw(4) << setprecision(2) << (float(jentry)/float(nentries))*100 << "% done: Scanned " << jentry << " events." << endl;
    }
    if (debugFlag) cout << "\nIn event number " << jentry << ":" << endl;
    if (checkTrigger) cout << "     Trigger info is: " << endl;
    for(map<string,bool>::iterator it = HLT_isFired->begin(); it != HLT_isFired->end(); ++it) {
      if (checkTrigger) { 
        cout << "       " << it->first << " = " << it->second << endl;
      }
      if (it->first == "HLT_Photon175_v1") {
        if (debugFlag) cout << "    " << it->first << " has value: " << it->second << endl;
        triggerFired = (1==it->second);
      }
    }
    
    // Loop over photons
    for (uint iPh = 0; iPh<ph_pt->size() ; ++iPh) { 
      if (debugFlag && dumpEventInfo) {
        cout << "    Photon " << iPh << " has pT " << ph_pt->at(iPh)  << ", eta =" << ph_eta->at(iPh) << ", ph_mvaVal = " << ph_mvaVal->at(iPh) << ", ph_mvaCat = " << ph_mvaCat->at(iPh) << endl;
      }
      // Check if this event has a photon passing ID requirements
      phoIsTight = (ph_mvaCat->at(iPh)==0 && ph_mvaVal->at(iPh)>=barrel_phoMVAcut) || (ph_mvaCat->at(iPh)==1 && ph_mvaVal->at(iPh)>=endcap_phoMVAcut);
      phoEtaPassesCut = ( abs(ph_eta->at(iPh))<phoEtaMax );
      eventHasTightPho |= (phoIsTight && phoEtaPassesCut) ;      
      // Fill the leading photon variables, requiring the photon to pass the ID requirements
      if (ph_pt->at(iPh) > leadingPhPt_noID ) {
        leadingPhPt_noID  = ph_pt     ->  at(iPh) ;
        leadingPhE_noID   = ph_e      ->  at(iPh) ;
        leadingPhEta_noID = ph_eta    ->  at(iPh) ;
        leadingPhMVA_noID = ph_mvaVal ->  at(iPh) ;
      }
      if (ph_pt->at(iPh) > leadingPhPt && phoIsTight && phoEtaPassesCut ) {
        leadingPhPt  = ph_pt     ->  at(iPh) ;
        leadingPhE   = ph_e      ->  at(iPh) ;
        leadingPhEta = ph_eta    ->  at(iPh) ;
        leadingPhPhi = ph_phi    ->  at(iPh) ;
        leadingPhMVA = ph_mvaVal ->  at(iPh) ;
        leadingPhCat = ph_mvaCat ->  at(iPh) ;
        leadingPhoton.SetPtEtaPhiE(ph_pt->at(iPh), ph_eta->at(iPh), ph_phi->at(iPh), ph_e->at(iPh));
      }
    }
    if (debugFlag && eventHasTightPho && dumpEventInfo) cout << "    This event has a tight photon." << endl;
    leadingPhPtHist->Fill(leadingPhPt);
    leadingPhEtaHist->Fill(leadingPhEta);
    leadingPhPhiHist->Fill(leadingPhPhi);
    leadingPhPtHist_noTrig->Fill(leadingPhPt);
    if(triggerFired) leadingPhPtHist_trig->Fill(leadingPhPt);
    if (leadingPhCat == 0) {
      leadingPhMVAhist_barrel->Fill(leadingPhMVA);
    }
    else if (leadingPhCat == 1) {
      leadingPhMVAhist_endcap->Fill(leadingPhMVA);
    }

    for (uint iProf=0; iProf<sizeof(phMVAvsEProf)/sizeof(phMVAvsEProf[0]); ++iProf) { 
      if (abs(leadingPhEta_noID) > phoEtaRanges[iProf] && abs(leadingPhEta_noID) < phoEtaRanges[iProf+1]) phMVAvsEProf[iProf]->Fill(leadingPhE_noID, leadingPhMVA_noID );
    }

    // Loop over jets
    for (uint iJet = 0; iJet<jetAK8_pt->size() ; ++iJet) { 
      if (debugFlag && dumpEventInfo) cout << "    AK8 Jet " << iJet << " has pT " << jetAK8_pt->at(iJet) << endl;
      if (debugFlag && dumpEventInfo) cout << "    jetAK8_IDLoose[" << iJet << "] is : " << jetAK8_IDLoose->at(iJet) << endl;
 
      if (jetAK8_IDLoose->at(iJet) == 1) { 
      // Get leading jet variables, requiring loose jet ID
        if (jetAK8_pt->at(iJet) > leadingJetPt) {
          leadingJetPt   = jetAK8_pt->at(iJet);
          leadingJetEta  = jetAK8_eta->at(iJet);
          leadingJetPhi  = jetAK8_phi->at(iJet);
          //if (leadingJetE > jetAK8_e->at(iJet)) cout << "A leading jet (highest pT) had lower energy than another jet.";
          leadingJetE          = jetAK8_e                 ->  at(iJet) ;
          leadingJetM          = jetAK8_mass              ->  at(iJet) ;
          leadingJetPrunedM    = jetAK8_pruned_massCorr   ->  at(iJet);
          leadingJetSoftdropM  = jetAK8_softdrop_massCorr ->  at(iJet);
          leadingJetTau1       = jetAK8_tau1              ->  at(iJet) ;
          leadingJetTau2       = jetAK8_tau2              ->  at(iJet) ;
          leadingJetTau3       = jetAK8_tau3              ->  at(iJet) ;
        }
        if (jetAK8_mass->at(iJet) > WZmassCutLow  && jetAK8_mass->at(iJet) < WZmassCutHigh && !eventHasMatchedRawJet) {
          if(debugFlag && dumpEventInfo) {
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
        if (jetAK8_pruned_massCorr->at(iJet) > WZmassCutLow  && jetAK8_pruned_massCorr->at(iJet) < WZmassCutHigh && !eventHasMatchedPrunedJet) {
          if(debugFlag && dumpEventInfo) {
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
        if (jetAK8_softdrop_massCorr->at(iJet) > WZmassCutLow  && jetAK8_softdrop_massCorr->at(iJet) < WZmassCutHigh && !eventHasMatchedSoftdropJet) {
          if(debugFlag && dumpEventInfo) {
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
    leadingJetPtHist  ->  Fill(leadingJetPt)  ;
    leadingJetEtaHist ->  Fill(leadingJetEta) ;
    leadingJetPhiHist ->  Fill(leadingJetPhi) ;
    HThist->Fill(HT);

    if (debugFlag && dumpEventInfo) {  // Print some checks
      cout << "    eventHasTightPho is: " <<  eventHasTightPho  << endl;
      cout << "    leadingJetPt is: "     <<  leadingJetPt      << endl;
    }
    if (debugFlag) cout <<  "Leading photon with no ID has pT: " << leadingPhPt_noID << " and triggerFired is: " << triggerFired << endl;
    leadingPhPt_noIDHist->Fill(leadingPhPt_noID);
    if (triggerFired) leadingPhPt_noIDHist_trig->Fill(leadingPhPt_noID);   
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
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with raw,      sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << raw_matchedJetTau2/raw_matchedJetTau1 << endl;
        }
        if (raw_matchedJetTau2/raw_matchedJetTau1<0.5) phJetInvMassHist_raw->Fill(sumVector.M());
      }
      if(eventHasMatchedPrunedJet && matchedJet_pruned.Pt() > 0) {
        sumVector = leadingPhoton + matchedJet_pruned;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << pruned_matchedJetTau2/pruned_matchedJetTau1 << endl;
        }
        if (pruned_matchedJetTau2/pruned_matchedJetTau1<0.5) phJetInvMassHist_pruned->Fill(sumVector.M());
      }
      if(eventHasMatchedSoftdropJet && matchedJet_softdrop.Pt() > 0) {
        sumVector = leadingPhoton + matchedJet_softdrop;
        if (debugFlag && dumpEventInfo)  {
          cout << "    using matching with softdrop, sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " <<softdrop_matchedJetTau2/softdrop_matchedJetTau1 << endl;
        }
        if (softdrop_matchedJetTau2/softdrop_matchedJetTau1<0.5) phJetInvMassHist_softdrop->Fill(sumVector.M());
      }
    }
    if (debugFlag && entriesToCheck == jentry) break; // when debugFlag is true, break the event loop after reaching entriesToCheck 
  }


  outputFile->cd();

  outputFile -> mkdir("Photon_kinematics") ;
  outputFile ->    cd("Photon_kinematics") ;
  leadingPhPtHist               -> Write() ;
  leadingPhEtaHist              -> Write() ;
  leadingPhPhiHist              -> Write() ;
  leadingPhMassHist             -> Write() ;

  outputFile ->         mkdir("Photon_id") ;
  outputFile ->            cd("Photon_id") ;
  leadingPhMVAhist_endcap       -> Write() ;
  leadingPhMVAhist_barrel       -> Write() ;
  for (uint iProf=0; iProf<sizeof(phMVAvsEProf)/sizeof(phMVAvsEProf[0]); ++iProf) { 
    phMVAvsEProf[iProf]->Write();
  }

  outputFile ->    mkdir("Jet_kinematics") ;
  outputFile ->       cd("Jet_kinematics") ;
  leadingJetPtHist              -> Write() ;
  leadingJetEtaHist             -> Write() ;
  leadingJetPhiHist             -> Write() ;
  leadingJetMassHist            -> Write() ;
  HThist                        -> Write() ;

  outputFile ->  mkdir("Jet_substructure") ;
  outputFile ->     cd("Jet_substructure") ;
  leadingJetTau1Hist            -> Write() ;
  leadingJetTau2Hist            -> Write() ;
  leadingJetTau3Hist            -> Write() ;
  leadingJetT2T1                -> Write() ;
  leadingJetT3T2                -> Write() ;
  leadingJetPrunedMassHist      -> Write() ;
  leadingJetSoftdropMassHist    -> Write() ;

  outputFile ->         mkdir("Resonance") ;
  outputFile ->            cd("Resonance") ;
  phJetInvMassHist_raw          -> Write() ;
  phJetInvMassHist_pruned       -> Write() ;
  phJetInvMassHist_softdrop     -> Write() ;

  outputFile ->    mkdir("Trigger_turnon") ;
  outputFile ->       cd("Trigger_turnon") ;
  leadingPhPtHist_trig          -> Write() ;
  leadingPhPtHist_noTrig        -> Write() ;
  leadingPhPt_noIDHist          -> Write() ;
  leadingPhPt_noIDHist_trig     -> Write() ;

  outputFile->Close();
  cout << "100% done: Scanned " << nentries << " events." << endl;
  cout << "\nCompleted output file is " << outputFileName.c_str() <<".\n" << endl;
}
