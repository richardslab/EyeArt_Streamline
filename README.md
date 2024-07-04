# EyeArt Streamline

### What?
Once your EyeArt reports have been exported into a nice and clean .csv (`Results_CSV/EyenukAnalysisResults_*.csv`), it only takes one line of code to:

1) Update your consult letters to send out (`Processing Log/BioPortal-Consultletters_DATA_LABELS_*.csv`) according to the retinal imaging results;
   
2) Update your reports log (`Processing Log/Reports Processing Log.xlsx`);
   
3) Prepare a spreadsheet that can be input into REDCap (patient-identifying features removed) (`Results_CSV/EyenukAnalysisResults_*-REDCap.csv`).

### Getting started

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

### Note: Variable Naming Conventions

`Eyenuk Reports\Results_CSV\EyenukAnalysisResults_YYYMMDD_HHhMMmSSs.csv`:
* `PatientID`: MRN:


