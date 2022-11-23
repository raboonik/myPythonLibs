import numpy as np

class domainDecompose1D:
    def __init__(self, size, n):
        self.size = size
        self.nt   = n
        
        # Parallel scheme
        stride = int(self.nt/self.size)
        
        l = np.array([i*stride for i in range(0,int(self.size)+1)])
        l[-1] = self.nt
        
        nl = np.array([i for i in range(0,int(self.size)+1)])
        
        slx = []
        elx = []
        for i in range(self.size):                      
            slx.append(l[0:-1][i])
            elx.append(l[1:][i])
        
        self.nblock      = np.array([self.size])
        self.coordinates = np.array(range(self.size))
        self.slx         = slx
        self.elx         = elx