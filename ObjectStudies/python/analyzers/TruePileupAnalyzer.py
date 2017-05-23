import ROOT
import filecmp
import os
import shutil
import json

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters
from PhysicsTools.HeppyCore.utils.deltar import *
import PhysicsTools.HeppyCore.framework.config as cfg


class TruePileupAnalyzer( Analyzer ):

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(TruePileupAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.minBiasXSEC = self.cfg_ana.minBiasXSEC

        self.remote_file = os.path.expandvars( self.cfg_ana.pileup_remote_file )
        #self.local_file  = os.path.expandvars( "$CMSSW_BASE/src/CMGTools/ObjectStudies/data/pileup_latest.txt" )

        #if not os.path.exists( self.local_file ) or ( os.path.exists( self.local_file )  and filecmp.cmp(self.local_file, self.remote_file) ):
        #    print "Updating pileup_latest.txt: cp %s %s" % (self.remote_file, self.local_file )
        #    shutil.copyfile( self.remote_file, self.local_file )    

        j_pu_data = json.load( file( self.remote_file ) )
        # turn into nested dictionary. The last number in pileup_latest.txt is the avg lumi I'd hope.
        self.pu_data = {run:{data[0]:data[-1] for data in lumis} for run, lumis in j_pu_data.iteritems()}

    def get_inst_lumi( self, run, lumi ):
        try:
            return self.pu_data[str(run)][lumi]
        except KeyError:
            return -1

    def declareHandles(self):
        super(TruePileupAnalyzer, self).declareHandles()
        self.mchandles['pusi'] =  AutoHandle(
            'slimmedAddPileupInfo',
            'std::vector<PileupSummaryInfo>',
            fallbackLabel="addPileupInfo"
            ) 

    def beginLoop(self, setup):
        super(TruePileupAnalyzer,self).beginLoop( setup )

    def process(self, event):

        if self.cfg_comp.isMC:

            if not hasattr( event, "pileUpInfo"):
                event.pileUpInfo = map( PileUpSummaryInfo,
                                    self.mchandles['pusi'].product() )
 
            for puInfo in event.pileUpInfo:
                if puInfo.getBunchCrossing()==0:
                    setattr(event, "truePileup_n", puInfo.nPU() )
                    setattr(event, "truePileup_mu", puInfo.nTrueInteractions() )
                    return True

            event.truePileup_mu = -1 # BX=0 not found

        setattr(event, "truePileup_mu",   self.minBiasXSEC*self.get_inst_lumi( event.input.eventAuxiliary().id().run(), event.input.eventAuxiliary().id().luminosityBlock()) )

        return True

setattr(TruePileupAnalyzer,"defaultConfig", cfg.Analyzer(
        class_object = TruePileupAnalyzer,
        minBiasXSEC  = 69200,
        pileup_remote_file = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt"
        )
)
