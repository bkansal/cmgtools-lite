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
    NTupleVariable("genBin", lambda ev: ev.genBin, float, mcOnly=True, help="generator binning variable (e.g. ptHat)" ),
]

# new ntuple type for genjets
genJetType = NTupleObjectType("genJets",  baseObjectTypes = [ fourVectorType ], mcOnly=True, variables = [
    NTupleVariable("nConstituents", lambda x : x.nConstituents() ,help="Number of Constituents"),
])

# Standard collections for leptons and AK4 jets

jetTypeSusyExtra.addVariables( [
    NTupleVariable("mcEta",   lambda x : x.mcJet.eta() if getattr(x,"mcJet",None) else 0., mcOnly=True, help="eta of associated gen jet"),
    NTupleVariable("mcPhi",   lambda x : x.mcJet.phi() if getattr(x,"mcJet",None) else 0., mcOnly=True, help="phi of associated gen jet"),
    NTupleVariable("mcDR",   lambda x : deltaR( x.mcJet.eta(), x.mcJet.phi(), x.eta(), x.phi() ) if getattr(x,"mcJet",None) else 0., mcOnly=True, help="phi of associated gen jet"),
] )

jet_globalObjects = { "met" :  NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
                    }

jet_collections = {
            "genParticles"       : NTupleCollection("genPartAll",  genParticleWithMotherId, 200, help="all pruned genparticles"),
            "selectedLeptons"    : NTupleCollection("LepGood", leptonTypeSusy, 8, help="Leptons after the preselection"),
            "otherLeptons"       : NTupleCollection("LepOther", leptonTypeSusy, 8, help="Leptons after the preselection"),
            "cleanJetsAll"       : NTupleCollection("Jet",     jetTypeSusyExtra, 100, help="all jets after full selection and cleaning, sorted by pt"),
            "discardedJets"      : NTupleCollection("DiscJet", jetTypeSusyExtra, 15, help="Jets discarted in the jet-lepton cleaning"),
            "cleanJetsFailIdAll" : NTupleCollection("JetFailId", jetTypeSusyExtra, 15, help="Jets failing id after jet-lepton cleaning"),
            "genJets"            : NTupleCollection("GenJet",  genJetType,  15, help="Gen Jets, sorted by pt"),
}

# MET variables
jet_metVariables = [

    NTupleVariable("chsSumPt", lambda ev : ev.chsSumPt, help="chs sumPt (fromPV definition)"),
    NTupleVariable("met_chsPt", lambda ev : ev.chsMET.pt(), help="chs met p_{T} (fromPV definition)"),
    NTupleVariable("met_chsPhi", lambda ev : ev.chsMET.phi(), help="chs met phi (fromPV definition)"),

]


## PV and PU information.
# define a new ntuple type for the IT PU vertices
pvType = NTupleObjectType("VertexType", variables = [   
    NTupleVariable("z",                 lambda v:v.z(), help="z positon" ), 
    NTupleVariable("ndof",              lambda v:v.ndof(), help="ndof" ), 
    NTupleVariable("isGood",            lambda v: not( v.isFake() or v.ndof()<=4 or abs(v.z())>24 or v.position().Rho()>2), int, help="isGood" ), 
    NTupleVariable("isFake",            lambda v: v.isFake() , int, help="isFake" ), 
    NTupleVariable("normalizedChi2",    lambda v:v.normalizedChi2(), help="normalizedChi2" ), 
    ])
puInfoType = NTupleObjectType("puInfoType", variables = [   
    NTupleVariable("truePUInt",      lambda p:p.nPU(), mcOnly = True, help=" number of true PU interactions" ), 
    ])

PVPU_collections = {
    'vertices' : NTupleCollection( "vertices", pvType, 100, help = "all offline primary vertices"),
    'pileUpInfo'   : NTupleCollection( "BX", puInfoType, 20, mcOnly = True, help = "all BX (sorted -12 ... +3)")
}

## L1res
# global variables for L1res
L1res_globalObjects   = []
L1res_extra_variables = [
    NTupleVariable("nAllVert",  lambda ev: len(ev.vertices), int, help="Number of all vertices"),
]

# define a new ntuple type for the offset energy density
from CMGTools.ObjectStudies.analyzers.OffsetAnalyzer import offset_flavors_stored, offset_eta_thresholds
offsetType = NTupleObjectType("offsetVectorType", variables = [   NTupleVariable(str(k),  operator.itemgetter(k), help="Component %s"%k ) for k in offset_flavors_stored ] )
# L1res extra collections 
L1res_extra_collections = {
    'offset' : NTupleCollection( "Offset", offsetType, len(offset_eta_thresholds) -1, help = "offset density")
}
L1res_extra_collections.update( PVPU_collections )

## L1L2L3
L1L2L3_globalObjects     = jet_globalObjects
L1L2L3_extra_variables   = jet_metVariables
L1L2L3_extra_collections = PVPU_collections 

## L2res

L2res_globalObjects     = jet_globalObjects
L2res_extra_variables   = jet_metVariables
L2res_extra_collections = PVPU_collections 

