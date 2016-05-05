//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu May  5 19:49:35 2016 by ROOT version 6.06/02
// from TTree higgs/higgs
// found on file: ../physics/may5_btagging/small3_SilverJson_may5.root
//////////////////////////////////////////////////////////

#ifndef higgs_h
#define higgs_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class higgs {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Float_t         higgsJett2t1;
   Float_t         higgsJet_HbbTag;
   Float_t         test_looseloose;
 //treeChecker::leadingSubjets *higgs_csvValues;
   Float_t         leading;
   Float_t         subleading;
 //treeChecker::passSubjetCuts *higgs_subjetCutDecisions;
   Bool_t          loose_loose;
   Bool_t          medium_loose;
   Bool_t          medium_medium;
   Bool_t          tight_loose;
   Bool_t          tight_medium;
   Bool_t          tight_tight;
   Bool_t          higgs_looseloose;
   Float_t         cosThetaStar;
   Float_t         phPtOverMgammaj;
   Float_t         leadingPhEta;
   Float_t         leadingPhPhi;
   Float_t         leadingPhPt;
   Float_t         leadingPhAbsEta;
   Float_t         phJetInvMass_pruned_higgs;
   Float_t         phJetDeltaR_higgs;
   Float_t         higgsJet_pruned_abseta;
   Float_t         higgsPrunedJetCorrMass;

   // List of branches
   TBranch        *b_higgsJett2t1;   //!
   TBranch        *b_higgsJet_HbbTag;   //!
   TBranch        *b_test_looseloose;   //!
   TBranch        *b_higgs_csvValues_leading;   //!
   TBranch        *b_higgs_csvValues_subleading;   //!
   TBranch        *b_higgs_subjetCutDecisions_loose_loose;   //!
   TBranch        *b_higgs_subjetCutDecisions_medium_loose;   //!
   TBranch        *b_higgs_subjetCutDecisions_medium_medium;   //!
   TBranch        *b_higgs_subjetCutDecisions_tight_loose;   //!
   TBranch        *b_higgs_subjetCutDecisions_tight_medium;   //!
   TBranch        *b_higgs_subjetCutDecisions_tight_tight;   //!
   TBranch        *b_higgs_looseloose;   //!
   TBranch        *b_cosThetaStar;   //!
   TBranch        *b_phPtOverMgammaj;   //!
   TBranch        *b_leadingPhEta;   //!
   TBranch        *b_leadingPhPhi;   //!
   TBranch        *b_leadingPhPt;   //!
   TBranch        *b_leadingPhAbsEta;   //!
   TBranch        *b_phJetInvMass_pruned_higgs;   //!
   TBranch        *b_phJetDeltaR_higgs;   //!
   TBranch        *b_higgsJet_pruned_abseta;   //!
   TBranch        *b_higgsPrunedJetCorrMass;   //!

   higgs(TTree *tree=0);
   virtual ~higgs();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual int     Loop(float cutvalue, float lowerMassBound, float upperMassBound);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef higgs_cxx
higgs::higgs(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("../physics/may5_btagging/small3_SilverJson_may5.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("../physics/may5_btagging/small3_SilverJson_may5.root");
      }
      f->GetObject("higgs",tree);

   }
   Init(tree);
}

higgs::~higgs()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t higgs::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t higgs::LoadTree(Long64_t entry)
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

void higgs::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("higgsJett2t1", &higgsJett2t1, &b_higgsJett2t1);
   fChain->SetBranchAddress("higgsJet_HbbTag", &higgsJet_HbbTag, &b_higgsJet_HbbTag);
   fChain->SetBranchAddress("test_looseloose", &test_looseloose, &b_test_looseloose);
   fChain->SetBranchAddress("leading", &leading, &b_higgs_csvValues_leading);
   fChain->SetBranchAddress("subleading", &subleading, &b_higgs_csvValues_subleading);
   fChain->SetBranchAddress("loose_loose", &loose_loose, &b_higgs_subjetCutDecisions_loose_loose);
   fChain->SetBranchAddress("medium_loose", &medium_loose, &b_higgs_subjetCutDecisions_medium_loose);
   fChain->SetBranchAddress("medium_medium", &medium_medium, &b_higgs_subjetCutDecisions_medium_medium);
   fChain->SetBranchAddress("tight_loose", &tight_loose, &b_higgs_subjetCutDecisions_tight_loose);
   fChain->SetBranchAddress("tight_medium", &tight_medium, &b_higgs_subjetCutDecisions_tight_medium);
   fChain->SetBranchAddress("tight_tight", &tight_tight, &b_higgs_subjetCutDecisions_tight_tight);
   fChain->SetBranchAddress("higgs_looseloose", &higgs_looseloose, &b_higgs_looseloose);
   fChain->SetBranchAddress("cosThetaStar", &cosThetaStar, &b_cosThetaStar);
   fChain->SetBranchAddress("phPtOverMgammaj", &phPtOverMgammaj, &b_phPtOverMgammaj);
   fChain->SetBranchAddress("leadingPhEta", &leadingPhEta, &b_leadingPhEta);
   fChain->SetBranchAddress("leadingPhPhi", &leadingPhPhi, &b_leadingPhPhi);
   fChain->SetBranchAddress("leadingPhPt", &leadingPhPt, &b_leadingPhPt);
   fChain->SetBranchAddress("leadingPhAbsEta", &leadingPhAbsEta, &b_leadingPhAbsEta);
   fChain->SetBranchAddress("phJetInvMass_pruned_higgs", &phJetInvMass_pruned_higgs, &b_phJetInvMass_pruned_higgs);
   fChain->SetBranchAddress("phJetDeltaR_higgs", &phJetDeltaR_higgs, &b_phJetDeltaR_higgs);
   fChain->SetBranchAddress("higgsJet_pruned_abseta", &higgsJet_pruned_abseta, &b_higgsJet_pruned_abseta);
   fChain->SetBranchAddress("higgsPrunedJetCorrMass", &higgsPrunedJetCorrMass, &b_higgsPrunedJetCorrMass);
   Notify();
}

Bool_t higgs::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void higgs::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
#endif // #ifdef higgs_cxx
