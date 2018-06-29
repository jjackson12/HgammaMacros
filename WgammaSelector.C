#define WgammaSelector_cxx
#include "WgammaSelector.h"
#include "LinkDef.h"

using namespace std;

// Class for analyzing the flatTuples from the EXOVVNtuplizer
// The output gives a few trees -- all of which are focused on a V(fatjet)gamma resonance
// The trees differ in the AK8 jet mass cuts -- different windows are used for different bosons 
// John Hakala -- May 11, 2016
// Jacob Jackson -- updated for Wgamma June 18, 2018

void WgammaSelector::Loop(string outputFileName, float mcWeight) {
  cout << "output filename is: " << outputFileName << endl;
  // Flags for running this macro
  bool debugFlag                     =  false ;  // If debugFlag is false, the trigger checking couts won't appear and the loop won't stop when it reaches entriesToCheck
  bool debugSF                       =  false ; 
  bool checkTrigger                  =  false ;
  bool dumpEventInfo                 =  false ;
  //bool ignoreAllCuts                 =  false ;
  bool noHLTinfo                     =  true  ;  // This is for the 2016 MC with no HLT info
  int  entriesToCheck                =  600000000000000 ;  // If debugFlag = true, stop once the number of checked entries reaches entriesToCheck
  int  reportEvery                   =  20  ;

  // Photon id cut values TODO: Update for 2017
  float endcap_phoMVAcut             = 0.20 ;  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariatePhotonIdentificationRun2#Recommended_MVA_recipes_for_2016
  float barrel_phoMVAcut             = 0.20 ;
  float phoEtaMax                    =   2.6 ;
  float jetEtaMax                    =   2.6 ;
  //float jetT2T1Max                   =   0.5 ;
  float phoEtaRanges[5]              = {0, 0.75, 1.479, 2.4, 3.0};// Isn't used
  float leadingPhoWJetDeltaRCut      = 0.8;
  float WJetMinPtCut                 = 250;
  float leadingPhPtCut               = 180;

  //NOTE: Yet to be implemented; outline for if I get curious about how many events have multiple W-passing jets, and what to do about them
   // nTwoOrMoreWJetEvents                   = 0
   // nPassingJetEvents                      nTwoOrMoreWJetEvents

  // for looking at cached trigger firing results
  //bool loadEventMap = true;
  //TFile* eventMapFile = TFile::Open("eventMap_HLT_Photon175.root", "READ");
  //cout << "eventMapFile " << eventMapFile << endl;
  //TTree* eventMapTree = (TTree*) eventMapFile->Get("eventMap");
  //cout << "eventMapTree " << eventMapTree << endl;
  //TBranch *b_eventMap = 0;
  //if (loadEventMap) {
  //  cout << "About to set branch address" << endl;
  //  eventMapTree->SetBranchAddress("eventMap", &eventMap, &b_eventMap);
  //  cout << "About to LoadTree" << endl;
  //  Long64_t tentry = eventMapTree->LoadTree(0);
  //  cout << "About to GetEntry" << endl;
  //  b_eventMap->GetEntry(tentry);
  //  cout << "Finished GetEntry" << endl;
  //}

  TFile* outputFile                 = new TFile(outputFileName.c_str(), "RECREATE");
  outputFile->cd();

  //TTree* outputTreeSig    = new TTree("sig",               "sig");
  TTree* outputTreeWgam  = new TTree("Wgam", "Wgam");
  outputTreeWgam -> SetAutoSave(-500000000);

  outputTreeWgam->Branch("WJetTau21", &WJetTau21);
  outputTreeWgam->Branch("cosThetaStar", &cosThetaStar);
  outputTreeWgam->Branch("phPtOverMgammaj", &phPtOverMgammaj);
  outputTreeWgam->Branch("WJetPtOverMgammaj", &WJetPtOverMgammaj);
  outputTreeWgam->Branch("leadingPhEta", &leadingPhEta);
  outputTreeWgam->Branch("leadingPhPhi", &leadingPhPhi);
  outputTreeWgam->Branch("leadingPhPt", &leadingPhPt);
  outputTreeWgam->Branch("leadingPhAbsEta", &leadingPhAbsEta);
  outputTreeWgam->Branch("phJetInvMass_puppi_softdrop_W", &phJetInvMass_puppi_softdrop_W);
  outputTreeWgam->Branch("phJetDeltaR_W", &phJetDeltaR_W);
  outputTreeWgam->Branch("WJet_puppi_abseta", &WJet_puppi_abseta);
  outputTreeWgam->Branch("WJet_puppi_eta", &WJet_puppi_eta);
  outputTreeWgam->Branch("WJet_puppi_phi", &WJet_puppi_phi);
  outputTreeWgam->Branch("WJet_puppi_pt", &WJet_puppi_pt);
  outputTreeWgam->Branch("WPuppi_softdropJetCorrMass", &WPuppi_softdropJetCorrMass);
  outputTreeWgam->Branch("triggerFired_165HE10", &triggerFired_165HE10);
  outputTreeWgam->Branch("triggerFired_175", &triggerFired_175);
  outputTreeWgam->Branch("weightFactor", &weightFactor);
  outputTreeWgam->Branch("mcWeight", &mcWeight);


  // Branches from EXOVVNtuplizer tree
  fChain->SetBranchStatus( "*"                        ,  0 );  // disable all branches
  fChain->SetBranchStatus( "HLT_isFired"              ,  1 );  // activate select branches
  fChain->SetBranchStatus( "ph_pt"                    ,  1 );  
  fChain->SetBranchStatus( "ph_e"                     ,  1 );  
  fChain->SetBranchStatus( "ph_eta"                   ,  1 );  
  fChain->SetBranchStatus( "ph_phi"                   ,  1 );  
  fChain->SetBranchStatus( "ph_mvaVal"                ,  1 );
  fChain->SetBranchStatus( "ph_mvaCat"                ,  1 ); //TODO: replace it for 2017
  fChain->SetBranchStatus( "ph_passEleVeto"           ,  1 );
  fChain->SetBranchStatus( "jetAK4_pt"                ,  1 );  
  fChain->SetBranchStatus( "jetAK4_IDLoose"           ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_pt"                ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_softdrop_mass"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_softdrop_massCorr"   ,  1 );
  fChain->SetBranchStatus( "jetAK8_puppi_softdrop_massCorr" ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_e"                 ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_eta"               ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_phi"               ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_tau1"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_puppi_tau2"              ,  1 );  
  //fChain->SetBranchStatus( "jetAK8_puppi_tau3"              ,  1 );  
  fChain->SetBranchStatus( "jetAK8_IDTight"           ,  1 );  
  fChain->SetBranchStatus( "jetAK8_IDTightLepVeto"    ,  1 );  
  //fChain->SetBranchStatus( "jetAK8_Hbbtag"            ,  1 );  
  //fChain->SetBranchStatus("EVENT_run"      ,  1 );
  //fChain->SetBranchStatus("EVENT_lumiBlock"      ,  1 );
  //fChain->SetBranchStatus("EVENT_event"      ,  1 );
  //fChain->SetBranchStatus("subjetAK8_puppi_softdrop_csv"      ,  1 );

  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;

  //TFile* trigEffFile = new TFile("inputs/JetTrig.root");
  //TCanvas* trigEffCan = (TCanvas*) trigEffFile->Get("effi");
  //TPad* trigEffPad = (TPad*) trigEffCan->GetPrimitive("pad1");
  //TIter it(trigEffPad->GetListOfPrimitives());
  //TH1D* trigEffHist = new TH1D();
  //while (TObject* obj = it()) {
  //  if (strncmp(obj->IsA()->GetName(), "TH1D", 4)==0) {
  //    if (((TH1D*)obj)->GetLineColor() == 432) {
  //      trigEffHist = (TH1D*)obj;
  //    }
  //  }
  //}
  //trigEffFile->Close();

  //TODO: What is this?
  // This is an error function
  TF1* turnOnCurve = new TF1("erf", "[0]*TMath::Erf((x-[1])/[2])+[3]", 0, 5000);
  turnOnCurve->SetParameters(0.493428, 197.58, 62.6643, 0.500232);
  
  cout << "\n\nStarting WgammaSelector::Loop().\n" << endl;
  // Loop over all events
  for (Long64_t jentry=0; jentry<nentries;++jentry) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;


    // internal variables used for computation
    eventHasWPuppi_softdropJet           = false ;
    leadingPhMVA                     = -999. ;
    leadingPhCat                     = -999. ;
    phoIsTight                       = false ;
    phoEtaPassesCut                  = false ;
    phoPtPassesCut                   = false ;
    eventHasTightPho                 = false ;
    leadingPhE                       = 0.    ;
    puppi_softdrop_WJetTau1              = -999. ;
    puppi_softdrop_WJetTau2              = -999. ;
    //puppi_softdrop_WJetTau3              = -999. ;


    // final output variables
    leadingPhPt                      = 0.    ;
    leadingPhEta                     = -999  ;
    leadingPhPhi                     = -999  ;
    leadingPhAbsEta                  = -999. ;
    WJet_puppi_abseta           = -999. ;
    WJet_puppi_eta              = -999. ;
    WJet_puppi_phi              = -999. ;
    WJet_puppi_pt               = -999. ;
    WPuppi_softdropJetCorrMass           = -999. ;
   // WJet_HbbTag                  = -999. ;
    cosThetaStar                     =  -99. ; 
    phPtOverMgammaj                  =  -99. ; 
    WJetPtOverMgammaj                  =  -99. ; 
    triggerFired_175                 = false ; 
    triggerFired_165HE10             = false ; 
    weightFactor                     =  -99. ;

    leadingPhoton        .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    sumVector            .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    boostedJet           .SetPtEtaPhiE( 0., 0., 0., 0.) ;
    boostedPho           .SetPtEtaPhiE( 0., 0., 0., 0.) ;

    //W_csvValues.leading=-10.;
    //W_csvValues.subleading=-10.;

    // Print out trigger information
    if (jentry%reportEvery==0) {
      cout.flush();
      cout << fixed << setw(4) << setprecision(2) << (float(jentry)/float(nentries))*100 << "% done: Scanned " << jentry << " events.        " << '\r';
    }
    if (debugFlag && dumpEventInfo) cout << "\nIn event number " << jentry << ":" << endl;
    if (checkTrigger && debugFlag) cout << "     Trigger info is: " << endl;
    

    //counts events passing triggers 175 and 165HE10 (TODO: Edit for 2017)
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
      //TODO: Read up on this mvaCat to see how to adjust these mva cuts for 2017
      // NOTE: mvaCat just delineates between barrel and endcap
      phoIsTight = (ph_mvaCat->at(iPh)==0 && ph_mvaVal->at(iPh)>=barrel_phoMVAcut && ph_passEleVeto->at(iPh)==1) || (ph_mvaCat->at(iPh)==1 && ph_mvaVal->at(iPh)>=endcap_phoMVAcut && ph_passEleVeto->at(iPh)==1);
      phoEtaPassesCut = ( abs(ph_eta->at(iPh))<phoEtaMax ) && ((abs(ph_eta->at(iPh)) < 1.4442) || abs(ph_eta->at(iPh))>1.566 );
      phoPtPassesCut = ( ph_pt->at(iPh)>180 );
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
    // TODO: Test
    // Does this loop from lowest pt to highest pt? If so, then this overwrites W-passing jets with lower pt's than other W-passing Jets. I should think about what that means for events with more than one high-pt Jet
    // It also takes into account the jet mass, but that is overwritten by jet pt
    // This definitely needs some work; why are the mass and tau variables only recorded when it has the closest mass? This could mean we output tau and mass values for DIFFERENT jets than the actual ones we use in the rest of the analysis
    // And what to do about events with more than one W-passing Jet?
    for (uint iJet = 0; iJet<jetAK8_puppi_pt->size() ; ++iJet) { 

          //debugging
          if(debugFlag && dumpEventInfo) {
            cout << "    At Jet number "                     << iJet                        <<endl ;
            cout << "    puppi_softdrop W AK8 jet e is: "    << jetAK8_puppi_e->at(iJet)    << endl ;
            cout << "    puppi_softdrop W AK8 jet mass is: " << jetAK8_puppi_softdrop_mass->at(iJet) << endl ;
            cout << "    puppi_softdrop W AK8 jet eta is: "  << jetAK8_puppi_eta->at(iJet)  << endl ;
            cout << "    puppi_softdrop W AK8 jet phi is: "  << jetAK8_puppi_phi->at(iJet)  << endl ;
            cout << "    puppi_softdrop W AK8 jet pt is: "   << jetAK8_puppi_pt->at(iJet)   << endl ;
          }
      tmpLeadingJet.SetPtEtaPhiE(jetAK8_puppi_pt->at(iJet), jetAK8_puppi_eta->at(iJet), jetAK8_puppi_phi->at(iJet), jetAK8_puppi_e->at(iJet));

      //Jet Cuts
      if (jetAK8_IDTight->at(iJet) == 1 && jetAK8_IDTightLepVeto->at(iJet) == 1 && jetAK8_puppi_pt->at(iJet)>WJetMinPtCut && tmpLeadingJet.DeltaR(leadingPhoton) >= leadingPhoWJetDeltaRCut && abs(jetAK8_puppi_softdrop_massCorr->at(iJet) - 80) <  abs(WPuppi_softdropJetCorrMass -  80 )) { 

        if (debugFlag && dumpEventInfo) cout << " this event PASSED the W Jet requirements! " << endl;

        eventHasWPuppi_softdropJet = true;
            
          
        // Get leading jet variables, requiring tight jet ID


       
        WPuppi_softdropJetCorrMass = jetAK8_puppi_softdrop_massCorr->at(iJet);
        puppi_softdrop_WJetTau1 = jetAK8_puppi_tau1 ->  at(iJet) ;
        puppi_softdrop_WJetTau2 = jetAK8_puppi_tau2 ->  at(iJet) ;
        WJet_puppi_softdrop.SetPtEtaPhiE(jetAK8_puppi_pt->at(iJet), jetAK8_puppi_eta->at(iJet), jetAK8_puppi_phi->at(iJet), jetAK8_puppi_e->at(iJet));
           
              //W_csvValues = getLeadingSubjets(subjetAK8_puppi_softdrop_csv->at(iJet));

              //cout << "    for W jet, get csv values " << W_csvValues.leading << ", " << W_csvValues.subleading << endl;
              //W_subjetCutDecisions = getSubjetCutDecisions(W_csvValues);
      }
          //}
        //}
      
      else if (debugFlag && dumpEventInfo) cout << " this event failed the jet requirement for the W branch!" << endl;
    }

    if (debugFlag && dumpEventInfo) {  // Print some checks
      cout << "    eventHasTightPho is: " <<  eventHasTightPho  << endl;
    }

    // Fill histograms with events that have a photon passing ID and a loose jet
    if ( (eventHasTightPho  && leadingPhoton.Pt()>leadingPhPtCut && abs(leadingPhoton.Eta()) < phoEtaMax)) {
      if( (eventHasWPuppi_softdropJet && WJet_puppi_softdrop.Pt() > WJetMinPtCut && abs(WJet_puppi_softdrop.Eta()) < jetEtaMax )) {
        sumVector = leadingPhoton + WJet_puppi_softdrop;
        if (debugFlag && dumpEventInfo) {
          cout << "    using matching with puppi_softdrop,   sumvector E is: " << sumVector.E() << endl;
          cout << "                                  sumvector M is: " << sumVector.M() << endl;
          cout << "                                    tau2/tau1 is: " << puppi_softdrop_WJetTau2/puppi_softdrop_WJetTau1 << endl;
        }

      //Base Observables
        WJet_puppi_abseta=std::abs(WJet_puppi_softdrop.Eta());
        WJet_puppi_eta=WJet_puppi_softdrop.Eta();
        WJet_puppi_phi=WJet_puppi_softdrop.Phi();
        WJet_puppi_pt=WJet_puppi_softdrop.Pt();

        //Boosting to reference frame
        boostedPho = leadingPhoton;
        boostedPho.Boost(-(sumVector.BoostVector()));
        boostedJet = WJet_puppi_softdrop;
        boostedJet.Boost(-(sumVector.BoostVector()));

        leadingPhAbsEta = std::abs(leadingPhEta);
        //TODO: Check this; seems too big
        phJetInvMass_puppi_softdrop_W=sumVector.M();


      //Physically derived observables 
        cosThetaStar = std::abs(boostedPho.Pz()/boostedPho.P());
        phPtOverMgammaj = leadingPhPt/phJetInvMass_puppi_softdrop_W;
        WJetTau21 = puppi_softdrop_WJetTau2/puppi_softdrop_WJetTau1;
        //weightFactor = 1/trigEffHist->GetBinContent(trigEffHist->GetXaxis()->FindBin(leadingPhoton.Pt()));
        // What is turnOnCurve
        weightFactor = 1.0/(turnOnCurve->Eval(leadingPhoton.Pt()));
        //New
        WJetPtOverMgammaj = WJet_puppi_pt/sumVector.M();

        phJetDeltaR_W=leadingPhoton.DeltaR(WJet_puppi_softdrop);
        

        if ( phJetDeltaR_W < leadingPhoWJetDeltaRCut) {
          if (debugFlag && dumpEventInfo) cout << "this event failed the DR cut!" << endl;
          continue;
        }
        //if (loadEventMap && FindEvent(EVENT_run, EVENT_lumiBlock, EVENT_event)!=0) cout << "found an event that passed selection but did not fire the trigger" << endl;
        outputTreeWgam->Fill();
        //WJet_puppi_softdrop.SetT(90);
      }
      else if (debugFlag && dumpEventInfo) {
        cout << " this event failed 'if( (eventHasWPuppi_softdropJet && WJet_puppi_softdrop.Pt() > 250 && abs(WJet_puppi_softdrop.Eta()) < 2.6 ))'" << endl;
        cout << "eventHasWPuppi_softdropJet="  << eventHasWPuppi_softdropJet << ", WJet_puppi_softdrop.Pt()=" << WJet_puppi_softdrop.Pt() << ", abs(WJet_puppi_softdrop.Eta())=" << WJet_puppi_softdrop.Eta() << endl;
      }
    }
    if (debugFlag && entriesToCheck == jentry) break; // when debugFlag is true, break the event loop after reaching entriesToCheck 
  }



  outputFile->Write();
  outputFile->Close();

  cout.flush();
  cout << "100% done: Scanned " << nentries << " events.       " << endl;
  cout << "HLT_Photon175 fired " << eventsPassingTrigger_175 << " times" << endl;
  cout << "The HLT_Photon175 efficiency was " << (float) eventsPassingTrigger_175/ (float)nentries << endl;
  cout << "HLT_Photon165_HE10 fired " << eventsPassingTrigger_165HE10 << " times" << endl;
  cout << "The HLT_Photon165_HE10 efficiency was " << (float) eventsPassingTrigger_165HE10/ (float)nentries << endl;
  cout << "\nCompleted output file is " << outputFileName.c_str() <<".\n" << endl;
}

float WgammaSelector::computeOverallSF(std::string category, float jetPt, float photonPt, float photonEta, bool debug) {
  return computePhotonSF(photonPt, photonEta, debug);
}

//TODO
float WgammaSelector::computePhotonSF(float photonPt, float photonEta, bool debug) {
  if (photonEta > 0) {
    if (photonEta < 0.8) {
      return 0.99667 * 0.9938;
    }
    else {
      return 1.01105 * 0.9938;
    }
  }
  else {
    if(photonEta > -0.8) {
      return 0.992282 * 0.9938;
    }
    else {
      return 0.995595 * 0.9938;
    }
  }
}


//HgammaSelector::leadingSubjets HgammaSelector::getLeadingSubjets(vector<float> puppi_softdropJet) {
//  // Note: in miniaod, there are only two subjets stored since the declustering is done recursively and miniaod's declustering stops after splitting into two subjets
//  leadingSubjets topCSVs;
//  topCSVs.leading = -10.;
//  topCSVs.subleading = -10.;
//  for (uint iSubjet=0; iSubjet<puppi_softdropJet.size(); ++iSubjet) {
//    if (puppi_softdropJet.at(iSubjet)>topCSVs.leading) {
//      topCSVs.subleading = topCSVs.leading;
//      topCSVs.leading = puppi_softdropJet.at(iSubjet);
//    }
//    else if (topCSVs.leading > puppi_softdropJet.at(iSubjet) && topCSVs.subleading < puppi_softdropJet.at(iSubjet)) {
//      topCSVs.subleading = puppi_softdropJet.at(iSubjet);
//    }
//  }
//  return topCSVs;
//}


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

//unsigned short HgammaSelector::FindEvent(unsigned int run, unsigned int lumiBlock, unsigned long long event) {
//  std::unordered_map<unsigned int, std::unordered_map<unsigned int, std::vector<unsigned long long> > >::iterator runIt = eventMap->find(run);
//  if (runIt != eventMap->end()) {
//    std::unordered_map<unsigned int, std::vector<unsigned long long> >::iterator lumiIt = eventMap->at(run).find(lumiBlock);
//    if (lumiIt != eventMap->at(run).end()) {
//
//      if (std::find(eventMap->at(run).at(lumiBlock).begin(), eventMap->at(run).at(lumiBlock).end(), event) != eventMap->at(run).at(lumiBlock).end()) {
//        return 0;    // found the event
//      }
//      else return 1; // found the run and lumiblock, but the event wasn't there
//    }
//    else return 2;   // found the run, but lumiblock wasn't there
//  }
//  else return 3;     // didn't find the run
//}
