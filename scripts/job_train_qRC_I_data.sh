#!/bin/bash

echo SWITCH OFF DISPLAY
export DISPLAY=

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
    echo Doing split training!
    spl=$6
    python ./qRC/training/train_qRC_I_data.py -c ${config} -v ${variable} -q ${quantile} -N ${N_evts} -E ${EBEE} -s ${spl}
else
    python ./qRC/training/train_qRC_I_data.py -c ${config} -v ${variable} -q ${quantile} -N ${N_evts} -E ${EBEE}
fi
