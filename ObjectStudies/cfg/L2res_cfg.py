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
coneSizes = [ 0.4,  0.8 ]
jetCollections = [ {'coneSize':coneSize, 'flavor':'PFchs'} for coneSize in coneSizes ]

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
        selectedComponents = [ JetHT_Run2016H_07Aug2017 ]
        selectedComponents[0].files = [
            'file:/data/rschoefbeck/local/JetHT_Run2017H_07Aug2017.root'
#            'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/JetHT/crab_pickEvents/170720_164451/0000/pickevents_1.root',
#            'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/JetHT/crab_pickEvents/170720_164451/0000/pickevents_2.root',
#            'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/JetHT/crab_pickEvents/170720_164451/0000/pickevents_3.root',
#            'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/JetHT/crab_pickEvents/170720_164451/0000/pickevents_4.root',
#            'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/JetHT/crab_pickEvents/170720_164451/0000/pickevents_5.root',
#            'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/JetHT/crab_pickEvents/170720_164451/0000/pickevents_6.root',
#            'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/JetHT/crab_pickEvents/170720_164451/0000/pickevents_7.root',
#            'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/JetHT/crab_pickEvents/170720_164451/0000/pickevents_8.root',
#            'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/JetHT/crab_pickEvents/170720_164451/0000/pickevents_9.root',
#            'root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/JetHT/crab_pickEvents/170720_164451/0000/pickevents_10.root',
            ]
#    for comp in selectedComponents:
#            comp.files = comp.files[:1]
#            comp.splitFactor = 1

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

