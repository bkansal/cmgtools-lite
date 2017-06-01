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

def sumXY(pxys):
    px, py = sum(x[0] for x in pxys), sum(x[1] for x in pxys)
    return ROOT.reco.Particle.LorentzVector(-px, -py, 0, hypot(px,py))

class chsMETAnalyzer( Analyzer ):

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(chsMETAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.maxDz = self.cfg_ana.maxDz

    def declareHandles(self):
        super(chsMETAnalyzer, self).declareHandles()
        self.handles['packedCandidates'] = AutoHandle( self.cfg_ana.packedCandidates, 'std::vector<pat::PackedCandidate>')

    def beginLoop(self, setup):
        super(chsMETAnalyzer,self).beginLoop( setup )

    def process(self, event):
        self.readCollections( event.input )

        #chs_dz     = []
        chs_fromPV = []
        chsSumPt   = 0.
        for pfcand in self.handles['packedCandidates'].product():

            # CHS definition
            if pfcand.fromPV()>0: 
                chs_fromPV.append( ( pfcand.px(), pfcand.py() ) )
                chsSumPt += pfcand.pt()

            ## W mass definition (dz)
            #if (pfcand.charge()!=0 and abs(pfcand.pdgId())==211):
            #    if abs(pfcand.dz())>self.maxDz:
            #        continue # skip CH with dz larger than maxDz 

            #chs_dz.append( (pfcand.px(), pfcand.py()) )

        setattr(event, "chsMET",     sumXY(chs_fromPV))
        setattr(event, "chsSumPt",   chsSumPt)
        #setattr(event, "chsMETDz", sumXY(chs_dz))

        return True

setattr(chsMETAnalyzer,"defaultConfig", cfg.Analyzer(
        class_object = chsMETAnalyzer,
        maxDz=0.1,
        packedCandidates = 'packedPFCandidates',
        )
)
