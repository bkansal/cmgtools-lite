#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *

for sample in dataSamples:
    sample.json="$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"

# L2res triggers
from CMGTools.ObjectStudies.samples.jet_triggers_13TeV_DATA2016 import L2res_triggers 
triggers = sum(L2res_triggers.values(),[])

JetHT_Run2016B_03Feb2017_v2.triggers    = triggers 
JetHT_Run2016C_03Feb2017.triggers       = triggers
JetHT_Run2016D_03Feb2017.triggers       = triggers
JetHT_Run2016E_03Feb2017.triggers       = triggers
JetHT_Run2016F_03Feb2017.triggers       = triggers
JetHT_Run2016G_03Feb2017.triggers       = triggers
JetHT_Run2016H_03Feb2017_v2.triggers    = triggers
JetHT_Run2016H_03Feb2017_v3.triggers    = triggers
