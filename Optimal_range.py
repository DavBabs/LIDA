# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 19:20:07 2024

@author: DavidBabula
"""

# Optimal Conditions
active_temp = (65,75)
moisture_active = (40,60) 
co2 = (1,1) # CO2 is Carbon Dioxide
o2 = (1,1) # O2 is Oxygen
ch4 = (1,1) # CH4 is Methane

active_min = active_temp[0]
active_max = active_temp[1]
moisture_min = moisture_active[0]
moisture_max = moisture_active[1]
co2_min = co2[0]
co2_max = co2[1]
o2_min = o2[0]
o2_max = o2[1]
ch4_min = ch4[0]
ch4_max = ch4[1] 

pump_on_seconds=900

                               
#Termination Condition:
# ≤40oC
# 1209600 seconds (2 Weeks in seconds, 14 days)
