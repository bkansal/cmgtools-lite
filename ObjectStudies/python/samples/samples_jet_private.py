import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

#dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"  # use environmental variable, useful for instance to run on CRAB
json='$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'


JetHT_Run2016B_18Apr2017 = kreator.makeDataComponent("JetHT_Run2016B_18Apr2017"         , "/JetHT/Run2016B-18Apr2017_ver2-v1/MINIAOD"         , "CMS", ".*root", json)
JetHT_Run2016C_18Apr2017 = kreator.makeDataComponent("JetHT_Run2016C_18Apr2017"         , "/JetHT/Run2016C-18Apr2017-v1/MINIAOD"         , "CMS", ".*root", json)
JetHT_Run2016D_18Apr2017 = kreator.makeDataComponent("JetHT_Run2016D_18Apr2017"         , "/JetHT/Run2016D-18Apr2017-v1/MINIAOD"         , "CMS", ".*root", json)
JetHT_Run2016E_18Apr2017 = kreator.makeDataComponent("JetHT_Run2016E_18Apr2017"         , "/JetHT/Run2016E-18Apr2017-v1/MINIAOD"         , "CMS", ".*root", json)
JetHT_Run2016F_18Apr2017 = kreator.makeDataComponent("JetHT_Run2016F_18Apr2017"         , "/JetHT/Run2016F-18Apr2017-v1/MINIAOD"         , "CMS", ".*root", json)
JetHT_Run2016G_18Apr2017 = kreator.makeDataComponent("JetHT_Run2016G_18Apr2017"         , "/JetHT/Run2016G-18Apr2017-v1/MINIAOD"         , "CMS", ".*root", json)
JetHT_Run2016H_18Apr2017 = kreator.makeDataComponent("JetHT_Run2016H_18Apr2017"         , "/JetHT/Run2016H-18Apr2017-v1/MINIAOD"         , "CMS", ".*root", json)

JetHT_legacy = [ JetHT_Run2016B_18Apr2017, JetHT_Run2016C_18Apr2017, JetHT_Run2016D_18Apr2017, JetHT_Run2016E_18Apr2017, JetHT_Run2016F_18Apr2017, JetHT_Run2016G_18Apr2017, JetHT_Run2016F_18Apr2017 ]

samples = JetHT_legacy 
