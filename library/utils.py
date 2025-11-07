import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import yaml
from pathlib import Path
from typing import Any, Dict, List, Union

def df_float_formatter(x):
    if x in (0, 0.0, None) or pd.isna(x):
        return " "
    return f"{x:.2e}" if isinstance(x, float) else str(x)

def df_int_formatter(x):
    if x in (0, 0.0, None) or pd.isna(x):
        return " "
    return f"{int(round(x))}"

def _process_commas_recursively(obj: Any) -> Any:
    """
    Recursively convert comma-separated strings into lists.
    Leaves None, numbers, and bools as-is; trims whitespace on strings.
    """
    if isinstance(obj, dict):
        return {k: _process_commas_recursively(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_process_commas_recursively(v) for v in obj]
    if isinstance(obj, str):
        s = obj.strip()
        if "," in s:
            parts = [p.strip() for p in s.split(",")]
            # Only treat as list if there are at least 2 non-empty items
            if sum(1 for p in parts if p != "") > 1:
                return parts
        return s
    return obj

def load_config(config_file: str|Path) -> dict:
    """
    Load a YAML config file, then recursively convert comma-separated
    strings into lists (e.g., 'A, B' -> ['A', 'B']). YAML null -> None.
    """
    path = Path(config_file)
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return _process_commas_recursively(data)


def check_activation_matrix(activation_matrix, operations):
    """
    Checks that every operation specified in the activation_matrix exists in the operations list.
    
    Parameters:
        activation_matrix (dict): Dictionary whose values are lists of operations.
        operations (list): List of allowed operations.
    
    Returns:
        bool: True if all operations are valid, otherwise raises a ValueError.
        
    Raises:
        ValueError: If any operation in the activation matrix is not in the allowed operations.
    """
    missing_ops = []  # To collect any invalid operation along with its key.
    
    # Iterate through each key and its associated list of operations.
    for cable, op_list in activation_matrix.items():
        for op in op_list:
            if op not in operations:
                missing_ops.append((cable, op))
    
    if missing_ops:
        error_message = "Error: The following operations are not allowed:\n"
        for cable, op in missing_ops:
            error_message += f" - Operation '{op}' found in '{cable}' is not in allowed list {operations}\n"
        raise ValueError(error_message)
    
    return True


def watts_to_dbm(power_watts):
    # Avoid taking log of zero or negative numbers by setting them to NaN
    if power_watts <= 0:
        return np.nan
    return 10 * np.log10(power_watts * 1000)

def dBm2Watts(dBm):
    """
    Converts dBm to Watts

    Parameters
    ----------
    dBm: Power in dBm

    Returns
    -------
    Equivalent power in Watts
    """

    if dBm is not None:
        return 10 ** ((dBm-30)/10)
    else:
        return 0


# https://stackoverflow.com/questions/47222585/matplotlib-generic-colormap-from-tab10
def categorical_cmap(nc, nsc, cmap="tab10", continuous=False):
    """
    nc: no. of categories
    nsc: no. of subcategories
    """
    if nc > plt.get_cmap(cmap).N:
        raise ValueError("Too many categories for colormap.")
    if continuous:
        ccolors = plt.get_cmap(cmap)(np.linspace(0,1,nc))
    else:
        ccolors = plt.get_cmap(cmap)(np.arange(nc, dtype=int))
    cols = np.zeros((nc*nsc, 3))
    for i, c in enumerate(ccolors):
        chsv = matplotlib.colors.rgb_to_hsv(c[:3])
        arhsv = np.tile(chsv,nsc).reshape(nsc,3)
        arhsv[:,1] = np.linspace(chsv[1],0.25,nsc)
        arhsv[:,2] = np.linspace(chsv[2],1,nsc)
        rgb = matplotlib.colors.hsv_to_rgb(arhsv)
        cols[i*nsc:(i+1)*nsc,:] = rgb       
    cmap = matplotlib.colors.ListedColormap(cols)
    return cmap

def get_color_dict():
    labels = [
        ('DRIVE', 'PASSIVE', 'IDLE'),
        ('DRIVE', 'ATT', '1Q'),
        ('DRIVE', 'ATT', '2Q'),
        ('DRIVE', 'ATT', 'READOUT'),
        
        ('FLUX_BIAS', 'PASSIVE', 'IDLE'),
        ('FLUX_BIAS', 'BIAS_RESISTOR_4K', 'IDLE'),
        
        ('COUPLER', 'PASSIVE', 'IDLE'),
        ('COUPLER', 'RESISTOR_2Q_4K', '2Q'),
        
        ('PUMP', 'PASSIVE', 'IDLE'),
        ('PUMP', 'ATT', 'READOUT'),
        
        ('READOUT_PIN', 'PASSIVE', 'IDLE'),
        ('READOUT_PIN', 'ATT', 'READOUT'),
        ('READOUT_PIN', 'PD', 'READOUT'), 
        ('READOUT_PIN', 'PM_v1', 'READOUT'),
        ('READOUT_PIN', 'PM_v2', 'READOUT'),
        ('READOUT_PIN', 'PM_v3', 'READOUT'),
        
        ('READOUT_POUT', 'PASSIVE', 'IDLE') ,
        
        ('AMP_BIAS', 'PASSIVE', 'IDLE') ,
        ('AMP_BIAS', 'AMP', 'IDLE'),
        ('AMP_BIAS', 'AMP_OHMIC', 'IDLE'),

        ('JJ_BIAS', 'PASSIVE', 'IDLE') ,
        
        
        ('DRIVE', 'PD', '1Q'),
        ('DRIVE', 'PM_v1', '1Q'),
        ('DRIVE', 'PM_v2', '1Q'),
        ('DRIVE', 'PM_v3', '1Q'),

        ('JJ_BIAS', 'JJ_Detector', 'IDLE'),
        
        ('DRIVE', 'PD', '2Q'),
        ('DRIVE', 'PM_v1', '2Q'),
        ('DRIVE', 'PM_v2', '2Q'),
        ('DRIVE', 'PM_v3', '2Q'),
        
        ('DRIVE', 'PM_v1', 'READOUT'),
        ('DRIVE', 'PM_v2', 'READOUT'),
        ('DRIVE', 'PM_v3', 'READOUT'),
        ]

    colors = categorical_cmap(nc=7, 
                              nsc=int(np.ceil(len(labels)/7)), 
                              cmap="tab10")
    color_dict = {}
    for i, label in enumerate(labels):
        color_dict[label] = colors(i)

    return color_dict

def get_OPERATION_COUNTS(OPERATIONS, QUBIT_TYPES, WORKLOAD):
    OPERATIONS_Spec= WORKLOAD["OPERATIONS_Spec"]
    
    # Workload requires a certain number of qubits.
    # Given the system qubit size, calculate the number of qubit groups
    no_of_groups = {}
    for qubit_type in ["DATA", "ANCILLA"]:
        no_of_groups[qubit_type] = QUBIT_TYPES[qubit_type]/WORKLOAD[qubit_type]
        if not no_of_groups[qubit_type].is_integer():
            error_message = f"Number of Qubit Groups = {no_of_groups[qubit_type]} is not an integer."
            raise ValueError(error_message)
    
    # Calculate the different types of operations and the total number of operations for a given workload
    OPERATION_COUNTS = {}
    for qubit_type, count_dict in OPERATIONS_Spec.items():
        OPERATION_COUNTS[qubit_type] = {}
        for operation, operation_count in count_dict.items():
            OPERATION_COUNTS[qubit_type][operation] = operation_count * no_of_groups[qubit_type]
    
    # Sum the subkey values into a new dictionary
    total_operations = {}
    for operation in OPERATIONS:
        total_operations[operation] = 0
        for qubit_type in OPERATION_COUNTS.keys():
            total_operations[operation] = total_operations[operation] + OPERATION_COUNTS[qubit_type][operation]
    
    if "COUPLER" in QUBIT_TYPES:
        OPERATION_COUNTS["COUPLER"] = {}
        for op in OPERATIONS:
            OPERATION_COUNTS["COUPLER"][op] = 0.0
        OPERATION_COUNTS["COUPLER"]["2Q"] = OPERATION_COUNTS["DATA"]["2Q"] + OPERATION_COUNTS["ANCILLA"]["2Q"] 
    
    OPERATION_COUNTS["TOTAL"] = total_operations
    return OPERATION_COUNTS


def get_DUTY_CYCLES(OPERATIONS, OPERATION_COUNTS, LATENCY, QUBIT_TYPES):
    # Check that OPERATION_COUNTS has the same or subset of keys in the first level as QUBIT_TYPES
    if set(OPERATION_COUNTS.keys()) <= set(QUBIT_TYPES.keys()):
        raise ValueError(
            f"Top-level keys mismatch:\n"
            f"OPERATION_COUNTS keys: {set(OPERATION_COUNTS.keys())}\n"
            f"QUBIT_TYPES keys: {set(QUBIT_TYPES.keys())}"
        )
    
    # Check that OPERATION_COUNTS has the same keys in the second level as OPERATIONS
    expected_op_keys = set(OPERATIONS)
    
    for label, op_dict in OPERATION_COUNTS.items():
        if set(op_dict.keys()) != expected_op_keys:
            raise ValueError(
                f"Second-level keys mismatch for '{label}':\n"
                f"Expected: {expected_op_keys}\n"
                f"Found: {set(op_dict.keys())}"
            )

    # First compute each qubit type’s duty cycles
    OPERATION_DUTY_CYCLES = {}
    for qubit_type, operation_count_dict in OPERATION_COUNTS.items():
        OPERATION_DUTY_CYCLES[qubit_type] = {}
        for operation, count in operation_count_dict.items():
            OPERATION_DUTY_CYCLES[qubit_type][operation] = OPERATION_COUNTS[qubit_type][operation] * LATENCY[operation] / LATENCY["TOTAL"]

    # Then do a weighted average based on how many data vs. ancilla qubits
    AVG_OPERATION_DUTY_CYCLES = {
        op: np.average(
            [OPERATION_DUTY_CYCLES[qtype][op] for qtype in QUBIT_TYPES],
            weights=[QUBIT_TYPES[qtype] for qtype in QUBIT_TYPES]
        )
        for op in OPERATIONS
    }

    return OPERATION_DUTY_CYCLES, AVG_OPERATION_DUTY_CYCLES

