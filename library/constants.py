# [2019krinnerEngineeringCryogenicSetups - Section 5.2]
R_CP     = 0.42 # DC resistance of bias cables from Still to CP
R_MXC    = 0.15 # DC resistance of bias cables from CP to MXC
I_BIAS   = 1E-3 # Ampere; Max current amplitude required to bias qubits for 1Q operation
I_2Q     = 0.4E-3 # Ampere: Current required to bias qubits for 2Q operation

# # Power required at the MXC for various qubit operations
# ########################################################
# DRIVE_CABLE_POWER_MXC_1Q = -73  #dBm (5.01e-11 W) Refer Explanations Notebook Sec 1 - assuming 100% duty cycle [2019krinnerEngineeringCryogenicSetups - Sec 2.2.2]

# READOUT_PIN_POWER_MXC    = -120 #dBm (1.00e-15 W) [2021bardinMicrowavesQuantumComputing] - Sec V (Pg. 418)
# TWPA_PUMP_POWER_MXC      = -55  #dBm (3.16e-09) [2019krinnerEngineeringCryogenicSetups] - Sec 3.4


### SIS Constants ###
# Wire Dimensions
length = 460E-3 # 460 mm # https://lownoisefactory.com/product/lnf-nano9m/
area = 0.0509E-6 # 30 AWG = 0.0509 mm2 # https://lownoisefactory.com/product/lnf-nano9m/

## Average Resistivity for 30 AWG wire between 4K and 50K
rho_Cu = 0.005142 # Ohm/m [Cu-k-rho.ipynb]
rho_Manganin = 8.823418 # Ohm/m [Manganin-k-rho.ipynb]

## Average Resistance
R_Cu = rho_Cu * length # 0.00236532 Ohms
R_Manganin = rho_Manganin * length # 4.05877228 Ohms
########################

ROW_ORDER = ["DRIVE", "FLUX_BIAS", "COUPLER", "PUMP", "READOUT_PIN", "READOUT_POUT", "AMP_BIAS", "JJ_BIAS"]
ORDER_DICT = {row: index for index, row in enumerate(ROW_ORDER)}