from required_pkgs import *

def partial(func, coord, grid):
    size = func.shape
    out = np.zeros(size)
    if len(size) == 1:
        #spl = interpolate.splrep(grid,func,k=3) # no smoothing, 3rd order spline
        spl = interpolate.splrep(grid,func)      # smoothing
        out = interpolate.splev(grid,spl,der=1)  # use those knots to get second derivative
    elif len(size) == 2:
        if coord == 'x':
            for i in range(size[1]):
                spl = interpolate.splrep(grid,func[:,i])
                out[:,i] = interpolate.splev(grid,spl,der=1)
        elif coord == 'y':
            for i in range(size[0]):
                spl = interpolate.splrep(grid,func[i,:])
                out[i,:] = interpolate.splev(grid,spl,der=1)
        else:
            for i in range(size[1]):
                spl = interpolate.splrep(grid,func[:,i])
                out[:,i] = interpolate.splev(grid,spl,der=1)
    #2.5D Sims with ny = 1 and array shape (nx, 1, nz)
    elif len(size) == 3 and size[1] == 1:
        if coord == 'x':
            for k in range(size[2]):
                spl = interpolate.splrep(grid,func[:,0,k]) 
                out[:,0,k] = interpolate.splev(grid,spl,der=1) 
        elif coord == 'y':
            out = 0.
        elif coord == 'z':
            for i in range(size[0]):
                spl = interpolate.splrep(grid,func[i,0,:])
                out[i,0,:] = interpolate.splev(grid,spl,der=1)
    elif len(size) == 3 and size[1] != 1:
        if coord == 'x':
            for i in range(size[1]):
                for j in range(size[2]):
                    spl = interpolate.splrep(grid,func[:,i,j]) 
                    out[:,i,j] = interpolate.splev(grid,spl,der=1) 
        elif coord == 'y':
            for i in range(size[0]):
                for j in range(size[2]):
                    spl = interpolate.splrep(grid,func[i,:,j])
                    out[i,:,j] = interpolate.splev(grid,spl,der=1)
        elif coord == 'z':
            for i in range(size[0]):
                for j in range(size[1]):
                    spl = interpolate.splrep(grid,func[i,j,:])
                    out[i,j,:] = interpolate.splev(grid,spl,der=1)
        else:
            print("ERROR: Something is not right!")
    else:
        print("Error: partial is not ready for functions with more than 3 variables!")
    return out


def deriv(y,x):
    n = len(x)
    deriv = np.zeros(n)
    
    #y' = y0(2x – x1 – x2)/(x01x02) – y1(2x – x0 – x2)/(x01x12) + y2(2x – x0 – x1)/(x02x12)
    #Given a discrete set of X locations and Y values, the DERIV function then computes the 
    #derivative at all of the X locations. For example, for all of the X locations (except 
    #the first and last points), the derivative y' is computed by substituting in x = x1:
    #y' = y0x12/(x01x02) + y1(1/x12 – 1/x01) – y2x01/(x02x12)
    # So each x[i] -->x1, hence y[i] --> y1, x[i+1] --> x1, x[i-1] --> x0
    for i in range(1, n-1):
        deriv[i] = y[i - 1]*(x[i] - x[i+1])/((x[i-1] - x[i])*(x[i-1] - x[i+1])) + \
                      y[i] * (1/(x[i] - x[i+1]) - 1/(x[i-1] - x[i]))               - \
                      y[i + 1]*(x[i-1] - x[i])/((x[i-1] - x[i+1])*(x[i] - x[i+1]))

    # At x=x0 (for the first point):
    #   y' = y0*(x01+x02)/(x01*x02) - y1*x02/(x01*x12) + y2*x01/(x02*x12)

    deriv[0] = y[0] * (2*x[0] - x[1]- x[2])/((x[0]-x[1])*(x[0]-x[2])) - \
                      y[1] * (x[0]-x[2])/((x[0]-x[1])*(x[1]-x[2]))           + \
                      y[2] * (x[0]-x[1])/((x[0]-x[2])*(x[1]-x[2]))


    # At x=x2 (for the last point):
    #   y' = -y0*x12/(x01*x02) + y1*x02/(x01*x12) - y2*(x02+x12)/(x02*x12)
    y0 = y[-3]
    x0 = x[-3]
    y1 = y[-2]
    x1 = x[-2]
    y2 = y[-1]
    x2 = x[-1]
    x01 = x0 - x1
    x02 = x0 - x2
    x12 = x1 - x2

    deriv[-1] = -y0*x12/(x01*x02) + y1*x02/(x01*x12) - y2*(x02+x12)/(x02*x12)

    return deriv

# x = np.arange(-2*np.pi,2*np.pi+np.pi/60,np.pi/60, 'float32') ; y = np.cos(x) ; dydx = -np.sin(x) ; 
# my_dydx = deriv(y,x) ; fig, axs = plt.subplots(1,1) ; axs.plot(dydx, 'r') ; axs.plot(my_dydx, 'b.') ; plt.show()

def partial_inefficient(func,coord, grid):
    size = func.shape
    out = np.zeros(size)
    if len(size) == 1:
        print("Warning: You can simply use \"deriv\"!")
        out = deriv(func,grid)
    elif len(size) == 2:
        if coord == 'x':
            for i in range(size[1]):
                out[:,i] = deriv(func[:,i], grid)
        elif coord == 'y':
            for i in range(size[0]):
                out[i,:] = deriv(func[i,:], grid)
        else:
            for i in range(size[1]):
                out[:,i] = deriv(func[:,i], grid)
    elif len(size) == 3:
        if coord == 'x':
            for i in range(size[1]):
                for j in range(size[2]):
                    out[:,i,j] = deriv(func[:,i,j], grid)
        elif coord == 'y':
            print("Calculating ... ")
            for i in range(size[0]):
                for j in range(size[2]):
                    out[i,:,j] = deriv(func[i,:,j], grid)
        elif coord == 'z':
            for i in range(size[0]):
                for j in range(size[1]):
                    out[i,j,:] = deriv(func[i,j,:], grid)
        else:
            print("ERROR: Something is not right!")
    else:
        print("Error: partial is not ready for functions with more than 3 variables!")
    return out


#compare with mathematica
# dx=0.2 ; dy=0.2 ; dz=0.1; xx = np.arange(-3, 7+dx,dx); yy = np.arange(-1, 3+dy,dy); 
# zz = np.arange(-1.6, 5+dz,dz);data = np.zeros([len(xx),len(yy),len(zz)]);
# for i in range(len(xx)):
    # for j in range(len(yy)):
        # for k in range(len(zz)):
            # data[i,j,k] = np.exp(-0.5 * xx[i]) * np.sin(yy[j]) * zz[k]**3
# a = {'x':partial(data,'x', xx), 'y':partial(data,'y', yy), 'z':partial(data,'z', zz)}
# [np.max(a[i]) for i in a]
# [np.min(a[i]) for i in a]
