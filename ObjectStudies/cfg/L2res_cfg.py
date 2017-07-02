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

# append offset analyzer for L2res to core sequence
from CMGTools.ObjectStudies.analyzers.offsetAnalyzer import offsetAnalyzer
offsetAna = offsetAnalyzer.defaultConfig
sequence.append( offsetAna )

# trigger
from CMGTools.ObjectStudies.samples.jet_triggers_13TeV_DATA2016 import L2res_triggers 
# trigger flag analyzer
triggerFlagsAna.triggerBits         = L2res_triggers

# make tree Producer
from CMGTools.ObjectStudies.analyzers.jet_treeProducer import *

# add the offset collections to the default (global) collections
L2res_collections = jet_collections
L2res_collections.update( L2res_extra_collections )
L2res_globalVariables = jet_globalVariables + L2res_extra_variables 

test       = 'mc'
if getHeppyOption("mc")  : test = "mc"
if getHeppyOption("data"): test = "data"

coneSizes = [ 0.3, 0.4, 0.5, 0.6, 0.7, 0.8 ]

if getHeppyOption("noPreProcessor")  : 
    preprocess = False
else:
    preprocess = True
    preprocessorFile = "$CMSSW_BASE/python/CMGTools/ObjectStudies/preprocessor/recluster.py"
    preprocessorPKL  = "$CMSSW_BASE/src/CMGTools/ObjectStudies/data/cmsswPreprocessorOptions.pkl"
    # to be consumed by the 
    pickle.dump( {
        'isMC': (test=='mc'), 
        'jetCollections':[ {'coneSize':coneSize, 'flavor':'PFchs'} for coneSize in coneSizes ]}, 
        file(os.path.expandvars( preprocessorPKL ), 'w') 
        )
         

if test=='mc':
    pass
else:                                     
    triggerFlagsAna.unrollbits          = True
    triggerFlagsAna.saveIsUnprescaled   = True
    triggerFlagsAna.checkL1prescale     = True

if preprocess:
    from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
    preprocessor = CmsswPreprocessor(preprocessorFile)
    jetAna.jetCol   = ("selectedPatJetsAK4PFCHS","","USER")
    jetAna.genJetCol= ("ak4GenJetsNoNu","","USER")

    for coneSize in coneSizes:
        if coneSize == 0.4: continue
        jetAna_ = jetAna.clone( 
            name = "jetAnalyzer_R%i"%(10*coneSize),
            jetCol = ("selectedPatJetsAK%iPFCHS"%(10*coneSize),"","USER"),
            genJetCol= ("ak%iGenJetsNoNu"%(10*coneSize),"","USER"),  
            collectionPostFix = 'R%i'%(10*coneSize)
            )
        sequence.append( jetAna_ )
        L2res_collections.update( { 
            "cleanJetsAllR%i"%(10*coneSize)       : NTupleCollection("JetR%i"%(10*coneSize), jetTypeSusyExtra, 25, help="all jets after full selection and cleaning, sorted by pt, R=%2.1f"%coneSize),
        } )
else:
    preprocessor = None

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
        selectedComponents = [ QCD_flat_noPU ]
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

