# books_analysis
Analyses Goodreads export of books read (csv). <br>
Designed to work with Goodreads data exported as csv (see instructions here: https://help.goodreads.com/s/article/How-do-I-import-or-export-my-books-1553870934590) <br>
Will also work with a csv of books in the format of the goodreads_library_export.csv blank csv. Just ensure that all entries are in the same format (particularly dates). The Book Id is used to count the individual books, so if you don't have the Good reads ID, just fill it in with any unique integer. <br>

## Outputs
The code produces several graphs as output: 
### Books Read per Year (all time)
<img src="https://github.com/madeleine200/books_analysis/assets/38779248/aeb5cb56-4054-4c9f-9921-6d8e0ea47f38" width=40% height=40%> <br>
### Books Read This Year (by month)
<img src="https://github.com/madeleine200/books_analysis/assets/38779248/40d4b0a0-5b3a-4cc7-a188-1569ab8df57b" width=40% height=40%> <br>
### Author Countries per Year
This shows the number of new author countries added per year (bars) and the cumulative number of author countries read (line). <br>
<img src="https://github.com/madeleine200/books_analysis/assets/38779248/7756fbb8-4688-4c21-b9ae-cee86ba39bc9" width=40% height=40%>
### Map of Author Countries 
Map showing the number of books read by authors from each country.  <br>
<img src="https://github.com/madeleine200/books_analysis/assets/38779248/3cf8361a-5039-4664-a0e4-518a6df3c0b6" width=40% height=40%>

### Author Countries by Continent
<img src="https://github.com/madeleine200/books_analysis/assets/38779248/c228d6d7-429d-48ef-9863-ff3f89b02533" width=40% height=40%>

### Books by Author Gender 
<img src="https://github.com/madeleine200/books_analysis/assets/38779248/e115d2fa-38ab-47df-bfc8-1a4a00861519" width=40% height=40%>

### Books by decade published 

<img src="https://github.com/madeleine200/books_analysis/assets/38779248/08c9826c-c20e-42f9-9736-453a70ac27ac" width=40% height=40%>


## Folder Structure 
Download the files and set up your folder structure as below. The <parent_folder> can be named whatever you like as long as books_analysis and my_data are in the same folder. Output goes into the my_data folder. <br>
The goodreads_library_export.csv should be in the my_data folder. All outputs will be saved in this folder too. 
For authors that are missing author data (birthplace, gender) you can edit the my_authors.csv that is produced as output and add those fields manually. 
```
|--<parent_folder>
   |--books_analysis
      |--books_analysis.py
      |--author_data_all.csv
      |--ne_110m_admin_0_countries
      |--sovereign_states.csv
   |--my_data
      |--goodreads_library_export.csv
   
```
## Set up: General 
The python code should be run in a virtual environment. Create a virtual environment and install the following packages: <br>
geopandas <br> pandas <br> numpy <br> matplotlib <br> seaborn <br>

### Set up: Spyder 
1. Open Anaconda prompt
2. Create virtual environment and install packages 
```
   conda create --name books-env  python==3.8.8 geopandas pandas numpy matplotlib seaborn
```
### Running analysis (every time)
1. Activate virtual environment in Anaconda prompt
```
conda activate books-env
```

2. Launch Spyder from Anaconda prompt:

```
spyder
```
### Troubleshooting
If you get the following error: 
```
'spyder' is not recongized as an internal or external command, operable program or batch file
```
Try installing Spyder using: 
```
conda install spyder
```
## Data Analysis 
### Missing Values 
Where there are missing data for authors, you can add this data directly into the my_authors.csv file (it won't get written over if you re-run the analysis)

Missing values are replaced in the following fields: <br>
'Date Read' : missing values replaced with 'Date Added' <br>
'Date Read' and 'Date Added' are missing, date is replaced with the year before the first year books were added <br>
'Original Publication Year' : missing values replaced with 'Year Published' <br>

### Author Countries 
Author countries are mapped from the Natural Earth 1:100m data set (https://www.naturalearthdata.com/downloads/110m-cultural-vectors/) which maps 177 countries (countries that are too small for the resolution are not mapped). <br>
The list of author countries (and the author countries by continent) use the sovereign states data (https://www.naturalearthdata.com/downloads/10m-cultural-vectors/) to group by continent/region

