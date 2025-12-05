import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import yaml
from pathlib import Path
from typing import Any, Dict, List, Union

# Define fontstyles
from matplotlib.font_manager import FontProperties
title_font = FontProperties(family='Arial',size=10, weight='bold')
axis_label_font = FontProperties(family='Arial',size=9, weight='bold')
tick_label_font = FontProperties(family='Arial',size=8, weight='light')
legend_font = FontProperties(family='Arial',size=5, weight='light')
text_font = FontProperties(family='Arial',size=7, weight='light')

fontstyle = [title_font, axis_label_font, tick_label_font, legend_font, text_font]

# Style map: a dict keyed by (Cable, Component, Operation) -> {'color': ..., 'hatch': ...}
style_map = {
    # --- DRIVE cable ---
    ('DRIVE', 'PASSIVE', 'IDLE'): {'color': '#1f77b4', 'hatch': ''},     # Tab20 dark blue (#1f77b4)
    ('DRIVE', 'ATT', '1Q'):        {'color': '#9ecae1', 'hatch': '++++'},   # Tab20 light blue (#9ecae1)
    ('DRIVE', 'ATT', '2Q'):        {'color': '#9ecae1', 'hatch': '////'},   # same light blue, (#9ecae1)
    ('DRIVE', 'PD', '1Q'):         {'color': '#17becf', 'hatch': '++++'}, # Tab20 cyan (#17becf)
    ('DRIVE', 'PD', '2Q'):         {'color': '#17becf', 'hatch': '////'}, # Tab20 cyan (#17becf)

    # --- FLUX_BIAS cable ---
    ('FLUX_BIAS', 'PASSIVE', 'IDLE'): {'color': '#8c564b', 'hatch': ''},     # Tab20 brown (#8c564b)
    ('FLUX_BIAS', 'BIAS_RESISTOR_4K', 'IDLE'): {'color': '#c49c94', 'hatch': 'xxx'},   # Tab20 light brown (#c49c94)

    # --- COUPLER cable ---
    ('COUPLER', 'PASSIVE', 'IDLE'): {'color': '#bcbd22', 'hatch': ''},     # Tab20 olive (#bcbd22),
    ('COUPLER', 'RESISTOR_2Q_4K', '2Q'): {'color': '#dbdb8d', 'hatch': 'xxx'},   # Tab20 light olive (#dbdb8d),
    
    # --- PUMP cable ---
    ('PUMP', 'PASSIVE', 'IDLE'):   {'color': '#ff7f0e', 'hatch': ''},    # Tab20 light orange (#ff7f0e)
    ('PUMP', 'ATT', 'READOUT'):    {'color': '#ffbb78', 'hatch': '|||'},   # Tab20 dark orange (#ffbb78)

    # --- READOUT_PIN cable ---
    ('READOUT_PIN', 'PASSIVE', 'IDLE'):  {'color': '#2ca02c', 'hatch': ''},  # Tab20 dark green (#2ca02c)
    ('READOUT_PIN', 'ATT', 'READOUT'):   {'color': '#98df8a', 'hatch': '|||'}, # Tab20 light green (#98df8a)
    ('READOUT_PIN', 'PD', 'READOUT'): {'color': '#17becf', 'hatch': '|||'}, # Tab20 cyan (#17becf)

    # --- READOUT_POUT cable ---
    ('READOUT_POUT', 'PASSIVE', 'IDLE'): {'color': '#d62728', 'hatch': ''},  # Tab20 dark red (#d62728)

    # --- AMP_BIAS cable ---
    ('AMP_BIAS', 'PASSIVE', 'IDLE'):     {'color': '#9467bd', 'hatch': ''},  # Tab20 dark purple (#9467bd)
    ('AMP_BIAS', 'AMP', 'IDLE'):     {'color': '#c5b0d5', 'hatch': 'xxx'},  # Tab20 light purple (#c5b0d5)
    ('AMP_BIAS', 'AMP_OHMIC', 'IDLE'):    {'color': '#c5b0d5', 'hatch': '...'},  # same dark purple
}

def plot_heat_load(df_plot, title, config_name, possible_physical_qubits, legend_bbox=(1.0, 1.0)):
    # # Change amplifier name and ohmic resistor to generic labels
    # --- Generate new column labels ---
    renamed_labels = [
        (a, 'AMP_OHMIC', c) if a == 'AMP_BIAS' and c == 'IDLE' and 'ohmic' in b.lower()
        else (a, 'PASSIVE', c)  if a == 'AMP_BIAS' and b == 'PASSIVE' and c == 'IDLE'
        else (a, 'AMP', c)  if a == 'AMP_BIAS' and c == 'IDLE'
        else (a, b, c)
        for a, b, c in df_plot.columns
    ]
    
    # --- Apply the renamed columns to df_plot ---
    df_plot.columns = pd.MultiIndex.from_tuples(renamed_labels, names=df_plot.columns.names)
    
    # 1) Decide the plotting order of stacks (columns)
    # Reorder columns: PASSIVE first
    original_columns = df_plot.columns.tolist()
    passive_cols = [col for col in df_plot.columns if col[1] == 'PASSIVE']
    active_cols  = [col for col in df_plot.columns if col[1] != 'PASSIVE']
    reordered_columns = passive_cols + active_cols
    
    # Reorder df_plot accordingly
    df_plot = df_plot[reordered_columns]
    cols = list(df_plot.columns)
    
    # Index: temperature stages (e.g., "4K", "Still", "CP", "MXC")
    # Columns: MultiIndex with levels (Cable, Component, Operation)
    
    # 2) (Optional but helpful) ensure the columns are a proper 3-level MultiIndex
    # If they already are, this does nothing.
    if not isinstance(df_plot.columns, pd.MultiIndex) or df_plot.columns.nlevels != 3:
        raise ValueError("dataframe columns must be a 3-level MultiIndex: (Cable, Component, Operation)")
    
    
    
    
    # 4) Define fallbacks (only used if a stack tuple isn’t in style_map)
    # fallback_colors = plt.cm.tab20.colors  # a nice, long qualitative palette
    # fallback_hatches = ['/', '\\', 'x', '-', '+', 'o', 'O', '.', '*']  # repeats cyclically
    fallback_color = 'white' 
    fallback_hatch = '//'   
    
    # 5) X positions and labels (temperature stages)
    x = np.arange(len(df_plot.index))
    # xticklabels = df_plot.index.astype(str)
    # xticklabels = ["4K", "Still (1K)", "CP (100 mK)", "MXC (10 mK)" ]
    xticklabels = ["4K", "Still", "CP", "MXC" ]
    
    # 6) Create the figure/axes
    # IEEE TQE Guidelines
    # Single column: 3.5" (wide) x 8.5" (height)
    # Double column: 7.16" (wide) x 8.5" (height)
    fig, ax = plt.subplots(figsize=(3.5, 3))
    
    # 7) Build the stacked bars
    bottom = np.zeros(len(x), dtype=float)
    
    for i, col in enumerate(cols):
        values = df_plot[col].astype(float).values
    
        # pull style from style_map if present, else fallback
        style = style_map.get(col, {})
        color = style.get('color', fallback_color)
        hatch = style.get('hatch', fallback_hatch)
    
        # readable label in legend
        label = f"{col[0]} | {col[1]} | {col[2]}"
    
        bars = ax.bar(
            x,
            values,
            bottom=bottom,
            label=label,
            color=color,
            edgecolor='black',
            linewidth=0.4
        )
        # apply hatch to each rectangle
        for b in bars:
            b.set_hatch(hatch)
    
        bottom += values  # update stack baseline

    # Display no. of supported qubits on top of the bar
    totals = df_plot.sum(axis=1)  # Sum over column. Get bar height
    for i, total in enumerate(totals):
        ax.text(i, total, f'{possible_physical_qubits[i]}', ha='center', va='bottom', fontproperties=text_font)
    
    # Draw horizantal line at y=1
    ax.axhline(y=1, color='k', linestyle='--',linewidth=0.6)
    
    # 8) Axis cosmetics
    # Set titles 
    ax.set_title(title, fontproperties=title_font)
    ax.set_xlabel("Temperature Stage", fontproperties=axis_label_font)
    ax.set_ylabel("Normalized Heat Load", fontproperties=axis_label_font)
    ax.set_xticks(x)
    ax.set_xticklabels(xticklabels, fontproperties=tick_label_font, rotation=0)
    for label in ax.get_yticklabels() :
        label.set_fontproperties(tick_label_font)
    ax.set_ylim(0, max(totals) + 1.5) # Set max y-value to be slightly higher than the tallest bar
    
    # 9) Legend: shrink and place outside
    ax.legend(ncol=1, 
              bbox_to_anchor=legend_bbox, 
              loc='upper right',
              prop=legend_font,
              frameon=False,
              borderaxespad=0.)
    
    ax.margins(x=0.02)
    plt.tight_layout()
    plt.savefig(f"./{config_name}_THL.png",dpi=600)
    plt.show()

    # Return the plot dataframe
    df_plot.to_pickle(config_name+".pkl")  # save dataframe

# Backup
# def plot_heat_load(df_plot, title, config_name, possible_physical_qubits, legend_bbox=(1.0, 1.0)):
#     # # Change amplifier name and ohmic resistor to generic labels
#     # --- Generate new column labels ---
#     renamed_labels = [
#         (a, 'AMP_OHMIC', c) if a == 'AMP_BIAS' and c == 'IDLE' and 'ohmic' in b.lower()
#         else (a, 'PASSIVE', c)  if a == 'AMP_BIAS' and b == 'PASSIVE' and c == 'IDLE'
#         else (a, 'AMP', c)  if a == 'AMP_BIAS' and c == 'IDLE'
#         else (a, b, c)
#         for a, b, c in df_plot.columns
#     ]
    
#     # --- Apply the renamed columns to df_plot ---
#     df_plot.columns = pd.MultiIndex.from_tuples(renamed_labels, names=df_plot.columns.names)
    
#     # 1) Decide the plotting order of stacks (columns)
#     # Reorder columns: PASSIVE first
#     original_columns = df_plot.columns.tolist()
#     passive_cols = [col for col in df_plot.columns if col[1] == 'PASSIVE']
#     active_cols  = [col for col in df_plot.columns if col[1] != 'PASSIVE']
#     reordered_columns = passive_cols + active_cols
    
#     # Reorder df_plot accordingly
#     df_plot = df_plot[reordered_columns]
#     cols = list(df_plot.columns)
    
#     # Index: temperature stages (e.g., "4K", "Still", "CP", "MXC")
#     # Columns: MultiIndex with levels (Cable, Component, Operation)
    
#     # 2) (Optional but helpful) ensure the columns are a proper 3-level MultiIndex
#     # If they already are, this does nothing.
#     if not isinstance(df_plot.columns, pd.MultiIndex) or df_plot.columns.nlevels != 3:
#         raise ValueError("dataframe columns must be a 3-level MultiIndex: (Cable, Component, Operation)")
    
    
#     # 3) Style map: a dict keyed by (Cable, Component, Operation) -> {'color': ..., 'hatch': ...}
#     style_map = {
#         # --- DRIVE cable ---
#         ('DRIVE', 'PASSIVE', 'IDLE'): {'color': '#1f77b4', 'hatch': ''},     # Tab20 dark blue (#1f77b4)
#         ('DRIVE', 'ATT', '1Q'):        {'color': '#9ecae1', 'hatch': '++++'},   # Tab20 light blue (#9ecae1)
#         ('DRIVE', 'ATT', '2Q'):        {'color': '#9ecae1', 'hatch': '////'},   # same light blue, (#9ecae1)
#         ('DRIVE', 'PD', '1Q'):         {'color': '#17becf', 'hatch': '++++'}, # Tab20 cyan (#17becf)
#         ('DRIVE', 'PD', '2Q'):         {'color': '#17becf', 'hatch': '////'}, # Tab20 cyan (#17becf)

#         # --- FLUX_BIAS cable ---
#         ('FLUX_BIAS', 'PASSIVE', 'IDLE'): {'color': '#8c564b', 'hatch': ''},     # Tab20 brown (#8c564b)
#         ('FLUX_BIAS', 'BIAS_RESISTOR_4K', 'IDLE'): {'color': '#c49c94', 'hatch': 'xxx'},   # Tab20 light brown (#c49c94)

#         # --- COUPLER cable ---
#         ('COUPLER', 'PASSIVE', 'IDLE'): {'color': '#bcbd22', 'hatch': ''},     # Tab20 olive (#bcbd22),
#         ('COUPLER', 'RESISTOR_2Q_4K', '2Q'): {'color': '#dbdb8d', 'hatch': 'xxx'},   # Tab20 light olive (#dbdb8d),
        
#         # --- PUMP cable ---
#         ('PUMP', 'PASSIVE', 'IDLE'):   {'color': '#ff7f0e', 'hatch': ''},    # Tab20 light orange (#ff7f0e)
#         ('PUMP', 'ATT', 'READOUT'):    {'color': '#ffbb78', 'hatch': '|||'},   # Tab20 dark orange (#ffbb78)
    
#         # --- READOUT_PIN cable ---
#         ('READOUT_PIN', 'PASSIVE', 'IDLE'):  {'color': '#2ca02c', 'hatch': ''},  # Tab20 dark green (#2ca02c)
#         ('READOUT_PIN', 'ATT', 'READOUT'):   {'color': '#98df8a', 'hatch': '|||'}, # Tab20 light green (#98df8a)
#         ('READOUT_PIN', 'PD', 'READOUT'): {'color': '#17becf', 'hatch': '|||'}, # Tab20 cyan (#17becf)
    
#         # --- READOUT_POUT cable ---
#         ('READOUT_POUT', 'PASSIVE', 'IDLE'): {'color': '#d62728', 'hatch': ''},  # Tab20 dark red (#d62728)
    
#         # --- AMP_BIAS cable ---
#         ('AMP_BIAS', 'PASSIVE', 'IDLE'):     {'color': '#9467bd', 'hatch': ''},  # Tab20 dark purple (#9467bd)
#         ('AMP_BIAS', 'AMP', 'IDLE'):     {'color': '#c5b0d5', 'hatch': 'xxx'},  # Tab20 light purple (#c5b0d5)
#         ('AMP_BIAS', 'AMP_OHMIC', 'IDLE'):    {'color': '#c5b0d5', 'hatch': '...'},  # same dark purple
#     }
    
#     # 4) Define fallbacks (only used if a stack tuple isn’t in style_map)
#     # fallback_colors = plt.cm.tab20.colors  # a nice, long qualitative palette
#     # fallback_hatches = ['/', '\\', 'x', '-', '+', 'o', 'O', '.', '*']  # repeats cyclically
#     fallback_color = 'white' 
#     fallback_hatch = '//'   
    
#     # 5) X positions and labels (temperature stages)
#     x = np.arange(len(df_plot.index))
#     # xticklabels = df_plot.index.astype(str)
#     xticklabels = ["4K", "Still (1K)", "CP (100 mK)", "MXC (10 mK)" ]

    
#     # 6) Create the figure/axes
#     fig, ax = plt.subplots(figsize=(7, 5))
    
#     # 7) Build the stacked bars
#     bottom = np.zeros(len(x), dtype=float)
    
#     for i, col in enumerate(cols):
#         values = df_plot[col].astype(float).values
    
#         # pull style from style_map if present, else fallback
#         style = style_map.get(col, {})
#         color = style.get('color', fallback_color)
#         hatch = style.get('hatch', fallback_hatch)
    
#         # readable label in legend
#         label = f"{col[0]} | {col[1]} | {col[2]}"
    
#         bars = ax.bar(
#             x,
#             values,
#             bottom=bottom,
#             label=label,
#             color=color,
#             edgecolor='black',
#             linewidth=0.6
#         )
#         # apply hatch to each rectangle
#         for b in bars:
#             b.set_hatch(hatch)
    
#         bottom += values  # update stack baseline

#     # Display no. of supported qubits on top of the bar
#     totals = df_plot.sum(axis=1)  # Sum over column. Get bar height
#     for i, total in enumerate(totals):
#         ax.text(i, total, f'{possible_physical_qubits[i]}', ha='center', va='bottom', fontsize=10)
    
#     # Draw horizantal line at y=1
#     ax.axhline(y=1, color='k', linestyle='--')
    
#     # 8) Axis cosmetics
#     # Set titles
#     ax.set_title(title)
#     ax.set_xlabel("Temperature Stage", fontsize = 'large',weight = 'bold')
#     ax.set_ylabel("Normalized Heat Load", fontsize = 'large',weight = 'bold')
#     ax.set_xticks(x)
#     ax.set_xticklabels(xticklabels)
#     ax.set_ylim(0, max(totals) + 1.5) # Set max y-value to be slightly higher than the tallest bar
    
#     # 9) Legend: shrink and place outside if many stacks
#     ax.legend(ncol=1, 
#               bbox_to_anchor=legend_bbox, 
#               loc='upper right',
#               fontsize='small',
#               frameon=False,
#               borderaxespad=0.)
    
#     ax.margins(x=0.02)
#     plt.tight_layout()
#     plt.savefig(f"./{config_name}_THL.png",dpi=300)
#     plt.show()

#     # Return the plot dataframe
#     df_plot.to_pickle(config_name+".pkl")  # save dataframe
    

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


# # https://stackoverflow.com/questions/47222585/matplotlib-generic-colormap-from-tab10
# def categorical_cmap(nc, nsc, cmap="tab10", continuous=False):
#     """
#     nc: no. of categories
#     nsc: no. of subcategories
#     """
#     if nc > plt.get_cmap(cmap).N:
#         raise ValueError("Too many categories for colormap.")
#     if continuous:
#         ccolors = plt.get_cmap(cmap)(np.linspace(0,1,nc))
#     else:
#         ccolors = plt.get_cmap(cmap)(np.arange(nc, dtype=int))
#     cols = np.zeros((nc*nsc, 3))
#     for i, c in enumerate(ccolors):
#         chsv = matplotlib.colors.rgb_to_hsv(c[:3])
#         arhsv = np.tile(chsv,nsc).reshape(nsc,3)
#         arhsv[:,1] = np.linspace(chsv[1],0.25,nsc)
#         arhsv[:,2] = np.linspace(chsv[2],1,nsc)
#         rgb = matplotlib.colors.hsv_to_rgb(arhsv)
#         cols[i*nsc:(i+1)*nsc,:] = rgb
#     # Convert to hex strings
#     hex_colors = [matplotlib.colors.to_hex(rgb) for rgb in cols]
#     cmap = matplotlib.colors.ListedColormap(hex_colors)
#     # cmap = matplotlib.colors.ListedColormap(cols)
#     return cmap

# def get_hatch_dict():
#     hatch_dict = {
#         'ATT': '/',
#         'HEMT_8F': '\\'       
#     }

#     return hatch_dict


# def get_color_dict():
#     labels = [
#         ('DRIVE', 'PASSIVE', 'IDLE'),
#         ('DRIVE', 'ATT', '1Q'),
#         ('DRIVE', 'ATT', '2Q'),
#         ('DRIVE', 'ATT', 'READOUT'),
        
#         ('FLUX_BIAS', 'PASSIVE', 'IDLE'),
#         ('FLUX_BIAS', 'BIAS_RESISTOR_4K', 'IDLE'),
        
#         ('COUPLER', 'PASSIVE', 'IDLE'),
#         ('COUPLER', 'RESISTOR_2Q_4K', '2Q'),
        
#         ('PUMP', 'PASSIVE', 'IDLE'),
#         ('PUMP', 'ATT', 'READOUT'),
        
#         ('READOUT_PIN', 'PASSIVE', 'IDLE'),
#         ('READOUT_PIN', 'ATT', 'READOUT'),
#         ('READOUT_PIN', 'PD', 'READOUT'), 
#         ('READOUT_PIN', 'PM_v1', 'READOUT'),
#         ('READOUT_PIN', 'PM_v2', 'READOUT'),
#         ('READOUT_PIN', 'PM_v3', 'READOUT'),
        
#         ('READOUT_POUT', 'PASSIVE', 'IDLE') ,
        
#         ('AMP_BIAS', 'PASSIVE', 'IDLE') ,
#         ('AMP_BIAS', 'AMP', 'IDLE'),
#         ('AMP_BIAS', 'AMP_OHMIC', 'IDLE'),

#         ('JJ_BIAS', 'PASSIVE', 'IDLE') ,
        
        
#         ('DRIVE', 'PD', '1Q'),
#         ('DRIVE', 'PM_v1', '1Q'),
#         ('DRIVE', 'PM_v2', '1Q'),
#         ('DRIVE', 'PM_v3', '1Q'),

#         ('JJ_BIAS', 'JJ_Detector', 'IDLE'),
        
#         ('DRIVE', 'PD', '2Q'),
#         ('DRIVE', 'PM_v1', '2Q'),
#         ('DRIVE', 'PM_v2', '2Q'),
#         ('DRIVE', 'PM_v3', '2Q'),
        
#         ('DRIVE', 'PM_v1', 'READOUT'),
#         ('DRIVE', 'PM_v2', 'READOUT'),
#         ('DRIVE', 'PM_v3', 'READOUT'),
#         ]

#     colors = categorical_cmap(nc=7, 
#                               nsc=int(np.ceil(len(labels)/7)), 
#                               cmap="tab10")
#     color_dict = {}
#     for i, label in enumerate(labels):
#         color_dict[label] = matplotlib.colors.to_hex(colors(i))
#         # color_dict[label] = colors(i)

#     return color_dict

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

