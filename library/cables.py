# Cables Passive Heatload (PHL) # https://delft-circuits.com/wp-content/uploads/2024/03/productsheets-Signal-line-22-febr-2024-.pdf
# actual heatload depends on the plate temperatures. Needs a function!

# PHL_Cu Notebook
PHL_Cu_4K = 5.76458e-03 #[Cu-k-rho.ipynb]

# PHL_Mn Notebook
PHL_Mn_4K = 2.24538e-05 #[Manganin-k-rho.ipynb]

PHL_YBCO_4K = 5.09000e-06 #[YBCO-k.ipynb]

####### 2025raicuCryogenicThermalModeling - Table V (Measured HL) ##########
PHL_HDW   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : 7.566E-3,  # (W/channel); from 300K flange to 50K plate
            '4K'   : 3.157E-4,  # (W/channel); from 50K plate to 4K plate
            'Still': 2.373E-6,  # (W/channel); from 4K plate to Still plate
            'CP'   : 5.491E-7,   # (W/channel); from Still plate to CP plate
            'MXC'  : 1.332E-8 # (W/channel); from CP plate to MXC plate
            }

####### 2019krinnerEngineeringCryogenicSetups - Table 2 (Measured HL) ##########
PHL_SS_Drive   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : 45E-3,  # (W/channel); from 300K flange to 50K plate
            '4K'   : 1E-3,  # (W/channel); from 50K plate to 4K plate
            'Still': 4E-6,  # (W/channel); from 4K plate to Still plate
            'CP'   : 0.4E-6,   # (W/channel); from Still plate to CP plate
            'MXC'  : 13E-9 # (W/channel); from CP plate to MXC plate
            }

PHL_SS_Flux   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : 56E-3,  # (W/channel); from 300K flange to 50K plate
            '4K'   : 1.2E-3,  # (W/channel); from 50K plate to 4K plate
            'Still': 2E-6,  # (W/channel); from 4K plate to Still plate
            'CP'   : 0.3E-6,   # (W/channel); from Still plate to CP plate
            'MXC'  : 29E-9 # (W/channel); from CP plate to MXC plate
            }

PHL_NbTi_coax   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : None,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : 0.3E-6,   # (W/channel); from Still plate to CP plate
            'MXC'  : 20E-9 # (W/channel); from CP plate to MXC plate
            }
################################################################################
PHL_Ag   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : 2.7E-3,  # (W/channel); from 300K flange to 50K plate
            '4K'   : 0.8E-3,  # (W/channel); from 50K plate to 4K plate
            'Still': 5.4E-6,  # (W/channel); from 4K plate to Still plate
            'CP'   : 290E-9,   # (W/channel); from Still plate to CP plate
            'MXC'  : 5.9E-9 # (W/channel); from CP plate to MXC plate
            }

PHL_NbTi = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : None,  # (W/channel); from 50K plate to 4K plate
            'Still': 540E-9,  # (W/channel); from 4K plate to Still plate
            'CP'   : 29E-9 ,  # (W/channel); from Still plate to CP plate
            'MXC'  : 590E-12 # (W/channel); from CP plate to MXC plate
            }

PHL_Fiber = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
             '50K'  : None,  # (W/channel); from 300K flange to 50K plate
             '4K'   : 5.6E-6,  # (W/channel); from 50K plate to 4K plate [2021lecocqControlReadoutSuperconducting - Methods: Passive heat load]
             'Still': 2.75E-09,  # (W/channel); from 4K plate to Still plate [assuming similar ratio with NbTi]
             'CP'   : 1.47E-10,   # (W/channel); from Still plate to CP plate [assuming similar ratio with NbTi]
             'MXC'  : 3.00E-12 # (W/channel); from CP plate to MXC plate [2021lecocqControlReadoutSuperconducting - Pg.577]
            }

# For photomixers, there is an input optical fiber and an "output" optical fiber that dissipates excess optical energy at RT
PHL_Fiber2 = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
             '50K'  : None,  # (W/channel); from 300K flange to 50K plate
             '4K'   : 2 * 5.6E-6,  # (W/channel); from 50K plate to 4K plate [2021lecocqControlReadoutSuperconducting - Methods: Passive heat load]
             'Still': 2 * 2.75E-09,  # (W/channel); from 4K plate to Still plate [assuming similar ratio with NbTi]
             'CP'   : 2 * 1.47E-10,   # (W/channel); from Still plate to CP plate [assuming similar ratio with NbTi]
             'MXC'  : 2 * 3.00E-12 # (W/channel); from CP plate to MXC plate [2021lecocqControlReadoutSuperconducting - Pg.577]
            }
################################################################################
# At least, three and two wires are needed for two SIS mixers and one Josephson oscillator, respectively (five wires in total)
PHL_SIS_5w_Mn   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Mn_4K*5,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

PHL_SIS_7w_Mn   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Mn_4K*7,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

# if acceptable, we would like to add four more wires (nine wires in total) for accurate biasing
PHL_SIS_9w_Mn   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Mn_4K*9,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

PHL_SIS_11w_Mn   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Mn_4K*11,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

PHL_SIS_19w_Mn   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Mn_4K*19,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

PHL_SIS_21w_Mn   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Mn_4K*21,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

PHL_SIS_5w_Cu   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Cu_4K*5,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

PHL_SIS_7w_Cu   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Cu_4K*7,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

# if acceptable, we would like to add four more wires (nine wires in total) for accurate biasing
PHL_SIS_9w_Cu   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Cu_4K*9,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

PHL_SIS_9w_YBCO   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_YBCO_4K*9,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

PHL_SIS_11w_Cu   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Cu_4K*11,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

PHL_SIS_19w_Cu   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Cu_4K*19,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

PHL_SIS_21w_YBCO   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_YBCO_4K*21,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
                     }

# three wires (ground, bias, gate) per one amplifier
PHL_HEMT_Bias_Cu   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Cu_4K*3,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

# three wires (ground, bias, gate) per one amplifier
PHL_HEMT_Bias_Mn   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Mn_4K*3,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

# 13 wires (6xground, 6xbias, 1xgate) per one amplifier
PHL_HEMT_13w_Bias_Mn   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_Mn_4K*13,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

# three wires (ground, bias, gate) per one amplifier
PHL_HEMT_Bias_YBCO   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_YBCO_4K*3,  # (W/channel); from 50K plate to 4K plate
            'Still': None,  # (W/channel); from 4K plate to Still plate
            'CP'   : None,   # (W/channel); from Still plate to CP plate
            'MXC'  : None # (W/channel); from CP plate to MXC plate
            }

################################################################################
# Josephson Detector in Photomixer
PHL_JJ_Bias_YBCO   = {'RT'   : None,    # (W/channel); from RT flange to 300K flange
            '50K'  : None,  # (W/channel); from 300K flange to 50K plate
            '4K'   : PHL_YBCO_4K*6,  # V+, V-, GND, I_in
            'Still': PHL_NbTi['Still']*6,  # V+, V-, GND, I_in
            'CP'   : PHL_NbTi['CP']*6,  # V+, V-, GND, I_in
            'MXC'  : PHL_NbTi['MXC']*6,  # V+, V-, GND, I_in
            }

CABLE_PHL_DATA = {
    "Ag"   : PHL_Ag,
    "NbTi" : PHL_NbTi,
    "Fiber": PHL_Fiber,
    "Fiber2": PHL_Fiber2,
    "SS_Drive": PHL_SS_Drive,
    "SS_Flux": PHL_SS_Flux,
    "NbTi_coax": PHL_NbTi_coax,
    "HDW": PHL_HDW,
    "HEMT_Bias_Cu": PHL_HEMT_Bias_Cu,
    "HEMT_Bias_Mn": PHL_HEMT_Bias_Mn,
    "HEMT_Bias_YBCO": PHL_HEMT_Bias_YBCO,
    "HEMT_13w_Bias_Mn": PHL_HEMT_13w_Bias_Mn,
    
    "SIS_v1_5w_Bias_Cu": PHL_SIS_5w_Cu,
    "SIS_v1_7w_Bias_Cu": PHL_SIS_7w_Cu,
    
    "SIS_v1_5w_Bias_Mn": PHL_SIS_5w_Mn,
    "SIS_v1_7w_Bias_Mn": PHL_SIS_7w_Mn,

    "SIS_v2_5w_Bias_Cu": PHL_SIS_5w_Cu,
    "SIS_v2_9w_Bias_Cu": PHL_SIS_9w_Cu,
    "SIS_v2_9w_Bias_YBCO": PHL_SIS_9w_YBCO,
    "SIS_v2_11w_Bias_Cu": PHL_SIS_11w_Cu,
    "SIS_v2_19w_Bias_Cu": PHL_SIS_19w_Cu,

    "SIS_v2_5w_Bias_Mn": PHL_SIS_5w_Mn,
    "SIS_v2_9w_Bias_Mn": PHL_SIS_9w_Mn,
    "SIS_v2_11w_Bias_Mn": PHL_SIS_11w_Mn,
    "SIS_v2_19w_Bias_Mn": PHL_SIS_19w_Mn,
    "SIS_v2_21w_Bias_Mn": PHL_SIS_21w_Mn,
    "SIS_v2_21w_Bias_YBCO": PHL_SIS_21w_YBCO,
    "JJ_Bias_YBCO":PHL_JJ_Bias_YBCO
 }
#####################################################
class CABLE():
    def __init__(self, PHL_dict, name):
        self.name = name
        self.PHL_dict = PHL_dict

#####################################################
def create_cable_instance(cable_type_str):
    if cable_type_str in list(CABLE_PHL_DATA.keys()):
        return CABLE(CABLE_PHL_DATA[cable_type_str], cable_type_str)
    else:
        return None
#####################################################
def get_cable_config(cable_config_names):
    cable_config = {}
    for cable_type, config in cable_config_names.items():
        cable_config[cable_type]={}
        for temp_stage, cable_name in config.items():
            if cable_name is not None:
               cable_config[cable_type][temp_stage] = create_cable_instance(cable_name)
            else:
                cable_config[cable_type][temp_stage] = None
    return cable_config
#####################################################
def cable_attenuator_dissipation(cable_attenuator_config, output_power_MXC):
    """
    Outputs the power inputs (or equivalently the power dissipated by the attenuators) at each temperature stage for a given cable. 
    At 10-20 dB attenuation, almost all (90%-99%) of the input power is dissipated in the attenuator so ** input power = dissipated power **

    Parameters
    ----------
    attenuator_config : dict
        configuration of attenuators in dB: {'RT'   : ATT_RT
                                             '50K'  : ATT_50K
                                             '4K'   : ATT_4K, 
                                             'Still': ATT_Still, 
                                             'CP'   : ATT_CP,
                                             'MXC'  : ATT_MXC}
        negative values not allowed
            
    output_power_MXC in dBm : int
        the final power level expected at MXC (qubit)

    Returns
    -------
    dict
        dictionary with keys ['RT','50K','4K', 'Still', 'CP', 'MXC'] whose values indicate the power dissipated by the attenuators at each stage in dBm.
        If no power is dissipated (i.e., the attenuator does not exist), then it returns None.
    """
    # Check if attenuations are all non-negative
    try:
        all(value >= 0 for value in cable_attenuator_config.values())
    except:
        print("Attenuator values must always be non-negative")

    # Initialize output dictionary
    output_dict = { 'RT'   : None,
                    '50K'  : None,        
                    '4K'   : None, 
                    'Still': None, 
                    'CP'   : None,
                    'MXC'  : None}

    # When output_power_MXC is not given
    if output_power_MXC is None:
        return output_dict

    # Given the output power, calculate the input power required
    total_line_attenuation = sum(value for value in cable_attenuator_config.values())
    input_power            = output_power_MXC + total_line_attenuation

    # Calculate the power dissipated at each stage
    remaining_power = input_power
    for key in cable_attenuator_config.keys():
        if cable_attenuator_config[key] > 0: # only positive values (in dBm allowed)
            output_dict[key] = remaining_power
            remaining_power -= cable_attenuator_config[key]
        else:
            output_dict[key] = None

    # Check if the final power matches the desired output power value
    try:
        remaining_power - cable_attenuator_config['MXC'] == output_power_MXC
    except:
        print("Final power level does not match the desired value.")

    return output_dict
#####################################################