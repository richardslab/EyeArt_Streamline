# EyeArt Streamline

## What?
Once your EyeArt analysis results have been exported into a nice and clean .csv (`Eyenuk Reports/Results_CSV/EyenukAnalysisResults_YYYYMMDD_HHhMMmSSs.csv`), it only takes one line of code to:

1) Update your spreadsheet for ophthamology consultation referrals letters (`Eyenuk Reports/Processing Log/BioPortal-Consultletters_DATA_LABELS_YYYY-MM-DD_????.csv`);
   
2) Update your EyeArt analysis result tracker (`Eyenuk Reports/Processing Log/Reports Processing Log.xlsx`) (and duplicate the previous copy as `Eyenuk Reports/Processing Log/Reports Processing Log-initial_file_YYYY-MM-DD.xlsx`);
   
3) Generate a data file that can safely be input into REDCap (`Eyenuk Reports/Results_CSV/EyenukAnalysisResults_YYYMMDD_HHhMMmSSs-REDCap.csv`).

> Note: throughout `eyeart_streamline.py`, there are several checkpoints that append information to a textfile called (`EyeArt_Streamline/sanity_check_YYYY_MM_DD.txt`) so that you can ensure that everything is functioning as expected. Each checkpoint is preceded by a `### Sanity check X` comment in the `eyeart_streamline.py` code.

## Getting started

1. Download [Anaconda Distribution](https://www.anaconda.com/download/success) for Windows.

2. Set up your working directory (`Eyenuk Reports`):
```
└───Eyenuk Reports
     ├───EyeArt_Streamline
     │      └─── environment.yml
     │      └─── eyeart_streamline.py
     ├───Processing Log
     │      └─── DDMMMYYYYs_DATA_LABELS_YYYY-MM-DD_NNNN.csv
     │      └─── Reports Processing Log.xlsx
     └───Results_CSV
            └─── EyenukAnalysisResults_YYYYMMDD_HHhMMmSSs.csv 
```
> _PS: [automating directory tree generation](https://tree.nathanfriend.io)_

3. Open [Visual Studio Code](https://code.visualstudio.com/) through the Anaconda Navigator.

4. Navigate to your working directory (`Eyenuk Reports`) and set up the following Conda environment:
```
cd PATH/TO/Eyenuk Reports/EyeArt_Streamline
conda env create -f environment.yml
conda activate eyeart_env
```
> Note: if using Windows, make sure to do this through the VS Code Command Prompt (not Powershell)
> Note: if using Mac, you may need to: `conda install openpyxl`

5. Run!
```
python eyeart_streamline.py
```

## Note: A Few Variable Naming Conventions

### `Eyenuk Reports/Results_CSV/EyenukAnalysisResults_YYYYMMDD_HHhMMmSSs.csv`

_Columns_:
* `PatientID`: MRN:####### RAMQ:############

### `Eyenuk Reports/Processing Log/DDMMMYYYY_DATA_LABELS_YYYY-MM-DD_NNNN.csv`

_Columns_:
* `Record ID`: number assigned to patient for the study for anonymization purposes.
* `RAMQ Number`: ############
* `Medical Record Number (MRN)`: #######

### `Eyenuk Reports/Processing Log/Reports Processing Log.xlsx`

_Columns_:
* `Subject Unique Number (00-000)`: same as `Record ID` above (number assigned to patient for the study for anonymization purposes).
