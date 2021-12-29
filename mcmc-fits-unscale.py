
# coding: utf-8

# # Unscale fits file
# This file is intended to unscale the output fits file of MCMC implementation in XSPEC. 
# Some variables should be modified for the code to work. First, please change the 'deftype' 
# variable to the one needed (1 for alpha_13, 2 for alpha_22). Then modify the input fits file 
# name. Remember that the input fits file will be edited with the original defpar being replaced 
# by unscaled defpar. So a copy of the original file is needed. Modify the column name of spin 
# parameter and deformation parameter by print the variable cols.names .
# 

# The "corner" module can be downloaded from here "https://github.com/dfm/corner.py". 

# In[1]:


import numpy as np
from pylab import *
import sys
#import triangle
from astropy.io import fits
#get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg'")


# In[2]:
deftype = 1

if(deftype==1):
    our_file = fits.open('/opt/tools/relxill_nk_v1.3.1/Trf_Johannsen_a13.fits')
elif(deftype==2):
    our_file = fits.open('/opt/tools/relxill_nk_v1.3.1/Trf_Johannsen_a22.fits')
elif(deftype==3):
    our_file = fits.open('/opt/tools/relxill_nk_v1.3.1/Trf_Johannsen_e3.fits')
elif(deftype==4):
    our_file = fits.open('/opt/tools/relxill_nk_v1.3.1/Trf_KRZ_d1.fits') # THIS IS FOR KRZ d1
else:
    print("deftype doesn't match with any deformation parameter")
spindpgrid = our_file[1].data


# In[3]:


# unscale the deformation parameter when giving a spin value and a corresponding deformation value
def unscale(spin_value, def_value):
    """
    To unscale a deformation parameter when given a defpar and corresponding
    spin value.
    spin_value:
    def_value:
    The type of deformation parameter is determinded by variable deftype
    """
    for j in np.arange(29):
        if((spin_value < spindpgrid[j+1][0]) and (spin_value > spindpgrid[j][0])):
            if(def_value < 0):
                if(np.abs(spindpgrid[j][1][0])<np.abs(spindpgrid[j+1][1][0])):
                    def_unscaled_value = -def_value*spindpgrid[j][1][0] 
                else:
                    def_unscaled_value = -def_value*spindpgrid[j+1][1][0]
            else:
                if(np.abs(spindpgrid[j][1][29])<np.abs(spindpgrid[j+1][1][29])):
                    def_unscaled_value = def_value*spindpgrid[j][1][29]
                else:
                    def_unscaled_value = def_value*spindpgrid[j+1][1][29]
    def_unscaled_value = ("%.6f" % def_unscaled_value)
    return def_unscaled_value


# In[4]:


fitsfile = 'chain_13_q1freeq2free_linear_l100000000_b50000000_w100-copy.fits'


# In[5]:

with fits.open(fitsfile, mode='update') as hdul:
    #hdul = fits.open(fitsfile)
    hdr=hdul[0].header
    data = hdul[1].data
    cols = hdul[1].columns
    
    a = data['a__17']
    defpar = data['defpar_value__23']
    
    length = len(a)
    if (len(a)!=len(defpar)):
        print('Warning: number of spin par and def par do not match \n Further checking is strongly recommanded')
    
    for i in arange(length):
        spin_value = data['a__17'][i]
        defpar_value = data['defpar_value__23'][i]
        if (spin_value<1):   
            unscaled_defpar = unscale(spin_value,defpar_value)
            hdul[1].data['defpar_value__23'][i] = unscaled_defpar
        else:
            print('spin value larger then 1, step number:' + str(i))
    
    hdul.flush()

