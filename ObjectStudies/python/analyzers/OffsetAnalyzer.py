import ROOT
import operator 
import itertools
import copy
import bisect

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters
from PhysicsTools.HeppyCore.utils.deltar import *
import PhysicsTools.HeppyCore.framework.config as cfg

from math import sqrt

def sumXY(pxys):
    px, py = sum(x[0] for x in pxys), sum(x[1] for x in pxys)
    return ROOT.reco.Particle.LorentzVector(-px, -py, 0, hypot(px,py))

offset_eta_thresholds =  [ -5.191, -4.889, -4.716, -4.538, -4.363, -4.191, -4.013, -3.839, -3.664, -3.489, -3.314, -3.139, -2.964, -2.853, -2.65,
   -2.5, -2.322, -2.172, -2.043, -1.93, -1.83, -1.74, -1.653, -1.566, -1.479, -1.392, -1.305, -1.218, -1.131, -1.044, -0.957,
   -0.879, -0.783, -0.696, -0.609, -0.522, -0.435, -0.348, -0.261, -0.174, -0.087, 0,
   0.087, 0.174, 0.261, 0.348, 0.435, 0.522, 0.609, 0.696, 0.783, 0.879, 0.957, 1.044, 1.131, 1.218, 1.305, 1.392, 1.479,
   1.566, 1.653, 1.74, 1.83, 1.93, 2.043, 2.172, 2.322, 2.5, 2.65, 2.853, 2.964, 3.139, 3.314, 3.489, 3.664, 3.839, 4.013,
   4.191, 4.363, 4.538, 4.716, 4.889, 5.191 ]

n_bins = len(offset_eta_thresholds) - 1

def find_eta_bin( eta ):
    if eta>offset_eta_thresholds[0] and eta<offset_eta_thresholds[-1]:
        return bisect.bisect_left(offset_eta_thresholds, eta) - 1

offset_flavors = [ 'e_lost', 'e_all', 'e_unm', 'e_ch', 'e_nh', 'e_ph', 'e_ele', 'e_mu', 'e_hhf', 'e_ehf', 'et_all', 'n', 'e2_all' ]
offset_flavors_stored = [ 'e_lost', 'e_all', 'e_unm', 'e_ch', 'e_nh', 'e_ph', 'e_ele', 'e_mu', 'e_hhf', 'e_ehf', 'et_all', 'e_rms' ]

name_dict = {211:'ch', 130:'nh', 22:'ph', 11:'ele', 13:'mu', 1:'hhf', 2:'ehf'}

class OffsetAnalyzer( Analyzer ):


    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(OffsetAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)

    def declareHandles(self):
        super(OffsetAnalyzer, self).declareHandles()
        self.handles['packedCandidates'] = AutoHandle( self.cfg_ana.packedCandidates, 'std::vector<pat::PackedCandidate>')
        self.handles['lostTracks']       = AutoHandle( self.cfg_ana.lostTracks,       'std::vector<pat::PackedCandidate>')

    def beginLoop(self, setup):
        super(OffsetAnalyzer,self).beginLoop( setup )

    def process(self, event):
        self.readCollections( event.input )

        # Store energy per flavor, energy (total), transverse energy and RMS
        offset_flavor  = [ {k:0 for k in offset_flavors} for i in xrange(n_bins) ]

        # Adding lost tracks
        for pfCand in self.handles['lostTracks'].product():
            et = pfCand.pt()
            e  = pfCand.p()

            eta_bin = find_eta_bin( pfCand.eta() )
            if eta_bin:
                offset_flavor[eta_bin]['e_lost']    += e 
                offset_flavor[eta_bin]['e_all']     += e 
                offset_flavor[eta_bin]['et_all']    += et
                offset_flavor[eta_bin]['n']         += 1
                offset_flavor[eta_bin]['e2_all']    += e*e

        for pfCand in self.handles['packedCandidates'].product():

            # CHS definition
            if  pfCand.fromPV()>0:
                k =  'e_%s'%name_dict[abs(pfCand.pdgId())]
            else:
                k = 'e_unm' 

            et = pfCand.et()
            e  = pfCand.p()

            eta_bin = find_eta_bin( pfCand.eta() )
            if eta_bin:
                offset_flavor[eta_bin][k]           += e 
                offset_flavor[eta_bin]['e_all']     += e 
                offset_flavor[eta_bin]['et_all']    += et
                offset_flavor[eta_bin]['n']         += 1
                offset_flavor[eta_bin]['e2_all']    += e*e

        # calculate RMS
        for i_bin in xrange(n_bins):
            offset_flavor[i_bin]['e_rms'] = sqrt( offset_flavor[i_bin]['e2_all']/offset_flavor[i_bin]['n'] ) if offset_flavor[i_bin]['n']>0 else 0

        event.offset = offset_flavor 
        return True

setattr(OffsetAnalyzer,"defaultConfig", cfg.Analyzer(
        class_object = OffsetAnalyzer,
        packedCandidates = 'packedPFCandidates',
        lostTracks = 'lostTracks',
        )
)
