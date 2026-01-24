# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 15:43:16 2024

@author: madeleine

INSTRUCTIONS: 
    

"""

import pandas as pd
import numpy as np 
import os
import sys
import datetime as dt
import warnings
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import seaborn as sns
sns.set_style("darkgrid")
import geopandas as gpd
import configparser
#supress warnings
warnings.filterwarnings("ignore")

def check_my_data_dir(my_data_dir):
    #set my_data directory 
    
    if os.path.isdir(my_data_dir): 
        file_exist=True
    else: 
        file_exist=False
    return file_exist
    

def check_goodreads_csv(filename='goodreads_library_export.csv'): 
    """Checks for a csv containing Goodreads export csv
    Args:
    filename (str): filename of csv containing goodreads data. Default: 'goodreads_library_export.csv'

    Returns:
    file_exist (boolean): Boolean True if file exists, False if not.
    
    Raises: Error if file not found. 
    """
    if os.path.isfile(filename): 
        file_exist=True
    else: 
        file_exist=False
        #print('ERROR: file "{}" not found in directory "{}" \nExiting analysis.'.format(filename,os.getcwd()))
    return file_exist 

def get_goodreads_csv(filename='goodreads_library_export.csv',shelf='Read'):
    """Imports Goodreads library export csv
    Args:
    filename (str): filename of csv containing goodreads data. Default: 'goodreads_library_export.csv'

    Returns:
    my_books (dataframe): Dataframe containing books read 
    """
    my_books=pd.read_csv(filename,dtype={'Book Id':str},usecols=['Book Id', 'Title', 'Author',
            'Number of Pages', 'Year Published', 'Original Publication Year','Date Added','Date Read','Exclusive Shelf','Read Count'])
    my_books['Date Added']=pd.to_datetime(my_books['Date Added'])
    my_books['Date Read']=pd.to_datetime(my_books['Date Read'])
    my_books=my_books[my_books['Exclusive Shelf']=='read']
    return my_books 
    
def clean_book_data(my_books):
    """ Cleans books data - missing values
    Args:
    my_books (dataframe): Dataframe of books read

    Returns:
    my_books (dataframe): Dataframe of books read (cleaned) 
    """
    #Fill in missing values for 'Original Publication Year' with values from 'Year Published'
    my_books['Original Publication Year'].fillna(my_books['Year Published'],inplace=True)
    #fill in missing valuesfor 'Date Read' with 'Date Added'
    #replace missing date read values with earliest dates
    earliest_data=my_books['Date Read'].min()
    #my_books['Date Read'].fillna(earliest_data,inplace=True)
    my_books['Date Read'].fillna(my_books['Date Added'],inplace=True)
    my_books['AuthorID']=my_books['Author'].str.replace(' ', '')
    return my_books 

def check_my_authors(author_file='my_authors.csv'):
    """Checks for a csv containing author data
    Args:
    author_file (str): filename of csv containing author data. Default: 'my_authors.csv'

    Returns:
    author_file_exist (boolean): Boolean True if file exists, False if not.
    
    Raises: Error if file not found. 
    """
    if os.path.isfile(author_file): 
        author_file_exist=True
    else: 
        author_file_exist=False
       
    return author_file_exist 

def create_authorid(my_authors):
    
    return my_authors
      

def get_myauthors(author_file='my_authors.csv'):
    dateparse = lambda x: dt.datetime.strptime(x, '%Y/%m/%d') if type(x)!=float else np.nan
    my_authors=pd.read_csv(author_file)
    #check if AuthorID columns
    #if 'AuthorID' in my_authors.columns:
    my_authors['AuthorID']=my_authors['Author'].str.replace(' ', '')
    #drop duplicates 
    my_authors.drop_duplicates(subset=['AuthorID','AuthorCountry','birthplace'],inplace=True)
    return my_authors 

def get_all_authors(file='\\'.join(os.getcwd().split('\\')[:-1])+'\\books_analysis\\author_data_all.csv'):
    """Imports full author dataset. 
    Args:
    file (str): filename of csv containing author data. Default: 'author_data_all.csv'

    Returns:
    all_authors (dataframe): Dataframe containing data for all authors. 
    
    Raises: Error if file not found. 
    """
    all_authors=pd.read_csv(file).rename(columns={'author_name':'Author'})
    all_authors['Author']=all_authors['Author'].str.strip('\n')
    return all_authors

def find_author(authors_ls,all_authors):
    """Takes a list of author names and searches for it in the  
    Args:
    authors_ls (list): list of author names to search for 

    Returns:
    author_details (dataframe): Dataframe containing details for authors in list. 
    """
    author_details=all_authors[all_authors['AuthorID'].isin(authors_ls)]
    author_no_details=pd.DataFrame({'AuthorID':[a for a in authors_ls if a not in author_details['AuthorID'].to_list()]})
    return pd.concat([author_details,author_no_details],ignore_index=True)
    
    
def get_new_authors(my_books,my_authors):
    """Takes a dataframe of books read and the my_authors dataframe to find any new authors in the my_books dataframe
        Args:
    book_data (dataframe): dataframe of read books 
    my_authors (dataframe): dataframe with author details

    Returns:
    new_authors (list): list of authors in my_books that aren't in my_authors
    Raises: 
    Print statement; [n] new authors found
     """
        
    new_authors=my_books[~my_books['AuthorID'].isin(my_authors['AuthorID'])]
    return new_authors['AuthorID'].unique()

def import_country_data(directory='\\'.join(os.getcwd().split('\\')[:-1]),world_file='\\books_analysis\\ne_110m_admin_0_countries\\ne_110m_admin_0_countries.shp',cont_file="\\books_analysis\\sovereign_states.csv"):
    useful_cols=['SOVEREIGNT','ISO_A3','ADM0_A3','geometry']
    world_data=gpd.read_file(directory+world_file)
    world_data=world_data[useful_cols]
    sov_st=pd.read_csv(directory+cont_file)
    #cont_data=pd.read_csv(directory+cont_file,usecols=['Code','Continent'])
    #world_data=world_data.merge(cont_data,how='left',on='Code')
    return world_data,sov_st
#%% CHECK FOR CONFIG FILE



#%% 
#-----------IMPORT AND UPDATE BOOKS AND AUTHOR DATA------------------
#1. CHECK THAT MY_DATA DIRECTORY EXISTS 
my_data_dir='\\'.join(os.getcwd().split('\\')[:-1])+'\\my_data'
if check_my_data_dir(my_data_dir):
    os.chdir(my_data_dir)
else: 
    print('ERROR: file structure not correct. Cannot find my_data folder')


#%%
#2 IMPORT AND CLEAN MY BOOKS DATA 
if check_goodreads_csv():
    my_books=get_goodreads_csv()
    my_books=clean_book_data(my_books)
else: 
    pass 

#%%
#3. IMPORT MY AUTHORS DATA 
all_authors=get_all_authors()

#%% 
if check_my_authors():
    #If my_authors.csv exists, import data
    my_authors=get_myauthors()
    
else: 
    
    #If my_authors.csv doesn't exist, import all_authors data and find my_authors data\\
    my_authors=my_books[["Author","AuthorID"]].drop_duplicates()
    #my_authors[['birthplace','author_gender','AuthorCountry','author_id']]=np.nan
    #my_authors=pd.DataFrame(columns={'Author':my_books['Author'].drop_duplicates()})
    authors_ls=my_authors['AuthorID'].to_list()
    #Find my_author details in all _authors dataset
    my_authors=find_author(authors_ls,all_authors)
    #add author where no details found 
    my_authors['AuthorCountry']=my_authors['birthplace']
    #export my_authors dataframe to csv
    #my_authors.rename(columns={'author_name':'Author'},inplace=True)
    
    #new_authors_ls=get_new_authors(my_books,my_authors)
#new_authors_ls=get_new_authors(my_books,my_authors)
#%%
#3. GET AUTHOR DATA FOR MY_BOOKS
#Find where there are new authors in my_books
new_authors_ls=get_new_authors(my_books,my_authors)
if len(new_authors_ls)>0:
    print("getting new author details")
    #Search for author deatils in all_authors data
    new_author_df=find_author(new_authors_ls,all_authors)
    #Join onto my_authors data 
    existing_author_list=my_authors[~my_authors['AuthorID'].isin(new_authors_ls)]
    my_authors=pd.concat([existing_author_list,new_author_df])
        #Export updated my_authors data
    my_authors['AuthorCountry'].fillna(my_authors['birthplace'],inplace=True)
    #my_authors.to_csv('my_authors.csv',index=False)
else:
    print("no new authors")
    pass

print("exporting authors file")
my_authors.to_csv('my_authors.csv',index=False)
#4. PRINT ERRORS

missing=my_authors[(my_authors['AuthorCountry'].isnull())|(my_authors['author_gender'].isnull())]
if len(missing)>0:
    print('The following authors are missing data: {}'.format(missing['AuthorID'].to_list()))
else:
    pass



#------ANALYSIS FUNCTIONS-------
#%%

def time_period(my_books,st_date,end_date=None):
    """Takes a time period start and end date and gets books read in that time 
        Args:
    st_date (string): start date in format %d/%m%Y (inclusive)
    end_date (string): end date in format %d/%m%Y (inclusive) default None = now

    Returns:
    my_books_time (dataframe): subset of my_books where 'Date Read' is within time period
    """
    st_date_dt=dt.datetime.strptime(st_date,'%d/%m/%Y')
   
    if end_date:
        end_date_dt=dt.datetime.strptime(end_date,'%d/%m/%Y')
    else: 
        end_date_dt=dt.datetime.now()
    my_books_time=my_books[(my_books['Date Read']>=st_date_dt)&(my_books['Date Read']<=end_date_dt)]
    return my_books_time

def books_per_time(my_books,time_group='M',count_var='Book Id'):
    """Takes a dataframe of books read count read books per time
        Args:
    my_books (dataframe): dataframe of read books 
    time_group (string): time to count books by. Year='Y', month='ME'

    Returns:
    books_per_time (dataframe): count of books read per time with index=datetime
    """
     #reset index to datetime
    my_books_dtidx=my_books.set_index('Date Read')
    books_per_time=my_books_dtidx[count_var].groupby(pd.Grouper(freq=time_group)).nunique()
    return books_per_time

def author_country_time(my_books):
    """Gets first date that an author country was added 
    Args:
    my_books (dataframe): dataframe of books read 
    Returns:
    country_time (dataframe): dtaframe grouped by country, taking the first date from each country group 
    """
    country_time=my_books[['Author','Title','AuthorCountry','Date Read']].sort_values('Date Read').groupby('AuthorCountry').first()
    
    return country_time

def calc_cumul(data):
    data=data.reset_index()
    data['cumulative']=data['AuthorCountry'].cumsum()
    data['cumulative%']=(data['cumulative'].div(193).round(2))*100
    return data

def decade(x):
    """Converts a year string (eg 2023) to decade (2020s) 
        Args:
    x (string): string of year eg 2023

    Returns:
    deacde (str): decade that the year is in
    """
    x_str=str(x)
    x_list=list(x_str)
    decade=x_list[0:3]
    decade.append('0s')
    decade=''.join(decade)
    return decade


# ---------GRAPHING FUNCTIONS-----------


def set_fig_width(my_books):
    min_time=my_books['Date Read'].min()

    max_time=my_books['Date Read'].max()
    #1cm per year
    w=((max_time-min_time).total_seconds()/3.154e+7)*0.55
    w=12
    return w

def bar_chart_time(plot_data,fig, ax, x_var='Date Read',y_var='Book Id',date_label='%m',y_ax_lab='Books'):
    """Takes a dataframe counts per time (with datetime index) and plots a bar chart of counts per time period
        Args:
    plot_data (dataframe): dataframe of counts per time with datetime index
    x_var (string): x variable (defaults to Date Read)
    y_var (string): y variable (defaults to book count )
    date_label (string): time format for date labels on x axis (default: %m (shortened month name))

    Returns:
    bar chart of counts per time 
    """
    plot_data=plot_data.reset_index()
    
    sns.barplot(data=plot_data,x=x_var,y=y_var,palette='viridis')
    ax.set_ylabel(y_ax_lab)
    ax.set_xticklabels([dt.datetime.strftime(i,date_label) for i in plot_data[x_var].drop_duplicates().to_list()])

    
def truncate_cmap(cmap,minval=0,maxval=1,n=100):
    new_cmap=colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name,a=minval,b=maxval),cmap(np.linspace(minval,maxval,n)))
    return new_cmap

def data_labels(ax,x,y,labels,space,fontweight='normal',fontcolor='#333333',fontsize=10):
    for x,y,lab in zip(x,y,labels):                                       # <--
        ax.annotate(f'{lab}', xy=(x,y+space), textcoords='data')
    
def label_bars(ax, labels, label_loc='outside',space=0,str_format='{}',orientation='v',fontweight='normal',fontcolor='#333333',fontsize=10):
    for bar,label in zip(ax.patches,labels):
        h_ref='center' if label_loc=='inside' else 'center'
        v_ref='top' if label_loc=='inside' else 'bottom'
        
        height=bar.get_height()
        width=bar.get_width()
        if orientation=='v':
            if fontcolor=='bar_color':
                ax.text(bar.get_x()+(width/2),(height+space),str_format.format(label),ha='center',va=v_ref,fontsize=fontsize,fontweight=fontweight,color=bar.get_facecolor())
            else:
                ax.text(bar.get_x()+(width/2),(height+space),str_format.format(label),ha='center',va=v_ref,fontsize=fontsize,fontweight=fontweight,color=fontcolor)
        elif orientation=='h':
            if fontcolor=='bar_color':
                ax.text(width+space,bar.get_y()+(height/2),str_format.format(label),ha='center',va=h_ref,fontsize=fontsize,fontweight=fontweight,color=bar.get_facecolor())
            else:
                ax.text(width+space,bar.get_y()+(height/2),str_format.format(label),ha='center',va=h_ref,fontsize=fontsize,fontweight=fontweight,color=fontcolor)
            
                
 #%% JOIN AUTHOR DATA ONTO BOOKS 

my_books=my_books.drop(columns='Author').merge(my_authors,how='left',on='AuthorID')

earliest_data=my_books['Date Read'].min()

#%% ALL BOOKS SUMMARY
try:
    my_book_year=time_period(my_books,st_date=dt.datetime.strftime(earliest_data,'%d/%m/%Y'))
    books_per_year=books_per_time(my_book_year,'Y')
    yr_av=books_per_year.mean()
    fig,ax=plt.subplots()
    bar_chart_time(books_per_year,fig,ax,x_var='Date Read',y_var='Book Id',date_label='%y')
    label_bars(ax, books_per_year.to_list(), label_loc='outside',space=0,str_format='{}',orientation='v',fontweight='bold',fontcolor='#333333',fontsize=10)
    ax.axhline(yr_av,zorder=0)
    plt.savefig('books_per_year.png',dpi=300, bbox_inches = "tight")
except Exception as e:
       # Print Error Message
        print("ERROR plotting decade published data. The error is: ",e)

#%% THIS YEAR SUMMARY 
current_year=dt.datetime.now().year
try:
    my_book_year=time_period(my_books,st_date='01/01/2026')
    prev_years=my_books[(my_books['Date Read']<dt.datetime(2025,1,1))&(my_books['Date Read']>dt.datetime(2020,1,1))]
    #get average books per month for previous years 
    av_books_monthly=books_per_time(prev_years,'M')
    av_books_monthly=av_books_monthly.reset_index()
    av_books_monthly['month']=av_books_monthly['Date Read'].dt.month
    av_books_monthly=av_books_monthly.groupby(['month']).mean()
    av_books_monthly['month']=av_books_monthly['Date Read'].dt.strftime('%b')
    
    if len(my_book_year)>0:
        books_per_month=books_per_time(my_book_year,'M')
        fig,ax=plt.subplots()
        sns.lineplot(data=av_books_monthly,x='month',y='Book Id',marker='o')
        bar_chart_time(books_per_month,fig,ax,x_var='Date Read',y_var='Book Id',date_label='%b')
        label_bars(ax, books_per_month.to_list(), label_loc='outside',space=0,str_format='{}',orientation='v',fontweight='bold',fontcolor='#333333',fontsize=10)
        plt.savefig('books_per_month.png',dpi=300, bbox_inches = "tight")
    else:
        print("WARNING: no data for time period")
except Exception as e:
       # Print Error Message
        print("ERROR plotting books read this year. The error is: ",e)

#%% COUNTRY DATA: NEW AUTHOR COUNTIRES PER YEAR 

#get year before year added 
#where no date data, ad to year before first books added
yr_before=earliest_data-dt.timedelta(days=365)
country_time=author_country_time(my_books.fillna(yr_before))
#counts books red per time (year)
country_per_year=books_per_time(country_time.reset_index(),time_group='Y',count_var='AuthorCountry')
#calculate cumulative authors
country_per_year=calc_cumul(country_per_year)

#books_per_time=author_country_time.reset_index()['birthplace'].groupby(pd.Grouper(freq='Y')).nunique()
#%% PLOT: CUMULATIVE AUTHORS PER YEAR 
"""
try:
    fig,ax=plt.subplots()
    #country_per_year['Date Read']=country_per_year['Date Read'].apply(lambda x: dt.datetime.strftime(x,'%Y'))
    sns.lineplot(data=country_per_year,x=country_per_year['Date Read'].apply(lambda x: dt.datetime.strftime(x,'%y')),y='cumulative',marker='o')
    data_labels(ax,x=country_per_year['Date Read'].apply(lambda x: dt.datetime.strftime(x,'%y')),y=country_per_year['cumulative'],labels=country_per_year['cumulative'],space=0.5)
    ax1=ax.twiny()
    bar_chart_time(country_per_year,fig,ax1,x_var='Date Read',y_var='AuthorCountry',date_label='%y')
    label_bars(ax1, country_per_year['AuthorCountry'].to_list(), label_loc='outside',space=0,str_format='{}',orientation='v',fontweight='bold',fontcolor='#333333',fontsize=10)
    ax1.set_xticklabels([])
    ax1.set_xticks([])
    ax1.set_xlabel(None)
    ax.set_ylabel('Author Countries')
    plt.savefig('author_countries_per_year.png',dpi=300, bbox_inches = "tight")
    plt.show()
except Exception as e:
       # Print Error Message
        print("ERROR plotting author countries by year. The error is: ",e)
"""
        
#%% CUMULATIVE AUTHORS COUNTRIES

fig,ax=plt.subplots()
country_per_year_plt=country_per_year.copy()
country_per_year_plt['Date Read']=country_per_year_plt['Date Read'].apply(lambda x: dt.datetime.strftime(x,'%y'))
sns.barplot(data=country_per_year_plt,x='Date Read',y='cumulative',palette='viridis')
sns.lineplot(data=country_per_year_plt,x='Date Read',y='AuthorCountry',marker='o')
label_bars(ax, country_per_year_plt['cumulative'].to_list(), label_loc='outside',space=0,str_format='{}',orientation='v',fontweight='bold',fontcolor='#333333',fontsize=10)
label_bars(ax, country_per_year_plt['cumulative%'].to_list(), label_loc='outside',space=-6,str_format='{:.0f}\n%',orientation='v',fontweight='bold',fontcolor='w',fontsize=7)
data_labels(ax,x=country_per_year_plt['Date Read'],y=country_per_year_plt['AuthorCountry'],labels=country_per_year_plt['AuthorCountry'],space=0,fontweight='bold',fontcolor='w')
plt.savefig('author_countries_per_year1.png',dpi=300, bbox_inches = "tight")

#%%% MAP OF AUTHORS 

##FUNCTIONS

def clean_country(country_df):
    #Changes country names to match those in the mappiong datasets 
    country_df=country_df.replace({'United States':'United States of America','Tanzania':'United Republic of Tanzania'})
    return country_df

def join_map_data(my_books,world_df):
    """Takes a dataframe of books read, and merges country data onto it (for low-res map)
    Args:
    my_books (dataframe): dataframe of books read
    world_df (dataframe): dataframe of geometries for countries from low-res worl map 

    Returns:
    my_books (dataframe):dataframe of books read
    world_outline (dataframe):
    """
    my_books=world_df.merge(my_books,how='outer',left_on='SOVEREIGNT',right_on='AuthorCountry')
    world_outline=my_books.copy()
    world_outline['Book Id'].fillna(0,inplace=True)
    #join on sov states
    return my_books,world_outline

def join_states_data(my_books,sov_states):
    #join sovereign states data onto books data 
    my_books=my_books.merge(sov_st,left_on='AuthorCountry',right_on='SOVEREIGNT',how='left')
    return my_books


def plot_map(fig,ax,country_count,world_outline,count_var='Book Id'):
    new_cmap=truncate_cmap(plt.get_cmap('Blues'),0.4,1.0,n=10)
    world_outline.plot(column=count_var,ax=ax,edgecolor='grey',linewidth=0.3,cmap='Greys')
    country_count.plot(column=count_var,cmap=new_cmap,edgecolor='grey',linewidth=0.3,ax=ax,legend=True,legend_kwds={"shrink":.3})
    ax.set_ylim([-60,90])
    ax.set_xlim([-182,182])
    ax.set_axis_off()
    
def show_countries(continent='all'):
    world_df=world_df[['CONTINENT', 'SOVEREIGNT']]
    if continent=='all':
        print(world_df)
    else:
        print(world_df[world_df['CONTINENT']==continent])
#%% JOIN COUNTRY DATA
my_books=clean_country(my_books)
#export my books to csv 
my_books.to_csv('my_books_data_all.csv',index=False)

#country_plot=clean_country(my_books)
country_plot=my_books[['Author','Book Id','AuthorCountry']].groupby('AuthorCountry').nunique().reset_index().sort_values(by='Author',ascending=False)
country_plot_mlt=pd.melt(country_plot.rename(columns={'Book Id':'Books','Author':'Authors'}),id_vars='AuthorCountry', value_vars=['Books','Authors'])
world_data,sov_st=import_country_data()
country_count,world_outline=join_map_data(country_plot[['AuthorCountry','Book Id']],world_data)

#%% OUTPUT COUNTRIES (SOVEREIGN STATES) TO READ 
#join continent data
sov_st_to_read=sov_st[~sov_st['SOVEREIGNT'].isin(my_books['AuthorCountry'].to_list())]
sov_st_to_read.to_csv('Countries_to_read.csv',index=False)

#%% 
try:
    fig,ax=plt.subplots(figsize=(10,10))
    plot_map(fig,ax,country_count,world_outline)
    plt.savefig('author_countries_map.png',dpi=300, bbox_inches = "tight")
    plt.show()

except Exception as e:
       # Print Error Message
        print("ERROR plotting countries map. The error is: ",e)

#%% LIST BY CONTINENT 
region='CONTINENT'


my_books=join_states_data(my_books,sov_st)
books_country_exp=my_books[['CONTINENT','AuthorCountry','Title','Author']].sort_values(by=['CONTINENT','AuthorCountry'])
country_count=my_books[['Author','Book Id','AuthorCountry',region]].groupby([region,'AuthorCountry']).nunique().reset_index().sort_values(by='Author',ascending=False)
#country_plot_mlt=pd.melt(country_plot.rename(columns={'Book Id':'Books','Author':'Authors'}),id_vars='birthplace', value_vars=['Books','Authors'])
#continent_gb=my_books.dropna(subset=['birthplace'])[[region,'birthplace','Book Id']].sort_values(by=[region,'Book Id'],ascending=[True,False])

continent_count=country_count.groupby(region)['Book Id'].sum().reset_index().rename(columns={'Book Id':'Continent_count'})
#
continent_gb=country_count.merge(continent_count,how='left',on=region).sort_values(['Continent_count','Book Id'],ascending=[False,False])

#%% 
def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_height()
        diff = current_width - new_value

        # we change the bar width
        patch.set_height(new_value)

        # we recenter the bar
        patch.set_y(patch.get_y() + diff * .5)
        
#%% PLOT: BOOKS READ PER COUNTRY, GROUPED BY CONTINENT
sov_states_count=sov_st.groupby('CONTINENT')['SOVEREIGNT'].count()

try:
    
    fig,ax=plt.subplots(2,3,figsize=(13,13))
    
    max_count=continent_gb['Book Id'].max()
    space=max_count*0.05
    continent_gb.sort_values('CONTINENT',inplace=True)
    for cont,axis in zip(continent_gb[region].dropna().unique(),ax.flat):
        #axis.set_facecolor('w')
        
        plot_data=continent_gb[continent_gb[region]==cont]
        plot_data.sort_values(['Book Id','AuthorCountry'],ascending=[False,True],inplace=True)
        book_count=plot_data['Book Id'].sum()
        
        book_cont_count=len(plot_data)
        sov_st_count=sov_states_count[sov_states_count.index==cont][0]
        axis.title.set_text(f'{cont} ({book_cont_count})')
        if len(plot_data)>0:
            plot_data.replace({'United States of America':'USA','United Kingdom':'UK','United Republic of Tanzania':'Tanzania'},inplace=True)
            sns.barplot(data=plot_data,y='AuthorCountry',x='Book Id',ax=axis,palette='viridis')
            label_bars(axis, plot_data['Book Id'].to_list(), label_loc='outside',space=space,str_format='{:.0f}',orientation='h',fontweight='normal',fontcolor='#333333',fontsize=10)
            #change_width(axis, .8)
            axis.set_xlabel(f'Books Read ({book_count})')
            
            axis.set_xticks([])
            axis.set_xlim([0,max_count+15])
            
            axis.set_ylim([23,-0.9])
            axis.set_ylabel(None)
        else:
            pass
        
    plt.savefig('books_read_by_authors_continent.png',dpi=300, bbox_inches = "tight")
    plt.show()
    #Show countries that weren't mapped
    missing=continent_gb[continent_gb[region].isnull()]
    if len(missing)>0:
        print('The following countries were not mapped: {}'.format(missing['AuthorCountry'].unique()))
    else:
        pass

except Exception as e:
       # Print Error Message
        print("ERROR plotting books by continent. The error is: ",e)
#%% 
try: 
    my_books['decadePublished']=my_books['Original Publication Year'].apply(lambda x: decade(x))
    pub_plot=my_books[['decadePublished','Book Id']].groupby('decadePublished').nunique().reset_index()
    
    fig,ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=pub_plot,x='decadePublished',y='Book Id',palette='viridis')
    label_bars(ax, pub_plot['Book Id'], label_loc='outside',space=0,str_format='{}',orientation='v',fontweight='bold',fontcolor='#333333',fontsize=10)
    ax.set_ylabel('Books Read')
    ax.set_xlabel('Original Publication Decade')
    plt.savefig('decade_published.png',dpi=300, bbox_inches = "tight")
    plt.show()
except Exception as e:
       # Print Error Message
        print("ERROR plotting decade published data. The error is: ",e)

#%% PLOT BY AUTHOR GENDER 

try: 
    
    #set colours 
    #get unique genders
    gender_plot=my_books[['Author','Book Id','Date Read','author_gender']].fillna({'author_gender':'unknown'}).set_index('Date Read').groupby([pd.Grouper(freq='Y'),'author_gender']).count().reset_index().sort_values(by='Author',ascending=False)
    num_cols=len(gender_plot['author_gender'].unique())
    grad_rg=np.linspace(0,1,num_cols,endpoint=True)
    
       
       
    fig,ax = plt.subplots(2,2,width_ratios=[3, 1],figsize=(12,6))
    #gender_plot1=my_books[(my_books['author_gender']=='male')|(my_books['author_gender']=='female')|(my_books['author_gender']=='other')]
    #gender_plot=my_books[['Author','Book Id','Date Read','author_gender']].fillna({'author_gender':'unknown'}).set_index('Date Read').groupby([pd.Grouper(freq='Y'),'author_gender']).count().reset_index().sort_values(by='Author',ascending=False)
    gender_plot2=pd.melt(gender_plot.rename(columns={'Book Id':'Books','Author':'Authors'}),id_vars=['Date Read','author_gender'], value_vars=['Books']).sort_values('Date Read')
    
       
    #BARPLOT BY YEAR 
    sns.barplot(data=gender_plot.sort_values('Date Read'),y='Book Id',x='Date Read',hue='author_gender',palette='viridis',ax=ax[0][0])
    
   
    
    #label_bars(ax[0], gender_plot2.sort_values(['author_gender','Date Read'],ascending=[False,True])['value'].to_list(), label_loc='outside',space=1,str_format='{:.0f}',orientation='v',fontweight='normal',fontcolor='#333333',fontsize=10)
    ax[0][0].set_xticklabels([dt.datetime.strftime(i,'%Y') for i in gender_plot2['Date Read'].drop_duplicates().to_list()])
    axis.set_ylabel('Books Read')
    #ax[0].title.set_text('By Year')
    gender_plot_all=gender_plot[['Author','Book Id','author_gender']].groupby('author_gender').sum().reset_index().rename(columns={'Book Id':'Books','Author':'Authors'}).sort_values(by='Authors',ascending=False)
    gender_plot_all['percentage']=(gender_plot_all['Books']/gender_plot_all['Books'].sum())*100
    
    
    #get % male authors 
    
    gender_perc=gender_plot2.pivot(index='Date Read', columns='author_gender', values='value').fillna(0).reset_index()
    gender_perc2=gender_plot2.set_index('Date Read').groupby(pd.Grouper(freq='Y'))['value'].sum().reset_index()
    gender_perc=gender_perc.merge(gender_perc2,how='left',on='Date Read')
    gender_perc['%Male']=gender_perc['male']/(gender_perc['value'])

        
        
    

    sns.lineplot(data=gender_perc,x='Date Read',y='%Male',marker='o',ax=ax[1][0])
    data_labels(ax[1][0],x=gender_perc['Date Read'],y=gender_perc['%Male'],labels=['{:.0f}%'.format(i*100) for i in gender_perc['%Male']],space=0.05,fontweight='bold',fontcolor='w')
    ###
    clr_male=ax[0][0].patches[-1].get_facecolor()
    clr_female=ax[0][0].patches[0].get_facecolor()
    
    
    # pie chart
    pie=ax[0][1].pie(gender_plot_all['Books'],labels=['{:.0f}%'.format(i) for i in gender_plot_all['percentage']],
                  colors=[clr_male,clr_female], labeldistance=0.5,textprops={'color':"w",                                                                                                         'fontweight':'bold',
                                                                            'fontsize':12})
    
    labels=['{}: {} books ({:.0f}%)'.format(i,j,k) for i,j,k in zip(gender_plot_all['author_gender'],
                                                                  gender_plot_all['Books'],gender_plot_all['percentage'])]
    
    ax[0][1].legend(pie[0],labels, bbox_to_anchor=(0.8,0.5), loc='upper center', fontsize=12, 
           bbox_transform=plt.gcf().transFigure)
    
    #ax[1].title.set_text('Overall')\
        
    ax[1][1].axis('off')    

    plt.savefig('author_gender.png',dpi=300, bbox_inches = "tight")
    plt.show()
except Exception as e:
       # Print Error Message
        print("ERROR plotting author gender data. The error is: ",e)
 
        
 
#%% EOY WRAP

this_year=my_books[(my_books['Date Read']>dt.datetime(2026,1,1))&(my_books['Date Read']<dt.datetime(2027,1,1))]
#my_books[my_books['Date Read']>dt.datetime(current_year,1,1)]
prev_years=my_books[my_books['Date Read']<dt.datetime(current_year,1,1)]

#CURRENT YEAR 
total_books=len(this_year)
unq_authors=len(this_year['AuthorID'].unique())

countries_count_yr=this_year['SOVEREIGNT'].value_counts()
gender_count_yr=this_year['author_gender'].value_counts()

new_authors=this_year[~this_year['AuthorID'].isin(prev_years['AuthorID'])]
pub_plot_yr=this_year[['decadePublished','Book Id']].groupby('decadePublished').nunique().reset_index()

#PREVIOUS YEARS 
#average books per year
total_av_prev=int(round(books_per_time(prev_years,time_group='Y',count_var='Book Id').mean(),0))


countries_count_prev=prev_years['SOVEREIGNT'].value_counts()

##average unique countries per year 
unq_cntry_yr=prev_years[['SOVEREIGNT','Date Read']].set_index('Date Read').groupby(pd.Grouper(freq='y')).nunique()
unq_cntry_yr.reset_index(inplace=True)
unq_cntry_yr.sort_values('SOVEREIGNT',ascending=False,inplace=True)
unq_cntry_yr['Date Read']=unq_cntry_yr['Date Read'].dt.strftime('%Y')

#%% YEAR SUMMARY IMAGE
cmap=matplotlib.colormaps['viridis']
fig,ax=plt.subplots(2,3,figsize=(12,10))


#FIG1
ax[0][0].title.set_text('Total Books {} Unique Countries {}'.format(total_books,len(countries_count_yr)))
sns.barplot(data=countries_count_yr.reset_index(),y='SOVEREIGNT',x='count',ax=ax[0][0],palette='viridis')
ax[0][0].set_xlabel('Number of Books')

#FIG2

gender_plot_yr=this_year[['Author','Book Id','author_gender']].groupby('author_gender').nunique().reset_index().rename(columns={'Book Id':'Books','Author':'Authors'}).sort_values(by='Authors',ascending=False)
gender_plot_yr['percentage']=(gender_plot_yr['Books']/gender_plot_yr['Books'].sum())*100
 
pie=ax[0][1].pie(gender_plot_yr['Books'],labels=['{:.0f}%'.format(i) for i in gender_plot_yr['percentage']],colors=[clr_male,clr_female],labeldistance=0.5,textprops={'color':"w",
                                                                                                                         'fontweight':'bold',
                                                                                                                         'fontsize':12})
 
labels=['{}: {} books ({:.0f}%)'.format(i,j,k) for i,j,k in zip(gender_plot_yr['author_gender'],
                                                               gender_plot_yr['Books'],gender_plot_yr['percentage'])]
ax[0][1].legend(pie[0],labels, bbox_to_anchor=(0.5,0.9), loc='upper center', fontsize=12, 
        bbox_transform=plt.gcf().transFigure)


#FIG 3

sns.barplot(data=pub_plot_yr,x='decadePublished',y='Book Id',palette='viridis',ax=ax[0][2])
ax[0][2].tick_params(axis='x', labelrotation=45)
#FIG 4
sns.barplot(data=unq_cntry_yr,y='Date Read',x='SOVEREIGNT',ax=ax[1][0],palette='viridis')
ax[1][0].set_xlabel('Unique Countries')

# FIG 5 

pages=np.array(my_books['Number of Pages'].dropna())
pages_med=np.median(pages)
pages_yr=np.array(this_year['Number of Pages'].dropna())
pages_med_yr=np.median(pages_yr)


ax[1][1].yaxis.set_visible(False)
#sns.distplot(pages_yr)
ax[1][1].hist(pages, bins=50, color=cmap(0.5), edgecolor=None, density=True, alpha=0.6)
sns.kdeplot(pages,color=cmap(0.5),ax=ax[1][1])
sns.kdeplot(pages_yr,color=cmap(0.1),ax=ax[1][1]) 
ax[1][1].set_xlabel('Book Length (pg)')
#Set up legend
green_patch = mpatches.Patch(color=cmap(0.5), alpha=0.6, label='All Time')
green_line=Line2D([0], [0], color=cmap(0.5), linewidth=2, label='All Time')
prp_line=Line2D([0], [0], color=cmap(0.1), linewidth=2, label='Current Year')
ax[1][1].legend(handles=[green_patch, green_line, prp_line], loc='upper right')

ax[1][1].set_xlim(0, None)

ax[1][2].axis('off') 

plt.savefig('year_wrap.png',dpi=300, bbox_inches = "tight")
plt.show()
   
#%% NUMBER OF PAGES

pages_mean=np.mean(pages)
pages_min=np.min(pages)
pages_max=np.max(pages)
fig,ax=plt.subplots()
ax.yaxis.set_visible(False)
#sns.distplot(pages_yr)
plt.hist(pages, bins=50, color=cmap(0.7), edgecolor='black', density=True, alpha=0.6)
sns.kdeplot(pages,color='green')

ax.set_xlabel('Book Length (pg)')
#Set up legend
green_patch = mpatches.Patch(color=cmap(0.7), label='All Time')
green_line=Line2D([0], [0], color='green', linewidth=2, label='All Time')

ax.text(0.95, 0.95, f'Median = {pages_med:.0f}\nMean = {pages_mean:.0f}\nMin = {pages_min:.0f}\nMax = {pages_max:.0f}',
        horizontalalignment='right',
        verticalalignment='top',
        transform=ax.transAxes, # Use axes coordinates
        bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))


#ax.legend(handles=[green_patch, green_line], loc='upper right')
plt.savefig('book_length.png',dpi=300, bbox_inches = "tight")
plt.show()

#%% TOP AUTHOR BY BOOKS READ

count_by_author=my_books[['Book Id','Author']].groupby('Author').count().sort_values('Book Id',ascending=False)

#Get top 10 
top_cutoff=count_by_author.iat[9,0]

top_authors=count_by_author[count_by_author['Book Id']>=top_cutoff].reset_index()


#GRAPH 
fig,ax=plt.subplots()
sns.barplot(data=top_authors,y='Author',x='Book Id',palette='viridis')
ax.set_xlabel('Books Read')
plt.savefig('top_authors.png',dpi=300, bbox_inches = "tight")
plt.show()

#%%
'''
sns.set_theme(style='white')

fig,ax=plt.subplots(2,3,figsize=(10,6))
for cont,axis in zip(continent_gb['continent'].unique(),ax.flat):
    #print(ax[axis])
    plot_data=continent_gb[continent_gb['continent']==cont]
    #fille  
    sns.barplot(data=plot_data,y='birthplace',x='Book Id',ax=axis,palette='viridis')
    sns.despine(bottom = True, left = True)
    change_width(axis, .8)
    axis.set_xticks([])
    axis.set_xlim([0,continent_gb['Book Id'].max()])
    axis.set_ylim([14,-0.9])
    axis.set_ylabel(None)
    axis.set_xlabel(None)
    
plt.show()
'''




