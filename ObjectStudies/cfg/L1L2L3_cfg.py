##########################################################
##       CONFIGURATION FOR L1L2L3 ntuples                ## 
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

#Load all analyzers
from CMGTools.ObjectStudies.analyzers.jet_modules_cff import *

#!# #-------- SAMPLES AND SEQUENCE -----------

selectedComponents = [
        ]

sequence  = cfg.Sequence( jet_coreSequence )
sequence += jet_objectSequence 

# make tree Producer
from CMGTools.ObjectStudies.analyzers.jet_treeProducer import *

# add the offset collections to the default (global) collections
L1L2L3_collections = jet_globalCollections
L1L2L3_collections.update( L1L2L3_extra_collections )
L1L2L3_globalVariables = jet_globalVariables + L1L2L3_extra_variables

treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducer',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     globalVariables = L1L2L3_globalVariables,
     globalObjects   = [],
     collections     = L1L2L3_collections 
)
# Append it to the sequence
sequence.append( treeProducer )

test       = 'mc'
preprocess = True

if getHeppyOption("mc")  : test = "mc"
if getHeppyOption("data"): test = "data"

if test=='mc':
    preprocessorFile = "$CMSSW_BASE/python/CMGTools/ObjectStudies/preprocessor/recluster_mc.py"
else:                                     
    preprocessorFile = "$CMSSW_BASE/python/CMGTools/ObjectStudies/preprocessor/recluster_data.py"
    triggerFlagsAna.unrollbits          = True
    triggerFlagsAna.saveIsUnprescaled   = True
    triggerFlagsAna.checkL1prescale     = True

if getHeppyOption("loadSamples"):
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *
    from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
    from CMGTools.RootTools.samples.samples_13TeV_signals import *
    for sample in dataSamples:
        sample.json="$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
    if test.lower() == 'mc': 
        selectedComponents = [ TT_pow ]
    else: 
        selectedComponents = [ JetHT_Run2016C_03Feb2017 ]
    for comp in selectedComponents:
            comp.files = comp.files[:1]
            comp.splitFactor = 1

from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
event_class = Events

if getHeppyOption("fetch"):
    event_class = EOSEventsWithDownload

if preprocess:
    from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
    preprocessor = CmsswPreprocessor(preprocessorFile)
    jetAna.jetCol   = ("selectedPatJetsAK4PFCHS","","USER")
    jetAna.genJetCol= ("ak4GenJetsNoNu","","USER")
else:
    preprocessor = None

config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
                     preprocessor=preprocessor, # comment if pre-processor non needed
                     events_class = event_class)

