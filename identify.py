import numpy as np
import os


def summary2ID(folder, modesID = None, ws_nan = None):
    
    summary = os.path.join(folder, 'Campbell_Summary.txt')
    if modesID is None:
        modesID = os.path.join(folder, 'Campbell_ModesID_Modif.csv')
    if ws_nan is None:
        ws_nan = np.arange(3,26)

    op = []
    ws = []
    rpm = []
    ID = []
    freq = []
    damp = []
    modes_ID_dict = {}
    modes_freq_dict = {}
    modes_damp_dict = {}
    counter = 0

    f = open(summary)
    tmp = f.readline()
    while 1:
        stop = False
        tmp = f.readline().split()
        # Stop while at the end of file    
        if tmp == []:
            break

        if len(tmp)>2:
            if tmp[2] == 'OP':
                id_start = 3
                op.append(int(tmp[id_start]))
                ws.append(float(tmp[id_start + 3]))
                rpm.append(float(tmp[id_start + 6]))
                f.readline()
                f.readline()
                f.readline()
                while 2:
                    tmp = f.readline()
                    tmp_split = tmp.split()
                    ADflag = True
                    # if len(tmp_split) >= 6:
                    #     if tmp_split[6].find('AD') >=0:
                    #         ADflag = False
                    
                    if tmp_split[0] != '#' and ADflag: 
                        ID.append(int(tmp_split[0]))
                        freq.append(float(tmp_split[2]))
                        damp.append(float(tmp_split[4]))
                    elif tmp.find('# --- Skipped (Frequency outside of `freqRange`') == 0:
                        while 3:
                            tmp = f.readline()
                            if tmp == '# -----------------------------------------------------------------------\n' or tmp == '':
                                stop = True
                                break
                    if stop == True:
                        break
        
        data = np.array([ID, freq, damp]).T
        data_sort = data[data[:, 1].argsort()]

        if np.isnan(ws[-1]):
            ws[-1] = ws_nan[counter]
            counter += 1

        modes_ID_dict[ws[-1]] = data_sort[:,0]
        modes_freq_dict[ws[-1]] = data_sort[:,1]
        modes_damp_dict[ws[-1]] = data_sort[:,2]
        ID = []
        freq = []
        damp = []

    f.close()

    n_ws = len(modes_ID_dict)
    n_modes = 23
    modes_ID = np.zeros((n_modes, n_ws), dtype=int)
    loose1flap = False
    for i in range(n_ws):
        tmp = np.array([modes_ID_dict[ws[i]][0:6], modes_freq_dict[ws[i]][0:6], modes_damp_dict[ws[i]][0:6]]).T
        # sort by damping
        tmp_sort = tmp[tmp[:, 2].argsort()]
        # select first edge and sort by freq
        edge1 = tmp_sort[:3,:]
        edge1_sort = edge1[edge1[:, 1].argsort()]
        modes_ID[3:6,i] = edge1_sort[:,0]
            
        if ws[i]==12:
            print('a')
        # select second flap
        tmp2f = np.array([modes_ID_dict[ws[i]][6:9], modes_freq_dict[ws[i]][6:9], modes_damp_dict[ws[i]][6:9]]).T
        # stack first and second flap, which usually at some point overlap
        tmp12f = np.vstack((tmp_sort[3:,:], tmp2f))
        # sort damp by damping
        tmp_sort12f = tmp12f[tmp12f[:, 2].argsort()]

        # assign to first and second flap
        if any(tmp_sort12f[:,2]>0.8):
            loose1flap = True
        
        extra_flap2 = []
        if loose1flap:
            flap1 = tmp_sort12f[3:,:]
            flap1_sort = flap1[flap1[:, 1].argsort()]
            flap1_sort2 = flap1_sort[flap1_sort[:,2]>0.5]
            modes_ID[:len(flap1_sort2),i] = flap1_sort2[:,0]
            extra_flap2 = flap1_sort[flap1_sort[:,2]<0.5]

            if len(extra_flap2) == 0:
                flap2 = tmp_sort12f[:3,:]
                flap2_sort = flap2[flap2[:, 1].argsort()]
                modes_ID[6:9,i] = flap2_sort[:,0]
            else:
                flap2 = np.vstack((extra_flap2, tmp_sort12f[len(extra_flap2):3,:],))
                flap2_sort = flap2[flap2[:, 1].argsort()]
                modes_ID[6:9,i] = flap2_sort[:,0]

            # if any(flap1_sort[:,2]<0.5):

        else:

            flap1 = tmp_sort12f[3:,:]
            flap1_sort = flap1[flap1[:, 1].argsort()]
            modes_ID[:3,i] = flap1_sort[:,0]

            flap2 = tmp_sort12f[:3,:]
            flap2_sort = flap2[flap2[:, 1].argsort()]
            modes_ID[6:9,i] = flap2_sort[:,0]

        # assign to second edge
        ixs = 9 - len(extra_flap2)
        ixe = 11 - len(extra_flap2)
        tmp2e = np.array([modes_ID_dict[ws[i]][ixs:ixe], modes_freq_dict[ws[i]][ixs:ixe], modes_damp_dict[ws[i]][ixs:ixe]]).T
        modes_ID[9:11,i] = tmp2e[:,0]

        # assign to third flap
        ixs = 11 - len(extra_flap2)
        ixe = 14 - len(extra_flap2)
        tmp3f = np.array([modes_ID_dict[ws[i]][ixs:ixe], modes_freq_dict[ws[i]][ixs:ixe], modes_damp_dict[ws[i]][ixs:ixe]]).T
        modes_ID[11:14,i] = tmp3f[:,0]
        
        # assign to third edge
        ixs = 14 - len(extra_flap2)
        ixe = 17 - len(extra_flap2)
        tmp3e = np.array([modes_ID_dict[ws[i]][ixs:ixe], modes_freq_dict[ws[i]][ixs:ixe], modes_damp_dict[ws[i]][ixs:ixe]]).T
        modes_ID[14:17,i] = tmp3e[:,0]
        
        # assign to fourth flap
        ixs = 17 - len(extra_flap2)
        ixe = 20 - len(extra_flap2)
        tmp4f = np.array([modes_ID_dict[ws[i]][ixs:ixe], modes_freq_dict[ws[i]][ixs:ixe], modes_damp_dict[ws[i]][ixs:ixe]]).T
        modes_ID[17:20,i] = tmp4f[:,0]
        
        # assign to first torsion
        ixs = 20 - len(extra_flap2)
        ixe = 23 - len(extra_flap2)
        tmp1t = np.array([modes_ID_dict[ws[i]][ixs:ixe], modes_freq_dict[ws[i]][ixs:ixe], modes_damp_dict[ws[i]][ixs:ixe]]).T
        try:
            modes_ID[20:23,i] = tmp1t[:,0]
        except:
            print('Fail',i)


        # populate_id = 0
        # while populate_id < n_modes:

        



    f = open(modesID, 'w')
    f.write('{:<17},{:<22}\n'.format('Mode Number Table', ','.join(np.array(np.arange(n_ws) + 1, dtype=str))))
    f.write('{:<16},{:<22}\n'.format('Wind Speed (mps)', ','.join(np.array(ws, dtype=str))))
    f.write('{:<16},{:<22}\n'.format('1st Blade Flap (Regressive)', ','.join(np.array(modes_ID[0,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('1st Blade Flap (Collective)', ','.join(np.array(modes_ID[1,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('1st Blade Flap (Progressive)', ','.join(np.array(modes_ID[2,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('1st Blade Edge (Regressive)', ','.join(np.array(modes_ID[3,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('1st Blade Edge (Progressive)', ','.join(np.array(modes_ID[4,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('1st Blade Edge (Collective)', ','.join(np.array(modes_ID[5,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('2nd Blade Flap (Regressive)', ','.join(np.array(modes_ID[6,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('2nd Blade Flap (Collective)', ','.join(np.array(modes_ID[7,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('2nd Blade Flap (Progressive)', ','.join(np.array(modes_ID[8,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('2nd Blade Edge (Regressive)', ','.join(np.array(modes_ID[9,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('2nd Blade Edge (Progressive)', ','.join(np.array(modes_ID[10,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('3rd Blade Flap (Regressive)', ','.join(np.array(modes_ID[11,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('3rd Blade Flap (Collective)', ','.join(np.array(modes_ID[12,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('3rd Blade Flap (Progressive)', ','.join(np.array(modes_ID[13,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('3rd Blade Edge (Regressive)', ','.join(np.array(modes_ID[14,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('3rd Blade Edge (Collective)', ','.join(np.array(modes_ID[15,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('3rd Blade Edge (Progressive)', ','.join(np.array(modes_ID[16,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('4th Blade Flap (Regressive)', ','.join(np.array(modes_ID[17,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('4th Blade Flap (Collective)', ','.join(np.array(modes_ID[18,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('4th Blade Flap (Progressive)', ','.join(np.array(modes_ID[19,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('1st Blade Torsion (Regressive)', ','.join(np.array(modes_ID[20,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('1st Blade Torsion (Collective)', ','.join(np.array(modes_ID[21,:], dtype=str))))
    f.write('{:<16},{:<22}\n'.format('1st Blade Torsion (Progressive)', ','.join(np.array(modes_ID[22,:], dtype=str))))
    f.close()
