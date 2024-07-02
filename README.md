# EyeArt Streamline

### What?
Once you have exported a new set of EyeArt reports into .csv, run one line of code from your command-line in order to:
1) Update your consult letters according to the retinal imaging results;
2) Update the reports log;
3) Prepare a spreadsheet that is ready to be input into REDCap (patient-identifying features are removed).

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

