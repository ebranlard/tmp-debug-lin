import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import pyFAST.linearization.campbell as lin

from identify import summary2ID

# Script Parameters
BladeLen     = 137.8  # Blade length, used to tune relative modal energy [m] NOTE: not needed if fst files exists
TowerLen     = 164.386  # Tower length, used to tune relative modal energy [m] idem
#     folder_name = 'ua-dev2/'

removeStatesPattern=None
for folder_name in ['ua-dev2', 'ua-dev1', 'ua-dev0', 'ua']:

# removeStatesPattern=r'^AD'
# for folder_name in ['ua-dev2-noAD/', 'ua-dev1-noAD/', 'ua-dev0-noAD/']:

# removeStatesPattern=r'^AD x'
# for folder_name in ['ua-dev2-noUA/', 'ua-dev1-noUA/', 'ua-dev0-noUA/']:

# removeStatesPattern=r'^AD vind'
# for folder_name in ['ua-dev2-noDB/', 'ua-dev1-noDB/', 'ua-dev0-noDB/']:


# removeStatesPattern='AD x1 blade 1, node 1,|AD x2 blade 1, node 1,|AD x3 blade 1, node 1,|AD x4 blade 1, node 1,|AD x1 blade 1, node 2,|AD x2 blade 1, node 2,|AD x3 blade 1, node 2,|AD x4 blade 1, node 2,|AD x1 blade 1, node 3,|AD x2 blade 1, node 3,|AD x3 blade 1, node 3,|AD x4 blade 1, node 3,|AD x1 blade 2, node 1,|AD x2 blade 2, node 1,|AD x3 blade 2, node 1,|AD x4 blade 2, node 1,|AD x1 blade 2, node 2,|AD x2 blade 2, node 2,|AD x3 blade 2, node 2,|AD x4 blade 2, node 2,|AD x1 blade 2, node 3,|AD x2 blade 2, node 3,|AD x3 blade 2, node 3,|AD x4 blade 2, node 3,|AD x1 blade 3, node 1,|AD x2 blade 3, node 1,|AD x3 blade 3, node 1,|AD x4 blade 3, node 1,|AD x1 blade 3, node 2,|AD x2 blade 3, node 2,|AD x3 blade 3, node 2,|AD x4 blade 3, node 2,|AD x1 blade 3, node 3,|AD x2 blade 3, node 3,|AD x3 blade 3, node 3,|AD x4 blade 3, node 3,'

# removeStatesPattern=r'AD x[1-4]* blade [1-3]*, node 1,|AD x[1-4]* blade [1-3]*, node 2,|AD x[1-4]* blade [1-3]*, node 3,'
# for folder_name in ['ua-dev0-noUAStart/',  'ua-dev1-noUAStart/','ua-dev2/']:



# removeStatesPattern=None
# for folder_name in ['ua-dev11', 'ua-dev12', 'ua-dev13']:

    fstFiles = glob.glob(folder_name + '/*.fst') # list of fst files where linearization were run, lin file will be looked for
    fig_name = 'Campbell-'+folder_name.replace('/','')
    fstFiles.sort() # not necessary

    modeID_file = folder_name + '/Campbell_ModesID_Modif.csv'
    modeID_file2 = folder_name + '/Campbell_ModesID_Modif_Manu.csv'
    if os.path.exists(modeID_file2):
        print('>>>> USING MANU FILE')
        modeID_file = modeID_file2
    try:
        # Edit the mode ID file manually to better identify/distribute the modes
        fig, axes, figName =  lin.plotCampbellDataFile(modeID_file, 'ws', ylim=None, to_csv=True, WS_legacy = np.arange(3,26))
    except:
        # Find lin files, perform MBC, and try to identify modes. A csv file is written with the mode IDs.
        freqRange=[0.3,5]

        posDampRange=[0, 0.9]


        OP, Freq, Damp, UnMapped, ModeData, modeID_file = lin.postproCampbell(fstFiles, BladeLen, 
                                                                            TowerLen, nFreqOut=5000, 
                                                                            freqRange = freqRange, 
                                                                            posDampRange = posDampRange,
                                                                            removeStatesPattern = removeStatesPattern)
        fig, axes, figName =  lin.plotCampbellDataFile(modeID_file, 'ws', ylim=None, to_csv=True, WS_legacy = np.arange(3,26))



        summary2ID(folder_name)

    axes[0].set_ylim([0., 5.])
    axes[0].set_xlim([0, 26])
    axes[1].set_ylim([-0.8, 1.])
    axes[1].set_xlim([0, 26])
    plt.tight_layout()
    print('fig_name',fig_name)
    fig.savefig(fig_name + '.png')
    fig.suptitle(fig_name)
# 
if __name__=='__main__':
    plt.show()
