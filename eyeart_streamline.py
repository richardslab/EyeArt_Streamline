# ========= Import =========

import pandas as pd
import os
import numpy as np
import sys
from datetime import datetime
import shutil
import re

# ========= Select Latest EyeArt Analysis Results Spreadsheet =========

main_dir = os.getcwd()
if main_dir.endswith("/EyeArt_Streamline"): main_dir = main_dir[:-len("/EyeArt_Streamline")]

# Function to extract the date from the file name
def extract_date(file_name, type='eyenuk_results'):
    # Regular expression to match the date part
    match = re.search(r'\d{4}\d{2}\d{2}_\d{2}h\d{2}m\d{2}s', file_name) if type == 'eyenuk_results' else re.search(r'\d{4}-\d{2}-\d{2}', file_name)
    return match.group(0) if match else None

dir = main_dir + '/Results_CSV'
eyenuk_results_dict = {}
for file in os.listdir(dir):
    if "EyenukAnalysisResults_" in file:
        date_tmp = extract_date(file)
        if date_tmp:
            date_str = datetime.strptime(date_tmp,'%Y%m%d_%Hh%Mm%Ss')
            eyenuk_results_dict[file] = date_str

latest = max(eyenuk_results_dict.values())

for key, value in eyenuk_results_dict.items():
    if value == latest: eyenuk_results = key

# ========= Select Latest Spreadsheet For Ophthamology Consultation Referrals Letters =========

consult_letters_dict = {}
for file in os.listdir(f"{main_dir}/Processing Log"):
    if "DATA_LABELS_" in file:
        date_tmp = extract_date(file, type = 'ConsultLetters')
        if date_tmp:
            date_str = datetime.strptime(date_tmp,'%Y-%m-%d')
            consult_letters_dict[file] = date_str

latest = max(consult_letters_dict.values())

for key, value in consult_letters_dict.items():
    if value == latest: consult_letters = key

# ========= Text File Where to 'Sanity Check' Outputs =========

now = datetime.now().strftime("_%Y_%m_%d")
sanity_check = open(f"sanity_check{now}.txt", "a")

# ========= Load data =========

df_eyenuk_results = pd.read_csv(f"{main_dir}/Results_CSV/{eyenuk_results}")
df_consult_letters = pd.read_csv(f"{main_dir}/Processing Log/{consult_letters}")
df_reports_log = pd.read_excel(f"{main_dir}/Processing Log/Reports Processing Log.xlsx")

### Sanity Check 1
print("\n========= Load data =========", file = sanity_check)
print(f"\nYou have EyeArt Analysis Results for {df_eyenuk_results.shape[0]} NEW subjects!", file = sanity_check)

# ========= Save Previous Copies =========

source_1 = f"{main_dir}/Processing Log/Reports Processing Log.xlsx"
dest_1 = f"{main_dir}/Processing Log/Reports Processing Log-initial_file{now}.xlsx"
source_2 = f"{main_dir}/Processing Log/{consult_letters}"
dest_2 = f"{main_dir}/Processing Log/" + consult_letters.rstrip('.csv') + f"-initial_file{now}.csv"

### Sanity Check 2
print("\n\n========= Save Previous Copies =========", file = sanity_check)
if not os.path.exists(dest_1):
    shutil.copyfile(source_1, dest_1)
    print(f"\nDuplicated file {source_1} as {dest_1}", file = sanity_check)
if not os.path.exists(dest_2):
    shutil.copyfile(source_2, dest_2)
    print(f"\nDuplicated file {source_2} as {dest_2}\n", file = sanity_check)

# ========= Update Spreadsheet For Ophthamology Consultation Referrals Letters =========
    # -> Sets positive or ungradable results to "Pos" in the "PatientExamResult" column

MRN_list = []
for val in df_eyenuk_results['PatientID']: MRN_list.append(float(val.split(' ')[0].split('MRN:')[1]))
df_eyenuk_results['Medical Record Number (MRN):'] = MRN_list

df_consult_letters_final = df_consult_letters.copy()
df_merged = pd.merge(df_consult_letters_final, df_eyenuk_results, on='Medical Record Number (MRN):', how='left')

### Sanity Check 3
print("\n\n========= Update Spreadsheet For Ophthamology Consultation Referrals Letters =========", file = sanity_check)
df_tmp = pd.merge(df_consult_letters_final, df_eyenuk_results, on='Medical Record Number (MRN):', how='inner')
print(f"\n{df_tmp.shape[0]} out of {df_eyenuk_results.shape[0]} new EyeArt Analysis Results subjects can be found in the {consult_letters} spreadsheet.", file = sanity_check)

pos_vals = []
for result in df_merged['PatientExamResult'].unique(): 
    if "Positive" in str(result): pos_vals.append(result)
    elif "Ungradable" in str(result): pos_vals.append(result)

df_consult_letters_final['Results'] = df_merged['PatientExamResult'].apply(lambda x: 'Pos' if x in pos_vals else '')
df_consult_letters_final.to_csv(f"{main_dir}/Processing Log/{consult_letters}", index = False)

### Sanity Check 4
print(f"\n\nPositive or ungradable results for {df_consult_letters_final[df_consult_letters_final['Results'] == 'Pos'].shape[0]} of your {df_eyenuk_results.shape[0]} new subjects.", file = sanity_check)

# ========= Update 'Reports Processing Log.xlsx' (EyeArt analysis result tracker)  =========

df_merged_2 = pd.merge(df_eyenuk_results, df_consult_letters_final, on='Medical Record Number (MRN):', how='left')
df_merged_2.rename(columns={'Record ID': 'Subject Unique Number (00-000)'}, inplace=True)

### Sanity Check 5
print("\n\n========= Update 'Test Done' & 'Report processed?' columns for 'Reports Processing Log.xlsx' (EyeArt analysis result tracker) =========", file = sanity_check)
df_tmp_2 = pd.merge(df_merged_2, df_reports_log, on='Subject Unique Number (00-000)', how='inner')
print(f"\n{df_tmp_2.shape[0]} out of {df_eyenuk_results.shape[0]} new EyeArt Analysis Results subjects can be found in 'Reports Processing Log.xlsx'.\n", file = sanity_check)

# === Update 'Test Done' column of 'Reports Processing Log.xlsx'

Test_Done_initial = df_reports_log[(df_reports_log['Test Done'] == 'Y') | (df_reports_log['Test Done'] == 'y')].shape[0]
Test_Done_update = 0
Test_Done_update_list = []

for subj in df_merged_2['Subject Unique Number (00-000)']:
    if str(df_reports_log[df_reports_log['Subject Unique Number (00-000)'] == subj]['Test Done'].values[0]).upper() == 'Y':
        Test_Done_update_list.append(subj)
        Test_Done_update += 1
df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'].isin(df_merged_2['Subject Unique Number (00-000)']), 'Test Done'] = 'Y'

### Sanity Check 6
Test_Done_final = df_reports_log[(df_reports_log['Test Done'] == 'Y') | (df_reports_log['Test Done'] == 'y')].shape[0]
print(f"\nTest already done for {Test_Done_update} subject(s): {Test_Done_update_list}.", file = sanity_check)
print(f"Updated 'Test Done' column of 'Reports Processing Log.xlsx' for {Test_Done_final-Test_Done_initial} out of {df_eyenuk_results.shape[0]} new subjects.", file = sanity_check)

# === Update 'Report processed?' column of 'Reports Processing Log.xlsx'

Report_Processed_initial = df_reports_log[(df_reports_log['Report processed?'] == 'Y') | (df_reports_log['Report processed?'] == 'y')].shape[0]
Report_Processed_update = 0
Report_Processed_update_list = []
for subj in df_merged_2['Subject Unique Number (00-000)']:
    if str(df_reports_log[df_reports_log['Subject Unique Number (00-000)'] == subj]['Report processed?'].values[0]).upper() == 'Y':
        Report_Processed_update_list.append(subj)
        Report_Processed_update += 1
df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'].isin(df_merged_2['Subject Unique Number (00-000)']), 'Report processed?'] = 'Y'

### Sanity Check 7
Report_Processed_final = df_reports_log[(df_reports_log['Report processed?'] == 'Y') | (df_reports_log['Report processed?'] == 'y')].shape[0]
print(f"\nReport already processed done for {Report_Processed_update} subject(s): {Report_Processed_update_list}.", file = sanity_check)
print(f"Updated 'Report processed?' column of 'Reports Processing Log.xlsx' for {Report_Processed_final-Report_Processed_initial} out of {df_eyenuk_results.shape[0]} new subjects.", file = sanity_check)

print(f"\n\n========= Update 'Batch date', 'Result' and 'Physicians Name' columns 'Reports Processing Log.xlsx'.", file = sanity_check)

for subj in df_merged_2['Subject Unique Number (00-000)']:
    
    # === Update 'Batch date' column of 'Reports Processing Log.xlsx'
    new_date = df_merged_2.loc[df_merged_2['Subject Unique Number (00-000)'] == subj, 'ExamAnalysisDate'].values[0]
    df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Batch date'] = new_date
    
    # === Update 'Result' column of 'Reports Processing Log.xlsx'
    prev_result = df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Result'].values[0]
    new_result = df_merged_2.loc[df_merged_2['Subject Unique Number (00-000)'] == subj, 'PatientExamResult'].values[0]
    df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Result'] = new_result
    
    # === Update 'Physicians Name' column of 'Reports Processing Log.xlsx'
    prev_physician = df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Physicians Name'].values[0]
    new_physician = df_merged_2.loc[df_merged_2['Subject Unique Number (00-000)'] == subj, 'Referring MD'].values[0]
    df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Physicians Name'] = new_physician
    
    ### Sanity Check 8
    print(f"\nSubject: {subj}", file = sanity_check)
    print(f"Batch date: {df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Batch date'].values[0]}", file = sanity_check)
    print(f"Previous result: {prev_result}\nNEW RESULT: {df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Result'].values[0]}", file = sanity_check)
    print(f"Previous physician: {prev_physician}\nNEW PHYSICIAN: {df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Physicians Name'].values[0]}", file = sanity_check)

df_reports_log.to_excel(f"{main_dir}/Processing Log/Reports Processing Log.xlsx", index = False)

# ========= Update EyeArt analysis results for REDCap =========

df_merged_3 = pd.merge(df_eyenuk_results, df_consult_letters_final, on='Medical Record Number (MRN):', how='left')
redcap_cols = ['Record ID']
redcap_cols += list(df_eyenuk_results.columns)
redcap_cols.remove('PatientID')
redcap_df = df_merged_3[redcap_cols]
if eyenuk_results.endswith(".csv"): eyenuk_results = eyenuk_results[:-len(".csv")]
redcap_df.to_csv(f"{main_dir}/Results_CSV/{eyenuk_results}-REDCap.csv", index = False)