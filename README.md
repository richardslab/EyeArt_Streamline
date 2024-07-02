# EyeArt Streamline

### Getting started

1. Download [Anaconda Distribution](https://www.anaconda.com/download/success) for Windows.

2. Set up your working directory:
```
└───Eyenuk Reports
     ├───PDF_Reports
     ├───Processing Log
     │      └─── BioPortal-Consultletters_DATA_LABELS_*.csv 
     ├───Results_CSV
     │      └─── EyenukAnalysisResults_*.csv 
     ├───environment.yml
     └───eyeart_streamline.py
```

3. Open [Visual Studio Code](https://code.visualstudio.com/) in Anaconda Navigator.

4. Navigate to directory and set up conda environment:
```
cd PATH/TO/Eyenuk Reports
conda create —name eyeart_env python=3.10 -f environment.yml
conda activate eyeart_env
```

5. Run!
```
python eyeart_streamline.py
```

