#!/usr/bin/env python
# coding: utf-8

# In[51]:


import requests
from bs4 import BeautifulSoup as bs
import os
from pathlib import Path
import pandas as pd
import csv


# ### Get Recipes from AllRecipes.com

# In[2]:


# make soup from main page
r = requests.get("https://www.allrecipes.com/recipes-a-z-6735880")
soup = bs(r.content)

# grab categories links from main page
categories = [cat_links['href'] for cat_links in soup.find(attrs={'class':'comp alphabetical-list mntl-block'}).find_all('a')]
print(categories)


# In[3]:


# check links
len(categories), len(set(categories))


# In[ ]:


# scrape for recipes part one

titles = []
recipes = []
ingredients = []


# In[111]:


# scrape for recipe links
for category in categories:
    
    r = requests.get(category)
    soup = bs(r.content)
    print(f"starting category: {category}")
    
    recipe_links = [rec_links['href'] for rec_links in soup.find(attrs={'class':'loc fixedContent'}).find_all('a')]    
    
    for recipe_link in recipe_links:
        if recipe_link == '/account/profile#/collections':
            continue
        else:
            print(f"downloading recipe... {recipe_link}")
            r = requests.get(recipe_link)
            soup = bs(r.content)

            try:
                recipe_title = [paragraph for paragraph in soup.find(attrs={'id':'allrecipes-article_1-0'}).find('h1')]
            except AttributeError:
                print(f"Skipping {recipe}.")
                continue
            titles.append(recipe_title)

            try:
                recipe_text = [paragraph.text for paragraph in soup.find(attrs={'id':'article-content_1-0'}).find_all('p')]
            except AttributeError:
                print(f"Skipping {recipe}.")
                continue
            recipes.append(recipe_text)

            try:
                ingredients_text = [paragraph.text for paragraph in soup.find(attrs={'id':'mntl-lrs-ingredients_1-0'}).find_all('ul')]
            except AttributeError:
                print(f"Skipping {recipe}.")
                continue
            ingredients.append(str(ingredients_text))


# In[112]:


#check for recipes
print(len(titles), len(ingredients), len(recipes))


# In[113]:


# write to csv to prevent losing data
df = pd.DataFrame([titles, ingredients, recipes])
df.to_csv('recipes_part1.csv')


# In[4]:


# find start for part two
print(categories.index("https://www.allrecipes.com/recipes/1023/meat-and-poultry/beef/steaks/flank-steak/"))


# In[116]:


titles2 = []
recipes2 = []
ingredients2 = []

category_links_part2 = [118:283]
for category in category_links_part2:
    
    r = requests.get(category)
    soup = bs(r.content)
    print(f"STARTING CATEGORY: {category}")
    
    recipe_links = [rec_links['href'] for rec_links in soup.find(attrs={'class':'loc fixedContent'}).find_all('a')]    
    
    for recipe_link in recipe_links:
        if recipe_link == '/account/profile#/collections':
            continue
        else:
            print(f"Downloading recipe... {recipe_link}")
            r = requests.get(recipe_link)
            soup = bs(r.content)

            try:
                recipe_title = [paragraph for paragraph in soup.find(attrs={'id':'allrecipes-article_1-0'}).find('h1')]
            except AttributeError:
                print(f"--Skipping title of {recipe}.")
                continue
            titles2.append(recipe_title)

            try:
                recipe_text = [paragraph.text for paragraph in soup.find(attrs={'id':'article-content_1-0'}).find_all('p')]
            except AttributeError:
                print(f"--Skipping recipe of {recipe}.")
                continue
            recipes2.append(recipe_text)

            try:
                ingredients_text = [paragraph.text for paragraph in soup.find(attrs={'id':'mntl-lrs-ingredients_1-0'}).find_all('ul')]
            except AttributeError:
                print(f"--Skipping ingredients of {recipe}.")
                continue
            ingredients2.append(str(ingredients_text))
            
print ("Completed List2.")


# In[119]:


# save recipes
df2 = pd.DataFrame([titles2, ingredients2, recipes2])
df2.to_csv('recipes_part2.csv')


# In[118]:


# check progress
print(len(titles2), len(ingredients2), len(recipes2))


# In[ ]:


# find start for part three
print(categories.index("https://www.allrecipes.com/recipes/13378/side-dish/sauces-and-condiments/relishes/"))


# In[121]:


#curious how many categories are left
len(categories[282:])


# In[5]:


# scrape for recipes part three
titles3 = []
recipes3 = []
ingredients3 = []

category_links_part3 = categories[282:]
for category in category_links_part3:
    
    r = requests.get(category)
    soup = bs(r.content)
    print(f"STARTING CATEGORY: {category}")
    
    recipe_links = [rec_links['href'] for rec_links in soup.find(attrs={'class':'loc fixedContent'}).find_all('a')]    
    
    for recipe_link in recipe_links:
        if recipe_link == '/account/profile#/collections':
            continue
        else:
            print(f"Downloading recipe... {recipe_link}")
            r = requests.get(recipe_link)
            soup = bs(r.content)

            try:
                recipe_title = [paragraph for paragraph in soup.find(attrs={'id':'allrecipes-article_1-0'}).find('h1')]
            except AttributeError:
                print(f"--Skipping title of {recipe_link}.")
                continue
            titles3.append(recipe_title)

            try:
                recipe_text = [paragraph.text for paragraph in soup.find(attrs={'id':'article-content_1-0'}).find_all('p')]
            except AttributeError:
                print(f"--Skipping recipe of {recipe_link}.")
                continue
            recipes3.append(recipe_text)

            try:
                ingredients_text = [paragraph.text for paragraph in soup.find(attrs={'id':'mntl-lrs-ingredients_1-0'}).find_all('ul')]
            except AttributeError:
                print(f"--Skipping ingredients of {recipe_link}.")
                continue
            ingredients3.append(str(ingredients_text))
            
print ("Completed full List. :)")


# In[6]:


# check recipes
print(len(titles3), len(ingredients3), len(recipes3))


# In[8]:


# save
df3 = pd.DataFrame([titles3, ingredients3, recipes3])
df3.to_csv('recipes_part3.csv')


# ### Cleaning the Data

# In[3]:


df1 = pd.read_csv('recipes_part1.csv')
print(len(df1.to_string()))
df2 = pd.read_csv('recipes_part2.csv')
print(len(df2.to_string()))
df3 = pd.read_csv('recipes_part3.csv')
print(len(df3.to_string()))


# In[4]:


all_recipes_df = pd.concat([df1, df2, df3], ignore_index=True)


# In[5]:


all_recipes_df.head()


# In[9]:


df1.head()


# In[10]:


df2.head()


# In[8]:


df3.head()


# In[15]:


df1_t = df1.transpose()
df1_t.head()


# In[16]:


df2_t = df2.transpose()
df3_t = df3.transpose()


# In[17]:


df_test = df1_t.append(df2_t)
df_test.head()


# In[18]:


df_test.tail()


# In[19]:


df_recipes = df_test.append(df3_t)
df_recipes.info()


# In[20]:


df_recipes = df_recipes.dropna()


# In[21]:


df_recipes.info()


# In[23]:


duplicates = df_recipes.duplicated()


# In[24]:


duplicates.head()


# In[37]:


i = 0
for dup in duplicates:
    if dup == True:
        i += 1
    else:
        continue
print(i)


# In[40]:


df_recipes.drop_duplicates(inplace = True)
df_recipes.info()


# In[41]:


df_recipes.to_csv('cleaned_ish_recipes.csv')


# In[82]:


recipes = pd.read_csv('cleaned_ish_recipes.csv')
recipes.head()


# In[84]:


recipes.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["",""], regex=True, inplace=True)
recipes.columns=['idk','Title','Ingredients','Recipe']
recipes.head()


# In[85]:


del recipes['idk']


# In[86]:


recipes.head()


# In[87]:


recipes.to_csv('recipes_data.csv', index=False)


# In[75]:


df_recipes.set_index(['Title','Ingredients','Recipe'], append=True)
df_recipes.head()


# In[79]:


df_recipes.drop(columns=df_recipes.columns[0], axis=1, inplace=True)
df_recipes.head()


# ### Test Code Below This Point

# In[92]:


# testing recipe scraper
titles = []
recipes = []
ingredients = []
all_links_test = ['https://www.allrecipes.com/recipe/24239/vietnamese-fresh-spring-rolls/','https://www.allrecipes.com/recipes/88/bbq-grilling/', 'https://www.allrecipes.com/recipes/92/meat-and-poultry/']
for recipe in all_links_test:
    r = requests.get(recipe)
    soup = bs(r.content)
    
    recipe_title = [paragraph for paragraph in soup.find(attrs={'id':'allrecipes-article_1-0'}).find('h1')]
    titles.append(recipe_title)
    if AttributeError:
        print(f"skipped: {recipe}.")
    continue
    recipe_text = [paragraph.text for paragraph in soup.find(attrs={'id':'article-content_1-0'}).find_all('p')]
    recipes.append(recipe_text)
    ingredients_text = [paragraph.text for paragraph in soup.find(attrs={'id':'mntl-lrs-ingredients_1-0'}).find_all('ul')]
    ingredients.append(str(ingredients_text))
    
df = pd.DataFrame([recipes_title_test, ingredients_text_test, recipes_text_test])
df.to_csv('recipes.csv')

print(len(recipes_title_test))
print(len(recipes_text_test))
print(len(ingredients_text_test))


# In[92]:


# make soup from category links
r = requests.get("https://www.allrecipes.com/recipes/14787/everyday-cooking/make-ahead/")
soup = bs(r.content)
# print(soup.prettify())


# In[100]:


# Recipe Soup url
recipes_title_test = []
recipes_text_test = []
ingredients_text_test = []


recipe_links_test = ['https://www.allrecipes.com/recipe/240502/easy-french-toast-casserole/', 'https://www.allrecipes.com/recipes/156/bread/','https://www.allrecipes.com/recipe/84892/strawberry-vanilla-pancakes/']
for recipe in recipe_links_test:
    r = requests.get(recipe)
    soup = bs(r.content)
    
    try:
        recipe_title = [paragraph for paragraph in soup.find(attrs={'id':'allrecipes-article_1-0'}).find('h1')]
    except AttributeError:
        print(f"Skipping {recipe}.")
        continue
    recipes_title_test.append(recipe_title)
    
    recipe_text = [paragraph.text for paragraph in soup.find(attrs={'id':'article-content_1-0'}).find_all('p')]
    recipes_text_test.append(recipe_text)
    
    ingredients_text = [paragraph.text for paragraph in soup.find(attrs={'id':'mntl-lrs-ingredients_1-0'}).find_all('ul')]
    ingredients_text_test.append(str(ingredients_text))
    
df = pd.DataFrame([recipes_title_test, ingredients_text_test, recipes_text_test])
df.to_csv('recipes_testing.csv')

print(len(recipes_title_test))
print(len(recipes_text_test))
print(len(ingredients_text_test))


# In[ ]:




