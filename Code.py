import math  
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = np.loadtxt('Data.txt')
Data = pd.DataFrame(data)
Data.columns = ['X', 'Y']
D = pd.DataFrame(index=range(300), columns=['D1','D2','D3'])
C = pd.DataFrame(index=range(200), columns=['Cluster1','Cluster2','Cluster3'])
Dx, D1, D2, D3, MinAvgDis, sniFinalC1, FinalC2, FinalC3 = [], 0, 0, 0, 1000, 0, 0, 0

def Dis(x1,y1,x2,y2):  # Distance function
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist

for Runs in range(100): # Initialize Centroids
    c1 = Data.sample(1)
    k, c2, c3, MaxD1, MaxD2 = 3, 0, 0, 0, 0
    for i in range(300):
        for x in range(301):
            if x-i == 1:
                Distance = Dis(c1['X'],c1['Y'],Data[i:x]['X'].values,Data[i:x]['Y'].values)
                if Distance > MaxD1:
                    MaxD1 = Distance
                    c2 = Data[i:x]
    for i in range(300):
        for x in range(301):
            if x-i == 1:
                if Data[i:x]['X'].values != c1['X'].values and Data[i:x]['Y'].values != c1['Y'].values:
                    Distance = Dis(c2['X'],c2['Y'],Data[i:x]['X'].values,Data[i:x]['Y'].values)
                    if Distance > MaxD2:
                        MaxD2 = Distance
                        c3 = Data[i:x]
    C1 = c1.values[0]
    C2 = c2.values[0]
    C3 = c3.values[0]

#%% Calculating distances and clusters
    
    for Converges in range(5): # Main algorithm
        Clus1,Clus2,Clus3,Cl1,Cl2,Cl3 = [],[],[],[],[],[]
        for i in range(300):
            for x in range(301): # Calculating Distances
                if x-i == 1:
                    Distance = Dis(C1[0],C1[1],Data[i:x]['X'].values,Data[i:x]['Y'].values)
                    D['D1'][i] = Distance
                    Distance = Dis(C2[0],C2[1],Data[i:x]['X'].values,Data[i:x]['Y'].values)
                    D['D2'][i] = Distance
                    Distance = Dis(C3[0],C3[1],Data[i:x]['X'].values,Data[i:x]['Y'].values)
                    D['D3'][i] = Distance
        
        for i in range(300):
            for x in range(301): # Adding points to Clusters
                if x-i == 1:
                    Min = min(D[i:x]['D1'].values,D[i:x]['D2'].values,D[i:x]['D3'].values)
                    if D[i:x]['D1'].values == Min :
                        Clus1.append(Data[i:x][['X']+['Y']].values)
                    if D[i:x]['D2'].values == Min :
                        Clus2.append(Data[i:x][['X']+['Y']].values)
                    if D[i:x]['D3'].values == Min :
                        Clus3.append(Data[i:x][['X']+['Y']].values)
        for i in range (len(Clus1)):
            Cl1.append(Clus1[i][0])
        for i in range (len(Clus2)):
            Cl2.append(Clus2[i][0])
        for i in range (len(Clus3)):
            Cl3.append(Clus3[i][0])
        C['Cluster1'], C['Cluster2'], C['Cluster3'] = pd.Series(Cl1), pd.Series(Cl2), pd.Series(Cl3)
        
        X1, Y1, X2, Y2, X3, Y3 = 0, 0, 0, 0, 0, 0
        for i in range(len(Cl1)):
            X1 = X1 + Cl1[i][0]
            Y1 = Y1 + Cl1[i][1]
        C1 = [X1/len(Cl1),Y1/len(Cl1)]
        for i in range(len(Cl2)):
            X2 = X2 + Cl2[i][0]
            Y2 = Y2 + Cl2[i][1]
        C2 = [X2/len(Cl2),Y2/len(Cl2)]
        for i in range(len(Cl3)):
            X3 = X3 + Cl3[i][0]
            Y3 = Y3 + Cl3[i][1]
        C3 = [X3/len(Cl3),Y3/len(Cl3)]
    D1 = sum(D['D1'])/len(D['D1'])
    D2 = sum(D['D2'])/len(D['D2'])
    D3 = sum(D['D3'])/len(D['D3'])
    AvgDis = D1+D2+D3
    Dx.append(AvgDis)
    if AvgDis < MinAvgDis:
        MinAvgDis = AvgDis
        FinalC1 = C1
        FinalC2 = C2
        FinalC3 = C3
         
#%% Final Plotting

plt.title('Original Data & Sample of random centers')
plt.scatter(Data['X'],Data['Y'])
plt.scatter(c1['X'],c1['Y'], marker='*', s=300, c='r')
plt.scatter(c2['X'],c2['Y'], marker='*', s=300, c='k')
plt.scatter(c3['X'],c3['Y'], marker='*', s=300, c='k')
plt.show()

plt.title('Clusters after converging & New centriods')
for i in range(len(Cl1)):
    plt.scatter(Cl1[i][0],Cl1[i][1], c='gold')
for i in range(len(Cl2)):
    plt.scatter(Cl2[i][0],Cl2[i][1], c='orange')
for i in range(len(Cl3)):
    plt.scatter(Cl3[i][0],Cl3[i][1], c='yellowgreen')
plt.scatter(FinalC1[0],FinalC1[1], marker='*', s=300, c='r')
plt.scatter(FinalC2[0],FinalC2[1], marker='*', s=300, c='k')
plt.scatter(FinalC3[0],FinalC3[1], marker='*', s=300, c='k')
plt.show()

print('Centriod One: ', C1,'\nCentriod Two: ', C2,'\nCentriod Three: ', C3)
print('With Minimum Avg Distance: ', MinAvgDis)