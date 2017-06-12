#!/bin/sh
#python launch.py --remoteDir="L1res" --cfg=../L1res_cfg.py --unitsPerJob=2 --production_label="V4" -o data ZeroBias_Run2016B_03Feb2017_v2
#python launch.py --remoteDir="L1res" --cfg=../L1res_cfg.py --unitsPerJob=2 --production_label="V4" -o data ZeroBias_Run2016C_03Feb2017
#python launch.py --remoteDir="L1res" --cfg=../L1res_cfg.py --unitsPerJob=2 --production_label="V4" -o data ZeroBias_Run2016D_03Feb2017
#python launch.py --remoteDir="L1res" --cfg=../L1res_cfg.py --unitsPerJob=2 --production_label="V4" -o data ZeroBias_Run2016E_03Feb2017
#python launch.py --remoteDir="L1res" --cfg=../L1res_cfg.py --unitsPerJob=2 --production_label="V4" -o data ZeroBias_Run2016F_03Feb2017
#python launch.py --remoteDir="L1res" --cfg=../L1res_cfg.py --unitsPerJob=2 --production_label="V4" -o data ZeroBias_Run2016G_03Feb2017
#python launch.py --remoteDir="L1res" --cfg=../L1res_cfg.py --unitsPerJob=2 --production_label="V4" -o data ZeroBias_Run2016H_03Feb2017_v2
#python launch.py --remoteDir="L1res" --cfg=../L1res_cfg.py --unitsPerJob=2 --production_label="V4" -o data ZeroBias_Run2016H_03Feb2017_v3

python launch.py --remoteDir="L1res" --cfg=../L1res_cfg.py --unitsPerJob=2 --production_label="V4" --inputDBS=phys03 -o mc SingleNeutrino 
