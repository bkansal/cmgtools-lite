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

SingleNeutrino = kreator.makeMyPrivateMCComponent( "SingleNeutrino", "/SingleNeutrino/schoef-mAOD8026p1-eb6a5691051d9ec7d68d729bb9e6c6fb/USER", "PRIVATE", ".*root", 'phys03', -1, useAAA=True) 

QCD_flat_noPU = kreator.makeMCComponent("QCD_flat_noPU", "/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISummer16MiniAODv2-NoPU_magnetOn_80X_mcRun2_asymptotic_2016_TrancheIV_v4-v2/MINIAODSIM", "CMS", ".*root", -1, useAAA=True)
QCD_flat =      kreator.makeMCComponent("QCD_flat",      "/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISummer16MiniAODv2-PUFlat0to70_magnetOn_80X_mcRun2_asymptotic_2016_TrancheIV_v4-v1/MINIAODSIM", "CMS", ".*root", -1, useAAA=True)

private_mcSamples   = [ SingleNeutrino, QCD_flat_noPU, QCD_flat]
private_dataSamples = JetHT_legacy
private_samples     = private_dataSamples + private_mcSamples 

from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"

#Define splitting
for comp in private_mcSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 250 #  if comp.name in [ "WJets", "DY3JetsM50", "DY4JetsM50","W1Jets","W2Jets","W3Jets","W4Jets","TTJetsHad" ] else 100
#    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
#    comp.puFileData=dataDir+"/puProfile_Data12.root"
#    comp.efficiency = eff2012

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(private_samples)
