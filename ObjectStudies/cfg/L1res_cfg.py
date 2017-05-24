##########################################################
##       CONFIGURATION FOR L1res ntuples                ## 
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

#Load all analyzers
from CMGTools.ObjectStudies.analyzers.jetCore_modules_cff import *

#!# #-------- SAMPLES AND SEQUENCE -----------

selectedComponents = [
        ]

sequence = cfg.Sequence( jet_coreSequence )

# append offset analyzer for L1res to core sequence
from CMGTools.ObjectStudies.analyzers.OffsetAnalyzer import OffsetAnalyzer
offsetAna = OffsetAnalyzer.defaultConfig
sequence.append( offsetAna )

# make tree Producer
from CMGTools.ObjectStudies.analyzers.jet_treeProducer import *

# add the offset collections to the default (global) collections
L1res_collections = {} 
L1res_collections.update( L1res_extra_collections )
L1res_globalVariables = jet_globalVariables + L1res_extra_variables

treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducer',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     globalVariables = L1res_globalVariables,
     globalObjects   = [],
     collections     = L1res_collections 
)
# Append it to the sequence
sequence.append( treeProducer )

test = 'mc'

if getHeppyOption("mc")  : test = "mc"
if getHeppyOption("data"): test = "data"

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

config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
#                     preprocessor=preprocessor, # comment if pre-processor non needed
                     events_class = event_class)

