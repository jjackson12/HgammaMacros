#define puppiCorrector_cxx
#include "puppiCorrector.h"

float puppiCorrector::getPUPPIweight(float puppipt, float puppieta) {

  float genCorr  = 1.;
  float recoCorr = 1.;
  float totalWeight = 1.;
        
  genCorr =  puppisd_corrGEN->Eval( puppipt );
  if( fabs(puppieta)  <= 1.3 ) {
    recoCorr = puppisd_corrRECO_cen->Eval( puppipt );
  }
  else {
    recoCorr = puppisd_corrRECO_for->Eval( puppipt );
  }
  
  totalWeight = genCorr * recoCorr;

  return totalWeight;
}
