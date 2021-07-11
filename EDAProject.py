#!/usr/bin/env python
# coding: utf-8

# ## <center> Exploratory Data Analytics Capstone Project </center>
# ### <center> Data Analytics On Terrorism </center>
# 
# 

# In[8]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[9]:


import seaborn as sns


# In[10]:


sns.color_palette('muted')


# ### IMPORT THE DATA

# In[14]:


data = pd.read_csv('globalterrorismdb_0718dist.csv', encoding = 'latin1')


# In[16]:


data.head()


# In[17]:


data.shape


# In[19]:


data.rename(columns={'eventid':'Eventid', 'iyear':'Year', 'imonth':'Month', 'iday':'Day', 'extended':'Extended', 
                     'resolution':'Resolution', 'attacktype1_txt':'Attacktype', 'country_txt':'Country', 
                     'region_txt':'Region', 'provstate':'Provstate', 'city':'City', 'crit1':'Crit1', 
                     'crit2':'Crit2', 'crit3':'Crit3', 'multiple':'Multiple', 'success':'Success', 
                     'suicide':'Suicide', 'targtype1_txt':'Targtype', 'natlty1_txt':'Natlty1', 
                     'natlty2_txt':'Natlty2',  'natlty3_txt':'Natlty3', 'gname':'Gname', 
                     'gname2':'Gname2', 'gname3':'Gname3', 'guncertain1':'Guncertain1', 
                     'guncertain2':'Guncertain2', 'guncertain3':'Guncertain3', 'claimed':'Claimed', 
                     'weaptype1_txt':'Weaptype', 'weapsubtype1_txt':'Weapsubtype', 'nkill':'Kill', 
                     'nkillus':'Nkillus', 'nkillter':'Nkillter', 'nwound':'Wound', 'nwoundus':'Nwoundus','nwoundte':'Nwoundter', 'property':'Property', 'propextent_txt':'Propextent', 
                     'propvalue':'Propvalue', 'ishostkid':'Ishostkid',  'nhostkid':'Nhostkid', 
                     'nhostkidus':'Nhostkidus', 'ransom':'Ransom', 'hostkidoutcome':'Hostkidoutcome', 
                     'nreleased':'Nreleased'} ,inplace=True)


# In[20]:


data.columns.values


# # keeping useful columns for the data analysis

# In[23]:


data = data[['Eventid','Year','Month','Day','Country','Provstate','Region','Provstate','City','latitude','Kill',
             'longitude','Crit1','Crit2','Crit3','Success','Suicide','Attacktype','Targtype','Natlty1','Gname', 
             'Guncertain1','Claimed', 'Weaptype','summary','motive','Wound','Extended','Ishostkid',
             'Hostkidoutcome']]


# In[24]:


data.shape


# # Descriptive analysis
# 

# In[25]:


data.describe().T


# ### Exploration of Data

# In[26]:


datacorr = data.corr()
plt.figure(figsize=(30, 20))
sns.heatmap(datacorr.iloc[:15, :15], annot=True, cmap='Greens')


# ### No of Attacks Each Year

# In[29]:


year = data['Year'].unique()
year_count = data['Year'].value_counts(dropna=True).sort_index()
plt.figure(figsize=(20, 30))
sns.barplot(x=year, y=year_count, palette='muted')
plt.xticks(rotation=50)
plt.xlabel('Attack Year', fontsize=8)
plt.ylabel('No of Attacks each year', fontsize=8)
plt.title('Attacks in Years', fontsize=12)


# - most attacks happened in the year 2014

# In[31]:


killData=data.loc[:, 'Kill']
print('No of Deaths by terror Attacks', int(sum(killData.dropna())))


# ### Terrorist Activities By region Each Year

# In[33]:


pd.crosstab(data.Year, data.Region).plot(kind='area', stacked=True, figsize=(20, 10))
plt.title('Terrorist Activities by Region Each Year')


# - top 2 regions: Middle East & South Asia

# In[34]:


attack=data.Country.value_counts()[:5]
attack


# In[37]:


plt.subplots(figsize=(20, 10))
sns.barplot(data['Country'].value_counts()[:15].index, data['Country'].value_counts()[:15].values, palette='dark')
plt.xticks(rotation=50)
plt.title('Top Counties By Attack', fontsize=15)


# In[39]:


data.Gname.value_counts()[:5]


# In[42]:


plt.subplots(figsize=(11, 10))
sns.barplot(y=data['Gname'].value_counts()[1:12].index, 
            x=data['Gname'].value_counts()[1:12].values, 
            palette='copper')
plt.title('Most Active Terrorist Groups')
plt.grid(True)


# - Most Ative Terrorist Group is Taliban

# ### Deaths By Year 

# In[47]:


df=data[['Year', 'Kill']].groupby(['Year']).sum()
plt.figure(figsize=(30, 15))
df.plot(kind='bar', color='darkred')
plt.xticks(rotation=65)
plt.title('Deaths due to Attacks', fontsize=18)


# ### Weapons Used

# In[49]:


plt.subplots(figsize=(10, 5))
sns.countplot('Weaptype', data=data, palette='inferno', order=data['Weaptype'].value_counts().index)
plt.xticks(rotation=75)
plt.xlabe=['Weapon Type']
plt.ylabel=['Count of Attacks']


# -Explosives are the most commonly used weapon by terrorists

# In[51]:


plt.subplots(figsize=(20, 10))
sns.countplot(x='Year', data=data, hue='Success')
plt.title('Trend for Increase in successful Attacks')
plt.xticks(rotation=50)
plt.xlabe=['Year']
plt.ylabel=['Number of Attacks']


# ### Attacks by Country and Region

# In[60]:


fig, axes=plt.subplots(figsize=(16, 11), nrows=1,  ncols=2)
sns.barplot(y=data['Country'].value_counts()[0:12].index, 
            x=data['Country'].value_counts()[0:12].values, ax=axes[0],
            palette='magma')
axes[0].set_title('Terrorist Attacks per Country', fontsize=15)
sns.barplot(y=data['Region'].value_counts()[0:12].index, 
            x=data['Region'].value_counts()[0:12].values, ax=axes[1])
axes[1].set_title('Terrorist Attacks per Region', fontsize=15)
fig.tight_layout()


# ### Extended VS Non-Extended Attacks

# In[56]:


fig, ax=plt.subplots(figsize=(16, 8), nrows=1,  ncols=2)
ax[0]=data[data['Extended']==1].groupby('Attacktype').count()['Extended'].sort_values().plot.barh(color='red', ax=ax[0])
ax[1]=data[data['Extended']==0].groupby('Attacktype').count()['Extended'].sort_values().plot.barh(color='green', ax=ax[1])
axes[0].set_title('No of Extended Attacks', fontsize=15)
axes[1].set_title('No of Unextended Attacks', fontsize=15)
ax[0].set_ylabel('Method')
ax[1].set_ylabel('Method')
fig.tight_layout()


# ### War on Terror

# In[59]:


df_after=data[data['Year']>=2001]
fig, ax=plt.subplots(figsize=(20, 10), nrows=2,  ncols=1)
ax[0]=pd.crosstab(data.Year, data.Region).plot(ax=ax[0])
ax[0].set_title('Changes in Region per Year')
ax[0].legend(loc='center left')
ax[0].vlines(x=2001, ymin=0,ymax=7000,color='darkgreen',linestyle='--')
pd.crosstab(df_after.Year, df_after.Region).plot.bar(stacked=True, ax=ax[1])
ax[0]=pd.crosstab(data.Year, data.Region).plot(ax=ax[0])
ax[0].set_title('Declaration of War on Terror')
ax[0].legend(loc='center left')


# # END OF PROJECT

# In[ ]:




