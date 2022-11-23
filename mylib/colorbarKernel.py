import numpy                 as np
import matplotlib.colors     as cols


def cMapRYWCB(field, vRange=None, nColors=1000,whitePerCent=5.,\
              colorFrac=[0.25,0.25,0.25,0.25],reverse=False):

  cminInput = np.amin(field)
  cmaxInput = np.amax(field)
  if vRange:
    cminInput = vRange[0]
    cmaxInput = vRange[1]

  if np.isnan(cminInput) or np.isnan(cmaxInput):
    raise Exception('Error cmax or cmin = Nan')

  nColorsPerSide = nColors*np.array(colorFrac)
  colorNumtotal  = nColors
  eps     = whitePerCent/100 
  redYel = None
  yelWht = None
  whtCyn = None
  cynBlu = None

  for i in range(nColors):
    if redYel is None:
      redYel = [[1.,0.,0.]]
      yelWht = [[1.,1.,0.]]
      whtCyn = [[1.,1.,1.]]
      cynBlu = [[0.,1.,1.]]
    else:
      if i < nColorsPerSide[0]:
        redYel = np.append(redYel,[[1.,(nColorsPerSide[0]+i)/float(nColorsPerSide[0])-1,0.]],axis=0)
      if i < nColorsPerSide[1]:
        yelWht = np.append(yelWht,[[1.,1.,(nColorsPerSide[1]+i)/float(nColorsPerSide[1])-1]],axis=0)
      if i < nColorsPerSide[2]:
        whtCyn = np.append(whtCyn,[[(nColorsPerSide[2]-i)/float(nColorsPerSide[2]),1.,1.  ]],axis=0)
      if i < nColorsPerSide[3]:
        cynBlu = np.append(cynBlu,[[0.,(nColorsPerSide[3]-i)/float(nColorsPerSide[3]),1.  ]],axis=0)

  whiteMiddle = np.ones((int(np.round(eps*nColors)),3))
  ucmap       = np.concatenate((redYel,yelWht,whiteMiddle,whtCyn,cynBlu,[[0.,0.,1.]]),axis=0)

  if not reverse:
    ucmap = np.flipud(ucmap)

  return cols.ListedColormap(ucmap)
