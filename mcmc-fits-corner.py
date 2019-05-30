
# coding: utf-8

# # MCMC corner plot
# 

# This code is written by Honghui to get the corner plot with MCMC sample from XSPEC. The corner module can be found on this website: "https://github.com/dfm/corner.py". The input fits file name needs to be modified and also the column name of each parameter.

# In[1]:


import numpy as np
import corner
import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import *
import pylab as plot
import sys
#import triangle
from astropy.io import fits
#get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg'")


# In[2]:


#infile = 'chain_nk_13_l100000_w100_t1.txt'
#fitsfile = 'chain_13_linear_ini_l100000000_w100_b50000000-copy.fits'
fitsfile = 'test.fits'


# In[3]:


hdul = fits.open(fitsfile)
hdr=hdul[0].header
data = hdul[1].data
cols = hdul[1].columns

#cols.names
#data['column__2']


# In[4]:

column = data['column__2']
rlogxi = data['rlogxi__3']
z = data['z__4']
chisq = data['FIT_STATISTIC']
a = data['a__17']
incl = data['Incl__18']
gamma = data['PhoIndex__6']
Ecut = data['HighECut__7']
norm1 = data['norm__8']
Tin = data['Tin__9']
norm2 = data['norm__10']
norm3 = data['norm__13']
qin = data['Index1__14']
rbr = data['Rbr__16']
alpha13 = data['defpar_value__23']
afe = data['Afe__27']
logxi = data['logxi__29']
norm4 = data['norm__33']
factor = data['factor__34']
# In[5]:


#sample = np.array([alpha13,rbr,qin,a,incl]).T.reshape([-1,5])
sample = np.array([alpha13,rbr,qin,a,incl,column,rlogxi,z,gamma,Ecut,Tin,afe,logxi]).T.reshape([-1,13])

# In[6]:
#fig=corner.corner(sample,labels=[r'$\alpha_{13}$',r'$R_{\rm br}$',r'$q_{\rm in}$',r'$a_{*}$',r'deg'])
fig=corner.corner(sample,labels=[r'$\alpha_{13}$',r'$R_{\rm br}$',r'$q_{\rm in}$',r'$a_{*}$',r'${\rm Incl}$',r'$N_{H} [cm^{-2}]$',
                                r'$r\log_{\xi}$',r'$z$',r'$\gamma$',r'$E_{\rm cut} [keV]$',r'$T_{\rm in} [keV]$',r'$A_{\rm Fe}$',
                                r'$\log_{\xi}$'], levels=(0.68,0.95,0.997))

axes = np.array(fig.axes).reshape(13,13)
for i in range(13):
    axes[i,0].axvline(0.0,color = 'red')
# #fig=triangle.corner(sample,labels=[r'$N_{H}$',r'$\log_{\xi}$',r'$z$'])
fig.savefig("e4-all-2M-fromXSPEC-unscaled-corner-newlevel-vline.pdf")
#plt.show()
# # #sample.shape

