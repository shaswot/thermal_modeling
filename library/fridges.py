TEMP_STAGES = ['RT', '50K', '4K', 'Still', 'CP', 'MXC']

XLD400 = { # 2019krinnerEngineeringCryogenicSetups
    'RT'   : 100,
    '50K'  : 30, # Watts
    '4K'   : 1.5, # Watts
    'Still': 40E-3, # Watts
    'CP'   : 200E-6, # Watts
    'MXC'  : 19E-6 # Watts
}

XLD400_v2 = { # 2019krinnerEngineeringCryogenicSetups - Sec 6 Proposed Setup
    'RT'   : 100,
    '50K'  : 30, # Watts
    '4K'   : 1.5, # Watts
    'Still': 40E-3, # Watts
    'CP'   : 400E-6, # Watts
    'MXC'  : 19E-6 # Watts
}

XLD1000SL_v1= { # 2022blueforsBlueforsXLD1000slSystem
    'RT'   : 100, # Watts
    '50K'  : 50, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 3]
    '4K'   : 1.8, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 3]
    'Still': 0.9, # Watts ~8.97416442e-01 from Still Estimate Notebook
    'CP'   : 1E-3, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 2]
    'MXC'  : 30E-6 # Watts [2022blueforsBlueforsXLD1000slSystem - Table 2]
}

XLD1000SL_v2= { # 2022blueforsBlueforsXLD1000slSystem
    'RT'   : 100, # Watts
    '50K'  : 50, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 3]
    '4K'   : 2.35, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 3]
    'Still': 1.0, # Watts ~9.98417455e-01 from Still Estimate Notebook
    'CP'   : 1E-3, # Watts [2022blueforsBlueforsXLD1000slSystem - Table 2]
    'MXC'  : 30E-6 # Watts [2022blueforsBlueforsXLD1000slSystem - Table 2]
}

# Most Realistic
XLD1000SL_v3= { # 2025raicuCryogenicThermalModeling - Table 1
    'RT'   : 100, # Watts
    '50K'  : 30, # Watts
    '4K'   : 0.7, # Watts
    'Still': 7e-3, # Watts
    'CP'   : 1E-3, # Watts
    'MXC'  : 30E-6 # Watts
}

ULVAC_v1= {# UDR-1000 (low end)
    'RT'   : 100, # Watts
    '50K'  : 10, # Watts
    '4K'   : 1, # Watts
    'Still': 15e-3, # Watts
    'CP'   : 1.5e-3, # Watts
    'MXC'  : 10E-6 # Watts
}

ULVAC_v2= {# UDR-1000 (high end)
    'RT'   : 100, # Watts
    '50K'  : 16.7, # Watts
    '4K'   : 1.7, # Watts
    'Still': 30e-3, # Watts
    'CP'   : 7e-4, # Watts
    'MXC'  : 20E-6 # Watts
}

ULVAC_v3= {# UDR-1000 (target)
    'RT'   : 100, # Watts
    '50K'  : 16.7, # Watts
    '4K'   : 1.7, # Watts
    'Still': 30e-3, # Watts
    'CP'   : 1.5e-3, # Watts
    'MXC'  : 45E-6 # Watts
}

ULVAC_v4= {# UDR-1000 (highest end) x 3
    'RT'   : 100, # Watts
    '50K'  : 16.7, # Watts
    '4K'   : 1.7 * 3, # Watts
    'Still': 30e-3 * 3, # Watts
    'CP'   : 1.5e-3 * 3, # Watts
    'MXC'  : 45E-6 * 3 # Watts
}


KIDE_v1= { # https://bluefors.com/products/kide-cryogenic-platform/
    'RT'   : 100, # Watts
    '50K'  : 50, # Watts 
    '4K'   : 6.0, # Watts # Ilkwon's Estimate from 2023mutusAlgorithmDrivenFault 
    'Still': 2.81, # Watts  ~2.80813688e+00 from Still Estimate Notebook
    'CP'   : 1E-3*3, # Watts 3 x XLD1000SL dilution units
    'MXC'  : 3E-5*3 # Watts 3 x XLD1000SL dilution units
}

KIDE_v2= { # 2024blueforsKIDEProductOverview
    'RT'   : 100, # Watts
    '50K'  : 50, # Watts # 9 Pulse Tube Cryocoolers - pg. 9
    '4K'   : 2.35, # Watts # Masubcichi sensei - 9 pulse tube coolers, only 1 is used to cool the 50K and 4K stage 
    'Still': 2.81, # Watts  ~2.80813688e+00 from Still Estimate Notebook
    'CP'   : 1E-3*3, # Watts 3 x XLD1000SL dilution units
    'MXC'  : 3E-5*3 # Watts 3 x XLD1000SL dilution units
}

KIDE_v3= { # 2024blueforsKIDEProductOverview
    'RT'   : 100, # Watts
    '50K'  : 50, # Watts
    '4K'   : 2 * 3, # Watts # Assuming operating temperature of 4K [https://bluefors.com/products/measurement-infrastructure/high-density-wiring/]
    'Still': 7e-3 * 3, # 
    'CP'   : 1E-3 * 3, # Watts
    'MXC'  : 30E-6 * 3 # Watts
}

FRIDGE_LIBRARY = {
    "XLD400"   : XLD400,
    "XLD400_v2"   : XLD400_v2,
    "XLD1000SL_v1" : XLD1000SL_v1,
    "XLD1000SL_v2": XLD1000SL_v2,
    "XLD1000SL_v3": XLD1000SL_v3,
    "KIDE_v1": KIDE_v1,
    "KIDE_v2": KIDE_v2,
    "KIDE_v3": KIDE_v3,
    "ULVAC_v1": ULVAC_v1,
    "ULVAC_v2": ULVAC_v2,
    "ULVAC_v3": ULVAC_v3,
    "ULVAC_v4":ULVAC_v4
}
