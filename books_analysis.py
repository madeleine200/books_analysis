# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 15:43:16 2024

@author: madel

code for analysing book data. 
TO DO: 
    1. ANALYSIS FUNCTIONS
    2. GRAPHING FUNCTIONS
    3. CLEAN STRING INPUTS

"""

import pandas as pd
import numpy as np 
import os
import sys
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns
sns.set_style("darkgrid")
import geopandas as gpd




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
    dateparse = lambda x: dt.datetime.strptime(x, '%d/%m/%Y') if type(x)!=float else np.nan
    my_books=pd.read_csv(filename,dtype={'Book Id':str},usecols=['Book Id', 'Title', 'Author',
            'Number of Pages', 'Year Published', 'Original Publication Year','Date Added','Date Read','Exclusive Shelf','Read Count'])
    my_books['Date Added']=pd.to_datetime(my_books['Date Added'])
    my_books['Date Read']=pd.to_datetime(my_books['Date Read'])
    my_books=my_books[my_books['Exclusive Shelf']=='read']
    return my_books 
    
def clean_book_data(my_books):
    #Fill in missing values for 'Original Publication Year' with values from 'Year Published'
    my_books['Original Publication Year'].fillna(my_books['Year Published'],inplace=True)
    #fill in missing valuesfor 'Date Read' with 'Date Added'
    my_books['Date Read'].fillna(my_books['Date Added'],inplace=True)
    
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

def get_myauthors(author_file='my_authors.csv'):
    dateparse = lambda x: dt.datetime.strptime(x, '%Y/%m/%d') if type(x)!=float else np.nan
    my_authors=pd.read_csv(author_file)
    
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
    author_details=all_authors[all_authors['Author'].isin(authors_ls)]
    author_no_details=pd.DataFrame({'Author':[a for a in authors_ls if a not in author_details['Author'].to_list()]})
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
        
    new_authors=my_books[~my_books['Author'].isin(my_authors['Author'])]
    return new_authors['Author'].unique()
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
    #If my_authors.csv doesn't exist, import all_authors data and find my_authors data
    my_authors=pd.DataFrame(columns={'Author':my_books['Author'].to_list()})
    authors_ls=my_books['Author'].to_list()
    #Find my_author details in all _authors dataset
    my_authors=find_author(authors_ls,all_authors)
    #add author where no details found 
    
    #export my_authors dataframe to csv
    #my_authors.rename(columns={'author_name':'Author'},inplace=True)
    my_authors.to_csv('my_authors.csv',index=False)
    #new_authors_ls=get_new_authors(my_books,my_authors)
#new_authors_ls=get_new_authors(my_books,my_authors)
#%%
#3. GET AUTHOR DATA FOR MY_BOOKS
#Find where there are new authors in my_books
new_authors_ls=get_new_authors(my_books,my_authors)
if len(new_authors_ls)>0:
    #Search for author deatils in all_authors data
    new_author_df=find_author(new_authors_ls,all_authors)
    #Join onto my_authors data 
    my_authors=pd.concat([my_authors,new_author_df])
        #Export updated my_authors data
    
else: 
    pass
my_authors.to_csv('my_authors.csv',index=False)
#4. PRINT ERRORS

print('The following authors are missing details: \n')
print(my_authors[(my_authors['birthplace'].isnull())|(my_authors['author_gender'].isnull())])


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
    my_books_time=my_books[(my_books['Date Added']>=st_date_dt)&(my_books['Date Added']<=end_date_dt)]
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

def author_country_time(my_books,time_group='Y'):
    country_time=my_books[['Author','Title','birthplace','Date Read']].sort_values('Date Read').groupby('birthplace').first()
    
    return country_time

def calc_cumul(data):
    data=data.reset_index()
    data['cumulative']=data['birthplace'].cumsum()
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

def data_labels(ax,x,y,labels,space):
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

my_books=my_books.merge(my_authors,how='left',on='Author')

#%% ALL BOOKS SUMMARY

my_book_year=time_period(my_books,st_date='01/01/2010')
books_per_year=books_per_time(my_book_year,'Y')
fig,ax=plt.subplots()
bar_chart_time(books_per_year,fig,ax,x_var='Date Read',y_var='Book Id',date_label='%Y')
label_bars(ax, books_per_year.to_list(), label_loc='outside',space=0,str_format='{}',orientation='v',fontweight='bold',fontcolor='#333333',fontsize=10)
plt.savefig('books_per_year.png',dpi=300, bbox_inches = "tight")

#%% THIS YEAR SUMMARY 
my_book_year=time_period(my_books,st_date='01/01/2024')
if len(my_book_year)>0:
    books_per_month=books_per_time(my_book_year,'M')
    fig,ax=plt.subplots()
    bar_chart_time(books_per_month,fig,ax,x_var='Date Read',y_var='Book Id',date_label='%b')
    label_bars(ax, books_per_month.to_list(), label_loc='outside',space=0,str_format='{}',orientation='v',fontweight='bold',fontcolor='#333333',fontsize=10)
    plt.savefig('books_per_month.png',dpi=300, bbox_inches = "tight")
else:
    print("WARNING: no data for time period")

#%% COUNTRY DATA

#new countries per year 

country_time=author_country_time(my_books.fillna(dt.datetime(2015,1,1)),time_group='Y')

country_per_year=books_per_time(country_time.reset_index(),time_group='Y',count_var='birthplace')
country_per_year=calc_cumul(country_per_year)

#books_per_time=author_country_time.reset_index()['birthplace'].groupby(pd.Grouper(freq='Y')).nunique()
#%%
fig,ax=plt.subplots()

#country_per_year['Date Read']=country_per_year['Date Read'].apply(lambda x: dt.datetime.strftime(x,'%Y'))
sns.lineplot(data=country_per_year,x=country_per_year['Date Read'].apply(lambda x: dt.datetime.strftime(x,'%Y')),y='cumulative',marker='o')
data_labels(ax,x=country_per_year['Date Read'].apply(lambda x: dt.datetime.strftime(x,'%Y')),y=country_per_year['cumulative'],labels=country_per_year['cumulative'],space=0.5)
ax1=ax.twiny()
bar_chart_time(country_per_year,fig,ax1,x_var='Date Read',y_var='birthplace',date_label='%Y')
label_bars(ax1, country_per_year['birthplace'].to_list(), label_loc='outside',space=0,str_format='{}',orientation='v',fontweight='bold',fontcolor='#333333',fontsize=10)
ax1.set_xticklabels([])
ax1.set_xticks([])
ax1.set_xlabel(None)
ax.set_ylabel('Author Countries')
plt.savefig('author_countries_per_year.png',dpi=300, bbox_inches = "tight")
plt.show()

#%%% MAP OF AUTHORS 


def clean_country(country_df):
    country_df=country_df.replace('United States','United States of America')
    return country_df

def join_country_data(my_books,world_df=gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))):
    my_books=world_df.merge(my_books,how='outer',left_on='name',right_on='birthplace')
    world_outline=my_books.copy()
    world_outline['Book Id'].fillna(0,inplace=True)
    return my_books,world_outline


def plot_map(fig,ax,country_count,world_outline,count_var='Book Id'):
    new_cmap=truncate_cmap(plt.get_cmap('Blues'),0.4,1.0,n=10)
    world_outline.plot(column=count_var,ax=ax,edgecolor='silver',cmap='Greys')
    country_count.plot(column=count_var,cmap=new_cmap,edgecolor='silver',linewidth=0.1,ax=ax,legend=True,legend_kwds={"shrink":.3})
    ax.set_ylim([-60,90])
    ax.set_xlim([-182,182])
    ax.set_axis_off()
    
#%% 



country_plot=clean_country(my_books)
country_plot=country_plot[['Author','Book Id','birthplace']].groupby('birthplace').nunique().reset_index().sort_values(by='Author',ascending=False)
country_plot_mlt=pd.melt(country_plot.rename(columns={'Book Id':'Books','Author':'Authors'}),id_vars='birthplace', value_vars=['Books','Authors'])

country_count,world_outline=join_country_data(country_plot[['birthplace','Book Id']])
#%% 

fig,ax=plt.subplots(figsize=(10,10))
plot_map(fig,ax,country_count,world_outline)
plt.savefig('author_countries_map.png',dpi=300, bbox_inches = "tight")
plt.show()


#%% LIST BY CONTINENT 

continent_gb=country_count.dropna(subset=['birthplace'])[['continent','birthplace','Book Id']].sort_values(by=['continent','Book Id'],ascending=[True,False])

continent_count=continent_gb.groupby('continent')['Book Id'].sum().reset_index().rename(columns={'Book Id':'Continent_count'})

continent_gb=continent_gb.merge(continent_count,how='left',on='continent').sort_values(['Continent_count','Book Id'],ascending=[False,False])

#%% 
def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_height()
        diff = current_width - new_value

        # we change the bar width
        patch.set_height(new_value)

        # we recenter the bar
        patch.set_y(patch.get_y() + diff * .5)
        
#%%

fig,ax=plt.subplots(2,3,figsize=(10,10))
max_count=continent_gb['Book Id'].max()
space=max_count*0.05
for cont,axis in zip(continent_gb['continent'].dropna().unique(),ax.flat):
    print(cont)
    axis.title.set_text(cont)
    plot_data=continent_gb[continent_gb['continent']==cont]
    if len(plot_data)>0:
        plot_data.replace({'United States of America':'USA','United Kingdom':'UK'},inplace=True)
        sns.barplot(data=plot_data,y='birthplace',x='Book Id',ax=axis,palette='viridis')
        label_bars(axis, plot_data['Book Id'].to_list(), label_loc='outside',space=space,str_format='{:.0f}',orientation='h',fontweight='normal',fontcolor='#333333',fontsize=10)
        #change_width(axis, .8)
        
        axis.set_xlabel('Books Read')
        
        axis.set_xticks([])
        axis.set_xlim([0,max_count+5])
        axis.set_ylim([14,-0.9])
        axis.set_ylabel(None)
    else:
        pass
    

plt.savefig('books_read_by_authors_continent.png',dpi=300, bbox_inches = "tight")
plt.show()
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
    fig,ax = plt.subplots(1,2,width_ratios=[3, 1],figsize=(12,6))

    gender_plot=my_books[['Author','Book Id','Date Read','author_gender']].set_index('Date Read').groupby([pd.Grouper(freq='Y'),'author_gender']).count().reset_index().sort_values(by='Author',ascending=False)
    dates_list=pd.date_range(gender_plot['Date Read'].min().date(),dt.datetime.now()+dt.timedelta(days=365),freq='Y')
    dates_df=pd.DataFrame({'Date Read':pd.Series(dates_list.append(dates_list)),'author_gender':pd.Series(['male']*(len(gender_plot['Date Read'].unique()))+['female']*(len(gender_plot['Date Read'].unique())))})
    gender_plot=gender_plot.merge(dates_df,how='right',on=['Date Read','author_gender']).fillna(0)
    gender_plot2=pd.melt(gender_plot.rename(columns={'Book Id':'Books','Author':'Authors'}),id_vars=['Date Read','author_gender'], value_vars=['Books']).sort_values('Date Read')

    sns.barplot(data=gender_plot2,y='value',x='Date Read',hue='author_gender',palette='viridis',ax=ax[0])
    label_bars(ax[0], gender_plot2.sort_values(['author_gender','Date Read'],ascending=[False,True])['value'].to_list(), label_loc='outside',space=1,str_format='{:.0f}',orientation='v',fontweight='normal',fontcolor='#333333',fontsize=10)
    ax[0].set_xticklabels([dt.datetime.strftime(i,'%Y') for i in gender_plot2['Date Read'].drop_duplicates().to_list()])
    axis.set_ylabel('Books Read')
    ax[0].title.set_text('By Year')
    gender_plot_all=my_books[['Author','Book Id','author_gender']].groupby('author_gender').nunique().reset_index().rename(columns={'Book Id':'Books','Author':'Authors'}).sort_values(by='Authors',ascending=False)
    gender_plot_all['percentage']=(gender_plot_all['Books']/gender_plot_all['Books'].sum())*100
    ax[1].pie(gender_plot_all['Books'],labels=['{} ({:.0f}%)'.format(i,j) for i,j in zip(gender_plot_all['author_gender'],gender_plot_all['percentage'])])
    ax[1].title.set_text('Overall')

    plt.savefig('author_gender.png',dpi=300, bbox_inches = "tight")
    plt.show()
except Exception as e:
       # Print Error Message
        print("ERROR plotting author gender data. The error is: ",e)
        
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




