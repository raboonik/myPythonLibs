from required_pkgs import *
#import numpy as np
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#import matplotlib
#import matplotlib.colors
#from matplotlib import ticker, cm
#import scipy.ndimag
#from read_vis import *

class nf(float):
    def __repr__(self):
        s = f'{self:.1f}'
        return f'{self:.0f}' if s[-1] == '0' else s

def if_point(pnt, axis, nxyz):
    if pnt == None:
        point = {'name': axis, 'val': myrandint(0,nxyz)}
    else:
        point = {'name': axis, 'val': pnt}
    return point

def inp(var, lst):
    while var not in lst:
            print("Error: the input must be one of the followings: \n")
            print(lst)
            var = input("Enter again:")
    return var


def mod_2dvec(my_ss,i,key1,key2):
    ampl = np.sqrt((my_ss[i][key1].real)**2 + (my_ss[i][key2].real)**2)
    return ampl

def quiver(obj, axis, skipnum = 2, point=None, direc = os.getcwd(), rank = 0,myveclbl=str(myrandint(0,10000)), hidden = 0):
    if direc[-1] != '/' : direc += '/'

    ss = obj.read()
    meta = obj.metadata()
    timelist = obj.timelist
    
    vec = []
    try:
        vec = list(ss[0].keys())
    except: pass
    
    if len(vec) == 0: raise TypeError("QUIVER: No data available! Double check the vector expression in you control file!")
    elif len(vec) == 1: 
        if rank == 0: print("QUIVER: Warning! The two components of the requested vector are the same!")
        vec = 2*vec
    elif len(vec) > 2: 
        if rank == 0: print("QUIVER: Warning! There are more than two components in the requested vector! Will plot the first two components!")
        vec = vec[0:2]
    else:
        pass
    
    d = list(meta['d'])                                                    
    nxyz = list(meta['n'])                                                 
    xyz = list(meta['axes'])
    axes_avail = ['xy','yx', 'xz','zx', 'yz','zy']
    axis = inp(axis, axes_avail)
    dic = {}
    if axis == 'xy' or axis == 'yx':
        axislbl = 'x-y'
        label = ['x (m)', 'y (m)']
        xyz1 = [xyz[0],xyz[1], d[2]]
        point = if_point(point, 'z', nxyz[2])
        for i in range(len(timelist)):
            dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][:,:,point['val']]), vec[1]:np.transpose(ss[i][vec[1]][:,:,point['val']])}
    elif axis == 'xz' or axis == 'zx':
        axislbl = 'x-z'
        label = ['x (m)', 'z (m)']
        point = if_point(point, 'y', nxyz[1])
        for i in range(len(timelist)):
            #if crop_nums == None:
            xyz1 = [xyz[0],xyz[2], d[1]]
            dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][:,point['val'],:]), vec[1]:np.transpose(ss[i][vec[1]][:,point['val'],:])}
            #else: 
            #    xyz1 = [xyz[0],xyz[2][crop_nums[0]:crop_nums[1]], d[1]]
            #    dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][:,point['val'],crop_nums[0]:crop_nums[1]]), vec[1]:np.transpose(ss[i][vec[1]][:,point['val'],crop_nums[0]:crop_nums[1]])}
    else:
        axislbl = 'y-z'
        label = ['y (m)', 'z (m)']
        point = if_point(point, 'x', nxyz[0])
        for i in range(len(timelist)):
            #if crop_nums == None:
            dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][point['val'],:,:]), vec[1]:np.transpose(ss[i][vec[1]][point['val'],:,:])}
            xyz1 = [xyz[1],xyz[2], d[0]]
            #else:
            #    xyz1 = [xyz[1],xyz[2][crop_nums[0]:crop_nums[1]], d[0]]
            #    dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][point['val'],:,crop_nums[0]:crop_nums[1]]), vec[1]:np.transpose(ss[i][vec[1]][point['val'],:,crop_nums[0]:crop_nums[1]])}
    meshx, meshy = np.meshgrid(xyz1[0],xyz1[1])
    #txt = "Vectorplot of "+(str(vec).replace("'",""))+" in "+axislbl+" plane at "+point['name']+" = "+str(round(point['val'] * xyz1[2]/1e6, 2))+"(Mm)"
    txt = "Data sliced at "+point['name']+" = "+str(round(point['val'] * xyz1[2]/1e6, 2))+"(Mm)"
    skip_pnt = (slice(None, None, skipnum), slice(None, None, skipnum))
    counter = 0
    for t in timelist:
        fig = plt.figure(figsize=(20, 12), dpi=150, facecolor='w', edgecolor='k')
        #fig.text(.5, .03, txt, ha='center', fontsize=16)  # increase 1st number to shift to left and increase the snd number to shift upwards 
        ax = fig.add_subplot(111)
        ax.xaxis.set_tick_params(labelsize=tickSize)
        ax.yaxis.set_tick_params(labelsize=tickSize)
        #plt1 = ax.quiver(xyz[0], xyz[1], dic[counter][vec[0]], dic[counter][vec[1]])
        mod = mod_2dvec(dic,counter,vec[0],vec[1])[skip_pnt]
        read_partx = dic[counter][vec[0]][skip_pnt]
        read_party = dic[counter][vec[1]][skip_pnt]
        size = [i for i in read_partx.shape]
        if any(np.reshape(np.iscomplex(read_partx),size[0]*size[1])): 
            print("*WARNING: Complex numbers detected! Quiver will proceed and plot the real part!")
        read_partx1 = read_partx.real
        if any(np.reshape(np.iscomplex(read_party),size[0]*size[1])): 
            print("*WARNING: Complex numbers detected! Quiver will proceed and plot the real part!")
        read_party1 = read_party.real
        plt1 = ax.quiver(meshx[skip_pnt], meshy[skip_pnt], read_partx1, read_party1, mod, cmap=plt.cm.jet)
        cbar = plt.colorbar(plt1, cmap=plt.cm.jet)
        cbar.ax.set_ylabel("mod(vec)", fontsize = axisFontSize)
        cbar.ax.tick_params(labelsize=tickSize) 
        ax.set_title("t = "+str(round(t, 1)), fontsize = titleFontSize)
        ax.set_xlabel(label[0], fontsize=axisFontSize)
        ax.set_ylabel(label[1], fontsize=axisFontSize)
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        ax.xaxis.get_offset_text().set_fontsize(tickSize)     # This adjusts fontsize of the scientific notation
        ax.yaxis.get_offset_text().set_fontsize(tickSize)     # This adjusts fontsize of the scientific notation
        ax.annotate(txt, xy=(0.5, 0.94), xytext=(0, 10), \
                                                        xycoords=('axes fraction', 'figure fraction'), \
                                                        textcoords='offset points',size=titleFontSize, ha='center', va='bottom', rotation=0)
        if hidden != -1: pngfilename = direc+"quiver_"+myveclbl+"_"+axis+"="+str(point['val'])+"_time="+str(int(t))+".png"
        else: pngfilename = direc+".quiver_"+myveclbl+"_"+axis+"="+str(point['val'])+"_time="+str(int(t))+".png"
        fig.savefig(pngfilename)
        plt.close()
        counter = counter + 1

global titleFontSize
titleFontSize = 24

global axisFontSize
axisFontSize  = 20

global tickSize 
tickSize = 16

def stream(raw_feed, vector_var, axis, feedlist=None, feed_range=None, skipnum = 2, point=None, crop_nums=None, direc = os.getcwd(), dt = 10, equil_feed=None, dens = 2):
    if direc[-1] != '/' : direc += '/'
    # Break down vector_var into components
    # strip of brackets and spaces
    vector_var = (vector_var.replace(" ",""))[1:-1]
    # Find comp1 and comp2
    comp1 = vector_var[:vector_var.index(",")]
    comp2 = vector_var[vector_var.index(",") + 1:]
    
                   #(raw_feed, variable, feedlist=None, feed_range=None, find_t = True, quiet=None, equil_feed=None, dt=10)
    obj1 = read_vis(raw_feed,comp1, feedlist, feed_range, quiet=1, equil_feed=equil_feed, dt=dt)
    ss1 = obj1.read()
    comp1 = list(ss1[list(ss1.keys())[0]].keys())[0]
    meta = obj1.metadata()
    timelist = obj1.rng
    del(obj1)
    obj2 = read_vis(raw_feed,comp2, feedlist, feed_range, quiet=1, equil_feed=equil_feed, dt=dt)
    ss2 = obj2.read()
    comp2 = list(ss2[list(ss2.keys())[0]].keys())[0]
    del(obj2)
    
    vec = [comp1, comp2]
    
    ss = {}
    for n in ss1.keys():
        ss[n] = {}
        ss[n][comp1] = ss1[n][comp1]
        ss[n][comp2] = ss2[n][comp2]
    del(ss1, ss2)
    
    d = list(meta['d'])                                                    
    nxyz = list(meta['n'])                                                 
    xyz = list(meta['axes'])
    axes_avail = ['xy','yx', 'xz','zx', 'yz','zy']
    axis = inp(axis, axes_avail)
    dic = {}
    if axis == 'xy' or axis == 'yx':
        axis = 'x-y'
        label = ['x (m)', 'y (m)']
        xyz1 = [xyz[0],xyz[1], d[2]]
        point = if_point(point, 'z', nxyz[2])
        for i in range(len(timelist)):
            dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][:,:,point['val']]), vec[1]:np.transpose(ss[i][vec[1]][:,:,point['val']])}
    elif axis == 'xz' or axis == 'zx':
        axis = 'x-z'
        label = ['x (m)', 'z (m)']
        point = if_point(point, 'y', nxyz[1])
        for i in range(len(timelist)):
            if crop_nums == None:
                xyz1 = [xyz[0],xyz[2], d[1]]
                dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][:,point['val'],:]), vec[1]:np.transpose(ss[i][vec[1]][:,point['val'],:])}
            else: 
                xyz1 = [xyz[0],xyz[2][crop_nums[0]:crop_nums[1]], d[1]]
                dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][:,point['val'],crop_nums[0]:crop_nums[1]]), vec[1]:np.transpose(ss[i][vec[1]][:,point['val'],crop_nums[0]:crop_nums[1]])}
    else:
        axis = 'y-z'
        label = ['y (m)', 'z (m)']
        point = if_point(point, 'x', nxyz[0])
        for i in range(len(timelist)):
            if crop_nums == None:
                dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][point['val'],:,:]), vec[1]:np.transpose(ss[i][vec[1]][point['val'],:,:])}
                xyz1 = [xyz[1],xyz[2], d[0]]
            else:
                xyz1 = [xyz[1],xyz[2][crop_nums[0]:crop_nums[1]], d[0]]
                dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][point['val'],:,crop_nums[0]:crop_nums[1]]), vec[1]:np.transpose(ss[i][vec[1]][point['val'],:,crop_nums[0]:crop_nums[1]])}
    meshx, meshy = np.meshgrid(xyz1[0],xyz1[1])
    txt = "Streamplot of ["+vector_var+"] in "+axis+" plane at "+point['name']+" = "+str(point['val'] * xyz1[2]/1e6)+"(Mm)"
    skip_pnt = (slice(None, None, skipnum), slice(None, None, skipnum))
    counter = 0
    for t in timelist:
        fig = plt.figure(figsize=(20, 12), dpi=80, facecolor='w', edgecolor='k')
        fig.text(.5, .03, txt, ha='center', fontsize=16)  # increase 1st number to shift to left and increase the snd number to shift upwards 
        ax = fig.add_subplot(111)
        #plt1 = ax.quiver(xyz[0], xyz[1], dic[counter][vec[0]], dic[counter][vec[1]])
        plt1 = ax.streamplot(meshx[skip_pnt], meshy[skip_pnt], dic[counter][vec[0]][skip_pnt], dic[counter][vec[1]][skip_pnt], density=dens)
        ax.set_title("t = "+str(t), fontsize = 16)
        ax.set_xlabel(label[0], fontsize=16)
        ax.set_ylabel(label[1], fontsize=16)
        #◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈unique_label◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
        unique_label = (vec[0]+"_"+vec[1])
        unique_label = [char for char in unique_label if char not in ['/','*','+','-','^','(',')','.']]
        unique_label = "".join(unique_label)
        #◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈Done◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
        fig.savefig(direc+"stream_"+unique_label+"_"+point['name']+"="+str(point['val'])+"_time="+str(int(t))+".png")
        print(direc+"stream_"+unique_label+"_"+point['name']+"="+str(point['val'])+"_time="+str(t)+".png")
        plt.close()
        counter = counter + 1

def stream_backup(obj, vec, axis, dens, point = None):
    ss = obj.read()
    vec = rv.inp(vec, ['v','b'])
    if vec == 'v' and rv.vec_avail(list(ss[0].keys()), ['vx','vy','vz']):
        cond = True
        vec = ['vx','vy','vz']
        vecname = 'velocity'
    elif vec == 'b' and rv.vec_avail(list(ss[0].keys()), ['bx','by','bz']):
        cond = True
        vec = ['bx','by','bz']
        vecname = 'magnetic field'
    else:
        del(ss)
        cond = False
        print("ERROR: Vector component(s) missing!")
        pass
        
    if cond:
        meta = obj.metadata()
        timelist = obj.rng
        d = list(meta['d'])                   
        nxyz = list(meta['n'])                                           
        xyz = list(meta['axes'])
        axes_avail = ['xy','yx', 'xz','zx', 'yz','zy']
        axis = rv.inp(axis, axes_avail)
        dic = {}
        if axis == 'xy' or axis == 'yx':
            axis = 'x-y'
            label = ['x (m)', 'y (m)']
            xyz = [xyz[0],xyz[1], d[2]]
            xyz = xyz[0],xyz[1]
            vec = [vec[0],vec[1]]
            point = if_point(point, 'z', nxyz[2])
            for i in range(len(timelist)):
                dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][:,:,point['val']]), vec[1]:np.transpose(ss[i][vec[1]][:,:,point['val']])}
        elif axis == 'xz' or axis == 'zx':
            axis = 'x-z'
            label = ['x (m)', 'z (m)']
            xyz = [xyz[0],xyz[2], d[1]]
            vec = [vec[0],vec[2]]
            point = if_point(point, 'y', nxyz[1])
            for i in range(len(timelist)):
                dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][:,point['val'],:]), vec[1]:np.transpose(ss[i][vec[1]][:,point['val'],:])}
        else:
            axis = 'y-z'
            label = ['y (m)', 'z (m)']
            xyz = [xyz[1],xyz[2], d[0]]
            vec = [vec[1],vec[2]]
            point = if_point(point, 'x', nxyz[0])
            for i in range(len(timelist)):
                dic[i] = {vec[0]:np.transpose(ss[i][vec[0]][point['val'],:,:]), vec[1]:np.transpose(ss[i][vec[1]][point['val'],:,:])}
        txt = "Streamplot of "+vecname+" in "+axis+" plane at "+point['name']+" = "+str(point['val'] * xyz[2]/1e6)+"(Mm)"
        counter = 0
        for t in timelist:
            fig = plt.figure(figsize=(20, 12), dpi=80, facecolor='w', edgecolor='k')
            fig.text(.5, .03, txt, ha='center', fontsize=16)  # increase 1st number to shift to left and increase the snd number to shift upwards 
            ax = fig.add_subplot(111)
            plt1 = ax.streamplot(xyz[0], xyz[1], dic[counter][vec[0]], dic[counter][vec[1]], density=dens)
            ax.set_title("t = "+str(t), fontsize = 16)
            ax.set_xlabel(label[0], fontsize=16)
            ax.set_ylabel(label[1], fontsize=16)
            fig.savefig("stream_"+vec[0]+"_"+vec[1]+"_"+point['name']+"="+str(point['val'])+"_time="+str(t*10)+".png")
            plt.close()
            counter = counter + 1

# HERE'S HOW WE CHOOSE SPECIFIC LEVELS FOR CONTOURS
def bnorm(obj, axes, point, connum, theta, lvlcoef, f=False):
    b0 = np.sqrt((10*np.sin(theta*np.pi/180.))**2 + (10*np.cos(theta*np.pi/180.))**2)* 10**-4
    ss = obj.read()
    ss = ss[0]
    n = obj.metadata()['n']
    for item in ['bx', 'by', 'bz', 'pe']:
        try:
            ss[item][0,0,0]
        except:
            raise Exception(item+" is not available!")
    b = np.sqrt(ss['bx']**2 + ss['by']**2 + ss['bz']**2)
    mu0=4.e-7*np.pi
    beta = 2*mu0*ss['pe'] / b**2
    #cond1 = beta < 7e-5
    #cond2 = beta > -7e-5
    #cond = (cond1==cond2)
    #idx = np.where(cond == True)
    fig, ax = plt.subplots(1,1)
    if axes == 'xy' or axes == 'yx':
        arr = np.transpose(b[:,:,point])
    elif axes == 'xz' or axes == 'zx':
        arr = np.transpose(b[:,point,:])
        betarr = np.transpose(beta[:,point,:])
    elif axes == 'yz' or axes == 'zy':
        arr = np.transpose(b[point,:,:])
        betarr = np.transpose(beta[point,:,:])
    else:
        raise Exception("Axes are not right!")
    print("min(b) = ", np.min(b), "     max(b) = ",np.max(b))
    levels = np.sort(list(set(arr[arr<b0+lvlcoef*np.min(arr)][arr[arr<b0+lvlcoef*np.min(arr)]>b0-lvlcoef*np.min(arr)])))
    print("levels = ", levels)
    levels = levels[int(len(levels)/2)]
    levels = np.sort(np.append(np.arange(np.min(arr),np.max(arr),(np.max(arr) - np.min(arr))/connum),levels))
    if f == True:
        pcm = ax.contourf(arr, levels=levels)
    else:
        pcm = ax.contour(arr, levels=levels)
    betaCM = ax.contour(betarr, levels = np.arange(0.5,2,0.5))
    betaCM.levels = [nf(val) for val in betaCM.levels]
    if plt.rcParams["text.usetex"]:
        fmt = r'%r'
    else:
        fmt = '%r'

    ax.clabel(betaCM, betaCM.levels, inline=True, fmt=fmt, fontsize=10)
    cbar = fig.colorbar(pcm, ax = ax)
    #yticks = np.arange(0,n[2],10)
    #ax.set_yticks(yticks)
    plt.show()
    
