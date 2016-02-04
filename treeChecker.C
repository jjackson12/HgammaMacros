#define treeChecker_cxx
#include "treeChecker.h"

using namespace std;

void treeChecker::Loop(string outputFileName)
{
  // Flags for running this macro
  bool debugFlag                    = false ;  // If debugFlag is false, the trigger checking couts won't appear and the loop won't stop when it reaches entriesToCheck
  bool checkTrigger                 = true ;
  bool dumpEventInfo                = false ;
  int  entriesToCheck               =   1   ;  // If debugFlag = true, stop once the number of checked entries reaches entriesToCheck
  int  reportEvery                  =  5000 ;

  // Photon id cut values
  //float endcap_phoMVAcut            = 0.336 ;  // See https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariatePhotonIdentificationRun2#Recommended_MVA_recipes_for_2015
  //float barrel_phoMVAcut            = 0.374 ;
  float endcap_phoMVAcut            = 0.336 ;  // See https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariatePhotonIdentificationRun2#Recommended_MVA_recipes_for_2015
  float barrel_phoMVAcut            = 0.374 ;
  float phoEtaMax                   =   2.4 ;
  float jetEtaMax                   =   2.4 ;
  float jetT2T1Max                  =   0.5 ;
  float phoEtaRanges[5]             = {0, 0.75, 1.479, 2.4, 3.0};

  // W/Z jet mass matching
  float WZmassCutLow                =   65. ;  // WZ mass window
  float WZmassCutHigh               =  105. ;

  // Z jet mass matching
  float sideLowCutLow              =   60. ;  
  float sideLowCutHigh             =   80. ;
  float ZmassCutLow                =   80. ;  // Z mass +- 10 GeV
  float ZmassCutHigh               =  100. ;
  float sideHiCutLow               =  100. ;  
  float sideHiCutHigh              =  120. ;

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
  fChain->SetBranchStatus( "jetAK4_pt"                ,  1 );  
  fChain->SetBranchStatus( "jetAK4_IDLoose"           ,  1 );  
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
    leadingPhCat_noID          = -1    ;
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
    eventHasSideHiPrunedJet   = false ;
    eventHasSideLowPrunedJet   = false ;
    eventHasMatchedSoftdropJet = false ;
    matchedRawJetMass          = -999. ;
    matchedPrunedJetCorrMass   = -999. ;
    sideLowPrunedJetCorrMass   = -999. ;
    sideHiPrunedJetCorrMass    = -999. ;
    matchedSoftdropJetCorrMass = -999. ;
    raw_matchedJetTau1         = -999. ;
    raw_matchedJetTau2         = -999. ;
    raw_matchedJetTau3         = -999. ;
    pruned_matchedJetTau1      = -999. ;
    pruned_matchedJetTau2      = -999. ;
    pruned_matchedJetTau3      = -999. ;
    pruned_sideLowJetTau1      = -999. ;
    pruned_sideLowJetTau2      = -999. ;
    pruned_sideLowJetTau3      = -999. ;
    pruned_sideHiJetTau1      = -999. ;
    pruned_sideHiJetTau2      = -999. ;
    pruned_sideHiJetTau3      = -999. ;
    softdrop_matchedJetTau1    = -999. ;
    softdrop_matchedJetTau2    = -999. ;
    softdrop_matchedJetTau3    = -999. ;
    HT                         = 0.    ;
    HT_ak4                     = 0.    ;
    phoIsTight                 = false ;
    phoEtaPassesCut            = false ;
    phoPtPassesCut             = false ;
    eventHasTightPho           = false ;
    eventHasMatchedRawJet      = false ;
    leadingPhMVA               = -999. ;
    leadingPhCat               = -999. ;
    triggerFired               = false ; 
    trigger2_Fired             = false ; 
    trigger3_Fired             = false ; 

    leadingPhoton       .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    matchedJet_raw      .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    matchedJet_pruned   .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sideHiJet_pruned   .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sideLowJet_pruned   .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    matchedJet_softdrop .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sumVector           .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    // Print out trigger information
    if (jentry%reportEvery==0) {
      cout << fixed << setw(4) << setprecision(2) << (float(jentry)/float(nentries))*100 << "% done: Scanned " << jentry << " events." << endl;
    }
    if (debugFlag) cout << "\nIn event number " << jentry << ":" << endl;
    if (checkTrigger && debugFlag) cout << "     Trigger info is: " << endl;
    for(map<string,bool>::iterator it = HLT_isFired->begin(); it != HLT_isFired->end(); ++it) {
      if (checkTrigger && debugFlag) { 
        cout << "       " << it->first << " = " << it->second << endl;
      }
      if (it->first == "HLT_Photon175_v1" || it->first == "HLT_Photon175_v2" ||  it->first == "HLT_Photon175_v3")  {
      //if (it->first == "HLT_Photon175_v1")  {
        if (debugFlag) cout << "    " << it->first << " has value: " << it->second << endl;
        triggerFired |= (1==it->second);
      }
      if (it->first == "HLT_Photon165_HE10_v1") {
      //if (it->first == "HLT_Photon165_HE10_v3") {
        if (debugFlag) cout << "    " << it->first << " has value: " << it->second << endl;
        trigger2_Fired = (1==it->second);
      }
      if (it->first == "HLT_Photon90_CaloIdL_PFHT500_v1") {
      //if (it->first == "HLT_Photon90_CaloIdL_PFHT500_v2") {
        if (debugFlag) cout << "    " << it->first << " has value: " << it->second << endl;
        trigger3_Fired = (1==it->second);
      }
    }
    if (triggerFired) ++eventsPassingTrigger;
    if (trigger2_Fired) ++eventsPassingTrigger_2;
    if (trigger3_Fired) ++eventsPassingTrigger_3;
    if (triggerFired || trigger3_Fired) ++eventsPassingTrigger_13;
    
    // Loop over photons
    for (uint iPh = 0; iPh<ph_pt->size() ; ++iPh) { 
      if (debugFlag && dumpEventInfo) {
        cout << "    Photon " << iPh << " has pT " << ph_pt->at(iPh)  << ", eta =" << ph_eta->at(iPh) << ", ph_mvaVal = " << ph_mvaVal->at(iPh) << ", ph_mvaCat = " << ph_mvaCat->at(iPh) << endl;
      }
      // Check if this event has a photon passing ID requirements
      phoIsTight = (ph_mvaCat->at(iPh)==0 && ph_mvaVal->at(iPh)>=barrel_phoMVAcut) || (ph_mvaCat->at(iPh)==1 && ph_mvaVal->at(iPh)>=endcap_phoMVAcut);
      phoEtaPassesCut = ( abs(ph_eta->at(iPh))<phoEtaMax );
      phoPtPassesCut = ( ph_pt->at(iPh)>100 );
      eventHasTightPho |= (phoIsTight && phoEtaPassesCut && phoPtPassesCut) ;      

      // Fill the leading photon variables, regardless of the ID
      if (ph_pt->at(iPh) > leadingPhPt_noID ) {
        leadingPhPt_noID  = ph_pt     ->  at(iPh) ;
        leadingPhE_noID   = ph_e      ->  at(iPh) ;
        leadingPhEta_noID = ph_eta    ->  at(iPh) ;
        leadingPhMVA_noID = ph_mvaVal ->  at(iPh) ;
        leadingPhCat_noID = ph_mvaCat ->  at(iPh) ;
      }

      // Fill the leading photon variables, requiring the photon to pass the ID requirements
      if (ph_pt->at(iPh) > leadingPhPt && phoIsTight && phoEtaPassesCut && phoPtPassesCut ) {
        leadingPhPt  = ph_pt     ->  at(iPh) ;
        leadingPhE   = ph_e      ->  at(iPh) ;
        leadingPhEta = ph_eta    ->  at(iPh) ;
        leadingPhPhi = ph_phi    ->  at(iPh) ;
        leadingPhMVA = ph_mvaVal ->  at(iPh) ;
        leadingPhCat = ph_mvaCat ->  at(iPh) ;
        leadingPhoton.SetPtEtaPhiE(ph_pt->at(iPh), ph_eta->at(iPh), ph_phi->at(iPh), ph_e->at(iPh));
      }
    }

    if (leadingPhCat_noID == 0) {
      leadingPhMVAhist_barrel->Fill(leadingPhMVA_noID);
    }
    else if (leadingPhCat_noID == 1) {
      leadingPhMVAhist_endcap->Fill(leadingPhMVA_noID);
    }

    if (debugFlag && eventHasTightPho && dumpEventInfo) cout << "    This event has a tight photon." << endl;

    for (uint iProf=0; iProf<sizeof(phMVAvsEProf)/sizeof(phMVAvsEProf[0]); ++iProf) { 
      if (abs(leadingPhEta_noID) > phoEtaRanges[iProf] && abs(leadingPhEta_noID) < phoEtaRanges[iProf+1]) phMVAvsEProf[iProf]->Fill(leadingPhE_noID, leadingPhMVA_noID );
    }

    // Loop over AK4 jets
    for (uint iJet = 0; iJet<jetAK4_pt->size() ; ++iJet) { 
      if (jetAK4_IDLoose->at(iJet) == 1) { 
        HT_ak4+=jetAK4_pt->at(iJet);
      }
    }
    HT_ak4hist->Fill(HT_ak4);

    // Loop over AK8 jets
    for (uint iJet = 0; iJet<jetAK8_pt->size() ; ++iJet) { 
      if (debugFlag && dumpEventInfo) cout << "    AK8 Jet " << iJet << " has pT " << jetAK8_pt->at(iJet) << endl;
      if (debugFlag && dumpEventInfo) cout << "    jetAK8_IDLoose[" << iJet << "] is : " << jetAK8_IDLoose->at(iJet) << endl;
 
      if (jetAK8_IDLoose->at(iJet) == 1) { 
      // Get leading jet variables, requiring loose jet ID
        tmpLeadingJet.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
        if (tmpLeadingJet.DeltaR(leadingPhoton) > 0.8 && (jetAK8_pt->at(iJet) > leadingJetPt)) {
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

        if (jetAK8_mass->at(iJet) > ZmassCutLow  && jetAK8_mass->at(iJet) < ZmassCutHigh && !eventHasMatchedRawJet) {
          eventHasMatchedRawJet = true;
          if(debugFlag && dumpEventInfo) {
            cout << "    raw matched AK8 jet e is: "    << jetAK8_e    -> at(iJet) << endl ;
            cout << "    raw matched AK8 jet mass is: " << jetAK8_mass -> at(iJet) << endl ;
            cout << "    raw matched AK8 jet eta is: "  << jetAK8_eta  -> at(iJet) << endl ;
            cout << "    raw matched AK8 jet phi is: "  << jetAK8_phi  -> at(iJet) << endl ;
            cout << "    raw matched AK8 jet pt is: "   << jetAK8_pt   -> at(iJet) << endl ;
          }
          matchedJet_raw.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
          matchedRawJetMass =  jetAK8_mass ->  at(iJet);
          raw_matchedJetTau1 = jetAK8_tau1 ->  at(iJet) ;
          raw_matchedJetTau2 = jetAK8_tau2 ->  at(iJet) ;
          raw_matchedJetTau3 = jetAK8_tau3 ->  at(iJet) ;
        }
        if (jetAK8_pruned_massCorr->at(iJet) > ZmassCutLow  && jetAK8_pruned_massCorr->at(iJet) < ZmassCutHigh && !eventHasMatchedPrunedJet) {
          eventHasMatchedPrunedJet = true;
          if(debugFlag && dumpEventInfo) {
            cout << "    pruned matched AK8 jet e is: "    << jetAK8_e->at(iJet)    << endl ;
            cout << "    pruned matched AK8 jet mass is: " << jetAK8_mass->at(iJet) << endl ;
            cout << "    pruned matched AK8 jet eta is: "  << jetAK8_eta->at(iJet)  << endl ;
            cout << "    pruned matched AK8 jet phi is: "  << jetAK8_phi->at(iJet)  << endl ;
            cout << "    pruned matched AK8 jet pt is: "   << jetAK8_pt->at(iJet)   << endl ;
          }
          matchedJet_pruned.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
          if (matchedJet_pruned.DeltaR(leadingPhoton) < 0.8) {
            matchedJet_pruned.SetPtEtaPhiE(0,0,0,0);
            eventHasMatchedPrunedJet = false;
          }
          else {
            matchedPrunedJetCorrMass = jetAK8_pruned_massCorr->at(iJet);
            pruned_matchedJetTau1 = jetAK8_tau1 ->  at(iJet) ;
            pruned_matchedJetTau2 = jetAK8_tau2 ->  at(iJet) ;
            pruned_matchedJetTau3 = jetAK8_tau3 ->  at(iJet) ;
          }
        }
        if (jetAK8_pruned_massCorr->at(iJet) > sideLowCutLow  && jetAK8_pruned_massCorr->at(iJet) < sideLowCutHigh && !eventHasSideLowPrunedJet) {
          eventHasSideLowPrunedJet = true;
          if(debugFlag && dumpEventInfo) {
            cout << "    pruned sideLow AK8 jet e is: "    << jetAK8_e->at(iJet)    << endl ;
            cout << "    pruned sideLow AK8 jet mass is: " << jetAK8_mass->at(iJet) << endl ;
            cout << "    pruned sideLow AK8 jet eta is: "  << jetAK8_eta->at(iJet)  << endl ;
            cout << "    pruned sideLow AK8 jet phi is: "  << jetAK8_phi->at(iJet)  << endl ;
            cout << "    pruned sideLow AK8 jet pt is: "   << jetAK8_pt->at(iJet)   << endl ;
          }
          sideLowJet_pruned.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
          if (sideLowJet_pruned.DeltaR(leadingPhoton) < 0.8) {
            sideLowJet_pruned.SetPtEtaPhiE(0,0,0,0);
            eventHasSideLowPrunedJet = false;
          }
          else {
            sideLowPrunedJetCorrMass = jetAK8_pruned_massCorr->at(iJet);
            pruned_sideLowJetTau1 = jetAK8_tau1 ->  at(iJet) ;
            pruned_sideLowJetTau2 = jetAK8_tau2 ->  at(iJet) ;
            pruned_sideLowJetTau3 = jetAK8_tau3 ->  at(iJet) ;
          }
        }
        if (jetAK8_pruned_massCorr->at(iJet) > sideHiCutLow  && jetAK8_pruned_massCorr->at(iJet) < sideHiCutHigh && !eventHasSideHiPrunedJet) {
          eventHasSideHiPrunedJet = true;
          if(debugFlag && dumpEventInfo) {
            cout << "    pruned sideHi AK8 jet e is: "    << jetAK8_e->at(iJet)    << endl ;
            cout << "    pruned sideHi AK8 jet mass is: " << jetAK8_mass->at(iJet) << endl ;
            cout << "    pruned sideHi AK8 jet eta is: "  << jetAK8_eta->at(iJet)  << endl ;
            cout << "    pruned sideHi AK8 jet phi is: "  << jetAK8_phi->at(iJet)  << endl ;
            cout << "    pruned sideHi AK8 jet pt is: "   << jetAK8_pt->at(iJet)   << endl ;
          }
          sideHiJet_pruned.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
          if (sideHiJet_pruned.DeltaR(leadingPhoton) < 0.8) {
            sideHiJet_pruned.SetPtEtaPhiE(0,0,0,0);
            eventHasSideHiPrunedJet = false;
          }
          else {
            sideHiPrunedJetCorrMass = jetAK8_pruned_massCorr->at(iJet);
            pruned_sideHiJetTau1 = jetAK8_tau1 ->  at(iJet) ;
            pruned_sideHiJetTau2 = jetAK8_tau2 ->  at(iJet) ;
            pruned_sideHiJetTau3 = jetAK8_tau3 ->  at(iJet) ;
          }
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
          matchedSoftdropJetCorrMass = jetAK8_softdrop_massCorr->at(iJet);
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

    if(eventHasMatchedRawJet && matchedJet_raw.Pt() > 0 && abs(matchedJet_raw.Eta()) < 2.4) {
      matchedJetMassHist_noPho ->Fill(matchedRawJetMass);
    }
    if(eventHasMatchedPrunedJet && matchedJet_pruned.Pt() > 0 && abs(matchedJet_pruned.Eta()) < 2.4) {
      matchedJetPrunedMassHist_noPho ->Fill(matchedPrunedJetCorrMass);
    }
    if(eventHasMatchedSoftdropJet && matchedJet_softdrop.Pt() > 0 && abs(matchedJet_softdrop.Eta()) < 2.4) {
      matchedJetSoftdropMassHist_noPho ->Fill(matchedSoftdropJetCorrMass);
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
      if(eventHasMatchedRawJet && matchedJet_raw.Pt() > 0 && abs(matchedJet_raw.Eta()) < 2.4 && abs(leadingPhoton.Eta()) < 2.4) {
        matchedJetMassHist ->Fill(matchedRawJetMass);
        sumVector = leadingPhoton + matchedJet_raw;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with raw,      sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << raw_matchedJetTau2/raw_matchedJetTau1 << endl;
        }
        if (raw_matchedJetTau2/raw_matchedJetTau1<0.5 && triggerFired && leadingPhoton.Pt() > 30) phJetInvMassHist_raw->Fill(sumVector.M());
      }
      if(eventHasSideLowPrunedJet && sideLowJet_pruned.Pt() > 100 && abs(sideLowJet_pruned.Eta()) < 2.4 && leadingPhoton.Pt()>200 && abs(leadingPhoton.Eta()) < 2.4) {
        sumVector = leadingPhoton + sideLowJet_pruned;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << pruned_sideLowJetTau2/pruned_sideLowJetTau1 << endl;
        }
                
        sideLowJett2t1Hist_noTrig->Fill(pruned_sideLowJetTau2/pruned_sideLowJetTau1);
        if (pruned_sideLowJetTau2/pruned_sideLowJetTau1<0.5 ) {
          phJetInvMassHist_pruned_sideLow_noTrig->Fill(sumVector.M());
          sideLowJetPtHist_noTrig->Fill(sideLowJet_pruned.Pt());
          sideLowJetEtaHist_noTrig->Fill(sideLowJet_pruned.Eta());
          sideLowJetPhiHist_noTrig->Fill(sideLowJet_pruned.Phi());
        }
        if (triggerFired ) {
          sideLowJett2t1Hist->Fill(pruned_sideLowJetTau2/pruned_sideLowJetTau1);
          if (pruned_sideLowJetTau2/pruned_sideLowJetTau1<0.5 ) {
            phJetInvMassHist_pruned_sideLow->Fill(sumVector.M());
            sideLowJetEtaHist->Fill(sideLowJet_pruned.Eta());
            sideLowJetPhiHist->Fill(sideLowJet_pruned.Phi());
            sideLowJetPtHist->Fill(sideLowJet_pruned.Pt());
          }
        }
        if (pruned_sideLowJetTau2/pruned_sideLowJetTau1<0.5) {
          sideLowJet_pruned.SetT(90);
          sumVector = leadingPhoton + sideLowJet_pruned;
          phCorrJetInvMassHist_pruned_sideLow_noTrig->Fill(sumVector.M());
          if (triggerFired)phCorrJetInvMassHist_pruned_sideLow->Fill(sumVector.M());
        }
      }
      if(eventHasSideHiPrunedJet && sideHiJet_pruned.Pt() > 30 && abs(sideHiJet_pruned.Eta()) < 2.4 && leadingPhoton.Pt()>30 && abs(leadingPhoton.Eta()) < 2.4) {
        sumVector = leadingPhoton + sideHiJet_pruned;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << pruned_sideHiJetTau2/pruned_sideHiJetTau1 << endl;
        }
                
        sideHiJett2t1Hist_noTrig->Fill(pruned_sideHiJetTau2/pruned_sideHiJetTau1);
        if (pruned_sideHiJetTau2/pruned_sideHiJetTau1<0.5 ) {
          phJetInvMassHist_pruned_sideHi_noTrig->Fill(sumVector.M());
          sideHiJetPtHist_noTrig->Fill(sideHiJet_pruned.Pt());
          sideHiJetEtaHist_noTrig->Fill(sideHiJet_pruned.Eta());
          sideHiJetPhiHist_noTrig->Fill(sideHiJet_pruned.Phi());
        }
        if (triggerFired ) {
          sideHiJett2t1Hist->Fill(pruned_sideHiJetTau2/pruned_sideHiJetTau1);
          if (pruned_sideHiJetTau2/pruned_sideHiJetTau1<0.5 ) {
            phJetInvMassHist_pruned_sideHi->Fill(sumVector.M());
            sideHiJetEtaHist->Fill(sideHiJet_pruned.Eta());
            sideHiJetPhiHist->Fill(sideHiJet_pruned.Phi());
            sideHiJetPtHist->Fill(sideHiJet_pruned.Pt());
          }
        }
        if (pruned_sideHiJetTau2/pruned_sideHiJetTau1<0.5) {
          sideHiJet_pruned.SetT(90);
          sumVector = leadingPhoton + sideHiJet_pruned;
          phCorrJetInvMassHist_pruned_sideHi_noTrig->Fill(sumVector.M());
          if (triggerFired)phCorrJetInvMassHist_pruned_sideHi->Fill(sumVector.M());
        }
      }
      if(eventHasMatchedPrunedJet && matchedJet_pruned.Pt() > 100 && abs(matchedJet_pruned.Eta()) < 2.4 && leadingPhoton.Pt()>200 && abs(leadingPhoton.Eta()) < 2.4) {
        matchedJetPrunedMassHist_noTrig ->Fill(matchedPrunedJetCorrMass);
        phJetDeltaPhi_pruned_noTrig->Fill(leadingPhoton.DeltaPhi(matchedJet_pruned));
        phJetDeltaEta_pruned_noTrig->Fill(abs( leadingPhoton.Eta() - matchedJet_pruned.Eta() ));
        phJetDeltaR_pruned_noTrig->Fill(leadingPhoton.DeltaR(matchedJet_pruned));
        leadingPhPtHist_noTrig->Fill(leadingPhPt);
        sumVector = leadingPhoton + matchedJet_pruned;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << pruned_matchedJetTau2/pruned_matchedJetTau1 << endl;
        }
                
        matchedJett2t1Hist_noTrig->Fill(pruned_matchedJetTau2/pruned_matchedJetTau1);
        if (pruned_matchedJetTau2/pruned_matchedJetTau1<0.5 ) {
          phJetInvMassHist_pruned_sig_noTrig->Fill(sumVector.M());
          matchedJetPtHist_noTrig->Fill( matchedJet_pruned.Pt());
          matchedJetEtaHist_noTrig->Fill(matchedJet_pruned.Eta());
          matchedJetPhiHist_noTrig->Fill(matchedJet_pruned.Phi());
        }
        if (triggerFired ) {
          matchedJett2t1Hist->Fill(pruned_matchedJetTau2/pruned_matchedJetTau1);
          if (pruned_matchedJetTau2/pruned_matchedJetTau1<0.5 && leadingPhoton.DeltaR(matchedJet_pruned)>0.8) {
            phJetDeltaPhi_pruned->Fill(leadingPhoton.DeltaPhi(matchedJet_pruned));
            phJetDeltaEta_pruned->Fill(abs( leadingPhoton.Eta() - matchedJet_pruned.Eta() ));
            phJetDeltaR_pruned->Fill(leadingPhoton.DeltaR(matchedJet_pruned));
            leadingPhPtHist->Fill(leadingPhPt);
            leadingPhEtaHist->Fill(leadingPhEta);
            leadingPhPhiHist->Fill(leadingPhPhi);
            phJetInvMassHist_pruned_sig->Fill(sumVector.M());
            matchedJetPrunedMassHist ->Fill(matchedPrunedJetCorrMass);
            bigWindowJetPrunedMassHist->Fill(matchedPrunedJetCorrMass);
            matchedJetPtHist->Fill( matchedJet_pruned.Pt());
            matchedJetEtaHist->Fill(matchedJet_pruned.Eta());
            matchedJetPhiHist->Fill(matchedJet_pruned.Phi());
            phPtOverMgammajHist->Fill(leadingPhPt/sumVector.M());
          }
        }
        if (pruned_matchedJetTau2/pruned_matchedJetTau1<0.5) {
          matchedJet_pruned.SetT(90);
          sumVector = leadingPhoton + matchedJet_pruned;
          phCorrJetInvMassHist_pruned_sig_noTrig->Fill(sumVector.M());
          if (triggerFired)phCorrJetInvMassHist_pruned_sig->Fill(sumVector.M());
        }
      }
      if(eventHasSideHiPrunedJet && sideHiJet_pruned.Pt() > 100 && abs(sideHiJet_pruned.Eta()) < 2.4 && leadingPhoton.Pt()>200 && abs(leadingPhoton.Eta()) < 2.4) {
        if (triggerFired ) {
          if (pruned_sideHiJetTau2/pruned_sideHiJetTau1<0.5 && leadingPhoton.DeltaR(sideHiJet_pruned)>0.8) {
            sideHiJetPrunedMassHist ->Fill(sideHiPrunedJetCorrMass);
            bigWindowJetPrunedMassHist->Fill(sideHiPrunedJetCorrMass);
          }
        }
      }
      if(eventHasSideLowPrunedJet && sideLowJet_pruned.Pt() > 100 && abs(sideLowJet_pruned.Eta()) < 2.4 && leadingPhoton.Pt()>200 && abs(leadingPhoton.Eta()) < 2.4) {
        if (triggerFired ) {
          if (pruned_sideLowJetTau2/pruned_sideLowJetTau1<0.5 && leadingPhoton.DeltaR(sideLowJet_pruned)>0.8) {
            sideLowJetPrunedMassHist ->Fill(sideLowPrunedJetCorrMass);
            bigWindowJetPrunedMassHist->Fill(sideLowPrunedJetCorrMass);
          }
        }
      }
      if(eventHasMatchedSoftdropJet && matchedJet_softdrop.Pt() > 0 && abs(matchedJet_softdrop.Eta()) < 2.4 && abs(leadingPhoton.Eta()) < 2.4) {
        matchedJetSoftdropMassHist ->Fill(matchedSoftdropJetCorrMass);
        sumVector = leadingPhoton + matchedJet_softdrop;
        if (debugFlag && dumpEventInfo)  {
          cout << "    using matching with softdrop, sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " <<softdrop_matchedJetTau2/softdrop_matchedJetTau1 << endl;
        }
        if (softdrop_matchedJetTau2/softdrop_matchedJetTau1<0.5 && triggerFired && leadingPhoton.Pt() > 200) phJetInvMassHist_softdrop->Fill(sumVector.M());
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

  outputFile ->       mkdir("Jet_kinematics") ;
  outputFile ->          cd("Jet_kinematics") ;
  leadingJetPtHist                 -> Write() ;
  leadingJetEtaHist                -> Write() ;
  leadingJetPhiHist                -> Write() ;
  leadingJetMassHist               -> Write() ;
  HThist                           -> Write() ;
  HT_ak4hist                       -> Write() ;

  outputFile ->     mkdir("Jet_substructure") ;
  outputFile ->        cd("Jet_substructure") ;
  leadingJetTau1Hist               -> Write() ;
  leadingJetTau2Hist               -> Write() ;
  leadingJetTau3Hist               -> Write() ;
  leadingJetT2T1                   -> Write() ;
  leadingJetT3T2                   -> Write() ;
  leadingJetPrunedMassHist         -> Write() ;
  leadingJetSoftdropMassHist       -> Write() ;
  matchedJett2t1Hist               -> Write() ;

  outputFile ->            mkdir("Resonance") ;
  outputFile ->               cd("Resonance") ;
  phJetInvMassHist_raw             -> Write() ;
  //phJetInvMassHist_pruned          -> Write() ;
  //phCorrJetInvMassHist_pruned      -> Write() ;
  //phJetInvMassHist_pruned_noTrig   -> Write() ;
  //phCorrJetInvMassHist_pruned_noTrig   -> Write() ;
  phJetInvMassHist_softdrop        -> Write() ;
  matchedJetMassHist               -> Write() ;
  matchedJetPrunedMassHist         -> Write() ;
  matchedJetSoftdropMassHist       -> Write() ;
  matchedJetPtHist                 -> Write() ;
  matchedJetEtaHist                -> Write() ;
  matchedJetPhiHist                -> Write() ;
  matchedJetMassHist_noPho         -> Write() ;
  matchedJetPrunedMassHist_noPho   -> Write() ;
  matchedJetSoftdropMassHist_noPho -> Write() ;
  phJetDeltaR_pruned_noTrig        -> Write() ;
  phJetDeltaPhi_pruned_noTrig      -> Write() ;
  phJetDeltaEta_pruned_noTrig      -> Write() ;
  phJetDeltaR_pruned               -> Write() ;
  phJetDeltaPhi_pruned             -> Write() ;
  phJetDeltaEta_pruned             -> Write() ;
  phJetInvMassHist_pruned_sig      -> Write() ;
  phJetInvMassHist_pruned_sideHi   -> Write() ;
  phJetInvMassHist_pruned_sideLow  -> Write() ;
  sideHiJetPrunedMassHist          -> Write() ;
  sideLowJetPrunedMassHist         -> Write() ;
  bigWindowJetPrunedMassHist       -> Write() ;
  phCorrJetInvMassHist_pruned_sig            -> Write() ;
  phCorrJetInvMassHist_pruned_sideHi         -> Write() ;
  phCorrJetInvMassHist_pruned_sideLow        -> Write() ;
  phJetInvMassHist_pruned_sig_noTrig         -> Write() ;
  phJetInvMassHist_pruned_sideHi_noTrig      -> Write() ;
  phJetInvMassHist_pruned_sideLow_noTrig     -> Write() ;
  phCorrJetInvMassHist_pruned_sig_noTrig     -> Write() ;
  phCorrJetInvMassHist_pruned_sideHi_noTrig  -> Write() ;
  phCorrJetInvMassHist_pruned_sideLow_noTrig -> Write() ;
  phPtOverMgammajHist                        -> Write() ;

  outputFile ->       mkdir("Trigger_turnon") ;
  outputFile ->          cd("Trigger_turnon") ;
  leadingPhPtHist                  -> Write() ;
  leadingPhPtHist_noTrig           -> Write() ;
  leadingPhPt_noIDHist             -> Write() ;
  leadingPhPt_noIDHist_trig        -> Write() ;

  outputFile->Close();

  cout << "100% done: Scanned " << nentries << " events." << endl;
  cout << "The trigger fired " << eventsPassingTrigger << " times" << endl;
  cout << "The trigger2 fired " << eventsPassingTrigger_2 << " times" << endl;
  cout << "The trigger3 fired " << eventsPassingTrigger_3 << " times" << endl;
  cout << "The trigger efficiency was " << (float) eventsPassingTrigger/ (float)nentries << endl;
  cout << "The trigger_2 efficiency was " << (float) eventsPassingTrigger_2/ (float)nentries << endl;
  cout << "The trigger_3 efficiency was " << (float) eventsPassingTrigger_3/ (float)nentries << endl;
  cout << "The trigger_13 efficiency was " << (float) eventsPassingTrigger_13/ (float)nentries << endl;
  cout << "\nCompleted output file is " << outputFileName.c_str() <<".\n" << endl;
}
