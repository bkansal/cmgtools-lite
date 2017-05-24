from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import * 
from PhysicsTools.Heppy.analyzers.core.autovars import NTupleCollection
from CMGTools.TTHAnalysis.analyzers.ntupleTypes import *

import operator

# Variables for everyone
jet_globalVariables = [

    NTupleVariable("Flag_badMuonMoriond2017",  lambda ev: ev.badMuonMoriond2017, int, help="bad muon found in event (Moriond 2017 filter)?"),
    NTupleVariable("Flag_badCloneMuonMoriond2017",  lambda ev: ev.badCloneMuonMoriond2017, int, help="clone muon found in event (Moriond 2017 filter)?"),
    NTupleVariable("badCloneMuonMoriond2017_maxPt",  lambda ev: max(mu.pt() for mu in ev.badCloneMuonMoriond2017_badMuons) if not ev.badCloneMuonMoriond2017 else 0, help="max pt of any clone muon found in event (Moriond 2017 filter)"),
    NTupleVariable("badNotCloneMuonMoriond2017_maxPt",  lambda ev: max((mu.pt() if mu not in ev.badCloneMuonMoriond2017_badMuons else 0) for mu in ev.badMuonMoriond2017_badMuons) if not ev.badMuonMoriond2017 else 0, help="max pt of any bad non-clone muon found in event (Moriond 2017 filter)"),

    NTupleVariable("rho",  lambda ev: ev.rho, float, help="fixed grid rho fastjet all"),
    NTupleVariable("rhoCN",  lambda ev: ev.rhoCN, float, help="fixed grid rho central neutral"),
    NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"), 
    NTupleVariable("LHEweight_original", lambda ev: ev.LHE_originalWeight if hasattr(ev,'LHE_originalWeight') else 0, mcOnly=True, help="original LHE weight"),

    # ----------------------- HT from LHE event (requires LHE analyzer to have run)  --------------------------------------------------------- #
    NTupleVariable("lheHT", lambda ev : ev.lheHT, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer", mcOnly=True),
    NTupleVariable("lheHTIncoming", lambda ev : ev.lheHTIncoming, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer (only LHE status<0 as mothers)", mcOnly=True),
    NTupleVariable("LHEweight_original", lambda ev: ev.LHE_originalWeight if hasattr(ev,'LHE_originalWeight') else 0, mcOnly=True, help="original LHE weight"),

    NTupleVariable("mu",  lambda ev: getattr(ev, "truePileup_mu", -1), float, help="true PU (mu) from pileup_latest.txt for data, same as nTrueInt for MC."),
    NTupleVariable("truePUIntBX0",  lambda ev: getattr(ev, "truePileup_n", -1), float, mcOnly=True, help="nPU (int number, as drawn from Poissonian with mean nTrueInt) for BX=0"),
]

# new ntuple type for genjets
genJetType = NTupleObjectType("genJets",  baseObjectTypes = [ fourVectorType ], mcOnly=True, variables = [
    NTupleVariable("nConstituents", lambda x : x.nConstituents() ,help="Number of Constituents"),
])

# Standard collections for leptons and AK4 jets
jet_globalCollections = {
            "genParticles"       : NTupleCollection("genPartAll",  genParticleWithMotherId, 200, help="all pruned genparticles"),
            "selectedLeptons"    : NTupleCollection("LepGood", leptonTypeSusy, 8, help="Leptons after the preselection"),
            "otherLeptons"       : NTupleCollection("LepOther", leptonTypeSusy, 8, help="Leptons after the preselection"),
            "cleanJetsAll"       : NTupleCollection("Jet",     jetTypeSusyExtra, 25, help="Cental jets after full selection and cleaning, sorted by pt"),
            "discardedJets"      : NTupleCollection("DiscJet", jetTypeSusyExtra, 15, help="Jets discarted in the jet-lepton cleaning"),
            "cleanJetsFailIdAll" : NTupleCollection("JetFailId", jetTypeSusyExtra, 15, help="Jets failing id after jet-lepton cleaning"),
            "genJets"            : NTupleCollection("GenJet",  genJetType,  15, help="Gen Jets, sorted by pt"),
}


## PV and PU information.
# define a new ntuple type for the IT PU vertices
pvType = NTupleObjectType("VertexType", variables = [   
    NTupleVariable("z",      lambda v:v.z(), help="z positon" ), 
    ])
puInfoType = NTupleObjectType("puInfoType", variables = [   
    NTupleVariable("truePUInt",      lambda p:p.nPU(), mcOnly = True, help=" number of true PU interactions" ), 
    ])

PVPU_collections = {
    'goodVertices' : NTupleCollection( "GoodVertices", pvType, 100, help = "good offline primary vertices"),
    'pileUpInfo'   : NTupleCollection( "BX", puInfoType, 20, mcOnly = True, help = "all BX (sorted -12 ... 0)")
}


## L1res
# global variables for L1res
L1res_extra_variables = [
    NTupleVariable("nAllVert",  lambda ev: len(ev.vertices), int, help="Number of all vertices"),
]

# define a new ntuple type for the offset energy density
from CMGTools.ObjectStudies.analyzers.OffsetAnalyzer import offset_flavors_stored, offset_eta_thresholds
offsetType = NTupleObjectType("offsetVectorType", variables = [   NTupleVariable(str(k),  operator.itemgetter(k), help="Component %s"%k ) for k in offset_flavors_stored ] )
# L1res extra collections 
L1res_extra_collections = {
    'offset' : NTupleCollection( "Offset", offsetType, len(offset_eta_thresholds) -1, help = "offset ET")
}

## L1L2L3

L1L2L3_extra_variables   = []
L1L2L3_extra_collections = PVPU_collections 

jet_metVariables = [
    NTupleVariable("met_caloPt", lambda ev : ev.met.caloMETPt(), help="calo met p_{T}"),
    NTupleVariable("met_caloPhi", lambda ev : ev.met.caloMETPhi(), help="calo met phi"),
    NTupleVariable("met_caloSumEt", lambda ev : ev.met.caloMETSumEt(), help="calo met sumEt"),

    NTupleVariable("met_chsPt", lambda ev : ev.chsMET.pt(), help="chs met p_{T} (fromPV definition)"),
    NTupleVariable("met_chsPhi", lambda ev : ev.chsMET.phi(), help="chs met phi (fromPV definition)"),

]

#            NTupleVariable("met_JetEnUp_Pt", lambda ev : ev.met.shiftedPt(ev.met.JetEnUp), help="type1, JetEnUp, pt"),
#            NTupleVariable("met_JetEnUp_Phi", lambda ev : ev.met.shiftedPhi(ev.met.JetEnUp), help="type1, JetEnUp, phi"),
#            NTupleVariable("met_JetResUp_Pt", lambda ev : ev.met.shiftedPt(ev.met.JetResUp), help="type1, JetResUp, pt"),
#            NTupleVariable("met_JetResUp_Phi", lambda ev : ev.met.shiftedPhi(ev.met.JetResUp), help="type1, JetResUp, phi"),
##            NTupleVariable("met_JetResUpSmear_Pt", lambda ev : ev.met.shiftedPt(ev.met.JetResUpSmear), help="type1, JetResUpSmear, pt"),
##            NTupleVariable("met_JetResUpSmear_Phi", lambda ev : ev.met.shiftedPhi(ev.met.JetResUpSmear), help="type1, JetResUpSmear, phi"),
#            NTupleVariable("met_MuonEnUp_Pt", lambda ev : ev.met.shiftedPt(ev.met.MuonEnUp), help="type1, MuonEnUp, pt"),
#            NTupleVariable("met_MuonEnUp_Phi", lambda ev : ev.met.shiftedPhi(ev.met.MuonEnUp), help="type1, MuonEnUp, phi"),
#            NTupleVariable("met_ElectronEnUp_Pt", lambda ev : ev.met.shiftedPt(ev.met.ElectronEnUp), help="type1, ElectronEnUp, pt"),
#            NTupleVariable("met_ElectronEnUp_Phi", lambda ev : ev.met.shiftedPhi(ev.met.ElectronEnUp), help="type1, ElectronEnUp, phi"),
#            NTupleVariable("met_TauEnUp_Pt", lambda ev : ev.met.shiftedPt(ev.met.TauEnUp), help="type1, TauEnUp, pt"),
#            NTupleVariable("met_TauEnUp_Phi", lambda ev : ev.met.shiftedPhi(ev.met.TauEnUp), help="type1, TauEnUp, phi"),
#            NTupleVariable("met_UnclusteredEnUp_Pt", lambda ev : ev.met.shiftedPt(ev.met.UnclusteredEnUp), help="type1, UnclusteredEnUp, pt"),
#            NTupleVariable("met_UnclusteredEnUp_Phi", lambda ev : ev.met.shiftedPhi(ev.met.UnclusteredEnUp), help="type1, UnclusteredEnUp, phi"),
#            NTupleVariable("met_ElectronEnUp_Pt", lambda ev : ev.met.shiftedPt(ev.met.ElectronEnUp), help="type1, ElectronEnUp, pt"),
#            NTupleVariable("met_ElectronEnUp_Phi", lambda ev : ev.met.shiftedPhi(ev.met.ElectronEnUp), help="type1, ElectronEnUp, phi"),
#
#
#            NTupleVariable("met_JetEnDown_Pt", lambda ev : ev.met.shiftedPt(ev.met.JetEnDown), help="type1, JetEnDown, pt"),
#            NTupleVariable("met_JetEnDown_Phi", lambda ev : ev.met.shiftedPhi(ev.met.JetEnDown), help="type1, JetEnDown, phi"),
#            NTupleVariable("met_JetResDown_Pt", lambda ev : ev.met.shiftedPt(ev.met.JetResDown), help="type1, JetResDown, pt"),
#            NTupleVariable("met_JetResDown_Phi", lambda ev : ev.met.shiftedPhi(ev.met.JetResDown), help="type1, JetResDown, phi"),
##            NTupleVariable("met_JetResDownSmear_Pt", lambda ev : ev.met.shiftedPt(ev.met.JetResDownSmear), help="type1, JetResDownSmear, pt"),
##            NTupleVariable("met_JetResDownSmear_Phi", lambda ev : ev.met.shiftedPhi(ev.met.JetResDownSmear), help="type1, JetResDownSmear, phi"),
#            NTupleVariable("met_MuonEnDown_Pt", lambda ev : ev.met.shiftedPt(ev.met.MuonEnDown), help="type1, MuonEnDown, pt"),
#            NTupleVariable("met_MuonEnDown_Phi", lambda ev : ev.met.shiftedPhi(ev.met.MuonEnDown), help="type1, MuonEnDown, phi"),
#            NTupleVariable("met_ElectronEnDown_Pt", lambda ev : ev.met.shiftedPt(ev.met.ElectronEnDown), help="type1, ElectronEnDown, pt"),
#            NTupleVariable("met_ElectronEnDown_Phi", lambda ev : ev.met.shiftedPhi(ev.met.ElectronEnDown), help="type1, ElectronEnDown, phi"),
#            NTupleVariable("met_TauEnDown_Pt", lambda ev : ev.met.shiftedPt(ev.met.TauEnDown), help="type1, TauEnDown, pt"),
#            NTupleVariable("met_TauEnDown_Phi", lambda ev : ev.met.shiftedPhi(ev.met.TauEnDown), help="type1, TauEnDown, phi"),
#            NTupleVariable("met_UnclusteredEnDown_Pt", lambda ev : ev.met.shiftedPt(ev.met.UnclusteredEnDown), help="type1, UnclusteredEnDown, pt"),
#            NTupleVariable("met_UnclusteredEnDown_Phi", lambda ev : ev.met.shiftedPhi(ev.met.UnclusteredEnDown), help="type1, UnclusteredEnDown, phi"),
#            NTupleVariable("met_ElectronEnDown_Pt", lambda ev : ev.met.shiftedPt(ev.met.ElectronEnDown), help="type1, ElectronEnDown, pt"),
#            NTupleVariable("met_ElectronEnDown_Phi", lambda ev : ev.met.shiftedPhi(ev.met.ElectronEnDown), help="type1, ElectronEnDown, phi"),


#            "genParticles"     : NTupleCollection("genPartAll",  genParticleWithMotherId, 200, help="all pruned genparticles"), # need to decide which gen collection ?
#            ## ---------------------------------------------
#            "selectedLeptons" : NTupleCollection("LepGood", leptonTypeSusy, 8, help="Leptons after the preselection"),
#            "otherLeptons"    : NTupleCollection("LepOther", leptonTypeSusy, 8, help="Leptons after the preselection"),
#            "selectedTaus"    : NTupleCollection("TauGood", tauTypeSusy, 3, help="Taus after the preselection"),
#            "selectedIsoTrack"    : NTupleCollection("isoTrack", isoTrackType, 50, help="isoTrack, sorted by pt"),


#        NTupleVariable("lheHT", lambda ev : ev.lheHT, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer"),
#        NTupleVariable("lheHTIncoming", lambda ev : ev.lheHTIncoming, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer (only LHE status<0 as mothers)"),

#met_globalObjects = {
#    "met" : NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
#    "metPuppi" : NTupleObject("metPuppi", metType, help="PF E_{T}^{miss}, after type 1 corrections (Puppi)"),
#    }
#
#met_collections = {
##    "genleps"         : NTupleCollection("genLep",     genParticleWithLinksType, 10, help="Generated leptons (e/mu) from W/Z decays"),
##    "gentauleps"      : NTupleCollection("genLepFromTau", genParticleWithLinksType, 10, help="Generated leptons (e/mu) from decays of taus from W/Z/h decays"),
##    "gentaus"         : NTupleCollection("genTau",     genParticleWithLinksType, 10, help="Generated leptons (tau) from W/Z decays"),
##    "generatorSummary" : NTupleCollection("GenPart", genParticleWithLinksType, 100 , help="Hard scattering particles, with ancestry and links"),
#    "selectedLeptons" : NTupleCollection("lep", leptonType, 50, help="Leptons after the preselection", filter=lambda l : l.pt()>10 ),
##    "selectedPhotons"    : NTupleCollection("gamma", photonType, 50, help="photons with pt>20 and loose cut based ID"),
##    "cleanJetsAll"       : NTupleCollection("jet", jetType, 100, help="all jets (w/ x-cleaning, w/ ID applied w/o PUID applied pt>20 |eta|<5.2) , sorted by pt", filter=lambda l : l.pt()>100  ),
#    }

#            ## ---------------------------------------------
#            ##------------------------------------------------
#            "selectedPhotons"    : NTupleCollection("gamma", photonTypeSusy, 50, help="photons with pt>15 and loose cut based ID"),
#            "LHE_weights" : NTupleCollection("LHEweight", weightsInfoType, 1000, mcOnly=True, help="LHE weight info"),
