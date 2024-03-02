# books_analysis
Analyses Goodreads export of books read (csv). <br>
Designed to work with Goodreads data exported as csv (see instuctions here: https://help.goodreads.com/s/article/How-do-I-import-or-export-my-books-1553870934590) <br>
Will also work with a csv of books in the format of the goodreads_library_export.csv blank csv. Just ensure that all entries are in the same format (particularly dates). The Book Id is used to count the individual books, so if you don't have the Good reads ID, just fill it in with any unique integer. <br>
The goodreads_library_export.csv should be in the same folder as the books_analysis.py file. All outputs will be saved in this folder too. 

## Folder Structure 
Output goes into the my_data folder
```
|--books_analysis
   |--books_analysis.py
   |--author_data_all.vs
|--my_data
   |--goodreads_library_export.csv
   
```
### Set up - Spyder 
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

