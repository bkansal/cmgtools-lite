import ROOT
import operator 
import itertools
import copy

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters
from PhysicsTools.HeppyCore.utils.deltar import *
import PhysicsTools.HeppyCore.framework.config as cfg

from math import hypot

class chsDoctor( Analyzer ):

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(chsDoctor,self).__init__(cfg_ana,cfg_comp,looperName)
        self.chsJets = self.cfg_ana.chsJets
        self.pfJets  = self.cfg_ana.pfJets
        self.postFix = self.cfg_ana.postFix

    def declareHandles(self):
        super(chsDoctor, self).declareHandles()
        #self.handles['packedCandidates'] = AutoHandle( self.cfg_ana.packedCandidates, 'std::vector<pat::PackedCandidate>')

    def beginLoop(self, setup):
        super(chsDoctor,self).beginLoop( setup )

    def process(self, event):
        self.readCollections( event.input )

        leading_jet_candidates = []
        # Default result
        setattr( event, "leading_jet_candidates"+self.postFix, leading_jet_candidates)

        chsJets = getattr( event, self.chsJets )
        pfJets  = getattr( event, self.pfJets )
        if len(chsJets)==0: return True
        if len(pfJets) ==0: return True

        # need to make AK4 PF and PFchs jets
        chsJet = chsJets[0]
        pfJet  = pfJets[0]

        # require same gen jet match (can't match genjet for reclustered jets)
        if (not chsJet.genJet()) or (not pfJet.genJet()): return 
        if  chsJet.genJet().pt() != pfJet.genJet().pt(): return

        chsCands = [chsJet.daughter(i) for i in range(chsJet.numberOfDaughters())]
        pfCands =  [pfJet.daughter(i)  for i in range(pfJet.numberOfDaughters())]
        cands = chsCands+pfCands

        for cand in cands:
            cand.inCHSJet = ( cand in chsCands )
            cand.inPFJet  = ( cand in pfCands )
            if cand not in leading_jet_candidates:
                leading_jet_candidates.append( cand )

        leading_jet_candidates.sort(key=lambda p:-p.pt())

        setattr( event, "leading_jet_candidates"+self.postFix, leading_jet_candidates)

        return True

setattr(chsDoctor,"defaultConfig", cfg.Analyzer(
        class_object = chsDoctor,
        chsJets = 'cleanJetsAll',
        pfJets  = 'cleanJetsAllAK4PF',
        postFix = '',
        )
)
