# ========= Import =========

import pandas as pd
import os
import numpy as np
import sys
from datetime import datetime
import shutil
import re

# ========= Select Latest EyeArt Analysis Results Spreadsheet =========

main_dir = os.getcwd().removesuffix("/EyeArt_Streamline")

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

# ========= Load data =========

df_eyenuk_results = pd.read_csv(f"{main_dir}/Results_CSV/{eyenuk_results}")
df_consult_letters = pd.read_csv(f"{main_dir}/Processing Log/{consult_letters}")
df_reports_log = pd.read_excel(f"{main_dir}/Processing Log/Reports Processing Log.xlsx")

# ========= Save Previous Copies =========

now = datetime.now().strftime("_%Y_%m_%d")
source_1 = f"{main_dir}/Processing Log/Reports Processing Log.xlsx"
dest_1 = f"{main_dir}/Processing Log/Reports Processing Log-initial_file{now}.xlsx"
source_2 = f"{main_dir}/Processing Log/{consult_letters}"
dest_2 = f"{main_dir}/Processing Log/" + consult_letters.rstrip('.csv') + f"-initial_file{now}.csv"
if not os.path.exists(dest_1):
    shutil.copyfile(source_1, dest_1)
    print(f"\nDuplicated file {source_1} as {dest_1}")
if not os.path.exists(dest_2):
    shutil.copyfile(source_2, dest_2)
    print(f"\nDuplicated file {source_2} as {dest_2}\n")

# ========= Update Spreadsheet For Ophthamology Consultation Referrals Letters =========
    # -> Sets positive or ungradable results to "Pos" in the "PatientExamResult" column

df_consult_letters_final = df_consult_letters.copy()
df_consult_letters_final['PatientName'] = (df_consult_letters_final['First name:'] + ' ' + df_consult_letters_final['Last name:']).str.title()
df_merged = pd.merge(df_consult_letters_final, df_eyenuk_results, on='PatientName', how='left')

pos_vals = []
for result in df_merged['PatientExamResult'].unique(): 
    if "Positive" in str(result): pos_vals.append(result)
    elif "Ungradable" in str(result): pos_vals.append(result)

df_consult_letters_final['Results'] = df_merged['PatientExamResult'].apply(lambda x: 'Pos' if x in pos_vals else '')
df_consult_letters_final.to_csv(f"{main_dir}/Processing Log/{consult_letters}", index = False)

# ========= Update EyeArt analysis result tracker  =========

df_merged_2 = pd.merge(df_eyenuk_results, df_consult_letters_final, on='PatientName', how='left')
df_merged_2.rename(columns={'Record ID': 'Subject Unique Number (00-000)'}, inplace=True)

df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'].isin(df_merged_2['Subject Unique Number (00-000)']), 'Test Done'] = 'Y'
df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'].isin(df_merged_2['Subject Unique Number (00-000)']), 'Report processed?'] = 'Y'

print(df_merged_2['Subject Unique Number (00-000)'].unique())
# for subj in df_merged_2['Subject Unique Number (00-000)']:
#     print(subj)
    # new_date = df_merged_2.loc[df_merged_2['Subject Unique Number (00-000)'] == subj, 'ExamAnalysisDate'].values[0]
    # df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Batch date'] = new_date
    #print(df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Batch date'])

#     new_result = df_merged_2.loc[df_merged_2['Subject Unique Number (00-000)'] == subj, 'PatientExamResult'].values[0]
#     df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Result'] = new_result
#     #print(df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Result'])

#     new_physician = df_merged_2.loc[df_merged_2['Subject Unique Number (00-000)'] == subj, 'Referring MD'].values[0]
#     df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Physicians Name'] = new_physician
#     #print(df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Physicians Name'])

# df_reports_log.to_excel("Processing Log/Reports Processing Log.xlsx", index = False)

# # # ========= Update EyeNuk Results Output for REDCap =========

# df_merged_3 = pd.merge(df_eyenuk_results, df_consult_letters_final, on='PatientName', how='left')
# redcap_cols = ['Record ID']
# redcap_cols += list(df_eyenuk_results.columns)
# redcap_cols.remove('PatientID')
# redcap_df = df_merged_3[redcap_cols]
# redcap_df.to_csv(f"Results_CSV/{eyenuk_results}-REDCap", index = False)
