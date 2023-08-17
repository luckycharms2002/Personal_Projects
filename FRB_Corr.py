import itertools
import pandas as pd
import numpy as np
from IPython.display import display
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler


#------------------------------------------------------Gold Data------------------------------------------------

#Get Data
data_path_GoldPrice = '/Users/lukascho/Desktop/CODING/Gold_Daily_Price_.xlsx'
GoldPrice_xls = pd.read_excel(data_path_GoldPrice)

#------------------------------------------------------Asset Data Master------------------------------------------------

ASSET_DATA = GoldPrice_xls

#------------------------------------------------------FRB Projections Data------------------------------------------------
#Get Data
data_path_Projections = '/Users/lukascho/Desktop/CODING/FRB_Data_Econ_Projections_Median.xlsx'

#Make Excel Object
projection_xls = pd.ExcelFile(data_path_Projections)

#Make list of sheet names (Dates of release)
when_data_release = projection_xls.sheet_names

#Make one big list of all dataframes/excel sheets. Add release date coloumn. Make Projection Years to Str.
dataframes = []
for sheet_name in when_data_release:
    df = pd.read_excel(projection_xls, sheet_name = sheet_name)
    df['Release Date'] = sheet_name
    dataframes.append(df)

#Put it all together (Med3 CT3 and R3 coloumns are added on for second-half year projections)   
final_dataframe = pd.concat(dataframes, ignore_index=True)    

#Organize coloumns
coloumns_order = ['Variable', 'Median 0', 'Median 1', 'Median 2', 'Median 3', 'Median LR', 
                  'Central Tendency 0', 'Central Tendency 1', 'Central Tendency 2', 
                  'Central Tendency 3', 'Central Tendency LR','Range 0', 'Range 1',	
                  'Range 2', 'Range 3', 'Range LR', 'Release Date']
final_dataframe = final_dataframe[coloumns_order]


#---------------------------------------------------------------------------------------------------------------------
#Just Doing Median!
prev_proj = ['GDP Previous Projection','UE Previous Projection', 'PCE Previous Projection', 'CPCE Previous Projection', 'FR Previous Projection']
new_proj = ['Change in real GDP', 'Unemployment rate', 'PCE inflation', 'Core PCE inflation', 'Federal funds rate']

# Collecting numpy array of discrepancies between projections for a variable type
def prev_vs_new(variable, date) -> np.ndarray:
    matching_rows = final_dataframe[(final_dataframe['Release Date'] == date) & (final_dataframe['Variable'] == variable)] 
    row_number = matching_rows.index[0]
    
    # Make numpy Arrays
    median_new_proj_array = final_dataframe.iloc[row_number, 1:6].values
    median_prev_proj_array = final_dataframe.iloc[row_number + 1, 1:6].values
    discrepancy = median_new_proj_array - median_prev_proj_array
    
    # Loop through the array, round non-NaN elements
    discrepancy_rounded = np.empty_like(discrepancy)
    for i, value in enumerate(discrepancy):
        if not np.isnan(value):
            discrepancy_rounded[i] = round(value, 6)
        else:
            discrepancy_rounded[i] = value
    
    return discrepancy_rounded
          
#Collecting the day's percent changes of the ASSET DATA's percent changes per Fed data release day        
def collect_pct_changes(asset_data) -> np.ndarray:
    percent_changes = [ ]
    for date in when_data_release:
        row = asset_data[asset_data['Date'] == date]['Change %'].values
        percent_changes.append(row[0])
    output = np.array(percent_changes)
    #Change into percentage number change, not real percent. (i.e. 0.73% = 0.73 not 0.73% = 0.0073)
    output = output*100
    return(output)

#Gets all the discrepancy arrays
def collect_prevvsnew_arrays():
    list_of_discrep_arrays_for_each_var_over_all_release_date = []
    for date in when_data_release:
        for variable in new_proj:
            list_of_discrep_arrays_for_each_var_over_all_release_date.append(prev_vs_new(variable, date))
      
    # Create a DataFrame from the list of arrays (if needed)
    df = pd.DataFrame(list_of_discrep_arrays_for_each_var_over_all_release_date)  
    
    return(df)

#Creating dataframes of discrepancies for each variable type.
def separate_per_variable():
    dfs_for_each_var = {}
    # Define the pattern step (evrery 5th row is referring to same variable type)
    pattern_step = 5

    # Iterate through the original dataframe rows and split them into new dataframes per var type. 
    for i, row in collect_prevvsnew_arrays().iterrows():
        remainder = i % pattern_step
        
        if new_proj[remainder] not in dfs_for_each_var:
            dfs_for_each_var[new_proj[remainder]] = (collect_prevvsnew_arrays().iloc[remainder])
            
        elif new_proj[remainder] in dfs_for_each_var:
            dfs_for_each_var[new_proj[remainder]] = pd.concat([dfs_for_each_var[new_proj[remainder]],collect_prevvsnew_arrays().iloc[remainder]], ignore_index=True)
    
    return(dfs_for_each_var)


def corr_finder():
    # Calculate correlations and store them in a 5x5 matrix
    correlation_matrix = np.zeros((5, 5))
    dict_dataframes = separate_per_variable()
    pct_changes_list = collect_pct_changes(ASSET_DATA)
    
    # Define the starting indices for each set of elements
    starting_indices = [0, 1, 2, 3, 4]
    
    # Convert pct_changes_list to a NumPy array
    pct_changes_array = np.array(pct_changes_list)
    
    # Iterate through the dataframes and calculate correlations
    for i, (key_i, df_i) in enumerate(dict_dataframes.items()):
        for j, start_idx in enumerate(starting_indices):
            subset_indices = list(range(start_idx, len(df_i), 5))
            subset_i = df_i.iloc[subset_indices]
            
            # Create a mask to ignore NaN values
            mask = ~np.isnan(subset_i)
            valid_indices = np.where(mask)[0]
            
            if valid_indices.size > 0:
                subset_i_array = subset_i.values[mask]
                reference_array = pct_changes_array[valid_indices]
                
                # Calculate the correlation using non-NaN values
                correlation = np.corrcoef(subset_i_array.flatten(), reference_array.flatten())[0, 1]
                correlation_matrix[i, j] = correlation
    
    return correlation_matrix

print(corr_finder())









