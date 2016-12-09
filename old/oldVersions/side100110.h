//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu May  5 19:59:02 2016 by ROOT version 6.06/02
// from TTree side100110/side100110
// found on file: ../physics/may5_btagging/small3_SilverJson_may5.root
//////////////////////////////////////////////////////////

#ifndef side100110_h
#define side100110_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class side100110 {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Float_t         sideLowFourJett2t1;
   Float_t         cosThetaStar;
   Float_t         phPtOverMgammaj;
   Float_t         leadingPhEta;
   Float_t         leadingPhPhi;
   Float_t         leadingPhPt;
   Float_t         phJetInvMass_pruned_sideLowFour;
   Float_t         phJetDeltaR_sideLowFour;
   Float_t         leadingPhAbsEta;
   Float_t         sideLowFourJet_pruned_abseta;
   Float_t         sideLowFourPrunedJetCorrMass;
   Float_t         sideLowFourJet_HbbTag;
 //treeChecker::leadingSubjets *sideLowFour_csvValues;
   Float_t         leading;
   Float_t         subleading;
 //treeChecker::passSubjetCuts *sideLowFour_subjetCutDecisions;
   Bool_t          loose_loose;
   Bool_t          medium_loose;
   Bool_t          medium_medium;
   Bool_t          tight_loose;
   Bool_t          tight_medium;
   Bool_t          tight_tight;

   // List of branches
   TBranch        *b_sideLowFourJett2t1;   //!
   TBranch        *b_cosThetaStar;   //!
   TBranch        *b_phPtOverMgammaj;   //!
   TBranch        *b_leadingPhEta;   //!
   TBranch        *b_leadingPhPhi;   //!
   TBranch        *b_leadingPhPt;   //!
   TBranch        *b_phJetInvMass_pruned_sideLowFour;   //!
   TBranch        *b_phJetDeltaR_sideLowFour;   //!
   TBranch        *b_leadingPhAbsEta;   //!
   TBranch        *b_sideLowFourJet_pruned_abseta;   //!
   TBranch        *b_sideLowFourPrunedJetCorrMass;   //!
   TBranch        *b_sideLowFourJet_HbbTag;   //!
   TBranch        *b_sideLowFour_csvValues_leading;   //!
   TBranch        *b_sideLowFour_csvValues_subleading;   //!
   TBranch        *b_sideLowFour_subjetCutDecisions_loose_loose;   //!
   TBranch        *b_sideLowFour_subjetCutDecisions_medium_loose;   //!
   TBranch        *b_sideLowFour_subjetCutDecisions_medium_medium;   //!
   TBranch        *b_sideLowFour_subjetCutDecisions_tight_loose;   //!
   TBranch        *b_sideLowFour_subjetCutDecisions_tight_medium;   //!
   TBranch        *b_sideLowFour_subjetCutDecisions_tight_tight;   //!

   side100110(TTree *tree=0);
   virtual ~side100110();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef side100110_cxx
side100110::side100110(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("../physics/may5_btagging/small3_SilverJson_may5.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("../physics/may5_btagging/small3_SilverJson_may5.root");
      }
      f->GetObject("side100110",tree);

   }
   Init(tree);
}

side100110::~side100110()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t side100110::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t side100110::LoadTree(Long64_t entry)
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

void side100110::Init(TTree *tree)
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

   fChain->SetBranchAddress("sideLowFourJett2t1", &sideLowFourJett2t1, &b_sideLowFourJett2t1);
   fChain->SetBranchAddress("cosThetaStar", &cosThetaStar, &b_cosThetaStar);
   fChain->SetBranchAddress("phPtOverMgammaj", &phPtOverMgammaj, &b_phPtOverMgammaj);
   fChain->SetBranchAddress("leadingPhEta", &leadingPhEta, &b_leadingPhEta);
   fChain->SetBranchAddress("leadingPhPhi", &leadingPhPhi, &b_leadingPhPhi);
   fChain->SetBranchAddress("leadingPhPt", &leadingPhPt, &b_leadingPhPt);
   fChain->SetBranchAddress("phJetInvMass_pruned_sideLowFour", &phJetInvMass_pruned_sideLowFour, &b_phJetInvMass_pruned_sideLowFour);
   fChain->SetBranchAddress("phJetDeltaR_sideLowFour", &phJetDeltaR_sideLowFour, &b_phJetDeltaR_sideLowFour);
   fChain->SetBranchAddress("leadingPhAbsEta", &leadingPhAbsEta, &b_leadingPhAbsEta);
   fChain->SetBranchAddress("sideLowFourJet_pruned_abseta", &sideLowFourJet_pruned_abseta, &b_sideLowFourJet_pruned_abseta);
   fChain->SetBranchAddress("sideLowFourPrunedJetCorrMass", &sideLowFourPrunedJetCorrMass, &b_sideLowFourPrunedJetCorrMass);
   fChain->SetBranchAddress("sideLowFourJet_HbbTag", &sideLowFourJet_HbbTag, &b_sideLowFourJet_HbbTag);
   fChain->SetBranchAddress("leading", &leading, &b_sideLowFour_csvValues_leading);
   fChain->SetBranchAddress("subleading", &subleading, &b_sideLowFour_csvValues_subleading);
   fChain->SetBranchAddress("loose_loose", &loose_loose, &b_sideLowFour_subjetCutDecisions_loose_loose);
   fChain->SetBranchAddress("medium_loose", &medium_loose, &b_sideLowFour_subjetCutDecisions_medium_loose);
   fChain->SetBranchAddress("medium_medium", &medium_medium, &b_sideLowFour_subjetCutDecisions_medium_medium);
   fChain->SetBranchAddress("tight_loose", &tight_loose, &b_sideLowFour_subjetCutDecisions_tight_loose);
   fChain->SetBranchAddress("tight_medium", &tight_medium, &b_sideLowFour_subjetCutDecisions_tight_medium);
   fChain->SetBranchAddress("tight_tight", &tight_tight, &b_sideLowFour_subjetCutDecisions_tight_tight);
   Notify();
}

Bool_t side100110::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void side100110::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t side100110::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef side100110_cxx
