# ========= Import =========
import pandas as pd
import os
import numpy as np
import sys
from datetime import datetime
import shutil
import re

# ========= Select files =========
main_dir = 'C:\\Users\\nadia.blostein\\Documents\\EyeArt_test\\Eyenuk Reports'

# Function to extract the date from the file name
def extract_date(file_name, type='eyenuk_results'):
    # Regular expression to match the date part
    match = re.search(r'\d{4}\d{2}\d{2}', file_name) if type == 'eyenuk_results' else re.search(r'\d{4}-\d{2}-\d{2}', file_name)
    return match.group(0) if match else None

# latest eyenuk results file
dir = main_dir + '/Results_CSV'
eyenuk_results_dict = {}
for file in os.listdir(dir):
    if "EyenukAnalysisResults_" in file:
        date_tmp = extract_date(file)
        if date_tmp:
            date_str = datetime.strptime(date_tmp,'%Y%m%d')
            eyenuk_results_dict[file] = date_str

latest = max(eyenuk_results_dict.values())
for key, value in eyenuk_results_dict.items():
    if value == latest: eyenuk_results = key

# latest consult letters file file
consult_letters_dict = {}
for file in os.listdir(os.getcwd()):
    if "BioPortal-Consultletters_DATA_LABELS_" in file:
        date_tmp = extract_date(file, type = 'ConsultLetters')
        if date_tmp:
            date_str = datetime.strptime(date_tmp,'%Y-%m-%d')
            consult_letters_dict[file] = date_str
latest = max(consult_letters_dict.values())
for key, value in consult_letters_dict.items():
    if value == latest: consult_letters = key

# ========= Set working dir =========
# Set working directory (e.g. `EyeArt_Test`) such that it has the following structure:
# ├───Eyenuk Images  
# │   └──last-name_first-name_patient-ID  
# │       └───Date  
# │         └─── 4 images (.jpg)  
# └───Eyenuk Reports
#     ├───PDF_Reports
#     ├───Processing Log
#     │      └─── BioPortal-Consultletters_DATA_LABELS_*.csv 
#     ├───Results_CSV
#     │      └─── EyenukAnalysisResults_*.csv 
#     └───streamline.ipynb

# ========= Read spreadsheets =========

df_eyenuk_results = pd.read_csv(f"{main_dir}/Results_CSV/{eyenuk_results}")
df_consult_letters = pd.read_csv(f"{main_dir}/Processing Log/{consult_letters}")
df_reports_log = pd.read_excel(f"{main_dir}/Processing Log/Reports Processing Log.xlsx")

# ========= Save previous copies =========

now = datetime.now().strftime("%Y-%m-%d")
source_1 = "Processing Log/Reports Processing Log.xlsx"
dest_1 = f"Processing Log/Reports Processing Log-last_used_{now}.xlsx"
source_2 = f"Processing Log/{consult_letters}"
dest_2 = "Processing Log/" + consult_letters.rstrip('.csv') + f"-last_used_{now}.csv"
if not os.path.exists(dest_1):
    shutil.copyfile(source_1, dest_1)
    print(f"Duplicated file {source_1} as {dest_1}")
if not os.path.exists(dest_2):
    shutil.copyfile(source_2, dest_2)
    print(f"Duplicated file {source_2} as {dest_2}")

# ========= Update Consult Letters Dataframe =========

df_consult_letters_final = df_consult_letters.copy()
df_consult_letters_final['PatientName'] = (df_consult_letters_final['First name:'] + ' ' + df_consult_letters_final['Last name:']).str.title()
df_merged = pd.merge(df_consult_letters_final, df_eyenuk_results, on='PatientName', how='left')
df_consult_letters_final['Results'] = df_merged['PatientExamResult'].apply(lambda x: 'Pos' if x in ['Positive','Positive for vtDR', 'Ungradable'] else '')
df_consult_letters_final.to_csv(f"Processing Log/{consult_letters}", index = False)


# ========= Update the reports log =========

df_merged_2 = pd.merge(df_eyenuk_results, df_consult_letters_final, on='PatientName', how='left')
df_merged_2.rename(columns={'Record ID': 'Subject Unique Number (00-000)'}, inplace=True)

df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'].isin(df_merged_2['Subject Unique Number (00-000)']), 'Test Done'] = 'Y'
df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'].isin(df_merged_2['Subject Unique Number (00-000)']), 'Report processed?'] = 'Y'

for subj in df_merged_2['Subject Unique Number (00-000)']:
    new_date = df_merged_2.loc[df_merged_2['Subject Unique Number (00-000)'] == subj, 'ExamAnalysisDate'].values[0]
    df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Batch date'] = new_date
    #print(df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Batch date'])

    new_result = df_merged_2.loc[df_merged_2['Subject Unique Number (00-000)'] == subj, 'PatientExamResult'].values[0]
    df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Result'] = new_result
    #print(df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Result'])

    new_physician = df_merged_2.loc[df_merged_2['Subject Unique Number (00-000)'] == subj, 'Referring MD'].values[0]
    df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Physicians Name'] = new_physician
    #print(df_reports_log.loc[df_reports_log['Subject Unique Number (00-000)'] == subj, 'Physicians Name'])

df_reports_log.to_excel("Processing Log/Reports Processing Log.xlsx", index = False)

# ========= Update EyeNuk Results Output for REDCap =========

df_merged_3 = pd.merge(df_eyenuk_results, df_consult_letters_final, on='PatientName', how='left')
redcap_cols = ['Record ID']
redcap_cols += list(df_eyenuk_results.columns)
redcap_cols.remove('PatientID')
redcap_df = df_merged_3[redcap_cols]
redcap_df.to_csv(f"Results_CSV/{eyenuk_results}-REDCap", index = False)