import numpy as np

def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    return all(n % i for i in range(3, int(np.sqrt(n)) + 1, 2))

class domainDecompose2D:
    def __init__(self, size, nx, ny):
        self.size = size
        self.nx   = nx
        self.ny   = ny
        
        # Parallel scheme
        tempx = []
        tempy = []
        if self.size**(1/2) - round(self.size**(1/2)) == 0.:
            nblockx = int(self.size**(1/2))
            nblocky = nblockx
        elif is_prime(self.size):
            nblockx = 1
            nblocky = self.size
        else:
            for i in range(1,self.size+1):
                if np.mod(self.size, i) == 0:
                    tempx.append(i)
                    tempy.append(int(self.size / i))
            nblockx = tempx[round(len(tempx)/2)]
            nblocky = tempy[round(len(tempx)/2)]
        
        if self.size != nblockx * nblocky:
            raise ValueError("The number of blocks don't match the number of procs!")
        
        # print(nblockx,nblocky,nblockz)
        del(tempx, tempy)
        
        stridex = int(self.nx/nblockx)
        stridey = int(self.ny/nblocky)
        
        lx = np.array([i*stridex for i in range(0,int(nblockx)+1)])
        ly = np.array([i*stridey for i in range(0,int(nblocky)+1)])
        lx[-1] = self.nx
        ly[-1] = self.ny
        
        nlx = np.array([i for i in range(0,int(nblockx)+1)])
        nly = np.array([i for i in range(0,int(nblocky)+1)])
        
        slx = []
        elx = []
        sly = []
        ely = []
        blcx = []
        blcy = []
        for i in range(nblockx):          
            for j in range(nblocky):              
                slx.append(lx[0:-1][i])
                elx.append(lx[1:][i])
                sly.append(ly[0:-1][j])
                ely.append(ly[1:][j])
                blcx.append(nlx[i])
                blcy.append(nly[j])
        
        self.nblock      = np.array([nblockx, nblocky])
        self.coordinates = np.array([blcx,blcy])
        self.slx         = slx
        self.elx         = elx
        self.sly         = sly
        self.ely         = ely