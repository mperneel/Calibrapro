# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 14:59:15 2022

@author: Maarten
"""
#%%

class Settings():
    """
    The Settings class contains all modifiable settings of the application
    """

    def __init__(self):

        #point size
        #unit: px
        self.point_size = 5

        #sensitivity for re-activation, expressed at the user scale
        #unit: px
        self.reactivation_sensitivity = 10

        #unit of 3D coordinates
        #options: m, dm, cm, mm
        self.unit_3d = "mm"
