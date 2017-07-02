import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

process = cms.Process("USER")

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag (process.GlobalTag, 'auto:run2_mc')
#process.GlobalTag = GlobalTag (process.GlobalTag, '80X_mcRun2_asymptotic_2016_TrancheIV_v6')

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

# Loading jet config pickle. This is written in the heppy cfg
import pickle, os
cfg_pkl = os.path.expandvars("$CMSSW_BASE/src/CMGTools/ObjectStudies/data/cmsswPreprocessorOptions.pkl")
try:
    options = pickle.load(file(cfg_pkl))
except IOError:
    print "Error. proprocessor config pkl not found:", cfg_pkl

print "Loaded recluster options: %r from file %s " % ( options, cfg_pkl )
jetCollections = options['jetCollections']

## Output file
stm = ['drop *']
for jetCollection in jetCollections:
    # Keep statetements for pat jet collection names
    jetCollection['genJetName'] = 'ak%iGenJetsNoNu'%(   10*jetCollection['coneSize'])
    jetCollection['PATSuffix']  = 'AK%i%s'%( 10*jetCollection['coneSize'], jetCollection['flavor'].upper()) 
    jetCollection['patJetCollectionName']  = 'selectedPatJets%s' % jetCollection['PATSuffix']

    stm.append( 'keep patJets_%s_*_*'%( jetCollection['patJetCollectionName'] ) )
    stm.append( 'keep recoGenJets_%s_*_*'%( jetCollection['genJetName'] ) )

print "Keep statements:", stm
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('test.root'),
    outputCommands = cms.untracked.vstring( stm )
)
process.endpath= cms.EndPath(process.out)

if options['isMC']:
    filename = 'root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/MINIAODSIM/NoPU_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/02758D78-52C0-E611-B027-0025905B8576.root'
else:
    filename = 'root://cms-xrd-global.cern.ch//store/data/Run2016D/ZeroBias/MINIAOD/03Feb2017-v1/100000/0057FDCB-28EC-E611-BB28-02163E019BAA.root'

## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        filename
    )
)


### Filter out neutrinos from packed GenParticles
if options['isMC']:
    process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedGenParticles"), cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16"))
    ## Define GenJets
    from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets

    for jetCollection in jetCollections:
        setattr( process, "ak%iGenJetsNoNu"%(10*jetCollection['coneSize']), ak4GenJets.clone(src = 'packedGenParticlesForJetsNoNu', rParam=jetCollection['coneSize']) )
        print "Added ak%iGenJetsNoNu"%(10*jetCollection['coneSize']), "to process"

## Select charged hadron subtracted packed PF candidates
process.pfCHS = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV"))
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets

## Define PFJetsCHS
for jetCollection in jetCollections:
    chs_postfix = 'CHS' if jetCollection['flavor'].upper().endswith( 'CHS') else ''
    source      = 'pfCHS' if jetCollection['flavor'].upper().endswith( 'CHS') else cms.InputTag("packedPFCandidates") 

    jetCollection['recoJetCollectionName'] = "ak%iPFJets"%(10*jetCollection['coneSize'])
    jetCollection['labelName']             = "AK%iPF"%(10*jetCollection['coneSize'])
    if jetCollection['flavor'].upper().endswith( 'CHS'): 
        jetCollection['recoJetCollectionName']+='CHS'
        jetCollection['labelName']            +='CHS'

    setattr( process, 
            jetCollection['recoJetCollectionName'],  
            ak4PFJets.clone(src = source, doAreaFastjet = True, rParam = jetCollection['coneSize'] ) 
        )

    print "Added", jetCollection['recoJetCollectionName'], "to process"

#################################################
## Remake PAT jets
#################################################

## b-tag discriminators
bTagDiscriminators = [
    'pfCombinedInclusiveSecondaryVertexV2BJetTags'
]

from PhysicsTools.PatAlgos.tools.jetTools import *
## Add PAT jet collection based on the above-defined ak4PFJetsCHS
process.p = cms.Path()

for jetCollection in jetCollections:
    if jetCollection['coneSize'] in [0.4, 0.8]:
        jetcorr='AK%iPFchs'%(10*jetCollection['coneSize'])
    else:
        jetcorr='AK4PFchs'
        print "Warning! No JEC for cone size %2.1f flavor %s, using CHS %s" % ( jetCollection['coneSize'], jetCollection['flavor'], jetcorr )
    if options['isMC']:
        jec = ['L1FastJet', 'L2Relative', 'L3Absolute']
    else:
        jec = ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']    
    addJetCollection(
        process,
        labelName = jetCollection['labelName'],
        jetSource = cms.InputTag( jetCollection['recoJetCollectionName'] ),
        pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
        pfCandidates = cms.InputTag('packedPFCandidates'),
        svSource = cms.InputTag('slimmedSecondaryVertices'),
        btagDiscriminators = bTagDiscriminators,
        jetCorrections = (jetcorr, jec, 'None'),
        genJetCollection = cms.InputTag( jetCollection['genJetName'] ),
        genParticles = cms.InputTag('prunedGenParticles'),
        algo = 'AK',
        rParam = jetCollection['coneSize']
    )
    getattr(process, jetCollection['patJetCollectionName']).cut = cms.string('pt > 3')

    process.p += getattr( process, jetCollection['patJetCollectionName'])
    print "Added", jetCollection['patJetCollectionName'], "to process"

from PhysicsTools.PatAlgos.tools.pfTools import *
# remove MC matching
if not options['isMC']: 
    removeMCMatching(process, ['Jets'])

## Adapt primary vertex collection
adaptPVs(process, pvCollection=cms.InputTag('offlineSlimmedPrimaryVertices'))

process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool(True), # while the timing of this is not reliable in unscheduled mode, it still helps understanding what was actually run
        allowUnscheduled = cms.untracked.bool(True)
)


