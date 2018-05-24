
# coding: utf-8

# # Read the Datafile

# In[3]:


import pandas as pd
import numpy as np
star_wars = pd.read_csv("./databank/StarWars.csv", encoding="ISO-8859-1")
star_wars.head(10)


# # Removing the RespondentID Irregularities

# In[4]:


star_wars = star_wars[pd.notnull(star_wars["RespondentID"])]
star_wars.head()


# # Converting to Boolean Data Type

# In[5]:


bool_dict = {"Yes": True, "No": False, np.nan: False}

star_wars["Have you seen any of the 6 films in the Star Wars franchise?"].map(bool_dict)
star_wars["Do you consider yourself to be a fan of the Star Wars film franchise?"].map(bool_dict)
print(star_wars["Have you seen any of the 6 films in the Star Wars franchise?"].unique())
print(star_wars["Do you consider yourself to be a fan of the Star Wars film franchise?"].unique())


# # Change Views Movies Column Names 

# In[6]:


column_names = star_wars.columns.values
for each in range(3,9):
    column_names[each] = "seen_" + str(each-2)
star_wars.columns = column_names

star_wars.columns


# # Converting Movie Response to Boolean Type

# In[7]:


movies = {
    "Star Wars: Episode I  The Phantom Menace": True, 
    np.nan: False, 
    "Star Wars: Episode II  Attack of the Clones": True,
    "Star Wars: Episode III  Revenge of the Sith": True,
    "Star Wars: Episode IV  A New Hope": True,
    "Star Wars: Episode V The Empire Strikes Back": True,
    "Star Wars: Episode VI Return of the Jedi": True
}

for cols in star_wars.columns[3:9]:
    star_wars[cols] = star_wars[cols].map(movies)

star_wars[3:9].head()


# # Change Movie Ranking Columns Names

# In[8]:


column_names = star_wars.columns.values
for i in range(9, 15):
    column_names[i] = "ranking_" + str(i-8)
star_wars.columns = column_names

print(star_wars.columns[9:15])


# # Change Movie Ranking Columns Data Type

# In[9]:


star_wars[star_wars.columns[9:15]] = star_wars[star_wars.columns[9:15]].astype(float)
print(star_wars["ranking_6"].dtype)


# # Plot Average Ranking of Movies

# In[10]:


cols = star_wars.columns[9:15]
bar_heights = star_wars[cols].mean()
print("Average Movie Rankings\n", bar_heights)


# In[11]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

fig, ax = plt.subplots()
bar_positions = range(1,7)

ax.set_xlim(0,7)
ax.bar(bar_positions, bar_heights, 0.40, align="center")
ax.set_xticks(range(1,7))
ax.set_xticklabels(cols, rotation=90)
ax.set_xlabel("Movie Names")
ax.set_title("Movie Average Rankings")    


# # Report Number of Movies Seen

# In[12]:


col = star_wars.columns[3:9]
print(star_wars[col].sum())


# # Plot Number of Movies Seen

# In[13]:


cols = star_wars.columns[3:9].values

fig, ax = plt.subplots()
ax.bar(range(1,7), star_wars[cols].sum(), 0.5, align="center")
ax.set_xticks(range(1,7))
ax.set_xticklabels(cols, rotation=90)
ax.set_xlabel("Movies Seen")
ax.set_title("Frequency of Movie Viewes")


# # Split Database into Male & Female Groups

# In[14]:


males = star_wars[star_wars["Gender"] == "Male"]
females = star_wars[star_wars["Gender"] == "Female"]
print(males["Gender"].head())
print(females["Gender"].head())


# # Report # of Movies Seen by Males

# In[15]:


print(males[cols].sum())


# # Plot # of Movies Seen by Males

# In[16]:


fig, ax = plt.subplots()
ax.bar(range(1,7), males[cols].sum(), 0.5, align="center")
ax.set_xticks(range(1,7))
ax.set_xticklabels(cols, rotation=90)
ax.set_xlabel("Movies Seen by Males")
ax.set_title("Frequency of Movie Viewed by Males")


# # Report # of Movies Seen by Females

# In[17]:


print(females[cols].sum())


# # Plot # of Movies Seen by Females

# In[18]:


fig, ax = plt.subplots()
ax.bar(range(1,7), females[cols].sum(), 0.5, align="center")
ax.set_xticks(range(1,7))
ax.set_xticklabels(cols, rotation=90)
ax.set_xlabel("Movies Seen by Females")
ax.set_title("Frequency of Movie Viewed by Female")


# # Plot Average Movie Rankings by Males

# In[19]:


cols = star_wars.columns[9:15].values
print( males[cols].mean())


# In[20]:


fig, ax = plt.subplots()
ax.bar(range(1,7), males[cols].mean(), 0.40, align="center")
ax.set_xticks(range(1,7))
ax.set_xticklabels(cols, rotation=90)
ax.set_xlabel("Movie Names")
ax.set_title("Movie Average Rankings by Males")   


# # Plot Average Movie Rankings by Females

# In[21]:


print(females[cols].mean())


# In[22]:


fig, ax = plt.subplots()
ax.bar(range(1,7), females[cols].mean(), 0.40, align="center")
ax.set_xticks(range(1,7))
ax.set_xticklabels(cols, rotation=90)
ax.set_xlabel("Movie Names")
ax.set_title("Movie Average Rankings by Females")   


# ## Finding the Characters' Preference Pattern

# In[23]:


print(star_wars['Please state whether you view the following characters favorably, unfavorably, or are unfamiliar with him/her.'].unique())


# ## Providing Character Rating Column Names

# In[24]:


cols = star_wars.columns.values
for i in range(15,29):
    cols[i] = "character_" + str(i-14)
star_wars.columns = cols
print(star_wars.columns[15:29])
print(star_wars['character_5'].unique())


# ## Filtering the Character Rating Column Responses

# In[25]:


cols = star_wars.columns[15:29].values
for col in cols:
    star_wars[col] = star_wars[~star_wars[col].isin(['Unfamiliar (N/A)'])][col]
    star_wars = star_wars.dropna(subset=[col])


# ## Setup the Voting Index based on the Character Ranking

# In[26]:


# Assigning voting map based on the level of likes/dislikes
char_map = {
    'Very favorably': 2,
    'Somewhat favorably': 1,
    'Neither favorably nor unfavorably (neutral)': 0,
    'Somewhat unfavorably': -1,
    'Very unfavorably': -2,
}

for i in star_wars.columns[15:29]:
    star_wars[i] = star_wars[i].map(char_map)
star_wars.iloc[:,15:29].head()


# ## Segregatting Respondents Voting Preferences

# In[27]:


for i in range(2):
    for col in cols:
        if i == 0:
            star_wars[col + str("_likes")] = star_wars[star_wars[col] > 0][col]
        else:
            star_wars[col + str("_dislikes")] = star_wars[star_wars[col] <= 0][col]
            
print(star_wars.columns[38:68])


# ## Respondents "Like" Response for Characters

# In[28]:


print(star_wars.iloc[:,38:52].sum().sort_values(ascending=False))


# ## Respondents "Dislike" Response for Characters

# In[29]:


print(star_wars.iloc[:,52:69].sum().sort_values())


# ## Plot of Respondents' Character Preference Pattern

# In[30]:


col_like = star_wars.columns[38:52].values
col_dislike = star_wars.columns[52:69].values
char_names = star_wars.columns[15:29].values
bar_height_like = star_wars[col_like].sum()
bar_height_dislike = star_wars[col_dislike].sum()
  
fig, ax = plt.subplots()
ax.bar(range(1,15), bar_height_like, 0.40, align="center", color="blue")
ax.bar(range(1,15), bar_height_dislike, 0.40, align="center", color='red')
ax.set_xticks(range(1,15))
ax.set_xticklabels(char_names, rotation=90)
ax.set_xlabel("Character Names")
ax.set_ylabel("Voting Index")
ax.set_title("Characters Popularity") 
plt.show()


# ## Male Respondents' "Like" Response for Characters

# In[31]:


col_like = list(star_wars.columns[38:52])
male_char_like = star_wars[star_wars["Gender"] == "Male"][col_like]
print(male_char_like.sum().sort_values(ascending=False))


# ## Male Respondents' "Dislike" Response for Characters

# In[32]:


col_dislike = list(star_wars.columns[52:69])
male_char_dislike = star_wars[star_wars["Gender"] == "Male"][col_dislike]
print(male_char_dislike.sum().sort_values())


# ## Plot of Male Respondents' Character Preference Pattern

# In[33]:


bar_height_like = male_char_like.sum()
bar_height_dislike = male_char_dislike.sum()
  
fig, ax = plt.subplots()
ax.bar(range(1,15), bar_height_like, 0.40, align="center", color="yellow")
ax.bar(range(1,15), bar_height_dislike, 0.40, align="center", color='green')
ax.set_xticks(range(1,15))
ax.set_xticklabels(char_names, rotation=90)
ax.set_xlabel("Character Names")
ax.set_ylabel("Voting Index")
ax.set_title("Characters Popularity for Males") 
plt.show()


# ### Female Respondents' "Like" Response for Characters

# In[34]:


col_like = list(star_wars.columns[38:52])
female_char_like = star_wars[star_wars["Gender"] == "Female"][col_like]
print(female_char_like.sum().sort_values(ascending=False))


# ### Female Respondents' "Dislike" Response for Characters

# In[35]:


col_dislike = list(star_wars.columns[52:69])
female_char_dislike = star_wars[star_wars["Gender"] == "Female"][col_dislike]
print(female_char_dislike.sum().sort_values())


# ### Plot of Female Respondents' Character Preference Pattern

# In[36]:


bar_height_like = female_char_like.sum()
bar_height_dislike = female_char_dislike.sum()
  
fig, ax = plt.subplots()
ax.bar(range(1,15), bar_height_like, 0.40, align="center", color="black")
ax.bar(range(1,15), bar_height_dislike, 0.40, align="center", color='grey')
ax.set_xticks(range(1,15))
ax.set_xticklabels(char_names, rotation=90)
ax.set_xlabel("Character Names")
ax.set_ylabel("Voting Index")
ax.set_title("Characters Popularity for Females") 
plt.show()


# ## Conclusion about favorite Star Wars movies
1. Earlier movies appear to be more popular since the respondents tend to see more original movies than the new movies. 
2. On an average more males watched the scenes 1 thru 3 than the female. However, females liked episodes_3 more than the males.
3. The respondents overall like character_1 the most followed by the character_5 and character_14.
4. The respondents overall dislike character_12 the most followed by the character_6 and character_7.
5. The average weightage of women's characters preference is around 72% that of male's characters preference. 
6. Considering thin marginal spread between the likes and dislikes for character_6; respondents' preference for this character appear to be controversial.