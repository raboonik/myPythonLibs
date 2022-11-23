import numpy as np

def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    return all(n % i for i in range(3, int(np.sqrt(n)) + 1, 2))

def is_second(n):
    if n % 2 == 0 and is_prime(n/2) and n > 4:
        return True
    else:
        return False 

class domainDecompose3D:
    def __init__(self, size, nx, ny, nz):
        self.size = size
        self.nx   = nx
        self.ny   = ny
        self.nz   = nz
        
        # Parallel scheme
        tempx = []
        tempy = []
        tempz = []
        if self.size**(1/3) - round(self.size**(1/3)) == 0.:
            nblockx = int(self.size**(1/3))
            nblocky = nblockx
            nblockz = nblockx
        elif is_prime(self.size):
            nblockx = 1
            nblocky = 1
            nblockz = self.size
        elif is_second(self.size):
            nblockz = 1
            for i in range(1,self.size+1):
                if np.mod(self.size, i) == 0:
                    tempx.append(i)
                    tempy.append(int(self.size / i))
            nblockx = tempx[round(len(tempx)/2)]
            nblocky = tempy[round(len(tempx)/2)]
        elif self.size == 4:
            nblockx = 2
            nblocky = 2
            nblockz = 1
        else:
            for i in range(1,self.size+1):
                for j in range(1,self.size+1):
                    if np.mod(self.size, i * j) == 0:
                        tempx.append(i)
                        tempy.append(j)
                        tempz.append(int(self.size / i / j))
            cond = True
            for i in range(len(tempx)):
                nblockx = tempx[i]
                nblocky = tempy[i]
                nblockz = tempz[i]
                if (nblockx > 1 and nblocky > 1 and nblockz > 1):
                    cond = False
                    break
            if cond:
                cond = True
                nblockz = 1
                for i in range(len(tempx)):
                    nblockx = tempx[i]
                    nblocky = tempy[i]
                    if (nblockx > 1 and nblocky > 1):
                        break
        
        if self.size != nblockx * nblocky * nblockz:
            raise ValueError("The number of blocks don't match the number of procs!")
        
        # print(nblockx,nblocky,nblockz)
        del(tempx, tempy, tempz)
        
        stridex = int(self.nx/nblockx)
        stridey = int(self.ny/nblocky)
        stridez = int(self.nz/nblockz)
        
        lx = np.array([i*stridex for i in range(0,int(nblockx)+1)])
        ly = np.array([i*stridey for i in range(0,int(nblocky)+1)])
        lz = np.array([i*stridez for i in range(0,int(nblockz)+1)])
        lx[-1] = self.nx
        ly[-1] = self.ny
        lz[-1] = self.nz
        
        nlx = np.array([i for i in range(0,int(nblockx)+1)])
        nly = np.array([i for i in range(0,int(nblocky)+1)])
        nlz = np.array([i for i in range(0,int(nblockz)+1)])
        
        slx = []
        elx = []
        sly = []
        ely = []
        slz = []
        elz = []   
        blcx = []
        blcy = []
        blcz = []
        for i in range(nblockx):          
            for j in range(nblocky):          
                for k in range(nblockz):     
                    slx.append(lx[0:-1][i])
                    elx.append(lx[1:][i])
                    sly.append(ly[0:-1][j])
                    ely.append(ly[1:][j])
                    slz.append(lz[0:-1][k])
                    elz.append(lz[1:][k])
                    blcx.append(nlx[i])
                    blcy.append(nly[j])
                    blcz.append(nlz[k])
        
        self.nblock      = np.array([nblockx, nblocky, nblockz])
        self.coordinates = np.array([blcx,blcy,blcz])
        self.slx         = slx
        self.elx         = elx
        self.sly         = sly
        self.ely         = ely
        self.slz         = slz
        self.elz         = elz
        


# Evoke by
# domDecomp = domainDecompose3D(size, nx, ny, nz)

# nblockx = domDecomp.nblock[0]
# nblocky = domDecomp.nblock[1]
# nblockz = domDecomp.nblock[2]

# slx  = domDecomp.slx[rank]
# elx  = domDecomp.elx[rank]
# mynx = elx - slx
# sly  = domDecomp.sly[rank]
# ely  = domDecomp.ely[rank]
# myny = ely - sly
# slz  = domDecomp.slz[rank]
# elz  = domDecomp.elz[rank]
# mynz = elz - slz

# # coord3d = [round(slx/mynx), round(sly/myny), round(slz/mynz)]
# coord3d = domDecomp.coordinates[:,rank]

# print ("In 3D topology, Processor ",rank, " has coordinates ",coord3d)

# print("")
# print("rank = ", rank,mynx,myny,mynz, 'slx = ',slx,'elx = ',elx, 'sly = ',sly,'ely = ',ely,'slz = ',slz,'elz = ',elz)