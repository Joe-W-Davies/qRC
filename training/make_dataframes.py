import argparse
import yaml
import qRC.python.quantileRegression_chain as QReg_C

#example command to run 2017 reReco for barrel (need to run endcap too):
#python qRC/training/make_dataframes.py -D /vols/cms/jwd18/qRCSamples/trees/reReco/2017 -O /vols/cms/jwd18/qRCSamples/dataframes/reReco/2017 -y 2017 -E EE -s 0.7
#scripts requires data and MC to be in same dir

def main(options):

    qRC = QReg_C.quantileRegression_chain(options.year, options.EBEE, options.outDir, ['probeR9'])
    
    #print 'Reading MC for SS corrections ({})'.format(qRC.EBEE)
    #df_ret = qRC.loadROOT('{}/outputMC.root'.format(options.sourceDir), 'tagAndProbeDumper/trees/DYJetsToLL_amcatnloFXFX_13TeV_All', 'df_mc_{}'.format(qRC.EBEE), 'tagPt>40 and tagR9>0.8 and mass>80 and mass<100 and probeChIso03<6 and tagScEta>-2.1 and tagScEta<2.1 and probePassEleVeto==0', options.split)
    #del df_ret
    print 'Reading Data for SS corrections ({})'.format(qRC.EBEE)
    df_ret = qRC.loadROOT('{}/outputData.root'.format(options.sourceDir), 'tagAndProbeDumper/trees/Data_13TeV_All', 'df_data_{}'.format(qRC.EBEE), 'tagPt>40 and tagR9>0.8 and mass>80 and mass<100 and probeChIso03<6 and tagScEta>-2.1 and tagScEta<2.1 and probePassEleVeto==0', options.split)
    del df_ret

    if options.EBEE == 'EB':
        print 'Reading MC for Iso corrections (EB)'
        qRC.loadROOT('{}/outputMC.root'.format(options.sourceDir), 'tagAndProbeDumper/trees/DYJetsToLL_amcatnloFXFX_13TeV_All', 'df_mc_{}_Iso'.format(qRC.EBEE), 'tagPt>40 and tagR9>0.8 and mass>80 and mass<100 and probeSigmaIeIe<0.0105 and tagScEta>-2.1 and tagScEta<2.1 and probePassEleVeto==0', options.split)
        print 'Reading Data for Iso corrections (EB)'
        qRC.loadROOT('{}/outputData.root'.format(options.sourceDir), 'tagAndProbeDumper/trees/Data_13TeV_All', 'df_data_{}_Iso'.format(qRC.EBEE), 'tagPt>40 and tagR9>0.8 and mass>80 and mass<100 and probeSigmaIeIe<0.0105 and tagScEta>-2.1 and tagScEta<2.1 and probePassEleVeto==0', options.split)
    elif options.EBEE == 'EE':
        print 'Reading MC for Iso corrections (EE)'
        qRC.loadROOT('{}/outputMC.root'.format(options.sourceDir), 'tagAndProbeDumper/trees/DYJetsToLL_amcatnloFXFX_13TeV_All', 'df_mc_{}_Iso'.format(qRC.EBEE), 'tagPt>40 and tagR9>0.8 and mass>80 and mass<100 and probeSigmaIeIe<0.028 and tagScEta>-2.1 and tagScEta<2.1 and probePassEleVeto==0', options.split)
        print 'Reading Data for Iso corrections (EE)'
        qRC.loadROOT('{}/outputData.root'.format(options.sourceDir), 'tagAndProbeDumper/trees/Data_13TeV_All', 'df_data_{}_Iso'.format(qRC.EBEE), 'tagPt>40 and tagR9>0.8 and mass>80 and mass<100 and probeSigmaIeIe<0.028 and tagScEta>-2.1 and tagScEta<2.1 and probePassEleVeto==0', options.split)
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    requiredArgs = parser.add_argument_group('Required Arguements')
    requiredArgs.add_argument('-D','--sourceDir', action='store', required=True)
    requiredArgs.add_argument('-O','--outDir', action='store', required=True)
    requiredArgs.add_argument('-y','--year', action='store', required=True)
    requiredArgs.add_argument('-E','--EBEE', action='store', required=True)
    requiredArgs.add_argument('-s','--split', action='store', type=float, required=True,)
    # optionalArgs = parser.add_argument_group('Optional Arguements')
    # optionalArgs.add_argument('-l', '--label', action='store', default='')
    options=parser.parse_args()
    main(options)
