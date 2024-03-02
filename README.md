# books_analysis
Analyses Goodreads export of books read (csv). 
Designed to work with Goodreads data exported as csv (see instuctions here: https://help.goodreads.com/s/article/How-do-I-import-or-export-my-books-1553870934590) \n
Will also work with a csv of books in the format of the goodreads_library_export.csv blank csv. Just ensure that all entries are in the same format (particularly dates). The Book Id is used to count the individual books, so if you don't have the Good reads ID, just fill it in with any unique integer. \n
The goodreads_library_export.csv should be in the same folder as the goodreads.py file. All outputs will be saved in this folder too. 


### Set up - Spyder 
1. Open Anaconda prompt
2. Create virtual environment and install packages 
```
   conda create --name books-env  python==3.8.8 geopandas pandas numpy os sys datetime matplotlib seaborn
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

