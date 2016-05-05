from ROOT import *
from pyrootTools import instance
instance("higgs", ["../physics/may5_btagging/small3_SilverJson_may5.root", "test.root", "compile"])
h = higgs()
h.Loop()


