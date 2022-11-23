

print("Imported functions: cd, ls(), ll(), rs(), pwd(), clear(), system_call(cmd), fid(path), png(), q()")
if len(fid("tube*.h5")) != 0:
    print("\n **********************************h5 Files in the Directory*******"+\
    "***************************** \n" + str(fid("tube*.h5")) + "\n**************"+\
    "****************************************************************************"+\
    "******    Count = "+str(len(fid("tube*.h5"))))
sys.path.append('/home/rabo0001/python_workplace')
#sys.path.append('/home/iac64/iac64275/python_workplace')
#sys.path.append('/home/ar1986/python_workplace')

print("hdf = h5py.File(fid(\"\")[0],'r') \n "+\
      "\nobj = read_vis(raw_feed, variable, feedlist=None, feed_range=None, find_t = True, quiet=None, equil_feed=None, dt=10) \n\npixel_opt(obj, 'zt', nx,ny)"+
      "  \n\nfor i in range(20): \n  pixel_zt(obj,i) \n\nquiver(raw_feed, vector_var, axis, feedlist=None, feed_range=None, skipnum = 2, point=None, crop_nums=None, direc = os.getcwd(), dt = 10, equil_feed=None)")

