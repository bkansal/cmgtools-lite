##########################################################
##       CONFIGURATION FOR L2res ntuples                ## 
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
import pickle, os

#Load all analyzers
from CMGTools.ObjectStudies.analyzers.jet_modules_cff import *

#!# #-------- SAMPLES AND SEQUENCE -----------

selectedComponents = [
        ]

sequence  = cfg.Sequence( jet_coreSequence )
sequence += jet_objectSequence 

# trigger
from CMGTools.ObjectStudies.samples.jet_triggers_13TeV_DATA2016 import L2res_triggers 
# trigger flag analyzer
triggerFlagsAna.triggerBits         = L2res_triggers

# make tree Producer
from CMGTools.ObjectStudies.analyzers.jet_treeProducer import *

# add the L2res collections to the default (global) collections
L2res_collections = jet_collections
L2res_collections.update( L2res_extra_collections )
L2res_globalVariables = jet_globalVariables + L2res_extra_variables 

test       = 'mc'
if getHeppyOption("mc")  : test = "mc"
if getHeppyOption("data"): test = "data"

# MC or data specific
if test=='mc':
    pass
else:                                     
    triggerFlagsAna.unrollbits          = True
    triggerFlagsAna.saveIsUnprescaled   = True
    triggerFlagsAna.checkL1prescale     = True

# jet collections
#coneSizes = [ 0.3, 0.4, 0.5, 0.6, 0.7, 0.8 ]
jetCollections = [ {'coneSize':0.4, 'flavor':'PFchs'}, {'coneSize':0.4, 'flavor':'PF'} ]
jetCollections += [ {'coneSize':0.3, 'flavor':'PFchs'}, {'coneSize':0.3, 'flavor':'PF'} ]
jetCollections += [ {'coneSize':0.5, 'flavor':'PFchs'}, {'coneSize':0.5, 'flavor':'PF'} ]
jetCollections += [ {'coneSize':0.8, 'flavor':'PFchs'}, {'coneSize':0.8, 'flavor':'PF'} ]

if getHeppyOption("noPreProcessor"): 
    preprocess = False
    preprocessor = None
else:
    preprocess = True
    preprocessorFile = "$CMSSW_BASE/python/CMGTools/ObjectStudies/preprocessor/recluster.py"
    preprocessorPKL  = "$CMSSW_BASE/src/CMGTools/ObjectStudies/data/cmsswPreprocessorOptions.pkl"

    # to be consumed by the preprocessor 
    pickle.dump( { 'isMC': (test=='mc'), 'jetCollections':jetCollections}, file(os.path.expandvars( preprocessorPKL ), 'w') )
    from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
    preprocessor = CmsswPreprocessor(preprocessorFile)
    # re-config default jetAna
    jetAna.jetCol   = ("selectedPatJetsAK4PFCHS","","USER")
    jetAna.genJetCol= ("ak4GenJetsNoNu","","USER")

    # add extra jet analyzers
    for jetCollection in jetCollections:
        coneSize, flavor = jetCollection['coneSize'], jetCollection['flavor']

        if coneSize == 0.4 and flavor=='PFchs': continue # jetAna is included by default with 0.4 cone size
        genJetName = 'ak%iGenJetsNoNu'%(   10*coneSize)
        PATSuffix  = 'AK%i%s'%( 10*coneSize, flavor.upper()) 
        patJetCollectionName  = 'selectedPatJets' + PATSuffix
        jetAna_ = jetAna.clone( 
            name = "jetAnalyzer_"+PATSuffix,
            jetCol = (patJetCollectionName,"","USER"),
            genJetCol= (genJetName,"","USER"),  
            collectionPostFix = PATSuffix 
            )
        sequence.append( jetAna_ )
        L2res_collections.update( { 
            "cleanJetsAll"+PATSuffix : NTupleCollection("Jet"+PATSuffix, jetTypeSusyExtra, 25, help="all jets after full selection and cleaning, sorted by pt, %s"%PATSuffix),
        } )

    # bad Ecal Calib bools
    from CMGTools.ObjectStudies.analyzers.BoolAnalyzer import BoolAnalyzer
    boolAna = BoolAnalyzer.defaultConfig
    boolAna.bools = ["ecalBadCalibFilter", "ecalBadCalibFilterEMin25", "ecalBadCalibFilterEMin75"]
    sequence.append( boolAna )
    L2res_globalVariables += [
        NTupleVariable("ecalBadCalibFilter",  lambda ev: ev.ecalBadCalibFilter, int, help="ecalBadCalibFilter"),
        NTupleVariable("ecalBadCalibFilterEMin25",  lambda ev: ev.ecalBadCalibFilterEMin25, int, help="ecalBadCalibFilterEMin25"),
        NTupleVariable("ecalBadCalibFilterEMin75",  lambda ev: ev.ecalBadCalibFilterEMin75, int, help="ecalBadCalibFilterEMin75"),
    ]
    particleTypeExtra = NTupleObjectType("particleTypeExtra",  baseObjectTypes = [ particleType ], variables = [
        NTupleVariable("pvAssociationQuality",  lambda x : x.pvAssociationQuality(),    type=int, help="pvAssociationQuality"),
        NTupleVariable("fromPV",                lambda x : x.fromPV(),                  type=int, help="fromPV"),
        NTupleVariable("dzAssociatedPV",        lambda x : x.dzAssociatedPV(),                    help="dzAssociatedPV"),
        NTupleVariable("dz",                    lambda x : x.dz(),                                help="dz"),
        NTupleVariable("inCHSJet",              lambda x : x.inCHSJet,                  type=int, help="whether particle is in the CHS Jet"),
        NTupleVariable("inPFJet",               lambda x : x.inPFJet,                   type=int, help="whether particle is in the PF Jet"),
        NTupleVariable("trackHighPurity",       lambda x : x.trackHighPurity(),         type=int, help="trackHighPurity"),
        NTupleVariable("lostInnerHits",         lambda x : x.lostInnerHits(),           type=int, help="lostInnerHits"),
    ])

    # chsDoctor
    from CMGTools.ObjectStudies.analyzers.chsDoctor import chsDoctor
    chsDoc = chsDoctor.defaultConfig
    sequence.append( chsDoc )
    L2res_collections.update( {'leading_jet_candidates' : NTupleCollection("leadingJetPFCands", particleTypeExtra, 100, help="particles of the leading jet") } )

    chsDocR3 = chsDoc.clone(
        name = "chsDocR3",
        postFix = 'R3',
        chsJets = 'cleanJetsAllAK3PFCHS',
        pfJets = 'cleanJetsAllAK3PF',
    )
    sequence.append( chsDocR3 )
    L2res_collections.update( {'leading_jet_candidatesR3' : NTupleCollection("leadingJetPFCandsR3", particleTypeExtra, 100, help="particles of the leading jet") } )

    chsDocR5 = chsDoc.clone(
        name = "chsDocR5",
        postFix = 'R5',
        chsJets = 'cleanJetsAllAK5PFCHS',
        pfJets = 'cleanJetsAllAK5PF',
    )
    sequence.append( chsDocR5 )
    L2res_collections.update( {'leading_jet_candidatesR5' : NTupleCollection("leadingJetPFCandsR5", particleTypeExtra, 100, help="particles of the leading jet") } )

    chsDocR8 = chsDoc.clone(
        name = "chsDocR8",
        postFix = 'R8',
        chsJets = 'cleanJetsAllAK8PFCHS',
        pfJets = 'cleanJetsAllAK8PF',
    )
    sequence.append( chsDocR8 )
    L2res_collections.update( {'leading_jet_candidatesR8' : NTupleCollection("leadingJetPFCandsR8", particleTypeExtra, 100, help="particles of the leading jet") } )

treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducer',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     globalVariables = L2res_globalVariables,
     globalObjects   = L2res_globalObjects,
     collections     = L2res_collections 
)
# Append it to the sequence
sequence.append( treeProducer )

if getHeppyOption("loadSamples"):
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *
    from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
    from CMGTools.RootTools.samples.samples_13TeV_signals import *
    from CMGTools.ObjectStudies.samples.samples_jet_private import *
    for sample in dataSamples:
        sample.json="$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
    if test.lower() == 'mc': 
        selectedComponents = [ QCD_flat ]
        #selectedComponents = [ QCD_flat_noPU ]
    else: 
        selectedComponents = [ JetHT_Run2016C_03Feb2017 ]
        #selectedComponents[0].files = ['file:/afs/cern.ch/user/z/zdemirag/public/forRobert/pickevents_optionA_dijets.root']
        selectedComponents[0].files = ['file:/afs/cern.ch/user/z/zdemirag/public/forRobert/pickevents_optionB_dijets.root']

    for comp in selectedComponents:
            comp.files = comp.files[:1]
            comp.splitFactor = 1

from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
event_class = Events

if getHeppyOption("fetch"):
    event_class = EOSEventsWithDownload

config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
                     preprocessor=preprocessor, # comment if pre-processor non needed
                     events_class = event_class)

