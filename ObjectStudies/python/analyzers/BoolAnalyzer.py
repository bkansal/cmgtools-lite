import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
import PhysicsTools.HeppyCore.framework.config as cfg


class BoolAnalyzer( Analyzer ):

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(BoolAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.bools = cfg_ana.bools

    def declareHandles(self):
        super(BoolAnalyzer, self).declareHandles()
        for b in self.bools:
            self.handles[b] =  AutoHandle( b, 'bool' ) 

    def beginLoop(self, setup):
        super(BoolAnalyzer,self).beginLoop( setup )

    def process(self, event):
        self.readCollections( event.input )

        for b in self.bools:
            setattr( event, b, self.handles[b].product()[0] )

 
        return True

setattr(BoolAnalyzer,"defaultConfig", cfg.Analyzer(
        class_object = BoolAnalyzer,
        bools = []
        )
)
