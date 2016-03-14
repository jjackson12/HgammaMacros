#define treeChecker_cxx
#include "treeChecker.h"

using namespace std;

void treeChecker::Loop(string outputFileName)
{
  // Flags for running this macro
  bool debugFlag                    = false ;  // If debugFlag is false, the trigger checking couts won't appear and the loop won't stop when it reaches entriesToCheck
  bool checkTrigger                 = false ;
  bool dumpEventInfo                = false ;
  int  entriesToCheck               =  30000   ;  // If debugFlag = true, stop once the number of checked entries reaches entriesToCheck
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
  float bigWindowLowCutLow              =   0.  ;  
  float bigWindowLowCutHigh             =   75. ;
  float sidebandThreeCutLow               = 50.;
  float sidebandThreeCutHigh               = 70.;
  float sidebandFourCutLow               = 100.;
  float sidebandFourCutHigh               = 110.;
  float ZmassCutLow                =   75. ;  // Z mass +- 15 GeV
  float ZmassCutHigh               =  105. ;
  float HmassCutLow                =  110. ;
  float HmassCutHigh                =  140. ;
  float bigWindowHiCutLow               =  105. ;  
  float bigWindowHiCutHigh              =  200. ;

  //outputTree->Branch("leadingPhMVA", &leadingPhMVA);
  //outputTree->Branch("leadingPhCat", &leadingPhCat);
  TFile* outputFile                 = new TFile(outputFileName.c_str(), "RECREATE");

  TTree* outputTreeSig                 = new TTree("sig", "sig");
  TTree* outputTreeHiggs                 = new TTree("higgs", "higgs");
  TTree* outputTree5070                 = new TTree("side5070", "side5070");
  TTree* outputTree100110                 = new TTree("side100110", "side100110");
  outputTreeSig->Branch("matchedJett2t1", &matchedJett2t1);
  outputTreeSig->Branch("cosThetaStar", &cosThetaStar);
  outputTreeSig->Branch("phPtOverMgammaj", &phPtOverMgammaj);
  outputTreeSig->Branch("leadingPhEta", &leadingPhEta);
  outputTreeSig->Branch("leadingPhPhi", &leadingPhPhi);
  outputTreeSig->Branch("leadingPhPt", &leadingPhPt);
  outputTreeSig->Branch("leadingPhAbsEta", &leadingPhAbsEta);
  outputTreeSig->Branch("phJetInvMass_pruned_sig", &phJetInvMass_pruned_sig);
  outputTreeSig->Branch("phJetDeltaR_sig", &phJetDeltaR_sig);
  outputTreeSig->Branch("matchedJet_pruned_abseta", &matchedJet_pruned_abseta);
  outputTreeSig->Branch("matchedPrunedJetCorrMass", &matchedPrunedJetCorrMass);
  outputTreeSig->Branch("matchedJett2t1", &matchedJett2t1);
  outputTreeHiggs->Branch("higgsJett2t1", &higgsJett2t1);
  outputTreeHiggs->Branch("cosThetaStar", &cosThetaStar);
  outputTreeHiggs->Branch("phPtOverMgammaj", &phPtOverMgammaj);
  outputTreeHiggs->Branch("leadingPhEta", &leadingPhEta);
  outputTreeHiggs->Branch("leadingPhPhi", &leadingPhPhi);
  outputTreeHiggs->Branch("leadingPhPt", &leadingPhPt);
  outputTreeHiggs->Branch("leadingPhAbsEta", &leadingPhAbsEta);
  outputTreeHiggs->Branch("phJetInvMass_pruned_higgs", &phJetInvMass_pruned_higgs);
  outputTreeHiggs->Branch("phJetDeltaR_higgs", &phJetDeltaR_higgs);
  outputTreeHiggs->Branch("higgsJet_pruned_abseta", &higgsJet_pruned_abseta);
  outputTreeHiggs->Branch("higgsPrunedJetCorrMass", &higgsPrunedJetCorrMass);
  outputTree5070->Branch("sideLowThreeJett2t1", &sideLowThreeJett2t1);
  outputTree5070->Branch("cosThetaStar", &cosThetaStar);
  outputTree5070->Branch("phPtOverMgammaj", &phPtOverMgammaj);
  outputTree5070->Branch("leadingPhEta", &leadingPhEta);
  outputTree5070->Branch("leadingPhPhi", &leadingPhPhi);
  outputTree5070->Branch("leadingPhPt", &leadingPhPt);
  outputTree5070->Branch("phJetInvMass_pruned_sideLowThree", &phJetInvMass_pruned_sideLowThree);
  outputTree5070->Branch("phJetDeltaR_sideLowThree", &phJetDeltaR_sideLowThree);
  outputTree5070->Branch("leadingPhAbsEta", &leadingPhAbsEta);
  outputTree5070->Branch("sideLowThreeJet_pruned_abseta", &sideLowThreeJet_pruned_abseta);
  outputTree5070->Branch("sideLowThreePrunedJetCorrMass", &sideLowThreePrunedJetCorrMass);
  outputTree5070->Branch("sideLowThreeJet_HbbTag", &sideLowThreeJet_HbbTag);
  outputTree100110->Branch("sideLowFourJett2t1", &sideLowFourJett2t1);
  outputTree100110->Branch("cosThetaStar", &cosThetaStar);
  outputTree100110->Branch("phPtOverMgammaj", &phPtOverMgammaj);
  outputTree100110->Branch("leadingPhEta", &leadingPhEta);
  outputTree100110->Branch("leadingPhPhi", &leadingPhPhi);
  outputTree100110->Branch("leadingPhPt", &leadingPhPt);
  outputTree100110->Branch("phJetInvMass_pruned_sideLowFour", &phJetInvMass_pruned_sideLowFour);
  outputTree100110->Branch("phJetDeltaR_sideLowFour", &phJetDeltaR_sideLowFour);
  outputTree100110->Branch("leadingPhAbsEta", &leadingPhAbsEta);
  outputTree100110->Branch("sideLowFourJet_pruned_abseta", &sideLowFourJet_pruned_abseta);
  outputTree100110->Branch("sideLowFourPrunedJetCorrMass", &sideLowFourPrunedJetCorrMass);
  outputTree100110->Branch("sideLowFourJet_HbbTag", &sideLowFourJet_HbbTag);
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
  fChain->SetBranchStatus( "ph_passEleVeto"                ,  1 );
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
  fChain->SetBranchStatus( "jetAK8_IDTight"           ,  1 );  
  fChain->SetBranchStatus( "jetAK8_IDTightLepVeto"           ,  1 );  
  fChain->SetBranchStatus( "jetAK8_Hbbtag"           ,  1 );  

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
    leadingPhE                 = 0.    ;
    eventHasMatchedPrunedJet   = false ;
    eventHasHiggsPrunedJet   = false ;
    eventHasSideHiPrunedJet   = false ;
    eventHasSideLowPrunedJet   = false ;
    eventHasSideLowThreePrunedJet   = false ;
    eventHasSideLowFourPrunedJet   = false ;
    eventHasMatchedSoftdropJet = false ;
    matchedPrunedJetCorrMass   = -999. ;
    higgsPrunedJetCorrMass   = -999. ;
    matchedJet_HbbTag          = -999. ;
    higgsJet_HbbTag          = -999. ;
    sideLowPrunedJetCorrMass   = -999. ;
    sideHiPrunedJetCorrMass    = -999. ;
    matchedSoftdropJetCorrMass = -999. ;
    pruned_matchedJetTau1      = -999. ;
    pruned_higgsJetTau1      = -999. ;
    pruned_matchedJetTau2      = -999. ;
    pruned_higgsJetTau2      = -999. ;
    pruned_matchedJetTau3      = -999. ;
    pruned_higgsJetTau3      = -999. ;
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
//    HT_ak4                     = 0.    ;
    phoIsTight                 = false ;
    phoEtaPassesCut            = false ;
    phoPtPassesCut             = false ;
    eventHasTightPho           = false ;
    leadingPhMVA               = -999. ;
    leadingPhCat               = -999. ;
    triggerFired               = false ; 
    leadingPhAbsEta             = -999  ;
    cosThetaStar               =   -99 ; 
    phPtOverMgammaj               =   -99 ; 
    matchedJet_pruned_abseta    = -999  ;
    higgsJet_pruned_abseta    = -999  ;
    sideLowThreeJet_pruned_abseta    = -999  ;
    sideLowThreeJet_HbbTag       = -999. ;
    phJetInvMass_pruned_sideLowThree                =  -99  ;
    phJetDeltaR_sideLowThree                =  -99  ;
    sideLowFourJet_pruned_abseta    = -999  ;
    sideLowFourJet_HbbTag       = -999. ;
    phJetInvMass_pruned_sig                =  -99  ;
    phJetInvMass_pruned_higgs                =  -99  ;
    phJetInvMass_pruned_sideLowFour                =  -99  ;
    phJetDeltaR_sig                =  -99  ;
    phJetDeltaR_higgs                =  -99  ;
    phJetDeltaR_sideLowFour                =  -99  ;

    leadingPhoton       .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    matchedJet_pruned   .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sideHiJet_pruned   .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sideLowJet_pruned   .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sideLowJet_pruned   .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    matchedJet_softdrop .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sumVector           .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    boostedJet           .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    boostedPho           .SetPtEtaPhiE( 0., 0., 0., 0.) ;
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
      if (it->first == "HLT_Photon175_v1" || it->first == "HLT_Photon175_v2" ||  it->first == "HLT_Photon175_v3" ||  it->first =="HLT_Photon165_HE10_v1" ||  it->first =="HLT_Photon165_HE10_v2" ||  it->first =="HLT_Photon165_HE10_v3")  {
      //if (it->first == "HLT_Photon175_v1")  {
        if (debugFlag) cout << "    " << it->first << " has value: " << it->second << endl;
        triggerFired |= (1==it->second);
      }
      //if (it->first == "HLT_Photon165_HE10_v1") {
      //if (it->first == "HLT_Photon165_HE10_v3") {
    }
    if (triggerFired) ++eventsPassingTrigger;
    
    // Loop over photons
    for (uint iPh = 0; iPh<ph_pt->size() ; ++iPh) { 
      if (debugFlag && dumpEventInfo) {
        cout << "    Photon " << iPh << " has pT " << ph_pt->at(iPh)  << ", eta =" << ph_eta->at(iPh) << ", ph_mvaVal = " << ph_mvaVal->at(iPh) << ", ph_mvaCat = " << ph_mvaCat->at(iPh) << endl;
      }
      // Check if this event has a photon passing ID requirements
      phoIsTight = (ph_mvaCat->at(iPh)==0 && ph_mvaVal->at(iPh)>=barrel_phoMVAcut && ph_passEleVeto->at(iPh)==1) || (ph_mvaCat->at(iPh)==1 && ph_mvaVal->at(iPh)>=endcap_phoMVAcut && ph_passEleVeto->at(iPh)==1);
      phoEtaPassesCut = ( abs(ph_eta->at(iPh))<phoEtaMax ) && ((abs(ph_eta->at(iPh)) < 1.4442) || abs(ph_eta->at(iPh))>1.566 );
      phoPtPassesCut = ( ph_pt->at(iPh)>100 );
      eventHasTightPho |= (phoIsTight && phoEtaPassesCut && phoPtPassesCut) ;      

      // Fill the leading photon variables, regardless of the ID

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


    if (debugFlag && eventHasTightPho && dumpEventInfo) cout << "    This event has a tight photon." << endl;


    // Loop over AK4 jets
    ////for (uint iJet = 0; iJet<jetAK4_pt->size() ; ++iJet) { 
    //  if (jetAK4_IDLoose->at(iJet) == 1) { 
    //    HT_ak4+=jetAK4_pt->at(iJet);
    //  }
    //}
    //HT_ak4hist->Fill(HT_ak4);

    // Loop over AK8 jets
    for (uint iJet = 0; iJet<jetAK8_pt->size() ; ++iJet) { 
      if (debugFlag && dumpEventInfo) cout << "    AK8 Jet " << iJet << " has pT " << jetAK8_pt->at(iJet) << endl;
      //if (debugFlag && dumpEventInfo) cout << "    jetAK8_IDLoose[" << iJet << "] is : " << jetAK8_IDLoose->at(iJet) << endl;
 
      if (jetAK8_IDTight->at(iJet) == 1 && jetAK8_IDTightLepVeto->at(iJet) == 1) { 
      // Get leading jet variables, requiring tight jet ID
        tmpLeadingJet.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));

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
            matchedJet_HbbTag = jetAK8_Hbbtag->at(iJet);
            pruned_matchedJetTau1 = jetAK8_tau1 ->  at(iJet) ;
            pruned_matchedJetTau2 = jetAK8_tau2 ->  at(iJet) ;
            pruned_matchedJetTau3 = jetAK8_tau3 ->  at(iJet) ;
          }
        }
        if (jetAK8_pruned_massCorr->at(iJet) > HmassCutLow  && jetAK8_pruned_massCorr->at(iJet) < HmassCutHigh && !eventHasHiggsPrunedJet) {
          eventHasHiggsPrunedJet = true;
          if(debugFlag && dumpEventInfo) {
            cout << "    pruned higgs AK8 jet e is: "    << jetAK8_e->at(iJet)    << endl ;
            cout << "    pruned higgs AK8 jet mass is: " << jetAK8_mass->at(iJet) << endl ;
            cout << "    pruned higgs AK8 jet eta is: "  << jetAK8_eta->at(iJet)  << endl ;
            cout << "    pruned higgs AK8 jet phi is: "  << jetAK8_phi->at(iJet)  << endl ;
            cout << "    pruned higgs AK8 jet pt is: "   << jetAK8_pt->at(iJet)   << endl ;
          }
          higgsJet_pruned.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
          if (higgsJet_pruned.DeltaR(leadingPhoton) < 0.8) {
            higgsJet_pruned.SetPtEtaPhiE(0,0,0,0);
            eventHasHiggsPrunedJet = false;
          }
          else {
            higgsPrunedJetCorrMass = jetAK8_pruned_massCorr->at(iJet);
            higgsJet_HbbTag = jetAK8_Hbbtag->at(iJet);
            pruned_higgsJetTau1 = jetAK8_tau1 ->  at(iJet) ;
            pruned_higgsJetTau2 = jetAK8_tau2 ->  at(iJet) ;
            pruned_higgsJetTau3 = jetAK8_tau3 ->  at(iJet) ;
          }
        }
        if (jetAK8_pruned_massCorr->at(iJet) > bigWindowLowCutLow  && jetAK8_pruned_massCorr->at(iJet) < bigWindowLowCutHigh && !eventHasSideLowPrunedJet) {
          eventHasSideLowPrunedJet = true;
          if (jetAK8_pruned_massCorr->at(iJet) >sidebandThreeCutLow  && jetAK8_pruned_massCorr->at(iJet) < sidebandThreeCutHigh && !eventHasSideLowThreePrunedJet) {
            eventHasSideLowThreePrunedJet = true;
            sideLowThreeJet_pruned.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
            if (sideLowThreeJet_pruned.DeltaR(leadingPhoton) < 0.8) {
              sideLowThreeJet_pruned.SetPtEtaPhiE(0,0,0,0);
              eventHasSideLowThreePrunedJet = false;
            }
            else {
              sideLowThreePrunedJetCorrMass = jetAK8_pruned_massCorr->at(iJet);
              sideLowThreeJet_HbbTag = jetAK8_Hbbtag->at(iJet);
              pruned_sideLowThreeJetTau1 = jetAK8_tau1 ->  at(iJet) ;
              pruned_sideLowThreeJetTau2 = jetAK8_tau2 ->  at(iJet) ;
              pruned_sideLowThreeJetTau3 = jetAK8_tau3 ->  at(iJet) ;
            }
          }

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
        if (jetAK8_pruned_massCorr->at(iJet) > bigWindowHiCutLow  && jetAK8_pruned_massCorr->at(iJet) < bigWindowHiCutHigh && !eventHasSideHiPrunedJet) {
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
          if (jetAK8_pruned_massCorr->at(iJet) >sidebandFourCutLow  && jetAK8_pruned_massCorr->at(iJet) < sidebandFourCutHigh && !eventHasSideLowFourPrunedJet) {
            eventHasSideLowFourPrunedJet = true;
            sideLowFourJet_pruned.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));
            if (sideLowFourJet_pruned.DeltaR(leadingPhoton) < 0.8) {
              sideLowFourJet_pruned.SetPtEtaPhiE(0,0,0,0);
              eventHasSideLowFourPrunedJet = false;
            }
            else {
              sideLowFourPrunedJetCorrMass = jetAK8_pruned_massCorr->at(iJet);
              sideLowFourJet_HbbTag = jetAK8_Hbbtag->at(iJet);
              pruned_sideLowFourJetTau1 = jetAK8_tau1 ->  at(iJet) ;
              pruned_sideLowFourJetTau2 = jetAK8_tau2 ->  at(iJet) ;
              pruned_sideLowFourJetTau3 = jetAK8_tau3 ->  at(iJet) ;
            }
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
    HThist->Fill(HT);

    if (debugFlag && dumpEventInfo) {  // Print some checks
      cout << "    eventHasTightPho is: " <<  eventHasTightPho  << endl;
    }

    // Fill histograms with events that have a photon passing ID and a loose jet
    if (eventHasTightPho  && leadingPhoton.Pt()>180 && abs(leadingPhoton.Eta()) < 2.6) {
      if(eventHasSideLowPrunedJet && sideLowJet_pruned.Pt() > 100 && abs(sideLowJet_pruned.Eta()) < 2.6 ) {
        sumVector = leadingPhoton + sideLowJet_pruned;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << pruned_sideLowJetTau2/pruned_sideLowJetTau1 << endl;
        }
                
        if (triggerFired ) {
          sideLowJett2t1Hist->Fill(pruned_sideLowJetTau2/pruned_sideLowJetTau1);
            phJetInvMassHist_pruned_sideLow->Fill(sumVector.M());
            sideLowJetEtaHist->Fill(sideLowJet_pruned.Eta());
            sideLowJetPhiHist->Fill(sideLowJet_pruned.Phi());
            sideLowJetPtHist->Fill(sideLowJet_pruned.Pt());
        }
          sideLowJet_pruned.SetT(90);
          sumVector = leadingPhoton + sideLowJet_pruned;
          if (triggerFired)phCorrJetInvMassHist_pruned_sideLow->Fill(sumVector.M());
      }
      if(eventHasSideHiPrunedJet && sideHiJet_pruned.Pt() > 200 && abs(sideHiJet_pruned.Eta()) < 2.6 ) {
        sumVector = leadingPhoton + sideHiJet_pruned;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << pruned_sideHiJetTau2/pruned_sideHiJetTau1 << endl;
        }
                
        if (triggerFired ) {
          sideHiJett2t1Hist->Fill(pruned_sideHiJetTau2/pruned_sideHiJetTau1);
            phJetInvMassHist_pruned_sideHi->Fill(sumVector.M());
            sideHiJetEtaHist->Fill(sideHiJet_pruned.Eta());
            sideHiJetPhiHist->Fill(sideHiJet_pruned.Phi());
            sideHiJetPtHist->Fill(sideHiJet_pruned.Pt());
        }
          sideHiJet_pruned.SetT(90);
          sumVector = leadingPhoton + sideHiJet_pruned;
          if (triggerFired)phCorrJetInvMassHist_pruned_sideHi->Fill(sumVector.M());
      }
      if(eventHasMatchedPrunedJet && matchedJet_pruned.Pt() > 200 && abs(matchedJet_pruned.Eta()) < 2.6 ) {
        sumVector = leadingPhoton + matchedJet_pruned;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << pruned_matchedJetTau2/pruned_matchedJetTau1 << endl;
        }
                
        if (triggerFired ) {
          matchedJett2t1 = pruned_matchedJetTau2/pruned_matchedJetTau1;
          matchedJett2t1Hist->Fill(matchedJett2t1);
          boostedPho = leadingPhoton;
          boostedPho.Boost(-(sumVector.BoostVector()));
          boostedJet = matchedJet_pruned;
          boostedJet.Boost(-(sumVector.BoostVector()));
          cosThetaStar = std::abs(boostedPho.Pz()/boostedPho.P());
          phPtOverMgammaj = leadingPhPt/sumVector.M();
          matchedJet_pruned_abseta=std::abs(matchedJet_pruned.Eta());
          leadingPhAbsEta = std::abs(leadingPhEta);
          phJetInvMass_pruned_sig=sumVector.M();
          phJetDeltaR_sig=leadingPhoton.DeltaR(matchedJet_pruned);
          if ( phJetDeltaR_sig>0.8) {
            phJetDeltaPhi_pruned->Fill(leadingPhoton.DeltaPhi(matchedJet_pruned));
            phJetDeltaEta_pruned->Fill(abs( leadingPhoton.Eta() - matchedJet_pruned.Eta() ));
            phJetDeltaR_pruned->Fill(leadingPhoton.DeltaR(matchedJet_pruned));
            leadingPhPtHist->Fill(leadingPhPt);
            leadingPhEtaHist->Fill(leadingPhEta);
            leadingPhPhiHist->Fill(leadingPhPhi);
            phJetInvMassHist_pruned_sig->Fill(phJetInvMass_pruned_sig);
            matchedJetPrunedMassHist ->Fill(matchedPrunedJetCorrMass);
            bigWindowJetPrunedMassHist->Fill(matchedPrunedJetCorrMass);
            matchedJetPtHist->Fill( matchedJet_pruned.Pt());
            matchedJetEtaHist->Fill(matchedJet_pruned.Eta());
            matchedJetPhiHist->Fill(matchedJet_pruned.Phi());
            phPtOverMgammajHist->Fill(phPtOverMgammaj);
            cosThetaStarHist->Fill(cosThetaStar);
          }
          outputTreeSig->Fill();
        }
          matchedJet_pruned.SetT(90);
          sumVector = leadingPhoton + matchedJet_pruned;
          if (triggerFired)phCorrJetInvMassHist_pruned_sig->Fill(sumVector.M());
      }
      if(eventHasHiggsPrunedJet && higgsJet_pruned.Pt() > 200 && abs(higgsJet_pruned.Eta()) < 2.6 ) {
        sumVector = leadingPhoton + higgsJet_pruned;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << pruned_higgsJetTau2/pruned_higgsJetTau1 << endl;
        }
                
        if (triggerFired ) {
          higgsJett2t1 = pruned_higgsJetTau2/pruned_higgsJetTau1;
          higgsJett2t1Hist->Fill(higgsJett2t1);
          boostedPho = leadingPhoton;
          boostedPho.Boost(-(sumVector.BoostVector()));
          boostedJet = higgsJet_pruned;
          boostedJet.Boost(-(sumVector.BoostVector()));
          cosThetaStar = std::abs(boostedPho.Pz()/boostedPho.P());
          phPtOverMgammaj = leadingPhPt/sumVector.M();
          higgsJet_pruned_abseta=std::abs(higgsJet_pruned.Eta());
          leadingPhAbsEta = std::abs(leadingPhEta);
          phJetInvMass_pruned_higgs=sumVector.M();
          phJetDeltaR_higgs=leadingPhoton.DeltaR(higgsJet_pruned);
          if ( phJetDeltaR_higgs>0.8) {
            phJetDeltaPhi_pruned->Fill(leadingPhoton.DeltaPhi(higgsJet_pruned));
            phJetDeltaEta_pruned->Fill(abs( leadingPhoton.Eta() - higgsJet_pruned.Eta() ));
            phJetDeltaR_pruned->Fill(leadingPhoton.DeltaR(higgsJet_pruned));
            leadingPhPtHist->Fill(leadingPhPt);
            leadingPhEtaHist->Fill(leadingPhEta);
            leadingPhPhiHist->Fill(leadingPhPhi);
            phJetInvMassHist_pruned_higgs->Fill(phJetInvMass_pruned_higgs);
            higgsJetPrunedMassHist ->Fill(higgsPrunedJetCorrMass);
            higgsJetPtHist->Fill( higgsJet_pruned.Pt());
            higgsJetEtaHist->Fill(higgsJet_pruned.Eta());
            higgsJetPhiHist->Fill(higgsJet_pruned.Phi());
            phPtOverMgammajHist->Fill(phPtOverMgammaj);
            cosThetaStarHist->Fill(cosThetaStar);
          }
          outputTreeHiggs->Fill();
        }
          higgsJet_pruned.SetT(90);
          sumVector = leadingPhoton + higgsJet_pruned;
          if (triggerFired)phCorrJetInvMassHist_pruned_higgs->Fill(sumVector.M());
      }
      if(eventHasSideLowThreePrunedJet && sideLowThreeJet_pruned.Pt() > 200 && abs(sideLowThreeJet_pruned.Eta()) < 2.6 ) {
        sumVector = leadingPhoton + sideLowThreeJet_pruned;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << pruned_sideLowThreeJetTau2/pruned_sideLowThreeJetTau1 << endl;
        }
                
        if (triggerFired ) {
          sideLowThreeJett2t1 = pruned_sideLowThreeJetTau2/pruned_sideLowThreeJetTau1;
          boostedPho = leadingPhoton;
          boostedPho.Boost(-(sumVector.BoostVector()));
          boostedJet = sideLowThreeJet_pruned;
          boostedJet.Boost(-(sumVector.BoostVector()));
          cosThetaStar = std::abs(boostedPho.Pz()/boostedPho.P());
          phPtOverMgammaj = leadingPhPt/sumVector.M();
          sideLowThreeJet_pruned_abseta=std::abs(sideLowThreeJet_pruned.Eta());
          leadingPhAbsEta = std::abs(leadingPhEta);
          phJetInvMass_pruned_sideLowThree=sumVector.M();
          phJetDeltaR_sideLowThree=leadingPhoton.DeltaR(sideLowThreeJet_pruned);
          outputTree5070->Fill();
        }
          sideLowThreeJet_pruned.SetT(90);
          sumVector = leadingPhoton + sideLowThreeJet_pruned;
      }
      if(eventHasSideLowFourPrunedJet && sideLowFourJet_pruned.Pt() > 200 && abs(sideLowFourJet_pruned.Eta()) < 2.6 ) {
        sumVector = leadingPhoton + sideLowFourJet_pruned;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << pruned_sideLowFourJetTau2/pruned_sideLowFourJetTau1 << endl;
        }
                
        if (triggerFired ) {
          sideLowFourJett2t1 = pruned_sideLowFourJetTau2/pruned_sideLowFourJetTau1;
          boostedPho = leadingPhoton;
          boostedPho.Boost(-(sumVector.BoostVector()));
          boostedJet = sideLowFourJet_pruned;
          boostedJet.Boost(-(sumVector.BoostVector()));
          cosThetaStar = std::abs(boostedPho.Pz()/boostedPho.P());
          phPtOverMgammaj = leadingPhPt/sumVector.M();
          sideLowFourJet_pruned_abseta=std::abs(sideLowFourJet_pruned.Eta());
          leadingPhAbsEta = std::abs(leadingPhEta);
          phJetInvMass_pruned_sideLowFour=sumVector.M();
          phJetDeltaR_sideLowFour=leadingPhoton.DeltaR(sideLowFourJet_pruned);
          outputTree100110->Fill();
        }
          sideLowFourJet_pruned.SetT(90);
          sumVector = leadingPhoton + sideLowFourJet_pruned;
      }
      if(eventHasSideHiPrunedJet && sideHiJet_pruned.Pt() > 200 && abs(sideHiJet_pruned.Eta()) < 2.6 ) {
        if (triggerFired ) {
          if ( leadingPhoton.DeltaR(sideHiJet_pruned)>0.8) {
            sideHiJetPrunedMassHist ->Fill(sideHiPrunedJetCorrMass);
            bigWindowJetPrunedMassHist->Fill(sideHiPrunedJetCorrMass);
          }
        }
      }
      if(eventHasSideLowPrunedJet && sideLowJet_pruned.Pt() > 200 && abs(sideLowJet_pruned.Eta()) < 2.6 ) {
        if (triggerFired ) {
          if ( leadingPhoton.DeltaR(sideLowJet_pruned)>0.8) {
            sideLowJetPrunedMassHist ->Fill(sideLowPrunedJetCorrMass);
            bigWindowJetPrunedMassHist->Fill(sideLowPrunedJetCorrMass);
          }
        }
      }
      if(eventHasMatchedSoftdropJet && matchedJet_softdrop.Pt() > 200 && abs(matchedJet_softdrop.Eta()) < 2.6 ) {
        matchedJetSoftdropMassHist ->Fill(matchedSoftdropJetCorrMass);
        sumVector = leadingPhoton + matchedJet_softdrop;
        if (debugFlag && dumpEventInfo)  {
          cout << "    using matching with softdrop, sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " <<softdrop_matchedJetTau2/softdrop_matchedJetTau1 << endl;
        }
        if ( triggerFired && leadingPhoton.Pt() > 180) phJetInvMassHist_softdrop->Fill(sumVector.M());
      }
    }
    if (debugFlag && entriesToCheck == jentry) break; // when debugFlag is true, break the event loop after reaching entriesToCheck 
  }

  outputFile->cd();

  outputTreeSig->Write();
  outputTreeHiggs->Write();
  outputTree5070->Write();
  outputTree100110->Write();

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
  HThist                           -> Write() ;
//  HT_ak4hist                       -> Write() ;

  outputFile ->     mkdir("Jet_substructure") ;
  outputFile ->        cd("Jet_substructure") ;
  matchedJett2t1Hist               -> Write() ;
  higgsJett2t1Hist               -> Write() ;

  outputFile ->            mkdir("Resonance") ;
  outputFile ->               cd("Resonance") ;
  //phJetInvMassHist_pruned          -> Write() ;
  //phCorrJetInvMassHist_pruned      -> Write() ;
  phJetInvMassHist_softdrop        -> Write() ;
  matchedJetMassHist               -> Write() ;
  matchedJetPrunedMassHist         -> Write() ;
  matchedJetSoftdropMassHist       -> Write() ;
  matchedJetPtHist                 -> Write() ;
  matchedJetEtaHist                -> Write() ;
  matchedJetPhiHist                -> Write() ;
  higgsJetMassHist               -> Write() ;
  higgsJetPrunedMassHist         -> Write() ;
  higgsJetSoftdropMassHist       -> Write() ;
  higgsJetPtHist                 -> Write() ;
  higgsJetEtaHist                -> Write() ;
  higgsJetPhiHist                -> Write() ;
  phJetDeltaR_pruned               -> Write() ;
  phJetDeltaPhi_pruned             -> Write() ;
  phJetDeltaEta_pruned             -> Write() ;
  phJetInvMassHist_pruned_sig      -> Write() ;
  phJetInvMassHist_pruned_higgs      -> Write() ;
  phJetInvMassHist_pruned_sideHi   -> Write() ;
  phJetInvMassHist_pruned_sideLow  -> Write() ;
  sideHiJetPrunedMassHist          -> Write() ;
  sideLowJetPrunedMassHist         -> Write() ;
  bigWindowJetPrunedMassHist       -> Write() ;
  phCorrJetInvMassHist_pruned_higgs            -> Write() ;
  phCorrJetInvMassHist_pruned_sideHi         -> Write() ;
  phCorrJetInvMassHist_pruned_sideLow        -> Write() ;
  phPtOverMgammajHist                        -> Write() ;
  cosThetaStarHist                           -> Write() ;

  outputFile ->       mkdir("Trigger_turnon") ;
  outputFile ->          cd("Trigger_turnon") ;
  leadingPhPtHist                  -> Write() ;

  outputFile->Close();

  cout << "100% done: Scanned " << nentries << " events." << endl;
  cout << "The trigger fired " << eventsPassingTrigger << " times" << endl;
  cout << "The trigger efficiency was " << (float) eventsPassingTrigger/ (float)nentries << endl;
  cout << "\nCompleted output file is " << outputFileName.c_str() <<".\n" << endl;
}
