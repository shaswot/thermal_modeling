import sys
import git
import pathlib

# Set up the PROJ_ROOT variable
PROJ_ROOT_PATH = pathlib.Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
PROJ_ROOT =  str(PROJ_ROOT_PATH)
if PROJ_ROOT not in sys.path:
    sys.path.append(PROJ_ROOT)
#####################################################
import numpy as np
from library.cables import R_Cu_4K, R_Cu_50K, R_Manganin_4K, R_Manganin_50K
from library.utils import watts_to_dbm, dBm2Watts
#####################################################
# Add DC resistance for flux-bias and coupler-bias lines
def add_flux_coupler_DC_resistance(COMP_CONFIG,
                                   QUBIT_FREQ, 
                                   QUBIT_COUPLING, 
                                   R_4K, R_Still, R_CP, R_MXC):
    if QUBIT_FREQ == "TUNABLE":
        [comp.set_values(R_4K, I_BIAS) for comp in COMP_CONFIG["FLUX_BIAS"]["4K"]]
        [comp.set_values(R_Still, I_BIAS) for comp in COMP_CONFIG["FLUX_BIAS"]["Still"]]
        [comp.set_values(R_CP, I_BIAS) for comp in COMP_CONFIG["FLUX_BIAS"]["CP"]]
        [comp.set_values(R_MXC, I_BIAS) for comp in COMP_CONFIG["FLUX_BIAS"]["MXC"]]
    if QUBIT_COUPLING == "TUNABLE":
        [comp.set_values(R_4K, I_2Q) for comp in COMP_CONFIG["COUPLER"]["4K"]]
        [comp.set_values(R_Still, I_2Q) for comp in COMP_CONFIG["COUPLER"]["Still"]]
        [comp.set_values(R_CP, I_2Q) for comp in COMP_CONFIG["COUPLER"]["CP"]]
        [comp.set_values(R_MXC,I_2Q) for comp in COMP_CONFIG["COUPLER"]["MXC"]]

    return COMP_CONFIG
#######################################################################
def add_ohmic_resistors_amp_at_4K(CABLE_CONFIG_NAMES, COMP_CONFIG):
    # Determine current in amplifier
    current = None
    if CABLE_CONFIG_NAMES['AMP_BIAS']['4K'] is not None:
        for component in COMP_CONFIG['AMP_BIAS']['4K']:
            if isinstance(component, AMPLIFIER):
                current = component.I

    # 4K stage
    # Determine Ohmic resistance for amplifier Biasing
    resistance = None
    name = None
    if CABLE_CONFIG_NAMES['AMP_BIAS']['4K'] is not None:
        if '_cu' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].lower():
            resistance = R_Cu_4K
            name = "ohmic_Cu"
        if '_mn' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].lower():
            resistance = R_Manganin_4K
            name = "ohmic_Mn"
        if '_ybco' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].lower():
            resistance = 0.0
            name = "ohmic_YBCO"
    else:
        resistance = 0.0
        name = "ohmic_zero"

    # Create Ohmic Resistor
    if CABLE_CONFIG_NAMES['AMP_BIAS']['4K'] is not None:
        if 'HEMT' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K']:
            ohmic_resistor = AMP_OHMIC_RESISTOR(resistance, current, name)
            if COMP_CONFIG['AMP_BIAS']['4K']is not None:
                COMP_CONFIG['AMP_BIAS']['4K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['4K'] = [ohmic_resistor]
        
        elif 'SIS_v1' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K']:
            _, _, tot_no_of_wires, _, _ = CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].split('_') # SIS_v1_5w_Bias_Mn 
            num_LO_pair    = (int(tot_no_of_wires[:-1]) - 3)/2 # [SIS_up, SIS_down, GND, (LO_in, LO_out)]
            current_list   = SIS_current_split(current, num_LO_pair)
            ohmic_resistor = SIS_OHMIC_RESISTOR(resistance, current_list, name)
            if COMP_CONFIG['AMP_BIAS']['4K']is not None:
                COMP_CONFIG['AMP_BIAS']['4K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['4K'] = [ohmic_resistor]
            
        elif 'SIS_v2' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K']:
            _, _, tot_no_of_wires, _, _ = CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].split('_') # SIS_v2_9w_Bias_Mn 
            num_LO_pair    = (int(tot_no_of_wires[:-1]) - 7)/2 # [SIS_up, SIS_up_V+, SIS_up_V-, SIS_down, SIS_down_V+, SIS_down_V-, GND, (LO_in, LO_out)]
            current_list   = SIS_current_split(current, num_LO_pair)
            ohmic_resistor = SIS_OHMIC_RESISTOR(resistance, current_list, name)
            if COMP_CONFIG['AMP_BIAS']['4K']is not None:
                COMP_CONFIG['AMP_BIAS']['4K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['4K'] = [ohmic_resistor]

    # 50K stage
    # Ohmic resistance for amplifier Biasing
    resistance = None
    name = None
    if CABLE_CONFIG_NAMES['AMP_BIAS']['50K'] is not None:
        if '_cu' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K'].lower():
            resistance = R_Cu_50K
            name = "ohmic_Cu"
        if '_mn' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K'].lower():
            resistance = R_Manganin_50K
            name = "ohmic_Mn"
        if '_ybco' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K'].lower():
            resistance = 0.0
            name = "ohmic_YBCO"
    else:
        resistance = 0.0
        name = "ohmic_zero"
    # 
    # Ohmic Resistor
    if CABLE_CONFIG_NAMES['AMP_BIAS']['50K'] is not None:
        if 'HEMT' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K']:
            ohmic_resistor = AMP_OHMIC_RESISTOR(resistance, current, name)
            if COMP_CONFIG['AMP_BIAS']['50K']is not None:
                COMP_CONFIG['AMP_BIAS']['50K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['50K'] = [ohmic_resistor]
        
        elif 'SIS_v1' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K']:
            _, _, tot_no_of_wires, _, _ = CABLE_CONFIG_NAMES['AMP_BIAS']['50K'].split('_') # SIS_v1_5w_Bias_Mn 
            num_LO_pair    = (int(tot_no_of_wires[:-1]) - 3)/2 # [SIS_up, SIS_down, GND, (LO_in, LO_out)]
            current_list   = SIS_current_split(current, num_LO_pair)
            ohmic_resistor = SIS_OHMIC_RESISTOR(resistance, current_list, name)
            if COMP_CONFIG['AMP_BIAS']['50K']is not None:
                COMP_CONFIG['AMP_BIAS']['50K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['50K'] = [ohmic_resistor]
            
        elif 'SIS_v2' in CABLE_CONFIG_NAMES['AMP_BIAS']['50K']:
            _, _, tot_no_of_wires, _, _ = CABLE_CONFIG_NAMES['AMP_BIAS']['50K'].split('_') # SIS_v2_9w_Bias_Mn 
            num_LO_pair    = (int(tot_no_of_wires[:-1]) - 7)/2 # [SIS_up, SIS_up_V+, SIS_up_V-, SIS_down, SIS_down_V+, SIS_down_V-, GND, (LO_in, LO_out)]
            current_list   = SIS_current_split(current, num_LO_pair)
            ohmic_resistor = SIS_OHMIC_RESISTOR(resistance, current_list, name)
            if COMP_CONFIG['AMP_BIAS']['50K']is not None:
                COMP_CONFIG['AMP_BIAS']['50K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS']['50K'] = [ohmic_resistor]
    return COMP_CONFIG
########################################################################
def add_ohmic_resistors_amp_at_50K(CABLE_CONFIG_NAMES, COMP_CONFIG):
    # Determine current in amplifier
    current = None
    if CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'] is not None:
        for component in COMP_CONFIG['AMP_BIAS_50K']['50K']:
            if isinstance(component, AMPLIFIER):
                current = component.I

    # 50K stage
    # Ohmic resistance for amplifier Biasing
    resistance = None
    name = None
    if CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'] is not None:
        if '_cu' in CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'].lower():
            resistance = R_Cu_50K
            name = "ohmic_Cu"
        if '_mn' in CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'].lower():
            resistance = R_Manganin_50K
            name = "ohmic_Mn"
        if '_ybco' in CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'].lower():
            resistance = 0.0
            name = "ohmic_YBCO"
    else:
        resistance = 0.0
        name = "ohmic_zero"

    # Ohmic Resistor
    if CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K'] is not None:
        if 'HEMT' in CABLE_CONFIG_NAMES['AMP_BIAS_50K']['50K']:
            ohmic_resistor = AMP_OHMIC_RESISTOR(resistance, current, name)
            if COMP_CONFIG['AMP_BIAS_50K']['50K']is not None:
                COMP_CONFIG['AMP_BIAS_50K']['50K'].append(ohmic_resistor)
            else:
                COMP_CONFIG['AMP_BIAS_50K']['50K'] = [ohmic_resistor]
    return COMP_CONFIG
########################################################################
# # Function to append generate ohmic resistor
# def get_amp_ohmic_resistor(CABLE_CONFIG_NAMES, COMP_CONFIG):
#     # Ohmic resistance for amplifier Biasing
#     resistance = None
#     name = None
#     if '_cu' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].lower():
#         resistance = R_Cu
#         name = "ohmic_Cu"
#     if '_mn' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].lower():
#         resistance = R_Manganin
#         name = "ohmic_Mn"
#     if '_ybco' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].lower():
#         resistance = 0.0
#         name = "ohmic_YBCO"
    
#     # Current in amplifier
#     current = None
#     for component in COMP_CONFIG['AMP_BIAS']['4K']:
#         if isinstance(component, AMPLIFIER):
#             current = component.I
    
#     # Ohmic Resistor
#     if 'HEMT' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K']:
#         num_params = len(CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].split('_')) # HEMT_13w_Bias_Mn vs # HEMT_Bias_Mn
#         if num_params == 3: # HEMT_Bias_Mn
#             ohmic_resistor = AMP_OHMIC_RESISTOR(resistance, current, name)
#         if num_params > 3:      
#             _, tot_no_of_wires, _, _ = CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].split('_') # HEMT_13w_Bias_Mn
#             num_split = (int(tot_no_of_wires[:-1]) - 1)/2 # [V_GS, (V_DS, GND)]
#             eqv_resistance = resistance/(2*num_split)
#             ohmic_resistor = AMP_OHMIC_RESISTOR(eqv_resistance, current, name)
#     else:
#         if 'SIS_v1' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K']:
#             _, _, tot_no_of_wires, _, _ = CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].split('_') # SIS_v1_5w_Bias_Mn 
#             num_LO_pair    = (int(tot_no_of_wires[:-1]) - 3)/2 # [SIS_up, SIS_down, GND, (LO_in, LO_out)]
        
#         if 'SIS_v2' in CABLE_CONFIG_NAMES['AMP_BIAS']['4K']:
#             _, _, tot_no_of_wires, _, _ = CABLE_CONFIG_NAMES['AMP_BIAS']['4K'].split('_') # SIS_v2_9w_Bias_Mn 
#             num_LO_pair    = (int(tot_no_of_wires[:-1]) - 7)/2 # [SIS_up, SIS_up_V+, SIS_up_V-, SIS_down, SIS_down_V+, SIS_down_V-, GND, (LO_in, LO_out)]
                
#         current_list   = SIS_current_split(current, num_LO_pair)
#         ohmic_resistor = SIS_OHMIC_RESISTOR(resistance, current_list, name)
        
#     return ohmic_resistor

# Amplifier Class
#################
class AMPLIFIER():
    def __init__(self, V, I, name):
        self.name = name
        self.V = V # operating voltage
        self.I = I # operating current

    def power_dissipation(self, *args, **kwargs):
        operation = None
        MXC_POWER = None
        
        # assign from positional args first
        if len(args) >= 1:
            operation = args[0]
        if len(args) >= 2:
            MXC_POWER = args[1]
        
        # then override with kwargs if present
        if "operation" in kwargs:
            operation = kwargs["operation"]
        if "MXC_POWER" in kwargs:
            MXC_POWER = kwargs["MXC_POWER"]
        
        power = self.V * self.I # dissipative power in Watts due to biasing (always ON)
        return power # dissipative power in Watts due to biasing (always ON)

class AMP_OHMIC_RESISTOR():
    def __init__(self,R,I,name):
        """
        R: float
            Resistance in ohms
        I: float
            Current in biasing wires in amperes
            Includes both incoming and outgoing currents
        name : stf
            Name of the component

        Returns power in Watts due to ohmic (joule) heating
        """
        self.name = name
        self.R = R
        self.I = I
        
    def power_dissipation(self, *args, **kwargs):
        operation = None
        MXC_POWER = None
        
        # assign from positional args first
        if len(args) >= 1:
            operation = args[0]
        if len(args) >= 2:
            MXC_POWER = args[1]
        
        # override with kwargs if present
        if "operation" in kwargs:
            operation = kwargs["operation"]
        if "MXC_POWER" in kwargs:
            MXC_POWER = kwargs["MXC_POWER"]
        
        power = 0.0
        if self.R == None or self.I == None:
            error_message = "Error: Values have not been set properly.\n"
            error_message += f"R = {self.R},  I = {self.I}"
            raise ValueError(error_message)
        else:
            ### factor = 2: incoming and outgoing current flows through both HEMT_Vd and HEMT_GND
            ### factor = 0.5: assuming joule heat flows equally into 50K and 4K thermal plate anchors
            power = 0.5 * 2 * self.I**2 * self.R
            return power

def SIS_current_split(SIS_I, num_LO_pair):
    # split_no: No. of wires in which LO current is split
    ## Currents
    SIS_up       = 25E-6  # 2023kojimaCharacterizationLownoiseSuperconductor
    SIS_up_vs1   = 0 
    SIS_up_vs2   = 0
    SIS_down     = 110E-6 # 2023kojimaCharacterizationLownoiseSuperconductor
    SIS_down_vs1 = 0
    SIS_down_vs2 = 0
    SIS_GND      = SIS_up + SIS_down
    SIS_LO       = SIS_I/ num_LO_pair # split current flowing through single wire 
    return [SIS_up, SIS_up_vs1, SIS_up_vs2, SIS_down, SIS_down_vs1, SIS_down_vs2, SIS_GND, SIS_LO, num_LO_pair]

class SIS_OHMIC_RESISTOR():
    def __init__(self,R, current_list, name):
        """
        R: float
            Resistance in ohms
        current: float
            LO current
        name : stf
            Name of the component

        Returns power in Watts due to ohmic (joule) heating
        """
        self.name = name
        self.R = R
        self.current_list= current_list # LO current
        
    def power_dissipation(self, *args, **kwargs):
        operation = None
        MXC_POWER = None
        num_LO_pair = 1
        
        # assign from positional args first
        if len(args) >= 1:
            operation = args[0]
        if len(args) >= 2:
            MXC_POWER = args[1]
        
        # override with kwargs if present
        if "operation" in kwargs:
            operation = kwargs["operation"]
        if "MXC_POWER" in kwargs:
            MXC_POWER = kwargs["MXC_POWER"]
        
        power = 0.0   
        SIS_up, SIS_up_vs1, SIS_up_vs2, SIS_down, SIS_down_vs1, SIS_down_vs2, SIS_GND, SIS_LO, num_LO_pair = self.current_list
        
        ### factor = 0.5: assuming joule heat flows equally into 50K and 4K thermal plate anchors
        P_up       = SIS_up**2       * self.R * 0.5
        P_up_vs1   = SIS_up_vs1**2   * self.R * 0.5
        P_up_vs2   = SIS_up_vs2**2   * self.R * 0.5
        P_down     = SIS_down**2     * self.R * 0.5
        P_down_vs1 = SIS_down_vs1**2 * self.R * 0.5
        P_down_vs2 = SIS_down_vs2**2 * self.R * 0.5
        P_GND      = SIS_GND**2      * self.R * 0.5
        ### factor = 2: current flows through both LO_in and LO_out
        P_LO = (num_LO_pair * 2) * SIS_LO**2 * self.R * 0.5 # ohmic dissipation through all LO wires  

        if self.R == None or self.current_list == None:
            error_message = "Error: Values have not been set properly.\n"
            error_message += f"R = {self.R},  current_list = {self.current_list}"
            raise ValueError(error_message)
        else:
            power = P_up + P_up_vs1 + P_up_vs2 + \
                    P_down + P_down_vs1 + P_down_vs2 + \
                    P_GND + P_LO
        return power

class BIAS_RESISTOR():
    def __init__(self, name):
        """
        R: float
            Resistance in ohms
        name : stf
            Name of the component

        Returns power in Watts due to biasing ONLY
        """
        self.name = name
        self.R = None
        self.I_BIAS= None

    def set_values(self, R, I_BIAS):
        self.R = R
        self.I_BIAS= I_BIAS
    
    def power_dissipation(self, operation, MXC_POWER):
        power = 0.0

        if self.R == None or self.I_BIAS == None:
            error_message = "Error: Values have not been set properly. Use set_values(R, I_BIAS) to set up the BIAS_RESISTOR object:\n"
            error_message += f"R = {self.R},  I_BIAS = {self.I_BIAS}"
            raise ValueError(error_message)
        else:
            power = self.R * self.I_BIAS**2

        return power

class RESISTOR_2Q():
    def __init__(self, name):
        """
        R: float
            Resistance in ohms
        name : stf
            Name of the component

        Returns power in Watts due to 2Q operation ONLY
        """
        self.name = name
        self.R = None
        self.I_2Q = None
    
    def set_values(self, R, I_2Q):
        self.R = R
        self.I_2Q= I_2Q
    
    def power_dissipation(self, operation, MXC_POWER):
        power = 0.0
        if self.R == None or self.I_2Q == None:
            error_message = "Error: Values have not been set properly. Use set_values(R, I_2Q) to set up the BIAS_RESISTOR object:\n"
            error_message += f"R = {self.R},  I_2Q = {self.I_2Q}"
            raise ValueError(error_message)
        else:
            power =   self.R * self.I_2Q**2
            
        return power

# Photomixer Class (Target)
#####################
class PhotoMixer():
    def __init__(self, reflection_coefficient, input_power_dict, name):
        """
        reflection_coefficient: float
            Power reflected (dissipated) as a fraction of input (optical) power, P_in

        input_power_dict: dict
            Dictionary for input (optical) power for each operation (1Q, 2Q and Readout)

        name : stf
            Name of the PhotoMixer component
        """
        self.input_power_dict = input_power_dict
        self.reflection_coefficient = reflection_coefficient
        self.name = name

    def power_dissipation(self, operation,  MXC_POWER):
        """
        Calculates the active heat load (P_act) in a photonic-link approach, 
        where all incident optical power is dissipated at millikelvin temperature.
        
        Parameters
        ----------
        operation : str
            Type　of operation i.e., 1Q, 2Q or Readout
        
        MXC_POWER : dict
            Power required at MXC for [cable_type][operation]
            
        Returns
        -------
        float
            The active heat load P_act (in watts).
        """
        P_operation = 0.0 # active power dissipated

        P_mu = None
        if operation == '1Q':
            P_in = dBm2Watts(self.input_power_dict['1Q'])
            P_operation = self.reflection_coefficient * P_in
        elif operation == '2Q':
            P_in = dBm2Watts(self.input_power_dict['2Q'])
            P_operation = self.reflection_coefficient * P_in
        elif operation == 'READOUT':
            P_in = dBm2Watts(self.input_power_dict['READOUT'])
            P_operation = self.reflection_coefficient * P_in
        return P_operation
#####################
        

# Photodetector Class
#####################
# """
# # "[2021lecocqControlReadoutSuperconducting - Methods: Primer on photodetection: Photocureent]"
# A photodiode can be modeled as a high impedance current source whose current is proportional to the incident optical power, $P_o$ .
# The responsivity of the photodiode $\mathcal{R}$, measured in $A W^{-1}$, determines the amount of current produced by the photodiode when optical power is incident on it.
# Thus, the photocurrent produced by the photodiode is

# $ I = \mathcal{R}  P_o$

# [//]: # "[2021lecocqControlReadoutSuperconducting - Methods: Active heat load]"
# When this photocurrent flows into an impedance $Z$, the microwave-frequency power is 

# $P_\mu = \frac{1}{2} I^2 . Z$

# Thus, combining the above two relations, we get

# $P_\mu = \frac{1}{2}( \mathcal{R}  P_o)^2 Z$

# Rearranging, we get
# $P_o = \sqrt{\frac{2 P_\mu}{ZR^2}}$

# In the photonic link approach, the optical power is fully dissipated as heat. Thus, if the qubit requires a microwave signal with power $P_\mu$, then the required incident optical power is $P_o$ (given by the above expression) which is dissipated as heat (i.e., the active load of the photodetector).
# """

class PhotoDetector():
    def __init__(self, Z, R, name):
        """
        Z : float
            Load impedance seen by the photodiode (in ohms).
        R : float
            Photodiode responsivity (in amperes per watt), i.e. A/W.
            A prefectly efficient photodiode has R = 1.2 Amp per Watt for a wavelength of 1490 nm
        MXC_POWER: dict
            Power required at the qubit for various operations (1Q, 2Q and Readout) in dBm
        name : stf
            Name of the Photodiode component
        """
        self.Z = Z
        self.R = R
        self.name = name
    
    def power_dissipation(self, operation, MXC_POWER):
        """
        Calculates the active heat load (P_act) in a photonic-link approach, 
        where all incident optical power is dissipated at millikelvin temperature.
        
        Parameters
        ----------
        operation : str
            Type　of operation i.e., 1Q, 2Q or Readout

        MXC_POWER : dict
            Power required at MXC for [cable_type][operation]
        Returns
        -------
        float
            The active heat load P_act (in watts).
        """
        power = 0.0
        # P_mu = Desired microwave power at the qubit (in watts).
        P_mu = None
        if operation == '1Q':
            P_mu = dBm2Watts(MXC_POWER['DRIVE']['1Q'])
        elif operation == '2Q':
            P_mu = dBm2Watts(MXC_POWER['DRIVE']['2Q'])
        elif operation == 'READOUT':
            P_mu = dBm2Watts(MXC_POWER['READOUT_PIN']['READOUT'])
        
        # Implements: P_act = sqrt( (2 * P_mu) / (Z * R^2) )
        if P_mu is not None:
            power = np.sqrt(2.0 * P_mu / self.Z) / self.R

        return power

################################################################################
      
################################################################################
# JJ Detector Integrated with Photomixer
#################
class JJ_Detector():
    def __init__(self, power, name):
        self.name = name
        self.power = power

    def power_dissipation(self, *args, **kwargs):
        operation = None
        MXC_POWER = None
        
        # assign from positional args first
        if len(args) >= 1:
            operation = args[0]
        if len(args) >= 2:
            MXC_POWER = args[1]
        
        # then override with kwargs if present
        if "operation" in kwargs:
            operation = kwargs["operation"]
        if "MXC_POWER" in kwargs:
            MXC_POWER = kwargs["MXC_POWER"]
            
        return self.power # dissipative power in Watts due to biasing (always ON)
################################################################################
      
################################################################################
# JJ Detector Integrated with Photomixer
#################
class CTRL():
    def __init__(self, power, name):
        self.name = name
        self.power = power

    def power_dissipation(self, *args, **kwargs):
        operation = None
        MXC_POWER = None
        
        # assign from positional args first
        if len(args) >= 1:
            operation = args[0]
        if len(args) >= 2:
            MXC_POWER = args[1]
        
        # then override with kwargs if present
        if "operation" in kwargs:
            operation = kwargs["operation"]
        if "MXC_POWER" in kwargs:
            MXC_POWER = kwargs["MXC_POWER"]
            
        return self.power # dissipative power in Watts due to biasing (always ON)
################################################################################

# Component Instantiations
def create_comp_instance(comp_type_str):
    if comp_type_str == "HEMT_8G":
        # HEMT Amplifier Instantiation
        # https://lownoisefactory.com/product/lnf-lnc4_8f/
        HEMT_V = 0.6 # Volts
        HEMT_I = 13E-3 # Amperes
        HEMT = AMPLIFIER(HEMT_V, HEMT_I, comp_type_str)
        return HEMT
    elif comp_type_str == "HEMT_8G_HP":
        # HEMT Amplifier Instantiation
        # https://lownoisefactory.com/product/lnf-lnc4_8g/
        HEMT_V = 1 # Volts
        HEMT_I = 20E-3 # Amperes
        HEMT = AMPLIFIER(HEMT_V, HEMT_I, comp_type_str)
        return HEMT
    elif comp_type_str == "HEMT_8G_LP":
        # HEMT Amplifier Instantiation
        # https://lownoisefactory.com/product/lnf-lnc4_8g/
        HEMT_V = 0.1 # Volts
        HEMT_I = 3E-3 # Amperes
        HEMT = AMPLIFIER(HEMT_V, HEMT_I, comp_type_str)
        return HEMT
    elif comp_type_str == "ULP_HEMT":
        # HEMT Amplifier Instantiation
        # 2024zengSubmWCryogenicInP
        HEMT_V = 0.08 # Volts
        HEMT_I = 1.5E-3 + 1E-3 # Amperes
        HEMT = AMPLIFIER(HEMT_V, HEMT_I, comp_type_str)
        return HEMT
    # elif comp_type_str == "HEMT_LP":
    #     # HEMT Amplifier Instantiation
    #     # 2024zengSubmWCryogenicInP
    #     # Real values from Fig. 13
    #     # (0.06 V * 1 mA) + (0.05 V * 0.8 mA) = 100 uW
    #     # Equivalent values
    #     HEMT_V = 10E-3 # Volts
    #     HEMT_I = 10E-3 # Amperes
    #     HEMT = AMPLIFIER(HEMT_V, HEMT_I, comp_type_str)
    #     return HEMT 
    # elif comp_type_str == "HEMT_8C":
    #     # HEMT Amplifier Instantiation
    #     # LNF-LNC4_8C [2019krinnerEngineeringCryogenicSetups]
    #     # https://lownoisefactory.com/wp-content/uploads/2022/03/lnf-lnc4_8c.pdf
    #     HEMT_GAIN = 42 # in dB 
    #     no_of_wires = 2 # (Vd, Gnd)
    #     HEMT_R = no_of_wires * 0 # Ohms, resistance of biasing wire
    #     HEMT_V = 0.7 # Volts
    #     HEMT_I = 15E-3 # Amperes
    #     HEMT_PWR = HEMT_V * HEMT_I + HEMT_I**2 * HEMT_R
    #     HEMT = AMPLIFIER(HEMT_GAIN, HEMT_PWR, comp_type_str)
    #     return HEMT
    # elif comp_type_str == "HEMT_Nitsuki_9848XD":
    #     # HEMT Amplifier Instantiation
    #     # https://nitsuki.com/pdf/microwave_pdf/9848xd.pdf
    #     HEMT_GAIN = 32 # in dB 
    #     HEMT_PWR = 10E-3 
    #     HEMT = AMPLIFIER(HEMT_GAIN, HEMT_PWR, comp_type_str)
    #     return HEMT
    elif comp_type_str == "SIS":
        # SIS Amplifier Instantiation      
        # Active Power [2025murayamaFabricationEvaluationWaveguide]
        SIS_V = 305E-6 # Volts (Local oscillator)
        SIS_I = 22E-3 # Amperes
        SIS = AMPLIFIER(SIS_V, SIS_I, comp_type_str)
        return SIS
    
    elif comp_type_str == "PD":
        # Photodetector Instantiation
        PD = PhotoDetector(Z = 10_000,
                            R = 1,
                            name = comp_type_str)
        return PD
        
    elif comp_type_str == "PM_v1":
        # Assuming Efficiency/Input Optical Power = 1000%/W
        # PhotoMixer Instantiation (Current Version)
        PM = PhotoMixer(reflection_coefficient = 0.01, 
                        input_power_dict = {'1Q': -20.5, '2Q': -18, 'READOUT': -45},
                        name = comp_type_str)
        return PM
    elif comp_type_str == "PM_v2":
        # PhotoMixer Instantiation (Target Version)
        PM = PhotoMixer(reflection_coefficient = 0.005, 
                        input_power_dict = {'1Q': -20.5, '2Q': -18, 'READOUT': -45},
                        name = comp_type_str)
        return PM
    elif comp_type_str == "PM_v3":
        # PhotoMixer Instantiation (Super Target Version)
        PM = PhotoMixer(reflection_coefficient = 0.001, 
                        input_power_dict = {'1Q': -20.5, '2Q': -18, 'READOUT': -45},
                        name = comp_type_str)
        return PM
           
    elif comp_type_str == "BIAS_RESISTOR_4K":
        BIAS_RESISTOR_4K = BIAS_RESISTOR(comp_type_str)
        return BIAS_RESISTOR_4K
    elif comp_type_str == "BIAS_RESISTOR_Still":
        BIAS_RESISTOR_Still = BIAS_RESISTOR(comp_type_str)
        return BIAS_RESISTOR_Still
    elif comp_type_str == "BIAS_RESISTOR_CP":
        BIAS_RESISTOR_CP = BIAS_RESISTOR(comp_type_str)
        return BIAS_RESISTOR_CP
    elif comp_type_str == "BIAS_RESISTOR_MXC":
        BIAS_RESISTOR_MXC = BIAS_RESISTOR(comp_type_str)
        return BIAS_RESISTOR_MXC
    elif comp_type_str == "RESISTOR_2Q_4K":
        RESISTOR_2Q_4K = RESISTOR_2Q(comp_type_str)
        return RESISTOR_2Q_4K
    elif comp_type_str == "RESISTOR_2Q_Still":
        RESISTOR_2Q_Still = RESISTOR_2Q(comp_type_str)
        return RESISTOR_2Q_Still
    elif comp_type_str == "RESISTOR_2Q_CP":
        RESISTOR_2Q_CP = RESISTOR_2Q(comp_type_str)
        return RESISTOR_2Q_CP
    elif comp_type_str == "RESISTOR_2Q_MXC":
        RESISTOR_2Q_MXC = RESISTOR_2Q(comp_type_str)
        return RESISTOR_2Q_MXC

    elif comp_type_str == "JJ_Detector":
        # Assuming same as SIS-amplifier
        SIS_V = 305E-6 # Volts (Local oscillator)
        SIS_I = 22E-3 # Amperes
        JJ_D_PWR = SIS_V * SIS_I   
        JJ_D = JJ_Detector(JJ_D_PWR, comp_type_str)
        return JJ_D
    elif comp_type_str == "CMOS_CTRL":
        # Assuming same as SIS-amplifier
        CMOS_CTRL = CTRL(JJ_D_PWR, comp_type_str)
        return JJ_D
        
    else:
        return None
#####################################################
def get_comp_config(comp_config_names):
    comp_config = {}
    for cable_type, config in comp_config_names.items():
        comp_config[cable_type]={}
        for temp_stage, comp_names in config.items():
            if comp_names is not None:
                if isinstance(comp_names, list):
                    for comp_name in comp_names:
                        comp_config[cable_type][temp_stage] = [create_comp_instance(comp_name) for comp_name in comp_names]
                else:
                    comp_config[cable_type][temp_stage] = [create_comp_instance(comp_names)]
            else:
                comp_config[cable_type][temp_stage] = None
    return comp_config

