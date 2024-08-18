This repository has been initiated after finishing the research of the Master's Thesis of the author.
The repository is comprised of Python files that can be used to analyse large datasets of website texts. These datasets came about by crawling web URL with ARGUS (https://github.com/datawizard1337/ARGUS). The tested and advised settings for ARGUS are added in the 'settings.py' file. These settings are geared towards conservative and slow crawling, to avoid overloading the host website.
Each file can be used as standalone code, to accommodate changing needs and applications. Each step and desired input is included in each file as well as possible. Below is a short summary of what each file does or can do.

  ‘BasicTests.py’ includes the code to execute a series of ‘basic’ tests on a large dataset. The seven fifferent tests can be found in the code, but note that Cronbach’s Alpha is currently not being written into the file, since a separate Cronbach calculation and optimalisation was used.

  ‘CleanRAW.py’ can be used to remove missing values from specific columns and remove the corresponding rows. It can simultaneously rename specific columns to help with further processing.

  ‘Cronbach.py’ calculates and returns the initial Cronbach’s Alpha of two constructs (can be altered to one). It then continues to find the five best changes, to make the measurement construct more reliable and gives those options in the terminal.

  ‘DMStoDD.py’ converts coordinates that are in a DMS (degree, minutes, seconds) format to a DD (decimal degrees) format, which opens up the opportunity for geospatial analyses.

  ‘DensityMaps.py’ creates two KDE smoothened density maps. It does so by loading the DD coordinates of ID’s that have scored high on certain traits (OI and CE in this case) into an actual map. This can be used to create a visual representation of the density and division of high scoring ID’s.

  ‘FreqCounter.py’  searches the pre-processed text for predefined keywords. In this case, certain words are counting towards a category total, which then counts towards a full total of two separate constructs of OI and CE.

  ‘LISAmaps.py’ identifies clusters of high scoring ID’s who have a positive spatial correlation score. This results in a map where geographical area’s where a specific ID and most importantly its neighbours are performing well on OI or CE. Two maps are formed

  ‘LISAmaps2.py’ is similar to ‘LISAmaps.py’ but now plots area’s where both constructs are found to score positive and above average. This can be used to show area’s where multiple characteristics thrive, in this case OI and CE.

  ‘MergeIDs.py’ merges two files based on their shared ID’s. Practically, this can be used to create an output file where columns from both input files are merged into a new file based on ID. 

  ‘MergeIURLS.py’ merges multiple based on their ID’s. Practically, this can be used to create an output file in where similar files can me merged to make URL crawling easier.

  ‘MoransI.py’ calculates the Moran’s I value for a certain value, in this case of the effect of OI on CE, this process automatically uses robust standard errors.

  ‘MultipleTopicRegression.py’ analyses columns of OI and CE (can be changed). These columns represent the predefined categories or topics. The file can be used to do a robust multiple regression, to see whether certain aspects of a construct have an influential or interesting coefficient. Output is in .png and is provided in the repository. The used visual preferences can be adjusted. 

  ‘RemoveOutliers.py’ removes the outliers of two columns (total_oi and total_ce in this case), based on the upper 0.5 percent. This number can be adjusted and a lower limit could be added.

  ‘SLM_SEM.py’ can be used to make execute a Spatial Lag Model and a Spatial Error Model. These can be used to determine how and in what manner an area or a company is influenced by its surroundings, using robust standard errors. This file looks at the effect of OI on CE.

  ‘SLM_SEM_reverse.py’ can be used to make execute a Spatial Lag Model and a Spatial Error Model. These can be used to determine how and in what manner an area or a company is influenced by its surroundings, using robust standard errors. This file looks at the effect of CE on OI.

  ‘openfirst.py’ can and should be used while testing for large datasets. The code reads and copies the first 2000 rows into a new file with the same headers. The row limit can be adjusted.

  ‘setting.py’ holds the advised ARGUS settings and is the only file that is not a standalone file. 

