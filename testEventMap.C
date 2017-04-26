#include <unordered_map>
#include "LinkDef.h"
#include <iostream>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TBranch.h>


std::unordered_map<unsigned int, std::unordered_map<unsigned int, std::vector<unsigned long long> > >* eventMap;

void testEventMap()  {
  TFile* eventMapFile = TFile::Open("eventMap_HLT_Photon175.root", "READ");
  TTree* eventMapTree = (TTree*) eventMapFile->Get("eventMap");
  TBranch *b_eventMap = 0;
  eventMapTree->SetBranchAddress("eventMap", &eventMap, &b_eventMap);
  Long64_t tentry = eventMapTree->LoadTree(0);
  b_eventMap->GetEntry(tentry);
  for (auto const &run : *eventMap) {
    cout << run.first << endl;
    for (auto const &lumiBlock : run.second) {
      cout << "   " << lumiBlock.first << endl;
      for (auto const &event : lumiBlock.second) {
        cout << "      " << event << endl;
      }
    }
  }
}

//ushort findEvent(uint run, uint lumiBlock, unsigned long long event) {
//  std::map<uint, std::map<uint, std::vector<unsigned long long> > >::iterator runIt = eventMap.find(run);
//  if (runIt != eventMap.end()) {
//    std::map<uint, std::vector<unsigned long long> >::iterator lumiIt = eventMap.at(run).find(lumiBlock);
//    if (lumiIt != eventMap.at(run).end()) {
//
//      if (std::find(eventMap.at(run).at(lumiBlock).begin(), eventMap.at(run).at(lumiBlock).end(), event) != eventMap.at(run).at(lumiBlock).end()) {
//        return 0;    // found the event
//      }
//      else return 1; // found the run and lumiblock, but the event wasn't there
//    }
//    else return 2;   // found the run, but lumiblock wasn't there
//  }
//  else return 3;     // didn't find the run
//}
