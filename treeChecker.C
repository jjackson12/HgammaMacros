#define treeChecker_cxx
#include <iostream>
#include <iomanip>
#include "treeChecker.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

using namespace std;

void treeChecker::Loop(string outputFileName)
{
  bool debugFlag             = false ;  // If debugFlag is false, the trigger checking couts won't appear and the loop won't stop when it reaches entriesToCheck
  bool checkTrigger          = false ;
  int  entriesToCheck        = 10    ;  // If debugFlag = true, stop once the number of checked entries reaches entriesToCheck

  float endcap_phoMVAcut     = 0.679 ;  // See here: https://twiki.cern.ch/twiki/bin/view/CMS/MultivariatePhotonIdentificationRun2#Recipes_for_74X_and_on_Phys14_tu
  float barrel_phoMVAcut     = 0.593 ;  // These should change once we move to CMSSW_7_4_16
  bool  eventHasTightPho     = false ; 

  TFile* outputFile          = new TFile(outputFileName.c_str(), "RECREATE");
  TH1F*  leadingPhPtHist     = new TH1F("leadingPhPtHist", "Leading photon pT", 700, 0, 7000);
  float leadingPhPt          = 0.    ;
  TH1F*  leadingJetPtHist    = new TH1F("leadingJetPtHist", "Leading AK8 jet pT", 700, 0, 7000);
  float leadingJetPt         = 0.    ;
  TH1F*  HThist              = new TH1F("HThist", "Scalar sum of jet PT", 700, 0, 7000);
  float HT                   = 0.    ;
  float leadingJetTau1       = -999.    ;
  float leadingJetTau2       = -999.    ;
  float leadingJetTau3       = -999.    ;
  TH1F*  leadingJetTau1Hist  = new TH1F("leadingJetTau1Hist", "Leading jet #tau_{1}",      110, -0.05, 1.05);
  TH1F*  leadingJetTau2Hist  = new TH1F("leadingJetTau2Hist", "Leading jet #tau_{2}",      110, -0.05, 1.05);
  TH1F*  leadingJetTau3Hist  = new TH1F("leadingJetTau3Hist", "Leading jet #tau_{3}",      110, -0.05, 1.05);
  TH1F*  leadingJetT2T1      = new TH1F("leadingJetT2T1", "Leading jet #tau_{2}/#tau_{1}", 110, -0.05, 1.05);
  TH1F*  leadingJetT3T2      = new TH1F("leadingJetT3T2", "Leading jet #tau_{3}/#tau_{2}", 110, -0.05, 1.05);

  //   In a ROOT session, you can do:
  //      root> .L treeChecker.C
  //      root> treeChecker t
  //      root> t.GetEntry(12); // Fill t data members with entry number 12
  //      root> t.Show();       // Show values of entry 12
  //      root> t.Show(16);     // Read and show values of entry 16
  //      root> t.Loop();       // Loop on all entries
  //

  //     This is the loop skeleton where:
  //    jentry is the global entry number in the chain
  //    ientry is the entry number in the current Tree
  //  Note that the argument to GetEntry must be:
  //    jentry for TChain::GetEntry
  //    ientry for TTree::GetEntry and TBranch::GetEntry
  //
  //       To read only selected branches, Insert statements like:
  // METHOD1:
    fChain->SetBranchStatus("*",0);  // disable all branches
    fChain->SetBranchStatus("HLT_isFired",1);  // activate branchname
    fChain->SetBranchStatus("ph_pt",1);  
    fChain->SetBranchStatus("ph_eta",1);  
    fChain->SetBranchStatus("ph_mvaVal",1);
    fChain->SetBranchStatus("ph_mvaCat",1);
    fChain->SetBranchStatus("jetAK8_pt",1);  
    fChain->SetBranchStatus("jetAK8_tau1",1);  
    fChain->SetBranchStatus("jetAK8_tau2",1);  
    fChain->SetBranchStatus("jetAK8_tau3",1);  
  // METHOD2: replace line
  //    fChain->GetEntry(jentry);       //read all branches
  //by  b_branchname->GetEntry(ientry); //read only this branch
  if (fChain == 0) return;

  Long64_t nentries = fChain->GetEntriesFast();

  Long64_t nbytes = 0, nb = 0;
  for (Long64_t jentry=0; jentry<nentries;++jentry) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;


    leadingPhPt      = 0.    ;
    leadingJetPt     = 0.    ;
    leadingJetTau1   = 0.    ;
    leadingJetTau2   = 0.    ;
    leadingJetTau3   = 0.    ;
    HT               = 0.    ;
    eventHasTightPho = false ;

    // print out trigger information
    if (jentry%10000==0) {
      cout << fixed << setw(3) << setprecision(1) << (float(jentry)/float(nentries))*100 << "% done: Scanned " << jentry << " events." << endl;
    }
    if (debugFlag && checkTrigger) {
      cout << "\n \n Trigger info for entry number " << jentry << ":" << endl;
      for(map<string,bool>::iterator it = HLT_isFired->begin(); it != HLT_isFired->end(); ++it) {
        if (debugFlag && checkTrigger) { 
          cout << it->first << " = " << it->second << endl;

        }
      }
    }
    //cout << "HLT_isFired[HLT_Photon175_v2] is: " << (*HLT_isFired)[string("HLT_Photon175_v2")] << endl;
    if (debugFlag) cout << "In event number " << jentry << ":" << endl;
    
    for (uint iPh = 0; iPh<ph_pt->size() ; ++iPh) { 
      if (debugFlag) {
        cout << "    Photon " << iPh << " has pT " << ph_pt->at(iPh)  << ", eta =" << ph_eta->at(iPh) << ", ph_mvaVal = " << ph_mvaVal->at(iPh) << ", ph_mvaCat = " << ph_mvaCat->at(iPh) << endl;
      }
      eventHasTightPho = (ph_mvaCat->at(iPh)==0 && ph_mvaVal->at(iPh)>=barrel_phoMVAcut) || (ph_mvaCat->at(iPh)==1 && ph_mvaVal->at(iPh)>=endcap_phoMVAcut);
      if (debugFlag && eventHasTightPho) cout << "    This event has a tight photon." << endl;
      if (ph_pt->at(iPh) > leadingPhPt) leadingPhPt = ph_pt->at(iPh);
    }
    leadingPhPtHist->Fill(leadingPhPt);
    
    for (uint iJet = 0; iJet<jetAK8_pt->size() ; ++iJet) { 
      if (debugFlag) cout << "    AK8 Jet " << iJet << " has pT " << jetAK8_pt->at(iJet) << endl;
      if (jetAK8_pt->at(iJet) > leadingJetPt) {
        leadingJetPt   = jetAK8_pt->at(iJet);
        leadingJetTau1 = jetAK8_tau1->at(iJet);
        leadingJetTau2 = jetAK8_tau2->at(iJet);
        leadingJetTau3 = jetAK8_tau3->at(iJet);
      }
      HT+=jetAK8_pt->at(iJet);
    }
    leadingJetPtHist->Fill(leadingJetPt);
    HThist->Fill(HT);
    if (eventHasTightPho && leadingJetPt>0) {
      leadingJetTau1Hist->Fill(leadingJetTau1);
      leadingJetTau2Hist->Fill(leadingJetTau2);
      leadingJetTau3Hist->Fill(leadingJetTau3);
      leadingJetT2T1->Fill(leadingJetTau2/leadingJetTau1);
      leadingJetT3T2->Fill(leadingJetTau3/leadingJetTau2);
    }

    nb = fChain->GetEntry(jentry);   nbytes += nb;
    // if (Cut(ientry) < 0) continue;
    if (debugFlag && entriesToCheck == jentry) break;
  }
  outputFile->cd();
  leadingPhPtHist->Write();
  leadingJetPtHist->Write();
  HThist->Write();
  leadingJetTau1Hist->Write();
  leadingJetTau2Hist->Write();
  leadingJetTau3Hist->Write();
  leadingJetT2T1->Write();
  leadingJetT3T2->Write();
  outputFile->Close();
}
