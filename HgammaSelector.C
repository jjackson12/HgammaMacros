#define HgammaSelector_cxx
#include "HgammaSelector.h"

using namespace std;

// Class for analyzing the flatTuples from the EXOVVNtuplizer
// The output gives a few trees -- all of which are focused on a V/H(fatjet)gamma resonance
// The trees differ in the AK8 jet mass cuts -- different windows are used for different bosons 
// John Hakala -- May 11, 2016

void HgammaSelector::Loop(string outputFileName) {
  cout << "output filename is: " << outputFileName << endl;
  // Flags for running this macro
  bool debugFlag                     =  true ;  // If debugFlag is false, the trigger checking couts won't appear and the loop won't stop when it reaches entriesToCheck
  bool checkTrigger                  =  true ;
  //bool ignoreAllCuts                 =  false ;
  bool dumpEventInfo                 =  true ;
  bool noHLTinfo                     =  false  ;  // This is for the 2016 MC with no HLT info
  int  entriesToCheck                =  100000000 ;  // If debugFlag = true, stop once the number of checked entries reaches entriesToCheck
  int  reportEvery                   =  5000  ;

  // Photon id cut values
  float endcap_phoMVAcut             = 0.336 ;  // See https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariatePhotonIdentificationRun2#Recommended_MVA_recipes_for_2015
  float barrel_phoMVAcut             = 0.374 ;
  float phoEtaMax                    =   2.4 ;
  float jetEtaMax                    =   2.4 ;
  //float jetT2T1Max                   =   0.5 ;
  float phoEtaRanges[5]              = {0, 0.75, 1.479, 2.4, 3.0};

  TFile* outputFile                 = new TFile(outputFileName.c_str(), "RECREATE");
  outputFile->cd();

  //TTree* outputTreeSig    = new TTree("sig",               "sig");
  TTree* outputTreeHiggs  = new TTree("higgs",           "higgs");
  outputTreeHiggs -> SetAutoSave(-500000000);

  outputTreeHiggs->Branch("higgsJett2t1", &higgsJett2t1);
  outputTreeHiggs->Branch("higgsJet_HbbTag", &higgsJet_HbbTag);
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
  outputTreeHiggs->Branch("triggerFired_165HE10", &triggerFired_165HE10);
  outputTreeHiggs->Branch("triggerFired_175", &triggerFired_175);


  // Branches from EXOVVNtuplizer tree
  fChain->SetBranchStatus( "*"                        ,  0 );  // disable all branches
  fChain->SetBranchStatus( "HLT_isFired"              ,  1 );  // activate select branches
  fChain->SetBranchStatus( "ph_pt"                    ,  1 );  
  fChain->SetBranchStatus( "ph_e"                     ,  1 );  
  fChain->SetBranchStatus( "ph_eta"                   ,  1 );  
  fChain->SetBranchStatus( "ph_phi"                   ,  1 );  
  fChain->SetBranchStatus( "ph_mvaVal"                ,  1 );
  fChain->SetBranchStatus( "ph_mvaCat"                ,  1 );
  fChain->SetBranchStatus( "ph_passEleVeto"           ,  1 );
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
  fChain->SetBranchStatus( "jetAK8_IDTightLepVeto"    ,  1 );  
  fChain->SetBranchStatus( "jetAK8_Hbbtag"            ,  1 );  
  fChain->SetBranchStatus("EVENT_run"      ,  1 );
  fChain->SetBranchStatus("EVENT_lumiBlock"      ,  1 );
  fChain->SetBranchStatus("EVENT_event"      ,  1 );
  //fChain->SetBranchStatus("subjetAK8_pruned_csv"      ,  1 );

  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;

  cout << "\n\nStarting HgammaSelector::Loop().\n" << endl;
  // Loop over all events
  for (Long64_t jentry=0; jentry<nentries;++jentry) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;


    // internal variables used for computation
    eventHasHiggsPrunedJet           = false ;
    leadingPhMVA                     = -999. ;
    leadingPhCat                     = -999. ;
    phoIsTight                       = false ;
    phoEtaPassesCut                  = false ;
    phoPtPassesCut                   = false ;
    eventHasTightPho                 = false ;
    leadingPhE                       = 0.    ;
    pruned_higgsJetTau1              = -999. ;
    pruned_higgsJetTau2              = -999. ;
    pruned_higgsJetTau3              = -999. ;

    // final output variables
    leadingPhPt                      = 0.    ;
    leadingPhEta                     = -999  ;
    leadingPhPhi                     = -999  ;
    leadingPhAbsEta                  = -999. ;
    higgsJet_pruned_abseta           = -999. ;
    higgsPrunedJetCorrMass           = -999. ;
    higgsJet_HbbTag                  = -999. ;
    cosThetaStar                     =  -99. ; 
    phPtOverMgammaj                  =  -99. ; 
    triggerFired_175                 = false ; 
    triggerFired_165HE10             = false ; 

    leadingPhoton        .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sumVector            .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    boostedJet           .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    boostedPho           .SetPtEtaPhiE( 0., 0., 0., 0.) ;

    //higgs_csvValues.leading=-10.;
    //higgs_csvValues.subleading=-10.;

    // Print out trigger information
    if (jentry%reportEvery==0) {
      cout.flush();
      cout << fixed << setw(4) << setprecision(2) << (float(jentry)/float(nentries))*100 << "% done: Scanned " << jentry << " events." << '\r';
    }
    if (debugFlag && dumpEventInfo) cout << "\nIn event number " << jentry << ":" << endl;
    if (checkTrigger && debugFlag) cout << "     Trigger info is: " << endl;
    for(map<string,bool>::iterator it = HLT_isFired->begin(); it != HLT_isFired->end(); ++it) {
      if (checkTrigger && debugFlag) { 
        cout << "       " << it->first << " = " << it->second << endl;
      }
      if (it->first.find("HLT_Photon175_") != std::string::npos )  {
        triggerFired_175 = (1==it->second);
        if (triggerFired_175) ++eventsPassingTrigger_175;
      }
      if (  it->first.find("HLT_Photon165_HE10_") != std::string::npos)  {
        triggerFired_165HE10 = (1==it->second);
        if (triggerFired_165HE10) ++eventsPassingTrigger_165HE10;
      }
    }
    
    // Loop over photons
    for (uint iPh = 0; iPh<ph_pt->size() ; ++iPh) { 
      if (debugFlag && dumpEventInfo) {
        cout << "    Photon " << iPh << " has pT " << ph_pt->at(iPh)  << ", eta =" << ph_eta->at(iPh) << ", ph_mvaVal = " << ph_mvaVal->at(iPh) << ", ph_mvaCat = " << ph_mvaCat->at(iPh) << endl;
      }
      // Check if this event has a photon passing ID requirements
      phoIsTight = (ph_mvaCat->at(iPh)==0 && ph_mvaVal->at(iPh)>=barrel_phoMVAcut && ph_passEleVeto->at(iPh)==1) || (ph_mvaCat->at(iPh)==1 && ph_mvaVal->at(iPh)>=endcap_phoMVAcut && ph_passEleVeto->at(iPh)==1);
      //phoEtaPassesCut = ( abs(ph_eta->at(iPh))<phoEtaMax ) && ((abs(ph_eta->at(iPh)) < 1.4442) || abs(ph_eta->at(iPh))>1.566 );
      phoEtaPassesCut = ( abs(ph_eta->at(iPh))<phoEtaMax ) && ((abs(ph_eta->at(iPh)) < 1.4442) || abs(ph_eta->at(iPh))>1.566 );
      phoPtPassesCut = ( ph_pt->at(iPh)>100 );
      eventHasTightPho |= (phoIsTight && phoEtaPassesCut && phoPtPassesCut) ;      

      // Fill the leading photon variables, regardless of the ID

      // Fill the leading photon variables, requiring the photon to pass the ID requirements
      if ( ph_pt->at(iPh) > leadingPhPt && phoIsTight && phoEtaPassesCut && phoPtPassesCut) {
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

    // Loop over AK8 jets
    for (uint iJet = 0; iJet<jetAK8_pt->size() ; ++iJet) { 
      if (debugFlag && dumpEventInfo) cout << "    AK8 Jet " << iJet << " has pT " << jetAK8_pt->at(iJet) << endl;
 
      if (jetAK8_IDTight->at(iJet) == 1 && jetAK8_IDTightLepVeto->at(iJet) == 1 && jetAK8_pt->at(iJet)>250) { 
      // Get leading jet variables, requiring tight jet ID
        tmpLeadingJet.SetPtEtaPhiE(jetAK8_pt->at(iJet), jetAK8_eta->at(iJet), jetAK8_phi->at(iJet), jetAK8_e->at(iJet));

        if (!eventHasHiggsPrunedJet) { 
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
            if  ( iJet<jetAK8_pruned_massCorr->size() && abs(jetAK8_pruned_massCorr->at(iJet) - 125) <  abs(higgsPrunedJetCorrMass -  125 )) {
              higgsPrunedJetCorrMass = jetAK8_pruned_massCorr->at(iJet);
              higgsJet_HbbTag = jetAK8_Hbbtag->at(iJet);
              pruned_higgsJetTau1 = jetAK8_tau1 ->  at(iJet) ;
              pruned_higgsJetTau2 = jetAK8_tau2 ->  at(iJet) ;
              pruned_higgsJetTau3 = jetAK8_tau3 ->  at(iJet) ;
              //higgs_csvValues = getLeadingSubjets(subjetAK8_pruned_csv->at(iJet));
              //cout << "    for higgs jet, get csv values " << higgs_csvValues.leading << ", " << higgs_csvValues.subleading << endl;
              //higgs_subjetCutDecisions = getSubjetCutDecisions(higgs_csvValues);
            }
          }
        }
        else if (debugFlag && dumpEventInfo) cout << " this event failed the jet requirement for the higgs branch!" << endl;
      } 
    }

    if (debugFlag && dumpEventInfo) {  // Print some checks
      cout << "    eventHasTightPho is: " <<  eventHasTightPho  << endl;
    }

    // Fill histograms with events that have a photon passing ID and a loose jet
    // TODO: photon pT cut applied here. unhardcode
    if ( (eventHasTightPho  && leadingPhoton.Pt()>180 && abs(leadingPhoton.Eta()) < 2.6)) {
      if( (eventHasHiggsPrunedJet && higgsJet_pruned.Pt() > 250 && abs(higgsJet_pruned.Eta()) < 2.6 )) {
        sumVector = leadingPhoton + higgsJet_pruned;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with pruned,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << pruned_higgsJetTau2/pruned_higgsJetTau1 << endl;
        }
        higgsJett2t1 = pruned_higgsJetTau2/pruned_higgsJetTau1;
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
        if ( phJetDeltaR_higgs<0.8 ) {
          if (debugFlag && dumpEventInfo) cout << "this event failed the DR cut!" << endl;
          continue;
        }
        outputTreeHiggs->Fill();
        //higgsJet_pruned.SetT(90);
        //sumVector = leadingPhoton + higgsJet_pruned;
      }
      else if (debugFlag && dumpEventInfo) {
        cout << " this event failed 'if( (eventHasHiggsPrunedJet && higgsJet_pruned.Pt() > 250 && abs(higgsJet_pruned.Eta()) < 2.6 ))'" << endl;
        cout << "eventHasHiggsPrunedJet="  << eventHasHiggsPrunedJet << ", higgsJet_pruned.Pt()=" << higgsJet_pruned.Pt() << ", abs(higgsJet_pruned.Eta())=" << higgsJet_pruned.Eta() << endl;
      }
    }
    if (debugFlag && entriesToCheck == jentry) break; // when debugFlag is true, break the event loop after reaching entriesToCheck 
  }



  outputFile->Write();
  outputFile->Close();

  cout.flush();
  cout << "100% done: Scanned " << nentries << " events." << endl;
  cout << "HLT_Photon175 fired " << eventsPassingTrigger_175 << " times" << endl;
  cout << "The HLT_Photon175 efficiency was " << (float) eventsPassingTrigger_175/ (float)nentries << endl;
  cout << "HLT_Photon165_HE10 fired " << eventsPassingTrigger_165HE10 << " times" << endl;
  cout << "The HLT_Photon165_HE10 efficiency was " << (float) eventsPassingTrigger_165HE10/ (float)nentries << endl;
  cout << "\nCompleted output file is " << outputFileName.c_str() <<".\n" << endl;
}

HgammaSelector::leadingSubjets HgammaSelector::getLeadingSubjets(vector<float> prunedJet) {
  // Note: in miniaod, there are only two subjets stored since the declustering is done recursively and miniaod's declustering stops after splitting into two subjets
  leadingSubjets topCSVs;
  topCSVs.leading = -10.;
  topCSVs.subleading = -10.;
  for (uint iSubjet=0; iSubjet<prunedJet.size(); ++iSubjet) {
    if (prunedJet.at(iSubjet)>topCSVs.leading) {
      topCSVs.subleading = topCSVs.leading;
      topCSVs.leading = prunedJet.at(iSubjet);
    }
    else if (topCSVs.leading > prunedJet.at(iSubjet) && topCSVs.subleading < prunedJet.at(iSubjet)) {
      topCSVs.subleading = prunedJet.at(iSubjet);
    }
  }
  return topCSVs;
}

//HgammaSelector::passSubjetCuts HgammaSelector::getSubjetCutDecisions(leadingSubjets subjets) {
//  float looseWP  = 0.605;
//  float mediumWP = 0.89;
//  float tightWP  = 0.97;
//
//  bool leadingIsLoose     = (subjets.leading    > looseWP);
//  bool leadingIsMedium    = (subjets.leading    > mediumWP);
//  bool leadingIsTight     = (subjets.leading    > tightWP);
//  bool subleadingIsLoose  = (subjets.subleading > looseWP);
//  bool subleadingIsMedium = (subjets.subleading > mediumWP);
//  bool subleadingIsTight  = (subjets.subleading > tightWP);
//
//  passSubjetCuts decisions;
//
//  decisions.loose_loose    = leadingIsLoose   &&  subleadingIsLoose;
//  decisions.medium_loose   = leadingIsMedium  &&  subleadingIsLoose;
//  decisions.tight_loose    = leadingIsTight   &&  subleadingIsLoose;
//  decisions.medium_medium  = leadingIsMedium  &&  subleadingIsMedium;
//  decisions.tight_medium   = leadingIsTight   &&  subleadingIsMedium;
//  decisions.tight_tight    = leadingIsTight   &&  subleadingIsTight;
//
//  return decisions;
//}
