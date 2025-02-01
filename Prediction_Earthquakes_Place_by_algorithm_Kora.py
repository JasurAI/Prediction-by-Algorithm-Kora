import pandas as pd
import numpy as np

num_plits = 3
df = pd.read_excel('Data_09.xlsx', index_col=0)
n_col = df.shape[1]-1  # number of columns of df
n_row = df.shape[0]  # number of rows of df

l=0
for i1 in range(1, n_col-1):
    for i2 in range(i1+1, n_col):
        for i3 in range (i2+1, n_col+1):
            l += 1
nc = l # number of combinatorics
plits2 = [[0] * num_plits for _ in range(nc)]; i = 0
for i1 in range(1, n_col-1):
    for i2 in range(i1+1, n_col):
        for i3 in range (i2+1, n_col+1):
            plits2[i][0]=i1; plits2[i][1]=i2; plits2[i][2]=i3;    i += 1

##################################  Machine Learning  ######################################

plits8 = [[0] * nc for _ in range(n_row)]
for j0 in df.index:
    for i0 in range(0,nc):
        j1 = plits2[i0][0]; j2 = plits2[i0][1]; j3 = plits2[i0][2]
        x1 = df[j1][j0]; x2 = df[j2][j0]; x3 = df[j3][j0]
        v8 = 4*x1+2*x2+1*x3
        # print(j0, i0, " || ", j1, j2, j3, " || ", x1, x2, x3, " || ", v8)
        plits8[j0-1][i0] = v8

t0 = 0; t1 = 0
for k in df.index:
    print(f"######################################### {k} - Block ###########################################")
    p_data = df.loc[k]
    data = df.drop(df.index[df.index.get_loc(k)])
    K1 = data[data['Target']==0]
    K2 = data[data['Target']==1]

    K1_plits8 = [plits8[i-1].copy() for i in K1.index]
    K2_plits8 = [plits8[j-1].copy() for j in K2.index]
    p_plits8 = plits8[k-1].copy()

    GK1 = 0; GK2 = 0
    for i in range(0,nc):
        for j in range(0,len(K1_plits8)):
            vk1 = K1_plits8[j][i]
            for jj in range(0,j):
                vk11 = K1_plits8[jj][i]
                if vk11==vk1:
                    K1_plits8[jj][i] = 8
            for j1 in range(0, len(K2_plits8)):
                vk2 = K2_plits8[j1][i]
                for j11 in range(0,j1):
                    vk22 = K2_plits8[j11][i]
                    if vk22==vk2:
                        K2_plits8[j11][i] = 8
                if vk2==vk1:
                    for i1 in range(0,len(K1_plits8)):
                        vkk1=K1_plits8[i1][i]
                        if vkk1==vk1:
                            K1_plits8[i1][i]=8
                    for i2 in range(0,len(K2_plits8)):
                        vkk2=K2_plits8[i2][i]
                        if vkk2==vk2:
                            K2_plits8[i2][i] = 8
    for i in range(0,nc):
        vp = p_plits8[i]
        for j in range(0,len(K1_plits8)):
            vk1 = K1_plits8[j][i]
            if vk1==vp:
                GK1 +=1  
        for j1 in range(0, len(K2_plits8)):
            vk2 = K2_plits8[j1][i]
            if vk2==vp:
                GK2 +=1
                
    ##################################   Prediction   #########################################
    if GK1>GK2:
        pred = 0
        if p_data["Target"]==0:
            t0+=1
    else:
        pred = 1
        if p_data["Target"]==1:
            t1+=1
    print(f"{k}-Zone: Golos K1(0) = {GK1}  Golos K2(1) = {GK2} Real - {p_data["Target"]}  Prediction - {pred}")
print(f"\nCorrectly found:{t0+t1}\nAlgorithm reliability: {int(100*(t0+t1)/n_row)}%")
