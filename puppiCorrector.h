#ifndef puppiCorrector_h
#define puppiCorrector_h
#include <TROOT.h>
#include <TFile.h>
#include <TF1.h>

class puppiCorrector {
public :
  TFile* corrFile;
  TF1* puppisd_corrGEN;  
  TF1* puppisd_corrRECO_cen;  
  TF1* puppisd_corrRECO_for;  
  puppiCorrector();
  puppiCorrector(TString inputCorrFileName);
  virtual ~puppiCorrector();
  virtual float getPUPPIweight(float puppipt, float puppieta);
};
#endif

#ifdef puppiCorrector_cxx
puppiCorrector::puppiCorrector() {
}
puppiCorrector::puppiCorrector(TString inputCorrFileName) {
  corrFile = TFile::Open(inputCorrFileName, "READ");
  puppisd_corrGEN      = (TF1*)corrFile->Get("puppiJECcorr_gen");
  puppisd_corrRECO_cen = (TF1*)corrFile->Get("puppiJECcorr_reco_0eta1v3");
  puppisd_corrRECO_for = (TF1*)corrFile->Get("puppiJECcorr_reco_1v3eta2v5");
}

puppiCorrector::~puppiCorrector()
{
  corrFile->Close();
}
#endif
