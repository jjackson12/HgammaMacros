//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Apr 25 16:56:46 2017 by ROOT version 6.06/01
// from TTree tree/tree
// found on file: ../HgammaCondor/smallified_singleMuon2016B_0.root
//////////////////////////////////////////////////////////

#ifndef eventMapper_h
#define eventMapper_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "vector"
#include "unordered_map"
#include <iostream>

class eventMapper {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain
   std::unordered_map<unsigned int, std::unordered_map<unsigned int, std::vector<unsigned long long> > > eventMap;

// Fixed size dimensions of array or collections stored in the TTree if any.
   const Int_t kMaxpassFilter_HBHE = 1;
   const Int_t kMaxpassFilter_HBHEIso = 1;
   const Int_t kMaxpassFilter_CSCTightHalo2015 = 1;
   const Int_t kMaxpassFilter_GoodVtx = 1;
   const Int_t kMaxpassFilter_EEBadSc = 1;
   const Int_t kMaxpassFilter_muonBadTrack = 1;

   // Declaration of leaf types
   Int_t           ph_N;
   vector<int>     *ph_pdgId;
   vector<float>   *ph_charge;
   vector<float>   *ph_e;
   vector<float>   *ph_eta;
   vector<float>   *ph_phi;
   vector<float>   *ph_mass;
   vector<float>   *ph_pt;
   vector<float>   *ph_et;
   vector<float>   *ph_rho;
   vector<float>   *ph_superCluster_eta;
   vector<float>   *ph_superCluster_phi;
   vector<float>   *ph_sigmaIetaIeta;
   vector<float>   *ph_hOverE;
   vector<float>   *ph_isoGamma;
   vector<float>   *ph_isoCh;
   vector<bool>    *ph_passEleVeto;
   vector<int>     *ph_passLooseId;
   vector<int>     *ph_passMediumId;
   vector<int>     *ph_passTightId;
   vector<float>   *ph_mvaVal;
   vector<float>   *ph_mvaCat;
   Float_t         rho;
   Int_t           jetAK4_N;
   vector<float>   *jetAK4_pt;
   vector<float>   *jetAK4_eta;
   vector<float>   *jetAK4_mass;
   vector<float>   *jetAK4_phi;
   vector<float>   *jetAK4_e;
   vector<float>   *jetAK4_jec;
   vector<bool>    *jetAK4_IDLoose;
   vector<bool>    *jetAK4_IDTight;
   vector<bool>    *jetAK4_IDTightLepVeto;
   vector<int>     *jetAK4_charge;
   vector<float>   *jetAK4_vtxMass;
   vector<float>   *jetAK4_vtxNtracks;
   vector<float>   *jetAK4_vtx3DVal;
   vector<float>   *jetAK4_vtx3DSig;
   Int_t           jetAK8_N;
   vector<float>   *jetAK8_pt;
   vector<float>   *jetAK8_eta;
   vector<float>   *jetAK8_mass;
   vector<float>   *jetAK8_phi;
   vector<float>   *jetAK8_e;
   vector<float>   *jetAK8_jec;
   vector<float>   *jetAK8_jecUp;
   vector<float>   *jetAK8_jecDown;
   vector<bool>    *jetAK8_IDLoose;
   vector<bool>    *jetAK8_IDTight;
   vector<bool>    *jetAK8_IDTightLepVeto;
   vector<int>     *jetAK8_charge;
   vector<float>   *jetAK8_Hbbtag;
   vector<float>   *jetAK8_csv;
   vector<float>   *jetAK8_tau1;
   vector<float>   *jetAK8_tau2;
   vector<float>   *jetAK8_tau3;
   vector<float>   *jetAK8_pruned_mass;
   vector<float>   *jetAK8_pruned_massCorr;
   vector<float>   *jetAK8_pruned_jec;
   vector<float>   *jetAK8_pruned_jecUp;
   vector<float>   *jetAK8_pruned_jecDown;
   vector<float>   *jetAK8_softdrop_mass;
   vector<float>   *jetAK8_softdrop_massCorr;
   vector<float>   *jetAK8_softdrop_jec;
   map<string,bool> *HLT_isFired;
   Bool_t          passFilter_HBHE;
   Bool_t          passFilter_HBHEIso;
   Bool_t          passFilter_CSCTightHalo2015;
   Bool_t          passFilter_GoodVtx;
   Bool_t          passFilter_EEBadSc;
   Bool_t          passFilter_muonBadTrack;
   Int_t           EVENT_event;
   Int_t           EVENT_run;
   Int_t           EVENT_lumiBlock;

   // List of branches
   TBranch        *b_ph_N;   //!
   TBranch        *b_ph_pdgId;   //!
   TBranch        *b_ph_charge;   //!
   TBranch        *b_ph_e;   //!
   TBranch        *b_ph_eta;   //!
   TBranch        *b_ph_phi;   //!
   TBranch        *b_ph_mass;   //!
   TBranch        *b_ph_pt;   //!
   TBranch        *b_ph_et;   //!
   TBranch        *b_ph_rho;   //!
   TBranch        *b_ph_superCluster_eta;   //!
   TBranch        *b_ph_superCluster_phi;   //!
   TBranch        *b_ph_sigmaIetaIeta;   //!
   TBranch        *b_ph_hOverE;   //!
   TBranch        *b_ph_isoGamma;   //!
   TBranch        *b_ph_isoCh;   //!
   TBranch        *b_ph_passEleVeto;   //!
   TBranch        *b_ph_passLooseId;   //!
   TBranch        *b_ph_passMediumId;   //!
   TBranch        *b_ph_passTightId;   //!
   TBranch        *b_ph_mvaVal;   //!
   TBranch        *b_ph_mvaCat;   //!
   TBranch        *b_rho;   //!
   TBranch        *b_jetAK4_N;   //!
   TBranch        *b_jetAK4_pt;   //!
   TBranch        *b_jetAK4_eta;   //!
   TBranch        *b_jetAK4_mass;   //!
   TBranch        *b_jetAK4_phi;   //!
   TBranch        *b_jetAK4_e;   //!
   TBranch        *b_jetAK4_jec;   //!
   TBranch        *b_jetAK4_IDLoose;   //!
   TBranch        *b_jetAK4_IDTight;   //!
   TBranch        *b_jetAK4_IDTightLepVeto;   //!
   TBranch        *b_jetAK4_charge;   //!
   TBranch        *b_jetAK4_vtxMass;   //!
   TBranch        *b_jetAK4_vtxNtracks;   //!
   TBranch        *b_jetAK4_vtx3DVal;   //!
   TBranch        *b_jetAK4_vtx3DSig;   //!
   TBranch        *b_jetAK8_N;   //!
   TBranch        *b_jetAK8_pt;   //!
   TBranch        *b_jetAK8_eta;   //!
   TBranch        *b_jetAK8_mass;   //!
   TBranch        *b_jetAK8_phi;   //!
   TBranch        *b_jetAK8_e;   //!
   TBranch        *b_jetAK8_jec;   //!
   TBranch        *b_jetAK8_jecUp;   //!
   TBranch        *b_jetAK8_jecDown;   //!
   TBranch        *b_jetAK8_IDLoose;   //!
   TBranch        *b_jetAK8_IDTight;   //!
   TBranch        *b_jetAK8_IDTightLepVeto;   //!
   TBranch        *b_jetAK8_charge;   //!
   TBranch        *b_jetAK8_Hbbtag;   //!
   TBranch        *b_jetAK8_csv;   //!
   TBranch        *b_jetAK8_tau1;   //!
   TBranch        *b_jetAK8_tau2;   //!
   TBranch        *b_jetAK8_tau3;   //!
   TBranch        *b_jetAK8_pruned_mass;   //!
   TBranch        *b_jetAK8_pruned_massCorr;   //!
   TBranch        *b_jetAK8_pruned_jec;   //!
   TBranch        *b_jetAK8_pruned_jecUp;   //!
   TBranch        *b_jetAK8_pruned_jecDown;   //!
   TBranch        *b_jetAK8_softdrop_mass;   //!
   TBranch        *b_jetAK8_softdrop_massCorr;   //!
   TBranch        *b_jetAK8_softdrop_jec;   //!
   TBranch        *b_HLT_isFired;   //!
   TBranch        *b_passFilter_HBHE_;   //!
   TBranch        *b_passFilter_HBHEIso_;   //!
   TBranch        *b_passFilter_CSCTightHalo2015_;   //!
   TBranch        *b_passFilter_GoodVtx_;   //!
   TBranch        *b_passFilter_EEBadSc_;   //!
   TBranch        *b_passFilter_muonBadTrack_;   //!
   TBranch        *b_EVENT_event;   //!
   TBranch        *b_EVENT_run;   //!
   TBranch        *b_EVENT_lumiBlock;   //!

   eventMapper(TTree *tree=0);
   virtual ~eventMapper();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop(std::string triggerName);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
   virtual void     addEvent(unsigned int run, unsigned int lumiBlock, unsigned long long event);
   virtual unsigned short     findEvent(unsigned int run, unsigned int lumiBlock, unsigned long long event);
};

#endif

#ifdef eventMapper_cxx
eventMapper::eventMapper(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("../HgammaCondor/smallified_singleMuon2016B_0.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("../HgammaCondor/smallified_singleMuon2016B_0.root");
      }
      TDirectory * dir = (TDirectory*)f->Get("../HgammaCondor/smallified_singleMuon2016B_0.root:/ntuplizer");
      dir->GetObject("tree",tree);

   }
   Init(tree);
}

eventMapper::~eventMapper()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t eventMapper::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t eventMapper::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void eventMapper::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   ph_pdgId = 0;
   ph_charge = 0;
   ph_e = 0;
   ph_eta = 0;
   ph_phi = 0;
   ph_mass = 0;
   ph_pt = 0;
   ph_et = 0;
   ph_rho = 0;
   ph_superCluster_eta = 0;
   ph_superCluster_phi = 0;
   ph_sigmaIetaIeta = 0;
   ph_hOverE = 0;
   ph_isoGamma = 0;
   ph_isoCh = 0;
   ph_passEleVeto = 0;
   ph_passLooseId = 0;
   ph_passMediumId = 0;
   ph_passTightId = 0;
   ph_mvaVal = 0;
   ph_mvaCat = 0;
   jetAK4_pt = 0;
   jetAK4_eta = 0;
   jetAK4_mass = 0;
   jetAK4_phi = 0;
   jetAK4_e = 0;
   jetAK4_jec = 0;
   jetAK4_IDLoose = 0;
   jetAK4_IDTight = 0;
   jetAK4_IDTightLepVeto = 0;
   jetAK4_charge = 0;
   jetAK4_vtxMass = 0;
   jetAK4_vtxNtracks = 0;
   jetAK4_vtx3DVal = 0;
   jetAK4_vtx3DSig = 0;
   jetAK8_pt = 0;
   jetAK8_eta = 0;
   jetAK8_mass = 0;
   jetAK8_phi = 0;
   jetAK8_e = 0;
   jetAK8_jec = 0;
   jetAK8_jecUp = 0;
   jetAK8_jecDown = 0;
   jetAK8_IDLoose = 0;
   jetAK8_IDTight = 0;
   jetAK8_IDTightLepVeto = 0;
   jetAK8_charge = 0;
   jetAK8_Hbbtag = 0;
   jetAK8_csv = 0;
   jetAK8_tau1 = 0;
   jetAK8_tau2 = 0;
   jetAK8_tau3 = 0;
   jetAK8_pruned_mass = 0;
   jetAK8_pruned_massCorr = 0;
   jetAK8_pruned_jec = 0;
   jetAK8_pruned_jecUp = 0;
   jetAK8_pruned_jecDown = 0;
   jetAK8_softdrop_mass = 0;
   jetAK8_softdrop_massCorr = 0;
   jetAK8_softdrop_jec = 0;
   HLT_isFired = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("ph_N", &ph_N, &b_ph_N);
   fChain->SetBranchAddress("ph_pdgId", &ph_pdgId, &b_ph_pdgId);
   fChain->SetBranchAddress("ph_charge", &ph_charge, &b_ph_charge);
   fChain->SetBranchAddress("ph_e", &ph_e, &b_ph_e);
   fChain->SetBranchAddress("ph_eta", &ph_eta, &b_ph_eta);
   fChain->SetBranchAddress("ph_phi", &ph_phi, &b_ph_phi);
   fChain->SetBranchAddress("ph_mass", &ph_mass, &b_ph_mass);
   fChain->SetBranchAddress("ph_pt", &ph_pt, &b_ph_pt);
   fChain->SetBranchAddress("ph_et", &ph_et, &b_ph_et);
   fChain->SetBranchAddress("ph_rho", &ph_rho, &b_ph_rho);
   fChain->SetBranchAddress("ph_superCluster_eta", &ph_superCluster_eta, &b_ph_superCluster_eta);
   fChain->SetBranchAddress("ph_superCluster_phi", &ph_superCluster_phi, &b_ph_superCluster_phi);
   fChain->SetBranchAddress("ph_sigmaIetaIeta", &ph_sigmaIetaIeta, &b_ph_sigmaIetaIeta);
   fChain->SetBranchAddress("ph_hOverE", &ph_hOverE, &b_ph_hOverE);
   fChain->SetBranchAddress("ph_isoGamma", &ph_isoGamma, &b_ph_isoGamma);
   fChain->SetBranchAddress("ph_isoCh", &ph_isoCh, &b_ph_isoCh);
   fChain->SetBranchAddress("ph_passEleVeto", &ph_passEleVeto, &b_ph_passEleVeto);
   fChain->SetBranchAddress("ph_passLooseId", &ph_passLooseId, &b_ph_passLooseId);
   fChain->SetBranchAddress("ph_passMediumId", &ph_passMediumId, &b_ph_passMediumId);
   fChain->SetBranchAddress("ph_passTightId", &ph_passTightId, &b_ph_passTightId);
   fChain->SetBranchAddress("ph_mvaVal", &ph_mvaVal, &b_ph_mvaVal);
   fChain->SetBranchAddress("ph_mvaCat", &ph_mvaCat, &b_ph_mvaCat);
   fChain->SetBranchAddress("rho", &rho, &b_rho);
   fChain->SetBranchAddress("jetAK4_N", &jetAK4_N, &b_jetAK4_N);
   fChain->SetBranchAddress("jetAK4_pt", &jetAK4_pt, &b_jetAK4_pt);
   fChain->SetBranchAddress("jetAK4_eta", &jetAK4_eta, &b_jetAK4_eta);
   fChain->SetBranchAddress("jetAK4_mass", &jetAK4_mass, &b_jetAK4_mass);
   fChain->SetBranchAddress("jetAK4_phi", &jetAK4_phi, &b_jetAK4_phi);
   fChain->SetBranchAddress("jetAK4_e", &jetAK4_e, &b_jetAK4_e);
   fChain->SetBranchAddress("jetAK4_jec", &jetAK4_jec, &b_jetAK4_jec);
   fChain->SetBranchAddress("jetAK4_IDLoose", &jetAK4_IDLoose, &b_jetAK4_IDLoose);
   fChain->SetBranchAddress("jetAK4_IDTight", &jetAK4_IDTight, &b_jetAK4_IDTight);
   fChain->SetBranchAddress("jetAK4_IDTightLepVeto", &jetAK4_IDTightLepVeto, &b_jetAK4_IDTightLepVeto);
   fChain->SetBranchAddress("jetAK4_charge", &jetAK4_charge, &b_jetAK4_charge);
   fChain->SetBranchAddress("jetAK4_vtxMass", &jetAK4_vtxMass, &b_jetAK4_vtxMass);
   fChain->SetBranchAddress("jetAK4_vtxNtracks", &jetAK4_vtxNtracks, &b_jetAK4_vtxNtracks);
   fChain->SetBranchAddress("jetAK4_vtx3DVal", &jetAK4_vtx3DVal, &b_jetAK4_vtx3DVal);
   fChain->SetBranchAddress("jetAK4_vtx3DSig", &jetAK4_vtx3DSig, &b_jetAK4_vtx3DSig);
   fChain->SetBranchAddress("jetAK8_N", &jetAK8_N, &b_jetAK8_N);
   fChain->SetBranchAddress("jetAK8_pt", &jetAK8_pt, &b_jetAK8_pt);
   fChain->SetBranchAddress("jetAK8_eta", &jetAK8_eta, &b_jetAK8_eta);
   fChain->SetBranchAddress("jetAK8_mass", &jetAK8_mass, &b_jetAK8_mass);
   fChain->SetBranchAddress("jetAK8_phi", &jetAK8_phi, &b_jetAK8_phi);
   fChain->SetBranchAddress("jetAK8_e", &jetAK8_e, &b_jetAK8_e);
   fChain->SetBranchAddress("jetAK8_jec", &jetAK8_jec, &b_jetAK8_jec);
   fChain->SetBranchAddress("jetAK8_jecUp", &jetAK8_jecUp, &b_jetAK8_jecUp);
   fChain->SetBranchAddress("jetAK8_jecDown", &jetAK8_jecDown, &b_jetAK8_jecDown);
   fChain->SetBranchAddress("jetAK8_IDLoose", &jetAK8_IDLoose, &b_jetAK8_IDLoose);
   fChain->SetBranchAddress("jetAK8_IDTight", &jetAK8_IDTight, &b_jetAK8_IDTight);
   fChain->SetBranchAddress("jetAK8_IDTightLepVeto", &jetAK8_IDTightLepVeto, &b_jetAK8_IDTightLepVeto);
   fChain->SetBranchAddress("jetAK8_charge", &jetAK8_charge, &b_jetAK8_charge);
   fChain->SetBranchAddress("jetAK8_Hbbtag", &jetAK8_Hbbtag, &b_jetAK8_Hbbtag);
   fChain->SetBranchAddress("jetAK8_csv", &jetAK8_csv, &b_jetAK8_csv);
   fChain->SetBranchAddress("jetAK8_tau1", &jetAK8_tau1, &b_jetAK8_tau1);
   fChain->SetBranchAddress("jetAK8_tau2", &jetAK8_tau2, &b_jetAK8_tau2);
   fChain->SetBranchAddress("jetAK8_tau3", &jetAK8_tau3, &b_jetAK8_tau3);
   fChain->SetBranchAddress("jetAK8_pruned_mass", &jetAK8_pruned_mass, &b_jetAK8_pruned_mass);
   fChain->SetBranchAddress("jetAK8_pruned_massCorr", &jetAK8_pruned_massCorr, &b_jetAK8_pruned_massCorr);
   fChain->SetBranchAddress("jetAK8_pruned_jec", &jetAK8_pruned_jec, &b_jetAK8_pruned_jec);
   fChain->SetBranchAddress("jetAK8_pruned_jecUp", &jetAK8_pruned_jecUp, &b_jetAK8_pruned_jecUp);
   fChain->SetBranchAddress("jetAK8_pruned_jecDown", &jetAK8_pruned_jecDown, &b_jetAK8_pruned_jecDown);
   fChain->SetBranchAddress("jetAK8_softdrop_mass", &jetAK8_softdrop_mass, &b_jetAK8_softdrop_mass);
   fChain->SetBranchAddress("jetAK8_softdrop_massCorr", &jetAK8_softdrop_massCorr, &b_jetAK8_softdrop_massCorr);
   fChain->SetBranchAddress("jetAK8_softdrop_jec", &jetAK8_softdrop_jec, &b_jetAK8_softdrop_jec);
   fChain->SetBranchAddress("HLT_isFired", &HLT_isFired, &b_HLT_isFired);
   fChain->SetBranchAddress("passFilter_HBHE", &passFilter_HBHE, &b_passFilter_HBHE_);
   fChain->SetBranchAddress("passFilter_HBHEIso", &passFilter_HBHEIso, &b_passFilter_HBHEIso_);
   fChain->SetBranchAddress("passFilter_CSCTightHalo2015", &passFilter_CSCTightHalo2015, &b_passFilter_CSCTightHalo2015_);
   fChain->SetBranchAddress("passFilter_GoodVtx", &passFilter_GoodVtx, &b_passFilter_GoodVtx_);
   fChain->SetBranchAddress("passFilter_EEBadSc", &passFilter_EEBadSc, &b_passFilter_EEBadSc_);
   fChain->SetBranchAddress("passFilter_muonBadTrack", &passFilter_muonBadTrack, &b_passFilter_muonBadTrack_);
   fChain->SetBranchAddress("EVENT_event", &EVENT_event, &b_EVENT_event);
   fChain->SetBranchAddress("EVENT_run", &EVENT_run, &b_EVENT_run);
   fChain->SetBranchAddress("EVENT_lumiBlock", &EVENT_lumiBlock, &b_EVENT_lumiBlock);
   Notify();
}

Bool_t eventMapper::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void eventMapper::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t eventMapper::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef eventMapper_cxx
