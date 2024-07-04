# EyeArt Streamline

## What?
Once your Eyenuk (Eyeart) analysis reports have been exported into a nice and clean .csv (`Eyenuk Reports/Results_CSV/EyenukAnalysisResults_YYYMMDD_HHhMMmSSs.csv`), it only takes one line of code to:

1) Update your data file containing information for ophthamology consult letter referrals (`Eyenuk Reports/Processing Log/BioPortal-Consultletters_DATA_LABELS_YYYY-MM-DD_????.csv`);
   
2) Update your Eyenuk analysis result tracker (`Eyenuk Reports/Processing Log/Reports Processing Log.xlsx`);
   
3) Generate a data file that can safely be input into REDCap (`Eyenuk Reports/Results_CSV/EyenukAnalysisResults_YYYMMDD_HHhMMmSSs-REDCap.csv`).

## Getting started

1. Download [Anaconda Distribution](https://www.anaconda.com/download/success) for Windows.

2. Set up your working directory (`Eyenuk Reports`):
```
└───Eyenuk Reports
     ├───PDF_Reports
     ├───Processing Log
     │      └─── BioPortal-Consultletters_DATA_LABELS_*.csv
     │      └─── Reports Processing Log.xlsx
     ├───Results_CSV
     │      └─── EyenukAnalysisResults_*.csv 
     ├───environment.yml
     └───eyeart_streamline.py
```

3. Open [Visual Studio Code](https://code.visualstudio.com/) through the Anaconda Navigator.

4. Navigate to your working directory (`Eyenuk Reports`) and set up the following Conda environment:
```
cd PATH/TO/Eyenuk Reports
conda create —name eyeart_env python=3.10 -f environment.yml
conda activate eyeart_env
```

5. Run!
```
python eyeart_streamline.py
```

## Note: A Few Variable Naming Conventions

### Dataframe containing Eyenuk analysis results
_File_: `Eyenuk Reports/Results_CSV/EyenukAnalysisResults_YYYMMDD_HHhMMmSSs.csv`

_Variables_:
* `PatientID`: MRN:???????.? RAMQ:????????????

### Dataframe containing information for consult letter referrals
_File_: `Eyenuk Reports/Processing Log/BioPortal-Consultletters_DATA_LABELS_YYYY-MM-DD_????.csv`

_Variables_:
* `Record ID`: number assigned to patient for the study for anonymization purposes.
* `RAMQ Number`: ????????????
* `Medical Record Number (MRN)`: ???????.?

### Eyenuk analysis result tracker**
_File_: `Eyenuk Reports/Processing Log/Reports Processing Log.xlsx`

_Variables_:
* `Subject Unique Number (00-000)`: same as `Record ID` above (number assigned to patient for the study for anonymization purposes).
