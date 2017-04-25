#define eventMapper_cxx
#include "eventMapper.h"
#include <TFile.h>
#include <TTree.h>

void eventMapper::Loop()
{
//   In a ROOT session, you can do:
//      root> .L eventMapper.C
//      root> eventMapper t
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
    cout << "about to set branch addresses" << endl;
    fChain->SetBranchStatus("*",0);  // disable all branches
    fChain->SetBranchStatus("EVENT_event",1);  // activate branchname
    fChain->SetBranchStatus("EVENT_lumiBlock",1);  // activate branchname
    fChain->SetBranchStatus("EVENT_run",1);  // activate branchname
    cout << "done setting branch addresses" << endl;
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      cout << "about to call LoadTree" << endl;
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      cout << "about to call GetEntry" << endl;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;
      cout << "about to call addEvent" << endl;
      addEvent((unsigned int)EVENT_run, (unsigned int)EVENT_lumiBlock, (unsigned long long)EVENT_event);
      cout << "done calling addEvent" << endl;
   }
   TFile* outFile = new TFile("eventMap.root", "RECREATE");
   TTree* mapTree = new TTree("eventMap", "eventMap");
   mapTree->Branch("eventMap", &eventMap);
   mapTree->Fill();
   mapTree->Write();
   outFile->Close();
   
}

unsigned short eventMapper::findEvent(unsigned int run, unsigned int lumiBlock, unsigned long long event) {
  std::unordered_map<unsigned int, std::unordered_map<unsigned int, std::vector<unsigned long long> > >::iterator runIt = eventMap.find(run);
  if (runIt != eventMap.end()) {
    std::unordered_map<unsigned int, std::vector<unsigned long long> >::iterator lumiIt = eventMap.at(run).find(lumiBlock);
    if (lumiIt != eventMap.at(run).end()) {

      if (std::find(eventMap.at(run).at(lumiBlock).begin(), eventMap.at(run).at(lumiBlock).end(), event) != eventMap.at(run).at(lumiBlock).end()) {
        return 0;    // found the event
      }
      else return 1; // found the run and lumiblock, but the event wasn't there
    }
    else return 2;   // found the run, but lumiblock wasn't there
  }
  else return 3;     // didn't find the run
}


void eventMapper::addEvent(unsigned int run, unsigned int lumiBlock, unsigned long long event) {
  unsigned short searchResult = findEvent(run, lumiBlock, event);
  if (searchResult==0) {
    std::cout << "Error! Trying to add an event that is already present!" << endl; 
  }  
  else if (searchResult == 1) {
    eventMap.at(run).at(lumiBlock).push_back(event);
  }
  else if (searchResult == 2) {
    std::vector<unsigned long long> newLumiBlock;
    newLumiBlock.push_back(event);
    eventMap.at(run).insert(std::pair<unsigned int, std::vector<unsigned long long> >(lumiBlock, newLumiBlock));
  }
  else if (searchResult == 3) {
    std::unordered_map<unsigned int, std::vector<unsigned long long> > newRun;
    std::vector<unsigned long long> newLumiBlock;
    newLumiBlock.push_back(event);
    newRun.insert(std::pair<unsigned int, std::vector<unsigned long long> >(lumiBlock, newLumiBlock));
    eventMap.insert(std::pair<unsigned int, std::unordered_map<unsigned int, std::vector<unsigned long long> > >(run, newRun));
  }
}
