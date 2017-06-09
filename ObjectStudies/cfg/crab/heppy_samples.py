#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
from CMGTools.ObjectStudies.samples.samples_jet_private import *

# L2res triggers
from CMGTools.ObjectStudies.samples.jet_triggers_13TeV_DATA2016 import L2res_triggers 
triggers = sum(L2res_triggers.values(),[])

for sample in dataSamples + JetHT_legacy:
    sample.json="$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
    sample.triggers = triggers 
