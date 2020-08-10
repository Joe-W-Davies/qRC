#!/bin/bash

echo SWITCH OFF DISPLAY
export DISPLAY=

#source /t3home/threiten/jupyter_env.sh
#could put all the below into a .sh
cd /vols/build/cms/jwd18/serviceTasks/CQR/CMSSW_10_2_0/src/
eval `scramv1 runtime -sh`
export PYTHONPATH=:/vols/build/cms/jwd18/serviceTasks/CQR/CMSSW_10_2_0/src/qRC/python
echo $PYTHONPATH

export OMP_NUM_THREADS=2
config=$1
variable=$2
quantile=$3
N_evts=$4
EBEE=$5

if [ ! -z "$6" ]
then
    echo Doing split training! #assume for systematic uncertainty estimation
    spl=$6
    #python /t3home/threiten/python/qRC/training/train_qRC_data.py -c ${config} -v ${variable} -q ${quantile} -N ${N_evts} -E ${EBEE} -s ${spl}
    #python /vols/build/cms/jwd18/serviceTasks/CQR/CMSSW_10_2_0/src/qRC/training/train_qRC_data.py -c ${config} -v ${variable} -q ${quantile} -N ${N_evts} -E ${EBEE} -s ${spl}
    python ./qRC/training/train_qRC_data.py -c ${config} -v ${variable} -q ${quantile} -N ${N_evts} -E ${EBEE} -s ${spl}
else
    #python /t3home/threiten/python/qRC/training/train_qRC_data.py -c ${config} -v ${variable} -q ${quantile} -N ${N_evts} -E ${EBEE}
    #python /vols/build/cms/jwd18/serviceTasks/CQR/CMSSW_10_2_0/src/qRC/training/train_qRC_data.py -c ${config} -v ${variable} -q ${quantile} -N ${N_evts} -E ${EBEE}
    python ./qRC/training/train_qRC_data.py -c ${config} -v ${variable} -q ${quantile} -N ${N_evts} -E ${EBEE}
fi
