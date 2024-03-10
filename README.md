# books_analysis
Analyses Goodreads export of books read (csv). <br>
Designed to work with Goodreads data exported as csv (see instuctions here: https://help.goodreads.com/s/article/How-do-I-import-or-export-my-books-1553870934590) <br>
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


## Folder Structure 
Set up your folder structure as below. Output goes into the my_data folder. <br>
The goodreads_library_export.csv should be in the my_data folder. All outputs will be saved in this folder too. 
For authors that are missing author data (birhtplace, gender) you can edit the my_authors.csv that is produced as output and add those fields manually. 
```
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
