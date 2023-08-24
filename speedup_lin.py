from pyFAST.input_output.fast_linearization_file import FASTLinearizationFile
from welib.tools.tictoc import Timer
import pyFAST.linearization.campbell as lin

# with Timer('>>> Reading'):
#     f =FASTLinearizationFile('ua-dev1/iea22_stab_00.1.lin', starSub=0)
#     #f =FASTLinearizationFile('DEBUG.lin', starSub=0)
#     print('x',f['x'][:3])
# #     print('u',f['u'][:3])
#     print('A',f['A'][:3,:4])
#     try:
#         print('B',f['B'][:3,:4])
#     except:
#         pass


folder_name ='ua-dev0'
modeID_file = folder_name + '/Campbell_ModesID_Modif.csv'
fig, axes, figName =  lin.plotCampbellDataFile(modeID_file, 'ws', ylim=None, to_csv=True)
