from asyncio.windows_events import NULL
from fileinput import filename
from traceback import print_tb
from weakref import ref
from sklearn import linear_model
from sklearn.model_selection import train_test_split

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from itertools import product
from scipy.spatial import ConvexHull
from sklearn.preprocessing import MinMaxScaler

#own imports
from csvpy import *


def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

#Sets Plotdesigndata on global Level
 #CHANGE FONT TYPE
plt.rc('font',family='Linux Biolinum')
#CHANGE FONT SIZES
# plt.rc('font', size=12, weight='bold') #controls default text size
#plt.rc('font', size=12) #controls default text size
plt.rc('figure', titlesize=12) #fontsize of the title
plt.rc('axes', titlesize=12) #fontsize of the title
plt.rc('axes', labelsize=12) #fontsize of the x and y labels
plt.rc('xtick', labelsize=12) #fontsize of the x tick labels
plt.rc('ytick', labelsize=12) #fontsize of the y tick labels
plt.rc('legend', fontsize=12) #fontsize of the legend
plt.set_loglevel("error") # just shows important error. Ignores warnings.





def preVal(model,f1min,f1max,f1num,f2min,f2max,f2num, automaticfeatsel, X_sel, scaler_p):
    num_col_sel = np.atleast_2d(X_sel).shape[1] # gets the number of columns of a numpy array
    if automaticfeatsel == 0:
        #Used in the thesis to plot a 8 Dimensional Model in 3d with the other dimensions constant
        # if num_col_sel == 8:
        #     maximum_element_col = np.max(X_sel, 0)
        #     minimum_element_col = np.min(X_sel, 0)
        #     a =[]

        #     a.append(np.linspace(minimum_element_col[4], maximum_element_col[4], f1num))
        #     a.append(np.linspace(minimum_element_col[5], maximum_element_col[5], f2num))

        #     X_l = list(product(*a)) # creates a list with all combinations of features
        #     X_l_arr = np.asarray(X_l) # turns the list in a numpy array
        #     X_pre_o=np.zeros((X_l_arr.shape[0],num_col_sel))
        #     X_pre_o[:,[4,5]]=X_l_arr

        #     #Define constant dimension of the 8 dimensional plot
        #     X_pre_o[:,0]=2710.043333
        #     X_pre_o[:,1]=86.77480904
        #     X_pre_o[:,2]=13.74265694
        #     X_pre_o[:,3]=52.73691608
            
        #     X_pre_o[:,6]=0.15
        #     X_pre_o[:,7]=57.37654321
            
        #     print(X_pre_o)
        #     print(X_pre_o[1][4])
        #     print(X_pre_o[1][3])

        #     print("shape X_pre_o",X_pre_o.shape[0])
        #     print("shape X_pre_o Ohne",X_pre_o.shape)
        # if num_col_sel == 2:
        #     #creates a set of values according to the input parameters
        #     f1 = np.linspace(f1min, f1max, f1num)
        #     f2 = np.linspace(f2min, f2max, f2num)
          
        #     #Transforms the the lines to vectors for further processing
        #     f1vt, u1 = np.meshgrid(f1,1)
        #     f2vt, u2 = np.meshgrid(f2,1)
        #     f1v= f1vt.T
        #     f2v= f2vt.T

        #     #Fill an numpy X array in the right form
        #     numrows=f1num*f2num
        #     X_pre_o = np.zeros((numrows,2))
        #     l = 0
        #     for i in range(f1num):
        #         for k in range(f2num):
        #             X_pre_o[l][0]=f1v[i]
        #             X_pre_o[l][1]=f2v[k]
        #             l+=1
      
        # elif num_col_sel == 1:
        #     #creates a set of values according to the input parameters
        #     f1 = np.linspace(f1min, f1max, f1num)
            
        #     #Transforms the the lines to vectors for further processing
        #     f1vt, u1 = np.meshgrid(f1,1)
            
        #     f1v= f1vt.T
            

        #     #Fill an numpy X array in the right form
        #     numrows=f1num*f2num
        #     X_pre_o = np.zeros((numrows,1))
        #     l = 0
        #     for i in range(f1num):
        #         for k in range(f2num):
        #             X_pre_o[l][0]=f1v[i]
                    
        #             l+=1
        # else:
        if num_col_sel < 3:
            maximum_element_col = np.max(X_sel, 0)
            minimum_element_col = np.min(X_sel, 0)
            a =[]
            for i in range(len(maximum_element_col)):
                a.append(np.linspace(minimum_element_col[i], maximum_element_col[i], f1num)) # adds a linspace array for each feature
            X_l = list(product(*a)) # creates a list with all combinations of features
            X_pre = np.asarray(X_l) # turns the list in a numpy array
            X_pre_o = scaler_p.inverse_transform(X_pre) # inverse normalization 
        else:
            print("\n")
            print("-----INFORMATION PROCESS WINDOW INFORMATION-----")
            print("The generated Data is 4 dimensional or more dimensional. Therefore, the prediction window can't be plotted. Please change input parameters. ")
            print("Program closed.")
            print("------------------------------------------------")
            quit()
    
        # scaler_a = MinMaxScaler()
        # X_pre = scaler_a.fit_transform(X_pre_o) # normalises the predicted data

    elif automaticfeatsel == 1:
        if num_col_sel < 3:
            maximum_element_col = np.max(X_sel, 0)
            minimum_element_col = np.min(X_sel, 0)
            a =[]
            for i in range(len(maximum_element_col)):
                a.append(np.linspace(minimum_element_col[i], maximum_element_col[i], f1num)) # adds a linspace array for each feature
            X_l = list(product(*a)) # creates a list with all combinations of features
            X_pre = np.asarray(X_l) # turns the list in a numpy array
            X_pre_o = scaler_p.inverse_transform(X_pre) # inverse normalization 
        else:
            print("\n")
            print("-----INFORMATION PROCESS WINDOW INFORMATION-----")
            print("The generated Data is 4 dimensional or more dimensional. Therefore, the prediction window can't be plotted. Please change input parameters. ")
            print("Program closed.")
            print("------------------------------------------------")
            quit()

    
    # Calculate preditions and add them together to one array
    
    y_pre = model.predict(X_pre)
    y_prevt, u1 = np.meshgrid(y_pre,1)
    num_col = np.atleast_2d(X_pre).shape[1] # gets the number of columns of a numpy array
    D = np.insert(X_pre_o,num_col, y_prevt, axis=1) # inserts a col vector in a numpy array at position num_col      
   
    return D 

def priProWin(D,colheadersidf,desden,cp1a,cp2a):
    
    num_col_D = np.atleast_2d(D).shape[1] # gets the number of columns of a numpy array
    if num_col_D == 2:
        figwin = range (1)
    elif num_col_D == 3:
        figwin = range (2)
    elif num_col_D >=4:
        print("\n")
        print("-----INFORMATION PROCESS WINDOW INFORMATION-----")
        print("The generated Data is 4 dimensional or more dimensional. Therefore, the prediction window can't be plotted. Please change input parameters. ")
        print("Program closed.")
        print("------------------------------------------------")
        quit()

    #Plots 2 Windows next to each other uses window pixel size
    start_x, start_y, dx, dy = (0, 30, 960, 1080)
    
    for i in figwin:
        if i%3 == 0:
            x = start_x
            y = start_y  + (dy * (i//3) )
        fig=plt.figure(figsize=(cm2inch(17,10)))
        

        if num_col_D == 3:# 3D plot with one col is the desired value
            if i == 0:
                # fig = plt.figure(num=None, figsize=(11.55, 13), dpi=80, facecolor='w', edgecolor='k')
                ax = plt.axes(projection='3d')

                maxVal =np.max(D[:,2])
                minVal =np.min(D[:,2])
               
                sc =ax.scatter(D.T[0], D.T[1], D.T[2], c=D.T[2], cmap='RdYlGn', linewidth=0.5, edgecolors='black',label='Predicted Process Points');
               
                ax.legend()
                cb=plt.colorbar(sc,ticks=np.linspace(minVal,maxVal,cp1a,dtype='float32'),format='%.2f',pad=0.15)
                # fig.suptitle('3D Visualisation of Predicted Process Points', fontweight ="bold")
                # print("Test123",np.linspace(minVal,maxVal,cp1a,dtype='str'))
                # cb.ax.set_yticklabels(np.linspace(minVal,maxVal,cp1a,dtype='str'))
                ax.set_xlabel(colheadersidf[0])
                ax.set_ylabel(colheadersidf[1])
                ax.set_zlabel(colheadersidf[2]);
                cb.set_label(colheadersidf[2]);
                # ax.set_xlabel('Laser Power [W]')
                # ax.set_ylabel('Scan Speed [mm/s]')
                # ax.set_zlabel('Relative Density [%]');
                # cb.set_label('Relative Density [%]');
                # plt.savefig("./Visual/3DVisualisation_temp.pdf", format='pdf',bbox_inches='tight') # saved as eps for high quality pictures
                plt.savefig("./Visual/3DVisualisation_temp.pdf", format='pdf',bbox_inches='tight') # saved as eps for high quality pictures


                # ax.set_title('Visualisation Dataset')
            
            if i == 1:
                
                # #Moifies the Dataset
                # D[D[:,2]>desden]
                # D_dm = D[D[:,2]>desden] # deletes each row with a density lower then the desired density desden
                # D_wd = np.delete(D_dm, 2, 1) # deletes the density column out of the dataset
                # maxVal2 =np.max(D_dm[:,2])#Searches for the maximal relative density in the dataset
                # minVal2 =np.min(D_dm[:,2])#Searches for the minimal relative density in the dataset

                D[D[:,2]>desden]
                D_dm = D[D[:,2]>desden] # deletes each row with a density lower then the desired density desden
                D_wd = np.delete(D_dm, 2, 1) # deletes the density column out of the dataset
                maxVal2 =np.max(D_dm[:,2])#Searches for the maximal relative density in the dataset
                minVal2 =np.min(D_dm[:,2])#Searches for the minimal relative density in the dataset

                #Second 2D plot
                ax = plt.axes()
                # sc2=ax.scatter(D_dm.T[1], D_dm.T[0], c=D_dm.T[2], cmap='RdYlGn', linewidth=0.5, edgecolors='black',label='Predicted Process Points')
                sc2=ax.scatter(D_dm.T[1], D_dm.T[0], c=D_dm.T[2], cmap='RdYlGn', linewidth=0.5, edgecolors='black',label='Predicted Process Points')
                D_red=D_wd
                #Creates a Hull from the points
                hull = ConvexHull(D_red,incremental=False) # defines a hull from the points
                hullverm= np.append(hull.vertices,hull.vertices[0]) # adds the first point to the array to have a closed convex hull
                plt.plot(D_red[hullverm,1], D_red[hullverm,0], 'k', lw=2, label='Predicted Process Window') #plots the hull
                ax.legend()#plots a legend
                cb = plt.colorbar(sc2,ticks=np.linspace(minVal2,maxVal2,cp2a,dtype='float32'),format='%.2f')#plots a colorbar

                #Defines Titels of the plot
                fig.suptitle('Predicted Process Window with a {} higher than {}. '.format(colheadersidf[2],desden), fontweight ="bold")
                ax.set_xlabel(colheadersidf[1])
                ax.set_ylabel(colheadersidf[0])
                cb.set_label(colheadersidf[2]);

                #saves the plot
                plt.savefig("./Visual/2DVisualisation_temp.pdf", format='pdf',bbox_inches='tight') # saved as eps for high quality pictures


######## This part was used to generate a process window with 8 dimensional input and plot it in 3d with the other dimensions stay constant. ######
        # elif num_col_D == 8:# 3D plot with one col is the desired value
        #     if i == 0:
        #         # fig = plt.figure(num=None, figsize=(11.55, 13), dpi=80, facecolor='w', edgecolor='k')
        #         ax = plt.axes(projection='3d')
        #         # print(D)
        #         # maxVal= D.max(axis=1)
        #         # maxVal =np.max(D[:,2])
        #         # minVal =np.min(D[:,2])
        #         maxVal =np.max(D[:,8])
        #         minVal =np.min(D[:,8])
        #         # print("MaxValue",maxVal)
        #         # print("MinValue",minVal)
        #         sc =ax.scatter(D.T[4], D.T[5], D.T[8], c=D.T[8], cmap='RdYlGn', linewidth=0.5, edgecolors='black',label='Predicted Process Points');
        #         # sc.set_clim(minVal,maxVal) #used to set colorbounds of the colormap
        #         ax.legend()
        #         cb=plt.colorbar(sc,ticks=np.linspace(minVal,maxVal,cp1a,dtype='float32'),format='%.2f',pad=0.15)
        #         # fig.suptitle('3D Visualisation of Predicted Process Points', fontweight ="bold")
        #         # print("Test123",np.linspace(minVal,maxVal,cp1a,dtype='str'))
        #         # cb.ax.set_yticklabels(np.linspace(minVal,maxVal,cp1a,dtype='str'))
        #         # ax.set_xlabel(colheadersidf[0])
        #         # ax.set_ylabel(colheadersidf[1])
        #         # ax.set_zlabel(colheadersidf[2]);
        #         # cb.set_label(colheadersidf[2]);
        #         ax.set_xlabel('Laser Power [W]')
        #         ax.set_ylabel('Scan Speed [mm/s]')
        #         ax.set_zlabel('Relative Density [%]');
        #         cb.set_label('Relative Density [%]');
        #         # plt.savefig("./Visual/3DVisualisation_temp.pdf", format='pdf',bbox_inches='tight') # saved as eps for high quality pictures
        #         plt.savefig("./Visual/3DVisualisation_temp.pdf", format='pdf',bbox_inches='tight') # saved as eps for high quality pictures


        #         # ax.set_title('Visualisation Dataset')
            
        #     if i == 1:
                
        #         # #Moifies the Dataset
        #         # D[D[:,2]>desden]
        #         # D_dm = D[D[:,2]>desden] # deletes each row with a density lower then the desired density desden
        #         # D_wd = np.delete(D_dm, 2, 1) # deletes the density column out of the dataset
        #         # maxVal2 =np.max(D_dm[:,2])#Searches for the maximal relative density in the dataset
        #         # minVal2 =np.min(D_dm[:,2])#Searches for the minimal relative density in the dataset

        #         D[D[:,8]>desden]
        #         print("Shape of D",D.shape)
        #         print("Data ",D)
        #         D_dm = D[D[:,8]>desden] # deletes each row with a density lower then the desired density desden
        #         print("Cleaned data D",D_dm.shape)
        #         D_wd = np.delete(D_dm, 8, 1) # deletes the density column out of the dataset
        #         print("Cleaned data D",D_wd.shape)
        #         print("Data wd deleted ",D_wd)
        #         maxVal2 =np.max(D_dm[:,8])#Searches for the maximal relative density in the dataset
        #         minVal2 =np.min(D_dm[:,8])#Searches for the minimal relative density in the dataset

        #         #Second 2D plot
        #         ax = plt.axes()
        #         # sc2=ax.scatter(D_dm.T[1], D_dm.T[0], c=D_dm.T[2], cmap='RdYlGn', linewidth=0.5, edgecolors='black',label='Predicted Process Points')
        #         sc2=ax.scatter(D_dm.T[5], D_dm.T[4], c=D_dm.T[8], cmap='RdYlGn', linewidth=0.5, edgecolors='black',label='Predicted Process Points')
        #         D_red=D_wd[:,[4,5]]
        #         #Creates a Hull from the points
        #         hull = ConvexHull(D_red,incremental=False) # defines a hull from the points
        #         hullverm= np.append(hull.vertices,hull.vertices[0]) # adds the first point to the array to have a closed convex hull
        #         plt.plot(D_red[hullverm,1], D_red[hullverm,0], 'k', lw=2, label='Predicted Process Window') #plots the hull
        #         ax.legend()#plots a legend
        #         cb = plt.colorbar(sc2,ticks=np.linspace(minVal2,maxVal2,cp2a,dtype='float32'),format='%.2f')#plots a colorbar

        #         #Defines Titels of the plot
        #         # fig.suptitle('Predicted Process Window with a {} higher than {}. '.format(colheadersidf[2],desden), fontweight ="bold")
        #         # ax.set_xlabel(colheadersidf[1])
        #         # ax.set_ylabel(colheadersidf[0])
        #         # cb.set_label(colheadersidf[2]);
        #         ax.set_xlabel('Laser Power [W]')
        #         ax.set_ylabel('Scan Speed [mm/s]')
        #         cb.set_label('Relative Density [%]');

        #         #saves the plot
        #         # plt.savefig("./Visual/2DVisualisation_temp.pdf", format='pdf',bbox_inches='tight') # saved as eps for high quality pictures
        #         plt.savefig("./Visual/2DVisualisation_temp.pdf", format='pdf',bbox_inches='tight') # saved as eps for high quality pictures
        elif num_col_D == 2:
            if i == 0:
                ax = plt.axes()

                maxVal =np.max(D[:,1])
                minVal =np.min(D[:,1])
                
                sc = plt.scatter(D.T[0],D.T[1], c=D.T[1], cmap='RdYlGn', linewidth=0.5, edgecolors='black',label='Predicted Process Points')
                # sc.set_clim(minVal,maxVal) #used to set colorbounds of the colormap
                ax.legend()
                cb=plt.colorbar(sc,ticks=np.linspace(minVal,maxVal,cp1a,dtype='float32'),format='%.2f')
                fig.suptitle('2D Visualisation of Predicted Process Points', fontweight ="bold")
                ax.set_xlabel(colheadersidf[0])
                ax.set_ylabel(colheadersidf[1])
                cb.set_label(colheadersidf[1]);
                plt.savefig("./Visual/2DVisualisation_temp.pdf", format='pdf',bbox_inches='tight') # saved as eps for high quality pictures

                # ax.set_title('Visualisation Dataset')
        


        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(x, y, dx, dy)
        x += dx
 
    plt.show()



def plotinputdata(Xm,ym,colheadersidf,cp1a ,path):
    #Plots 2 Windows next to each other uses window pixel size
    start_x, start_y, dx, dy = (0, 30, 1920, 1080)
    for i in range(1): # determins the number of plotted windows
        if i%3 == 0:
            x = start_x
            y = start_y  + (dy * (i//3) )

        fig=plt.figure()
        if i == 0:
            ax = plt.axes(projection='3d')
            maxVal =np.max(ym)
            minVal =np.min(ym)
            sc =ax.scatter(Xm.T[0], Xm.T[1], ym, c=ym, cmap='RdYlGn',  linewidth=0.5, edgecolors='black',label='Input Data Points');
            # sc.set_clim(minVal,maxVal) #used to set colorbounds of the colormap
            ax.legend()
            cb=plt.colorbar(sc,ticks=np.linspace(minVal,maxVal,cp1a),format='%.2f')
            fig.suptitle('3D Visualisation of Input Data Points', fontweight ="bold")
            ax.set_xlabel(colheadersidf[0])
            ax.set_ylabel(colheadersidf[1])
            ax.set_zlabel(colheadersidf[len(colheadersidf)-1]);
            cb.set_label(colheadersidf[len(colheadersidf)-1]);
            plt.savefig(path+'.pdf', format='pdf',bbox_inches='tight') # saved as eps for high quality pictures
            # plt.savefig(path+'.svg', format='svg',bbox_inches='tight')
            # plt.savefig(path+'.png', bbox_inches='tight')
            

        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(x, y, dx, dy)
        x += dx
    plt.show()


def plotinputdataML(X_train,y_train,X_test, y_test,colheadersidf,testdatasize):

    #Plots 2 Windows next to each other uses window pixel size
    start_x, start_y, dx, dy = (0, 30, 1920, 1080)
    for i in range(1): # determins the number of plotted windows
        if i%3 == 0:
            x = start_x
            y = start_y  + (dy * (i//3) )

        fig=plt.figure()
        if i == 0:
            ax = plt.axes(projection='3d')
            # maxVal =np.max(ym)
            # minVal =np.min(ym)
            sc =ax.scatter(X_train.T[0], X_train.T[1], y_train, c='black', linewidth=0.5,label='Trainings Data Points');
            sc2 =ax.scatter(X_test.T[0], X_test.T[1], y_test, c='red', linewidth=0.5, label='Test Data Points');
            # sc.set_clim(minVal,maxVal) #used to set colorbounds of the colormap
            ax.legend()
            # cb=plt.colorbar(sc,ticks=np.linspace(minVal,maxVal,cp1a),format='%.2f')
            trainingdatasize = (1-testdatasize)*100
            fig.suptitle('3D Visualisation of Input Data Divided in {:.2f} % Training and {:.2f} % Test Data Set '.format(trainingdatasize,testdatasize*100), fontweight ="bold")
            ax.set_xlabel(colheadersidf[0])
            ax.set_ylabel(colheadersidf[1])
            ax.set_zlabel(colheadersidf[len(colheadersidf)-1]);
            # cb.set_label(colheadersidf[2]);
            plt.savefig("./Visual/3DVisualisationTestandTrainingData_temp.eps",bbox_inches='tight', format='eps') # saved as eps for high quality pictures
            plt.savefig("./Visual/3DVisualisationTestandTrainingData_temp.svg",bbox_inches='tight', format='svg')
            plt.savefig("./Visual/3DVisualisationTestandTrainingData_temp.png",bbox_inches='tight')
            

        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(x, y, dx, dy)
        x += dx
    plt.show()



def plotpermutationimportance(X_train,y_train,X_test, y_test,colheadersidf,testdatasize):

    #Plots 2 Windows next to each other uses window pixel size
    start_x, start_y, dx, dy = (0, 30, 1920, 1080)
    for i in range(1): # determins the number of plotted windows
        if i%3 == 0:
            x = start_x
            y = start_y  + (dy * (i//3) )

        fig, ax = plt.subplots(figsize =(16, 9))
        if i == 0:
            ax.barh(colheadersidf,)
            # maxVal =np.max(ym)
            # minVal =np.min(ym)
            sc =ax.scatter(X_train.T[0], X_train.T[1], y_train, c='black', linewidth=0.5,label='Trainings Data Points');
            sc2 =ax.scatter(X_test.T[0], X_test.T[1], y_test, c='red', linewidth=0.5, label='Test Data Points');
            # sc.set_clim(minVal,maxVal) #used to set colorbounds of the colormap
            ax.legend()
            # cb=plt.colorbar(sc,ticks=np.linspace(minVal,maxVal,cp1a),format='%.2f')
            trainingdatasize = (1-testdatasize)*100
            fig.suptitle('3D Visualisation of Input Data Divided in {:.2f} % Training and {:.2f} % Test Data Set '.format(trainingdatasize,testdatasize*100), fontweight ="bold")
            ax.set_xlabel(colheadersidf[0])
            ax.set_ylabel(colheadersidf[1])
            ax.set_zlabel(colheadersidf[2])
            # cb.set_label(colheadersidf[2]);
            plt.savefig("./Visual/3DVisualisationTestandTrainingData_temp.pdf",bbox_inches='tight', format='pdf') # saved as eps for high quality pictures
            

        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(x, y, dx, dy)
        x += dx
    plt.show()

def drawNN(file_name ,layers):
    
    num_layers = len(layers)
    max_neurons_per_layer = np.amax(layers)
    dist = 2*max(1, max_neurons_per_layer/num_layers)
    y_shift = layers/2-.5
    rad = .3

    fig = plt.figure(frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Draw all circles
    for i in range(num_layers):
        for j in range(layers[i]):
            circle = plt.Circle((i*dist, j-y_shift[i]),
                                radius=rad, fill=False)
            ax.add_patch(circle)

    # Draw the lines between the layers.
    for i in range(num_layers-1):
        for j in range(layers[i]):
            for k in range(layers[i+1]):
                angle = np.arctan((j-k+y_shift[i+1]-y_shift[i]) / dist)
                x_adjust = rad * np.cos(angle)
                y_adjust = rad * np.sin(angle)
                line = plt.Line2D((i*dist+x_adjust,
                                    (i+1)*dist-x_adjust),
                                    (j-y_shift[i]-y_adjust,
                                    k-y_shift[i+1]+y_adjust),
                                    lw=2 / np.sqrt(layers[i]
                                                    + layers[i+1]),
                                    color='b')
                ax.add_line(line)

    ax.axis('scaled')

    if file_name is None:
        plt.show()
    else:
        fig.savefig(file_name, bbox_inches='tight', format='pdf')
        plt.show()


if __name__ == "__main__":
    idf=readcsvcol("./InputData/collected_data.csv",[3,4,5])
    colheadersidf=list(idf.columns.values) # gets a list of df header strings

    #Spilts the Pandas dataframe in to numpy array Inputs X and result y 
    X = idf.iloc[:,0:2].values
    y = idf.iloc[:,2:3].values.ravel() #ravel funktion converts the array to a (n,) array instead of an (n,1) vector
  

    # plotinputdata(X,y,colheadersidf,8)
    # Divide data in TRAINING DATA and TEST DATA
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.1)

    # Train LINEAR REGRESSON MODEL
    l_reg = linear_model.LinearRegression()
    model = l_reg.fit(X_train, y_train)

    


    D = preVal(model,0,100,4,0,100,4,1,X)
    # priProWin(D,colheadersidf,95,8,8)