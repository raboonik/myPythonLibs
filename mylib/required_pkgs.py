# pip3 install --target=/group/y94/ar1986/ scipy
# export PYTHONPATH=/group/y94/ar1986/

import sys
import os
# In the following 2 lines the 1 is the position we want to insert the new path entry into the existing list of paths recognized by python
sys.path.insert(1, os.path.expanduser('~')+'/synced_XPS_iMac/Python Codes/python_workplace/plot_parallel/lib')
sys.path.insert(1, '/home/abbas/projects/larexD/V4/2D/Lare2D_V4/SDF/utilities/pybuild/lib.linux-x86_64-3.10')
sys.path.insert(1, os.path.expanduser('~')+'/synced_XPS_iMac/Python Codes/python_workplace/larexd')
sys.path.insert(1, '/home/abbas/projects/larexD/Lucas/')

import h5py
import sdf
import numpy as np
import glob, os, subprocess   # subprocess for storing output of bash commands
from os import system as bash
from os import chdir as cd
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
import imageio 
import scipy as spy
from numpy import savetxt
from numpy import loadtxt
from scipy import interpolate as interpolate
from scipy.interpolate import splev, splrep
import imageio
from random import *
from datetime import datetime

global titleFontSize
titleFontSize = 30

global axisFontSize
axisFontSize  = 25

global tickSize 
tickSize = 20


# ~ plt.rc('text', usetex=True)
# ~ plt.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}\usepackage[T1]{fontenc}"
# ~ plt.rcParams["font.weight"] = "bold"
# ~ plt.rcParams["axes.labelweight"] = "bold"


# ~ rc = {"font.family" : "serif", 
      # ~ "mathtext.fontset" : "stix"}
# ~ plt.rcParams.update(rc)
# ~ plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

#plt.rc('font', family='serif', serif='cm10', weight='heavy')
#plt.rc('text', usetex=True)
#plt.rcParams['text.latex.preamble'] = r'\boldmath\renewcommand{\seriesdefault}{\bfdefault}\renewcommand{\seriesdefault}{bx}\renewcommand{\mddefault}{bx}\fontseries{bx}\selectfont'

# ~ matplotlib.rcParams['mathtext.fontset'] = 'stix'
# ~ matplotlib.rcParams['font.family'] = 'Times New Roman'
# ~ plt.rcParams["font.family"] = "Times New Roman"

#import pickle

def myrandint(min_bound,max_bound):
    now = datetime.now()
    seed(now.microsecond)
    return randint(min_bound,max_bound)

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    #p = str(p.stdout.read()[0:-1])
    #p = p[2:-1] + "/"
    if len(err) > 5:
        return 0
    else:
        return 1


def rs():
    for name in list(globals()):   # Delete Variables
        if not name.startswith('_'):
            del globals()[name]
    print('All global variables have been cleared!')
    import os
    exec(open(os.path.expanduser('~')+'/synced_XPS_iMac/Python Codes/python_workplace/plot_parallel/lib/required_pkgs.py').read(), globals())


def ls():
    bash("ls")

def pwd():
    bash("pwd")
    
def clear():
    bash("clear")


def ll():
    bash("ls -l")

def png():
    bash("rm *.png")
    
def fid(path):
    return sorted(glob.glob(path))

def q():
    exit()


from formula_symbolic_sin_asin import *
from time_evol import *
from colorbarKernel import *
from read_vis import *
from deriv import *
from domainDecompose3D import *
from domainDecompose2D import *
from domainDecompose1D import *