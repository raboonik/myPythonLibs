#Invocation: obj = read_vis(raw_feed, feed_range=None, variable=None, quiet=None, equil_feed=None, dt=10, direct_timelist=None)
#Example:    obj = read_vis('tube*', [4,10], ['bx*rho0^2','vy'], True, None, equil_feed=None, 10)
#            data_dic = obj.read()

from required_pkgs import *

#import h5py
#import numpy as np
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#from matplotlib import ticker, cm
#import scipy as spy
#import glob, os, subprocess   # subprocess for storing output of bash commands
#from os import system as bash
#from os import chdir as cd
#import scipy.ndimage
#from time_evol import myrandint
#import sys
#from formula_symbolic import *

#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#◈                                                           ◈
#◈                                                           ◈
#◈                                                           ◈
#◈                                                           ◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈

alphabet = 'abcdefghijklmnopqrstuvwxyz'

#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
Mancha_TimeStamps = []                                               #◈
i = 0                                                                #◈
while sys.getsizeof(Mancha_TimeStamps) < 10000:                      #◈
    for j in range(10):                                              #◈
        for k in range(10):                                          #◈
            for l in range(10):                                      #◈
                Mancha_TimeStamps.append(str(i)+str(j)+str(k)+str(l))#◈
    i+=1                                                             #◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈

#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#           FUNCTIONS                       ◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈                                                                                                #◈
                                                                                                                                            #◈
def trans(vec, cond):                                                                                                                       #◈
    if cond:                                                                                                                                #◈
        vec = np.transpose(vec)                                                                                                             #◈
    else:                                                                                                                                   #◈
        pass                                                                                                                                #◈
    return vec                                                                                                                              #◈
                                                                                                                                            #◈
# We'll assume feedlist containts the list of all snapshots:                                                                                #◈
# The argument 'lag' is defined to shift the filename number since 0001 is associated with time=0.                                          #◈
def find_timelist(feedlist,dt, lag = 1):                                                                                                    #◈
    # Three ways to find the time stamp of a snapshot                                                                                       #◈
    #   1) Directly from the H5 file                                                                                                        #◈
    #   2) Read the file name and find the four digit number                                                                                #◈
    #   3) Having number of files, the start time, and the time step                                                                        #◈
                                                                                                                                            #◈
    # 1)                                                                                                                                    #◈
    timelist_hdf = []                                                                                                                       #◈
    item_inx = 0                                                                                                                            #◈
    for item in feedlist:                                                                                                                   #◈
        with h5py.File(item, 'r') as hdf:                                                                                                   #◈
            if 'time' in hdf.attrs.keys():                                                                                                  #◈
                timelist_hdf.append(float(hdf.attrs['time']))                                                                               #◈
                # Make sure the timestamps are not just 0.                                                                                  #◈
                if item_inx == 2:                                                                                                           #◈
                    if all([t == 0. for t in timelist_hdf]):                                                                                #◈
                        timelist_hdf = []                                                                                                   #◈
                        print("Time stamps in snapshots are all 0.")                                                                        #◈
                        break                                                                                                               #◈
            else:                                                                                                                           #◈
                print("No attribute 'time' available!")                                                                                     #◈
                timelist_hdf = []                                                                                                           #◈
                break                                                                                                                       #◈
        item_inx += 1                                                                                                                       #◈
    # 2)                                                                                                                                    #◈
    if len(timelist_hdf) == 0:                                                                                                              #◈    
        item = feedlist[0]                                                                                                                  #◈    
        if '/' in item:                                                                                                                     #◈    
            i = 0                                                                                                                           #◈    
            while True:                                                                                                                     #◈    
                if item[-i-1] == '/': break                                                                                                 #◈    
                else: i+=1                                                                                                                  #◈    
                                                                                                                                            #◈    
        item = item[-i:]                                                                                                                    #◈    
        filenames = [filename[-i:] for filename in feedlist]                                                                                #◈    
        timelist_filename = []                                                                                                              #◈    
        # Drop 'h5' in item so that we can reference like item[-i-5:-i-1] dropping the '.'                                                  #◈    
        item = item[:-len('h5')]                                                                                                            #◈    
        i = 0                                                                                                                               #◈    
        while True:                                                                                                                         #◈    
            if item[-i-5:-i-1] in Mancha_TimeStamps:                                                                                        #◈    
                temp = [filename[-i-5-len('h5'):-i-1-len('h5')] for filename in filenames]                                                  #◈    
                break                                                                                                                       #◈    
            elif i > 100:                                                                                                                   #◈    
                print("While loop in find_timelist() saturated! No Mancha-specific time stamp found in snapshot filename!")                 #◈    
                temp = []                                                                                                                   #◈    
                break                                                                                                                       #◈    
            else: i+=1                                                                                                                      #◈    
        if len(temp) > 0:                                                                                                                   #◈    
            timelist_filename = [(int(timestamp) - lag)*dt for timestamp in temp]                                                           #◈    
            timelist_filename = [t if t>=0 else 0 for t in timelist_filename]                                                               #◈    
            return timelist_filename                                                                                                        #◈
        else:                                                                                                                               #◈
            print("*************************************WARNING!*********************************************!")                            #◈
            print("Could not retrieve a time list neither from the h5 'time' attribute nor from the filenames!")                            #◈
    else:                                                                                                                                   #◈
        return timelist_hdf                                                                                                                 #◈   
                                                                                                                                            #◈
def fid(path):                                                                                                                              #◈
    if isinstance(path, str):                                                                                                               #◈
        return sorted(glob.glob(path))                                                                                                      #◈
    elif isinstance(path, list):                                                                                                            #◈
        return path                                                                                                                         #◈
    else:                                                                                                                                   #◈
        raise OSError("The list of snapshot files could not be retrieved!")                                                                 #◈
                                                                                                                                            #◈
                                                                                                                                            #◈
def save_fig(fig,comp,i,num, string=None):                                                                                                  #◈
    seed(1)                                                                                                                                 #◈
    if string == None:                                                                                                                      #◈
        fig.savefig("contourplot_"+comp+str(i)+"_"+str(myrandint(0,10000))+str(num))                                                        #◈
    else:                                                                                                                                   #◈
        fig.savefig("contourplot_"+comp+string+str(i)+"_"+str(myrandint(0,10000))+str(num))                                                 #◈
                                                                                                                                            #◈
                                                                                                                                            #◈
def vec_avail(data_avail, vec_lst):                                                                                                         #◈
    cond = 0                                                                                                                                #◈
    for item in data_avail:                                                                                                                 #◈
        if item in vec_lst:                                                                                                                 #◈
            cond += 1                                                                                                                       #◈
    if cond >= 3:                                                                                                                           #◈
        return True                                                                                                                         #◈
    else:                                                                                                                                   #◈
        return False                                                                                                                        #◈
                                                                                                                                            #◈
def inp(comp,lst):                                                                                                                          #◈
    while comp not in lst:                                                                                                                  #◈
            print("Error: the input must be one of the followings: \n")                                                                     #◈
            print(lst)                                                                                                                      #◈
            comp = input("Enter again:")                                                                                                    #◈
    return comp                                                                                                                             #◈
                                                                                                                                            #◈
def inp_h5_file(word, var, failsafe_max=3):                                                                                                 #◈
    # Take user input until they get it right                                                                                               #◈
    m = 0    # Failsafe counter                                                                                                             #◈
    while True:                                                                                                                             #◈
        var = input("Enter the "+word+" file:")                                                                                             #◈
        if "'" in var: var = var.replace("'","")                                                                                            #◈
        try:                                                                                                                                #◈
            h5py.File(var, 'r')                                                                                                             #◈
            break                                                                                                                           #◈
        except:                                                                                                                             #◈
            print("File not found! Try again!")                                                                                             #◈
            m += 1                                                                                                                          #◈
        if m > failsafe_max: raise OSError("File not found!")                                                                               #◈
    return var                                                                                                                              #◈
                                                                                                                                            #◈
def remove_charbychar(mainstring ,string):                                                                                                  #◈
    for char in string:                                                                                                                     #◈
        if char in mainstring: mainstring = mainstring.replace(char,'')                                                                     #◈
    return mainstring                                                                                                                       #◈
                                                                                                                                            #◈
# data = np.arange(300*200*400)                                                                                                             #◈
# data = data.reshape(300,200,400)                                                                                                          #◈
# dataslice = data[3:27, 91:112, 329:397]                                                                                                   #◈
# datatras = np.transpose(data)                                                                                                             #◈
# datatrasslice = datatras[329:397,91:112,3:27]                                                                                             #◈
# dataslice == np.transpose(datatrasslice)                                                                                                  #◈
# np.min(dataslice- np.transpose(datatrasslice)) == np.max(dataslice- np.transpose(datatrasslice))                                          #◈
def readAquantity(hdf_dir, hdf_file, quantity, keys_avail, my_transpose,myquiet, minmax):                                                   #◈
    # minmax = [nx0,nx1,ny0,ny1,nz0,nz1]                                                                                                    #◈
    out = []                                                                                                                                #◈
    if quantity in keys_avail:                                                                                                              #◈
            if myquiet == 0 : print("Reading "+quantity+" in "+hdf_dir)                                                                     #◈
            if len(minmax) > 0:                                                                                                             #◈
                if my_transpose:                                                                                                            #◈
                    out = np.transpose(hdf_file[quantity][minmax[4]:minmax[5],minmax[2]:minmax[3],minmax[0]:minmax[1]])                     #◈
                else:                                                                                                                       #◈
                    out = hdf_file[quantity][minmax[0]:minmax[1],minmax[2]:minmax[3],minmax[4]:minmax[5]]                                   #◈
            else: out = trans(np.array(hdf_file.get(quantity, "f")), my_transpose)                                                          #◈
    else:                                                                                                                                   #◈
        print(quantity+" is not available!")                                                                                                #◈
    return out                                                                                                                              #◈
                                                                                                                                            #◈
def get_tobe_readlist_item(my_item, my_avail_equillist, my_keys):                                                                           #◈
    equil_out = []                                                                                                                          #◈
    for t in my_avail_equillist:                                                                                                            #◈
        if t in my_item:                                                                                                                    #◈
            equil_out.append(t)                                                                                                             #◈
            my_item = my_item.replace(t,"")                                                                                                 #◈
    nonequil_out = [t for t in my_keys if t in my_item]                                                                                     #◈
    return equil_out, nonequil_out                                                                                                          #◈
                                                                                                                                            #◈
#                                            ◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈                                                                             #◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈        END       ◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#                                            ◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
                                           

# raw_feed: can either be a direct list of snapshot directories:
#           e.g. ['/home/tube_structured_2D_6x1x4Mm_20x20x10km_0003.h5', '/home/tube_structured_2D_6x1x4Mm_20x20x10km_0004.h5'] 
#           or '/home/rabo0001/Desktop/structured_2d/h5_B50_5mhz/tube*'
# If feed_range = None, then the entire list provided by raw_feed will be read
# Set feed_range = [n1,n2] to pick a range of files between n1 and n2 from raw_feed
# Set dt = -1 to avoid processing the timeslist
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#           READ_VIS                        ◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈                                                                                                #◈
class read_vis:                                                                                                                             #◈
    def __init__(self, raw_feed, feed_range=None, variable=None, quiet=0, equil_feed=None, dt=10, direct_timelist=None, crop=0):            #◈
        if variable == None: raise OSError("Variable not found!")                                                                           #◈
        else               : self.variable = variable                                                                                       #◈
        self.crop            = crop                                                                                                         #◈
        self.direct_timelist = direct_timelist                                                                                              #◈
        self.dt              = dt                                                                                                           #◈
        self.raw_feed        = raw_feed                                                                                                     #◈
        self.quiet           = quiet                                                                                                        #◈
        self.equil_feed      = equil_feed                                                                                                   #◈
        self.feed_range      = feed_range                                                                                                   #◈
        #◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈Get the list of H5 files◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
        fid1 = fid(raw_feed)                                                                                                                #◈
        # To directly feed in a premade list of h5 files set feed_range=None and just provide the list by raw_feed                          #◈        
        if self.feed_range == None:                                                                                                         #◈
            pass                                                                                                                            #◈
        else:                                                                                                                               #◈
            cond = True                                                                                                                     #◈
            try: # Try to see if feed_range is a list. If it is, then it must have more than two elements                                   #◈
                l = len(self.feed_range)                                                                                                    #◈
                cond = False                                                                                                                #◈
                while l > 2 or np.min(self.feed_range) < 0 or np.max(self.feed_range) > len(fid1):                                          #◈
                    if l < 3 and np.min(self.feed_range) < 0 or np.max(self.feed_range) > len(fid1):                                        #◈
                        print("out of bounds! \n")                                                                                          #◈
                        num1 = int(input("Enter the lower bound: \n"))                                                                      #◈
                        num2 = int(input("Enter the upper bound: \n"))                                                                      #◈
                        self.feed_range = [num1, num2]                                                                                      #◈
                        l = len(self.feed_range)                                                                                            #◈
                    if l > 2:                                                                                                               #◈
                        print("The length of range can't be more then 2! \n")                                                               #◈
                        num1 = int(input("Enter the lower bound: \n"))                                                                      #◈
                        num2 = int(input("Enter the upper bound: \n"))                                                                      #◈
                        self.feed_range = [num1, num2]                                                                                      #◈
                        l = len(self.feed_range)                                                                                            #◈
                fid1 = fid1[np.min(self.feed_range):np.max(self.feed_range)+1]                                                              #◈
            except:                                                                                                                         #◈
                pass                                                                                                                        #◈
            if cond:                                                                                                                        #◈
                fid1 = fid1[int(self.feed_range):]                                                                                          #◈
                                                                                                                                            #◈
        hdf0 = h5py.File(fid1[0], 'r')                                                                                                      #◈
        dx = hdf0.attrs['cellsize'][0]                                                                                                      #◈
        dy = hdf0.attrs['cellsize'][1]                                                                                                      #◈
        if dy == 0: dy = dx                                                                                                                 #◈
        dz = hdf0.attrs['cellsize'][2]                                                                                                      #◈
        nx = hdf0.attrs['metadata'][1]                                                                                                      #◈
        ny = hdf0.attrs['metadata'][2]                                                                                                      #◈
        nz = hdf0.attrs['metadata'][3]                                                                                                      #◈
        x = np.arange(0., dx*nx, dx)                                                                                                        #◈
        y = np.arange(0., dy*ny, dy)                                                                                                        #◈
        z = np.arange(0., dz*nz, dz)                                                                                                        #◈
        meta_original = {'d':[dx,dy,dz], 'axes':[x,y,z], 'n':[nx,ny,nz]}                                                                    #◈
        meta_cropped = {key:meta_original[key] for key in meta_original.keys()}                                                             #◈
        # Take care of the subslab if slicing is to be done                                                                                 #◈
        if crop == 0: minmax_crop=[]                                                                                                        #◈
        # crop = {'x':[nx0,nx1], 'y':[ny0,ny1], 'z':[nz0,nz1]}                                                                              #◈
        else:                                                                                                                               #◈
            linx = 0                                                                                                                        #◈
            for axis in ['x','y','z']:                                                                                                      #◈
                if axis not in crop.keys(): self.crop[axis] = [0,meta_cropped['n'][linx]]                                                   #◈
                elif crop[axis][0] == crop[axis][1]: self.crop[axis][1] += 1                                                                #◈
                linx+=1                                                                                                                     #◈
            minx = np.min(np.abs(crop['x']))                                                                                                #◈
            maxx = np.max(np.abs(crop['x']))                                                                                                #◈
            miny = np.min(np.abs(crop['y']))                                                                                                #◈
            maxy = np.max(np.abs(crop['y']))                                                                                                #◈
            minz = np.min(np.abs(crop['z']))                                                                                                #◈
            maxz = np.max(np.abs(crop['z']))                                                                                                #◈
            # Update meta only not nx, ... so we can determine if data is to be transoposed!                                                #◈
            meta_cropped['n'] = [maxx-minx,maxy-miny,maxz-minz]                                                                             #◈
            meta_cropped['axes'] = [x[minx:maxx],y[miny:maxy],z[minz:maxz]]                                                                 #◈
            minmax_crop = [minx,maxx,miny,maxy,minz,maxz]                                                                                   #◈
                                                                                                                                            #◈
        nt = 0                                                                                                                              #◈
        if len(hdf0[list(hdf0.keys())[0]].shape) > 3:   # For when we append arrays into a 4d one nt times!                                 #◈
            try:                                                                                                                            #◈
                nt = len(hdf0[list(hdf0.keys())[0]])                                                                                        #◈
            except:                                                                                                                         #◈
                nt = hdf0[list(hdf0.keys())[0]].shape[0]                                                                                    #◈
                                                                                                                                            #◈
        transpose = False                                                                                                                   #◈
        if nt == 0:                                                                                                                         #◈
            if hdf0[list(hdf0.keys())[0]].shape != (nx, ny, nz):                                                                            #◈
                transpose = True                                                                                                            #◈
        else:                                                                                                                               #◈
            if hdf0[list(hdf0.keys())[0]].shape != (nt, nx, ny, nz):                                                                        #◈
                transpose = True                                                                                                            #◈
        if self.quiet == 0 :print("Transpose = ", transpose)                                                                                #◈
                                                                                                                                            #◈
        self.fid1 = fid1  # this is necessary if we need to use the variables created here in other functions inside the class              #◈
        #◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈fid1 Done◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
        #◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
        #◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈Parse variable◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
        # Get the list of available data: we wanna use this only to warn the user if a data they requested wasn't available.                #◈
        # If they request for the equil variables: make sure equil_feed is provided.                                                        #◈
        # We take in variable both as string and list. If it's a string, it can be either a single quantity e.g. 'bx', a single expressi-   #◈
        # on e.g. 'bx*2', or a vector containing quantities and/or expressions e.g. '[rho0, bx*bx0]'. If it's a list, the elements of       #◈
        # the list can either be single quantities and/or expressions e.g. ['bx','rho0','bx*rho0'] which we will treat as vectors.          #◈
        # Algortithm: We can take care of the string case and if variable is a list, the first convert it to a string, preserving form.     #◈
                                                                                                                                            #◈
        # A fixed assumption we're making is that ',' is only used to separate requested quantities. Each member of the final string        #◈
        # needs to be checked if it's a formula or a single quantity: if formula, use formula_func_symbolic, if not read directly           #◈
        avail_varlist = list(hdf0.keys())                                                                                                   #◈
        hdf0.close()                                                                                                                        #◈
        if equil_feed != None:                                                                                                              #◈
            hdf_equil = h5py.File(self.equil_feed, 'r')                                                                                     #◈
            avail_equillist = [(key+'0') for key in hdf_equil.keys()]                                                                       #◈
            if 'e0' in avail_equillist:                                                                                                     #◈
                avail_equillist.remove('e0')                                                                                                #◈
                avail_equillist.append('etot0')                                                                                             #◈
        else: avail_equillist = ['bx0', 'by0', 'bz0', 'etot0', 'eint0', 'pe0', 'pelectron0', 'pml_b0', 'pml_t0', 'qtot0', 'rho0', 'te0']    #◈
        vector_checklist = [']','[']                                                                                                        #◈
        formula_checklist = ['*','/','-','+','^','sqrt','(',')']                                                                            #◈
                                                                                                                                            #◈
        # Use while to loop back to the case with variable being a string in case the input variable is a list: this way, we'll only        #◈
        # have to deal with strings!                                                                                                        #◈
        while True:                                                                                                                         #◈
            # If variable is string: We handle everything about "variable" in this case!                                                    #◈
            if isinstance(self.variable, str):                                                                                              #◈
                # strip out of spaces                                                                                                       #◈
                self.variable = self.variable.replace(" ","")                                                                               #◈
                # Handle the equil cases: we wanna store the equil quantities in ss appending a '0' to their original keys                  #◈
                equil_list = []                                                                                                             #◈
                for mem in avail_equillist:                                                                                                 #◈
                    if mem in self.variable: equil_list.append(mem)                                                                         #◈
                # Remove the 0 from equil_list to make it ready to be passed for data reading                                               #◈
                if len(equil_list) != 0: equil_list = [mem.replace("0","") for mem in equil_list]                                           #◈
                if self.quiet == 0 :print("equil_list = ", equil_list)                                                                      #◈
                                                                                                                                            #◈
                # If there are no equil vars to be read                                                                                     #◈
                equil_cond = True                                                                                                           #◈
                if len(equil_list) == 0:                                                                                                    #◈
                    equil_cond = False                                                                                                      #◈
                    pass                                                                                                                    #◈
                # If there are equil vars to be read                                                                                        #◈
                elif self.equil_feed == None:                                                                                               #◈
                    print("The equilibrium file is not supplied!")                                                                          #◈
                    self.equil_feed = inp_h5_file(word="equilibrium", var=self.equil_feed)                                                  #◈
                else:                                                                                                                       #◈
                    pass                                                                                                                    #◈
                # From here on out we assume there are either no equil arguments or in case they do, we know their keys                     #◈
                # Read and save equil data if needed                                                                                        #◈
                equil_ss = {}                                                                                                               #◈
                if equil_cond:                                                                                                              #◈
                    if self.quiet == 0: print("Reading required equilibrium data provided in:", self.equil_feed)                            #◈
                    for mem in equil_list:                                                                                                  #◈
                        memtmp = mem                                                                                                        #◈
                        if mem == 'etot': memtmp = 'e'                                                                                      #◈
                        if self.quiet == 0:print("Reading "+mem+"0 ...")                                                                    #◈
                        equil_ss[mem+'0'] = readAquantity(self.equil_feed, hdf_equil, memtmp, hdf_equil.keys(), transpose,1, minmax_crop)   #◈
                    hdf_equil.close()                                                                                                       #◈
                else:                                                                                                                       #◈
                    pass                                                                                                                    #◈
                                                                                                                                            #◈
                contain_brackets = all([mem in self.variable for mem in vector_checklist])                                                  #◈
                contain_comma = ',' in self.variable                                                                                        #◈
                tobe_readlist = []                                                                                                          #◈
                # Handling the case variable_type = vector                                                                                  #◈
                # How do you wanna handle multicomponent variables containing formulae?                                                     #◈
                # We want the final ss to contain all the keys in variable and nothing more!                                                #◈
                # Let's create a list of components of variable and handle the formulas and                                                 #◈
                # quantities as two different conditions when reaeding the data in next step                                                #◈
                if contain_brackets:                                                                                                        #◈
                    tobe_readlist = remove_charbychar(self.variable,'[]')                                                                   #◈
                    if contain_comma: # Vector                                                                                              #◈
                        tobe_readlist = tobe_readlist.split(",")                                                                            #◈
                    else: # Bracketed single variable: Remember we already got rid of the brackets                                          #◈
                        tobe_readlist = [tobe_readlist] # Must be a list since we are going to loop over tobe_readlist                      #◈
                elif contain_comma:                                                                                                         #◈
                    raise TypeError("Comma ',' detected in a single-component variable! Embrace with square brackets for vectors!\n"        #◈
                                   +"Example: '[rho0, bx*bx0]' or ['rho0', 'bx*bx0']")                                                      #◈
                else:                                                                                                                       #◈
                    tobe_readlist = [self.variable]     # Must be a list since we are going to loop over tobe_readlist                      #◈
                break                                                                                                                       #◈
                                                                                                                                            #◈
            # If variable is list: Merely convert to string and pass back to 1st case                                                       #◈
            elif isinstance(self.variable, list):                                                                                           #◈
                if all([isinstance(i,str) for i in self.variable]):                                                                         #◈
                    self.variable = str(self.variable)                                                                                      #◈
                    self.variable = self.variable.replace("'","")                                                                           #◈
            else:                                                                                                                           #◈
                raise TypeError("The input variable can only be a string, or a list of strings!")                                           #◈
                                                                                                                                            #◈
        # Find out which members in tobe_readlist are formulae: This is easily done with a dict but let's                                   #◈
        # do it with an accompanying list instead!                                                                                          #◈
        accompany_tobe_readlist_formula = []                                                                                                #◈
        accompany_tobe_readlist_equil = []                                                                                                  #◈
        for mem in tobe_readlist:                                                                                                           #◈
            if any([char in formula_checklist for char in mem]): accompany_tobe_readlist_formula.append(1)                                  #◈
            else: accompany_tobe_readlist_formula.append(0)                                                                                 #◈
            if any([equil_q in mem for equil_q in avail_equillist]): accompany_tobe_readlist_equil.append(1)                                #◈
            else: accompany_tobe_readlist_equil.append(0)                                                                                   #◈
        #◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈Parse variable Done◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
        #◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
        #◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈Recording data into ss◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈#◈
        if self.quiet == 0 : print('List of datasets to be read: \n', tobe_readlist)                                                        #◈
        ss = dict()                                                                                                                         #◈
        ss[0] = {}                                                                                                                          #◈
        i = 0                                                                                                                               #◈
        # If you want, you can add a while loop to allow for user mistakes and keyboard inputs!                                             #◈
        # Use the following function to read a single quantity available in a snapshot an get the data back                                 #◈
        # readAquantity(hdf_dir, hdf_file, quantity, keys_avail, my_transpose,quiet)                                                        #◈
        for snapshot_dir in fid1:                                                                                                           #◈
            # In each snapshot, try not to read the datasets already read in a previous step! Store them in a provisional dic               #◈
            # that is replaced everytime a loop in the outersmost for loop is completed.                                                    #◈
            snapshot_h5 = h5py.File(snapshot_dir,'r')                                                                                       #◈
            keys = list(snapshot_h5.keys())                                                                                                 #◈
            item_inx = 0                                                                                                                    #◈
            item_dic = {}                                                                                                                   #◈
            for item in tobe_readlist:                                                                                                      #◈
                # Check if item is whether a formula or a single expression                                                                 #◈
                temp = dict()                                                                                                               #◈
                if accompany_tobe_readlist_formula[item_inx]:                                                                               #◈
                    # item is formula: call formula_func_symbolic() to handle                                                               #◈
                    # first get the list of ingredients and write into tobe_readlist_item                                                   #◈
                    # then loop over tobe_readlist_item and generate a provisional ss_item                                                  #◈
                    # to pass to formula_func_symbolic() and get back the final ss dic for item                                             #◈ 
                    readlist_item_equil, readlist_item_nonequil= get_tobe_readlist_item(item, avail_equillist, keys)                        #◈
                    # No need to check if the list is empty. Python ignores empty lists in a loop                                           #◈
                    for jtem in readlist_item_nonequil:                                                                                     #◈
                        if jtem not in item_dic.keys():                                                                                     #◈
                            item_dic[jtem]=readAquantity(snapshot_dir,snapshot_h5,jtem,keys,transpose,self.quiet,minmax_crop)               #◈                              
                    for jtem in readlist_item_equil:                                                                                        #◈
                        if jtem not in item_dic.keys(): item_dic[jtem] = equil_ss[jtem]                                                     #◈
                    temp = formula_func_symbolic(dict(item_dic), item)                                                                      #◈
                # If not a formula but contains equil quantities                                                                            #◈
                elif accompany_tobe_readlist_equil[item_inx]:                                                                               #◈
                    # item is just an equil quantity                                                                                        #◈
                    temp[item] = equil_ss[item]                                                                                             #◈
                else:                                                                                                                       #◈
                    # item is just a quantity in snapshot                                                                                   #◈
                    if item not in item_dic.keys():                                                                                         #◈
                        temp[item] = readAquantity(snapshot_dir,snapshot_h5,item,keys,transpose,self.quiet,minmax_crop)                     #◈
                    else:                                                                                                                   #◈
                        temp[item] = item_dic[item]                                                                                         #◈
                                                                                                                                            #◈
                item_inx += 1                                                                                                               #◈
                if len(temp) > 0:                                                                                                           #◈ 
                    tempkey = list(temp.keys())[0]                                                                                          #◈
                    ss[i][tempkey] = temp[tempkey]                                                                                          #◈
                else:                                                                                                                       #◈
                    print("*****************************Warning*****************************\n"+                                            #◈
                          item+" could not be read form "+snapshot_dir+"! Make sure all the quantities"+                                    #◈
                          " in your requested expression exist in the file!")                                                               #◈
            i += 1                                                                                                                          #◈
            if i < len(fid1): ss[i] = {}                                                                                                    #◈
                                                                                                                                            #◈
        # Take care of the timelist                                                                                                         #◈
        timelist = []                                                                                                                       #◈
        if dt != -1: timelist = find_timelist(fid1,self.dt)                                                                                 #◈
        if self.direct_timelist != None: timelist = self.direct_timelist                                                                    #◈
                                                                                                                                            #◈
        sskeys = list(ss[0].keys())                                                                                                         #◈
                                                                                                                                            #◈
        #raise OSError("Done!")                                                                                                             #◈
        # this is necessary if we need to use the variables created here in other functions inside the class                                #◈
        self.ss            = ss                                                                                                             #◈
        self.sskeys        = sskeys                                                                                                         #◈
        self.timelist      = timelist                                                                                                       #◈
        self.meta_original = meta_original                                                                                                  #◈
        self.meta_cropped  = meta_cropped                                                                                                   #◈
        self.transpose     = transpose                                                                                                      #◈
        if self.quiet == 0 : print("Number of data files = ", len(self.fid1))                                                               #◈
#                                            ◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈                                                                             #◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈        END       ◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈#◈
#                                            ◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈                                                                          
                                                                                                                                         
    def read(self):
        return self.ss
    
    def metadata(self):                       # using a function's head identical to a var's name present in the same
        return self.meta_cropped              # namespace, i.e., within a class, would cause a namespace conflict
    
    def updated_crop(self):
        return self.crop
        
    def metadata_original(self): 
        return self.meta_original 
    
    def timelist(self):
        return self.timelist

    def keys(self):
        return self.sskeys
        
    def numfile(self):
        return len(self.fid1)
        
    def transpose(self):
        return self.transpose
    
    def contour(self, numfig, frames, var, axes, point, rand=None, direc=os.getcwd(), varlbl = None, hidden = 0, maxminCoef = 1):
        self.n = numfig
        self.f = frames
        self.var = var
        self.axes = axes
        self.point = point
        self.rand = rand
        if self.rand == None:
            self.rand = 1
        
        if varlbl == None: varlbl = var
        x = self.meta_cropped['axes'][0]
        y = self.meta_cropped['axes'][1]
        z = self.meta_cropped['axes'][2]
        
        axes_list = ['xy','xz', 'yz']
        colormap = 'seismic'
        #print("Enter the pair of axes from the list below, based on which you want to plot the contours:\n",axes_list, "\n")
        #axes = input()
        dic = {}
        self.axes = inp(self.axes, axes_list)
        if self.axes == 'xy':
            axislst  = [x,y]
            pntDelta = self.meta_cropped['d'][2]
            label    = ['x (m)','y (m)', "Data sliced at z = "+str(round(pntDelta*self.point/1.e6 ,2))+" Mm"]
            for item in self.ss.keys():
                dic[item] = np.transpose(self.ss[item][self.var][:,:,self.point])
        elif self.axes == 'xz':
            axislst  = [x,z]
            pntDelta = self.meta_cropped['d'][1]
            label    = ['x (m)','z (m)', "Data sliced at y = "+str(round(pntDelta*self.point/1.e6 ,2))+" Mm"]
            for item in self.ss.keys():
                dic[item] = np.transpose(self.ss[item][self.var][:,self.point,:])
        else:
            axislst  = [y,z]
            pntDelta = self.meta_cropped['d'][0]
            label    = ['y (m)','z (m)', "Data sliced at x = "+str(round(pntDelta*self.point/1.e6 ,2))+" Mm"]
            for item in self.ss.keys():
                dic[item] = np.transpose(self.ss[item][self.var][self.point,:,:])
        fig = {} 
        if self.quiet == 0 :print("Number of data files = ", len(self.fid1))
        if len(self.fid1) > 2 and self.n * self.f > 2:
            rmnder = self.n * self.f - len(self.fid1)
            while rmnder > 0:
                self.n = self.n - 1
                rmnder = self.n * self.f - len(self.fid1)
            print("Remainder = ", rmnder)
            print("self.n = ", self.n)
            for count in range(self.n):
                if self.f % 2 == 0:
                    fig, axs = plt.subplots(int(self.f/2), 2, figsize=(20, 12), dpi=80, facecolor='w', edgecolor='k',squeeze=False)
                    axs[int(self.f/2)-1, 0].set_xlabel(label[0])
                else:
                    fig, axs = plt.subplots(int(self.f/2)+1, 2, figsize=(20, 12), dpi=80, facecolor='w', edgecolor='k',squeeze=False)
                    axs[int(self.f/2), 0].set_xlabel(label[0])
                    axs[int(self.f/2),1].set_visible(False)
                axs[int(self.f/2)-1, 1].set_xlabel(label[0])
                fig.text(.5, .05, label[2], ha='center', fontsize=20)
                for i in range(self.f):
                    print(i)
                    if i % 2 == 0:
                        pcm = axs[int(i/2), 0].contourf(axislst[0], axislst[1], dic[i + count*self.f][:,:], cmap=colormap)
                        axs[int(i/2), 0].set_title("t = "+str((self.timelist[i] + count*self.f)))
                        axs[int(i/2), 0].set_ylabel(label[1])
                        cbar = fig.colorbar(pcm, ax = axs[int(i/2), 0])
                        cbar.ax.set_ylabel(self.var)
                    else:
                        pcm = axs[int(i/2), 1].contourf(axislst[0], axislst[1], dic[i + count*self.f][:,:], cmap=colormap)
                        axs[int(i/2), 1].set_title("t = "+str(self.timelist[i] + count*self.f))
                        axs[int(i/2), 1].set_ylabel(label[1])
                        cbar = fig.colorbar(pcm, ax = axs[int(i/2), 1])
                        cbar.ax.set_ylabel(self.var)
                    save_fig(fig,varlbl,count,self.rand)
                if self.f % 2 != 0:
                    for l in axs[int(i/2)-1,1].get_xaxis().get_majorticklabels():
                        l.set_visible(True)
                    fig.delaxes(axs[int(i/2), 1])
            if rmnder < 0:
                rmnder = abs(rmnder)
                print(rmnder)
                if rmnder > 2:
                    if rmnder % 2 == 0:
                        fig, axs_rmnder = plt.subplots(int(rmnder/2), 2, figsize=(20, 12), dpi=80, facecolor='w', edgecolor='k',squeeze=False)
                        axs_rmnder[int(rmnder/2)-1, 0].set_xlabel(label[0])
                    else:
                        fig, axs_rmnder = plt.subplots(int(rmnder/2) + 1, 2, figsize=(20, 12), dpi=80, facecolor='w', edgecolor='k',squeeze=False)
                        axs_rmnder[int(rmnder/2), 0].set_xlabel(label[0])
                        axs_rmnder[int(rmnder/2),1].set_visible(False)
                    axs_rmnder[int(rmnder/2)-1, 1].set_xlabel(label[0])
                    fig.text(.5, .05, label[2], ha='center', fontsize=20)
                    for i in range(rmnder):
                        if i % 2 == 0:
                            pcm = axs_rmnder[int(i/2), 0].contourf(axislst[0], axislst[1], dic[len(dic.keys()) - rmnder + i][:,:], cmap=colormap)
                            axs_rmnder[int(i/2), 0].set_title("t = "+str(self.timelist[-rmnder + i]))
                            axs_rmnder[int(i/2), 0].set_ylabel(label[1])
                            cbar = fig.colorbar(pcm, ax = axs_rmnder[int(i/2), 0])
                            cbar.ax.set_ylabel(self.var)
                        else:
                            pcm = axs_rmnder[int(i/2), 1].contourf(axislst[0], axislst[1], dic[len(dic.keys()) - rmnder + i][:,:], cmap=colormap)
                            axs_rmnder[int(i/2), 1].set_title("t = "+str(self.timelist[-rmnder + i]))
                            axs_rmnder[int(i/2), 1].set_ylabel(label[1])
                            cbar = fig.colorbar(pcm, ax = axs_rmnder[int(i/2), 1])
                            cbar.ax.set_ylabel(self.var)
                    save_fig(fig,varlbl,i,self.rand,"_last")
                else:
                    axs_rmnder = {}
                    fig, axs_rmnder = plt.subplots(rmnder, 1, sharex=True, figsize=(20, 12), dpi=80, facecolor='w', edgecolor='k')
                    fig.text(.5, .05, label[2], ha='center', fontsize=20)
                    if rmnder == 1:
                        axs_rmnder = {0 : [axs_rmnder, axs_rmnder]}
                    else: 
                        axs_rmnder = {0 : axs_rmnder}
                    for i in range(rmnder):
                        pcm = axs_rmnder[0][i].contourf(axislst[0], axislst[1], dic[len(dic.keys()) - rmnder + i][:,:], cmap=colormap)
                        axs_rmnder[0][i].set_title("t = "+str(self.timelist[-rmnder + i]))
                        axs_rmnder[0][i].set_xlabel(label[0])
                        axs_rmnder[0][i].set_ylabel(label[1])
                        cbar = fig.colorbar(pcm, ax = axs_rmnder[0][i])
                        cbar.ax.set_ylabel(self.var)
                    save_fig(fig,varlbl,i,self.rand,"_last")
            #plt.show()
            
        # The case with only 2 files, hence two figures
        elif len(self.fid1) >= 2 and self.n * self.f == 2:
            fig, axs = plt.subplots(2, 1, sharex=True, figsize=(20, 12), dpi=80, facecolor='w', edgecolor='k')
            for i in range(2):
                pcm = axs[i].contourf(axislst[0], axislst[1], dic[i][:,:])
                axs[i].set_title("t = "+str(self.timelist[i]))
                axs[i].set_xlabel(label[0])
                axs[i].set_ylabel(label[1])
                cbar = fig.colorbar(pcm, ax = axs[i])
                cbar.ax.set_ylabel(self.var)
            save_fig(fig,varlbl,i,self.rand)
            #plt.show()
            
        # The case with only 1 files, hence two figures
        else:
            fig, axs = plt.subplots(1, 1, sharex=True, figsize=(20, 12), dpi=150, facecolor='w', edgecolor='k')
            pntLbl   = 'xyz'.replace(self.axes[0],'').replace(self.axes[1],'')
            maxi = np.max(dic[0][:,:]) * maxminCoef
            mini = np.min(dic[0][:,:]) * maxminCoef
            colorMap = cMapRYWCB(dic[0][:,:], vRange=[mini,maxi],\
                               whitePerCent=5.,nColors=5000,\
                               colorFrac=[0.4,0.1,0.1,0.4])
            pcm = axs.pcolormesh(axislst[0],axislst[1], dic[0][:,:],vmin=mini,vmax=maxi,cmap=colorMap, shading='gouraud')
            axs.set_xlabel(label[0], fontsize=axisFontSize)
            axs.xaxis.set_tick_params(labelsize=tickSize)
            plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
            axs.xaxis.get_offset_text().set_fontsize(tickSize)     # This adjusts fontsize of the scientific notation
            
            axs.set_ylabel(label[1], fontsize=axisFontSize)
            axs.yaxis.set_tick_params(labelsize=tickSize)
            axs.set_title("t = "+str(round(self.timelist[0], 1)), fontsize = axisFontSize)
            plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
            axs.yaxis.get_offset_text().set_fontsize(tickSize)     # This adjusts fontsize of the scientific notation
            
            cbar = fig.colorbar(pcm, ax = axs)
            cbar.ax.set_ylabel(self.var, fontsize=axisFontSize)
            cbar.ax.tick_params(labelsize=tickSize) 
            figSize = fig.get_size_inches()*fig.dpi
            axs.annotate(label[2], xy=(0.5, 0.94), xytext=(0, 10), \
                                                        xycoords=('axes fraction', 'figure fraction'), \
                                                        textcoords='offset points',size=titleFontSize, ha='center', va='bottom', rotation=0)
            if hidden != -1: pngfilename = direc+"contour_"+varlbl+"_"+self.axes+"="+str(self.point)+"_time="+str(int(self.timelist[0]))+".png"
            else: pngfilename = direc+".contour_"+varlbl+"_"+self.axes+"="+str(self.point)+"_time="+str(int(self.timelist[0]))+".png"
            fig.savefig(pngfilename)
            #save_fig(fig,comp,1,self.rand)
            #plt.show()
# fig.savefig(direc+"quiver_"+vec[0]+"_"+vec[1]+"_"+point['name']+"="+str(point['val'])+"_time="+str(t*10)+".png")
# def quiver(obj, vec, axis, skipnum, point=None, lim=None, direc = os.getcwd()):
# contour(self, numfig, frames, comp, axes, point, rand=None, direc=os.getcwd()):
#d = {}
#d[0] = {'bx':np.array([[1,2,3],[4,5,6]]), 'by':np.array([[10,11,12],[13,14,15]])}
#d[1] = {'bx':np.array([[11,12,13],[14,15,16]]), 'by':np.array([[110,111,112],[113,114,115]])}

#with open('therm.pkl', 'wb') as output:
#    pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
#with open('b.pkl', 'rb') as input:
#    obj = pickle.load(input)


# Deprecated:
#def find_rng(my_fid,dt):                                                                                                                 #◈
#    l=len(".h5")                                                                                                                         #◈
#    i = 0                                                                                                                                #◈
#    out=[]                                                                                                                               #◈
#    if not isinstance(my_fid, str):                                                                                                      #◈
#        for item in my_fid:                                                                                                              #◈
#            while 1:                                                                                                                     #◈
#                try:                                                                                                                     #◈
#                    num = int(item[-l - i - 1:-l - i])                                                                                   #◈
#                    try:                                                                                                                 #◈
#                        num = int(item[-l - i - 4:-l - i])                                                                               #◈
#                        break                                                                                                            #◈
#                    except:                                                                                                              #◈
#                        pass                                                                                                             #◈
#                except:                                                                                                                  #◈
#                    i+=1                                                                                                                 #◈
#            if num in [0,1]:                                                                                                             #◈
#                out.append(0)                                                                                                            #◈
#            else:                                                                                                                        #◈
#                out.append((num-1) * dt)                                                                                                 #◈
#    else:                                                                                                                                #◈
#        while 1:                                                                                                                         #◈
#            try:                                                                                                                         #◈
#                num = int(my_fid[-l - i - 1:-l - i])                                                                                     #◈
#                try:                                                                                                                     #◈
#                    num = int(my_fid[-l - i - 4:-l - i])                                                                                 #◈
#                    break                                                                                                                #◈
#                except:                                                                                                                  #◈
#                    pass                                                                                                                 #◈
#            except:                                                                                                                      #◈
#                i+=1                                                                                                                     #◈
#        if num in [0,1]:                                                                                                                 #◈
#            out.append(0)                                                                                                                #◈
#        else:                                                                                                                            #◈
#            out.append((num-1) * dt)                                                                                                     #◈
#    return out                                                                                                                           #◈

#def print_max_min(fid1, timelist, switch, func, comp, supress=None):                                                                          #◈
#    M = 0                                                                                                                                #◈
#    try:                                                                                                                                 #◈
#        if switch == 'max':                                                                                                              #◈
#            for i in range(len(fid1)):                                                                                                   #◈
#                if M < np.max(func[i][comp]):                                                                                            #◈
#                    M = np.max(func[i][comp])                                                                                            #◈
#                if supress=='p':                                                                                                         #◈
#                    print("t = "+str(timelist[i])+" ---> "+"max("+comp+") = "+str(np.max(func[i][comp]))                                      #◈
#                    + " ---> at ("+str(np.where(func[i][comp] == np.max(func[i][comp]))[0][0])+", "                                      #◈
#                    + str(np.where(func[i][comp] == np.max(func[i][comp]))[1][0])+", "                                                   #◈
#                    + str(np.where(func[i][comp] == np.max(func[i][comp]))[2][0])+")")                                                   #◈
#        elif switch == 'min':                                                                                                            #◈
#            for i in range(len(fid1)):                                                                                                   #◈
#                if M > np.min(func[i][comp]):                                                                                            #◈
#                    M = np.min(func[i][comp])                                                                                            #◈
#                if supress=='p':                                                                                                         #◈
#                    print("t = "+str(timelist[i])+" ---> "+"min("+comp+") = "+str(np.min(func[i][comp]))                                 #◈
#                    + " ---> at ("+str(np.where(func[i][comp] == np.min(func[i][comp]))[0][0])+", "                                      #◈
#                    + str(np.where(func[i][comp] == np.min(func[i][comp]))[1][0])+", "                                                   #◈
#                    + str(np.where(func[i][comp] == np.min(func[i][comp]))[2][0])+")")                                                   #◈
#        elif switch == 'avg':                                                                                                            #◈
#            for i in range(len(fid1)):                                                                                                   #◈
#                where = np.where(abs(func[i][comp] - np.average(func[i][comp])*func[i][comp]/func[i][comp])                              #◈
#                == np.min(abs(func[i][comp] - np.average(func[i][comp])*func[i][comp]/func[i][comp])))                                   #◈
#                if str(where)[7:9] == '[]':                                                                                              #◈
#                    where = [[0],[0],[0]]                                                                                                #◈
#                print("t = "+str(timelist[i])+" ---> "+"average("+comp+") = "+str(np.average(func[i][comp]))                             #◈
#                + " ---> at ("+str(where[0][0])+", "+ str(where[1][0])+", "+ str(where[2][0])+")")                                       #◈
#    except:                                                                                                                              #◈
#        pass                                                                                                                             #◈
#                                                                                                                                         #◈
#    return M                                                                                                                             #◈

  # def mod_b(self):
        # if vec_avail(list(self.ss[0].keys()), ['bx','by','bz']):
            # mod_b = {}
            # for i in range(len(self.ss.keys())):
                # mod_b[i] = {'mod_b':np.sqrt(self.ss[i]['bx']*self.ss[i]['bx'] + self.ss[i]['by']*self.ss[i]['by'] + self.ss[i]['bz']*self.ss[i]['bz'])}
            # return mod_b
        # else:
            # print("Error: Not all 3 magnetic field components are read from the data!")
        
    
    # def mod_v(self):
        # if vec_avail(list(self.ss[0].keys()), ['vx','vy','vz']):
            # mod_v = {}
            # for i in range(len(self.ss.keys())):
                # mod_v[i] = {'mod_v':np.sqrt(self.ss[i]['vx']*self.ss[i]['vx'] + self.ss[i]['vy']*self.ss[i]['vy'] + self.ss[i]['vz']*self.ss[i]['vz'])}
            # return mod_v
        # else:
            # print("Error: Not all 3 velocity field components are read from the data!")

    # def max(self, comp, supress=None):
        # M = 0
        # self.comp = comp
        # self.comp = inp(self.comp, self.variable + ['mod_b', 'mod_v'])
        # self.supress = supress
        # if self.comp == 'mod_b':
            # M = print_max_min(self.fid1, self.rng, 'max', self.mod_b(), self.comp, self.supress)
        # elif self.comp == 'mod_v':
            # M = print_max_min(self.fid1, self.rng, 'max', self.mod_v(), self.comp, self.supress)
        # else:
            # M = print_max_min(self.fid1, self.rng, 'max', self.ss, self.comp, self.supress)
        # return M
            # #self.rng[i] - 1 because tube*0001.h5 corresponds to t = 0
            
    # def min(self, comp, supress=None):
        # M = 0
        # self.comp = comp
        # self.comp = inp(self.comp, self.variable + ['mod_b', 'mod_v'])
        # self.supress = supress
        # if self.comp == 'mod_b':
            # M = print_max_min(self.fid1, self.rng, 'min', self.mod_b(), self.comp, self.supress)
        # elif self.comp == 'mod_v':
            # M = print_max_min(self.fid1, self.rng, 'min', self.mod_v(), self.comp, self.supress)
        # else:
            # M = print_max_min(self.fid1, self.rng, 'min', self.ss, self.comp, self.supress)
        # return M
    
    # def average(self, comp):
        # self.comp = comp
        # self.comp = inp(self.comp, self.variable + ['mod_b', 'mod_v'])
        # if self.comp == 'mod_b':
            # print_max_min(self.fid1, self.rng, 'avg', self.mod_b(), self.comp)
        # elif self.comp == 'mod_v':
            # print_max_min(self.fid1, self.rng, 'avg', self.mod_v(), self.comp)
        # else:
            # print_max_min(self.fid1, self.rng, 'avg', self.ss, self.comp)
