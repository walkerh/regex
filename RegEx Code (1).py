#!/usr/bin/env python
# coding: utf-8

# # Overview

# **Goal**
# 
# Extract makeup category, brand, product name/line, and shade mentions from each makeup tutorial (of an instagram account) into a dataframe that I will perform exploratory data analysis on and/or use to build a basic recommender (purposely scraped data for medium-tan skintones). Focusing on makeup because I'm curious about colors and their creative combinations.
# 
# **Ideal output**
# 
# Groupdict to convert into dataframe
# 
# {'category': foundation, 'brand': @hudabeauty, 'product': #fauxfilter, 'shade': 'tres leches'; 'category': concealer, 'brand': @lancomeofficial, 'product': 'teint idole ultra wear, 'shade': '220 buff'; 'category': bronzer, 'brand': @kikomilanousa, 'product': None, 'shade': 'bronze melange'; 'category': lips, 'brand': @ofracosmetics, 'product': None, 'shade':'mocha'}
# 
# **Notebook contents**
# 
# 1. Single tutorial post
# 2. Top six patterns across posts
# 3. Sample dataset of data scraped from an individual beauty blogger's account on instagram

# # Practice on single tutorial post

# In[1]:


import re
import pandas as pd
import nltk
from nltk import regexp_tokenize, sent_tokenize
import os

post1 = 'paox33Matte eyes and glossy lips 😋 featuring my baby hairs👶🏻🙃Eyes : @urbandecaycosmetics #urbandecay #nakedheatpalette Lashes : @lillylashes #lillylashes "lush" Mascara : @eyeko #eyekolashalertmascara Lips : @doseofcolors "knock on wood " topped off with @beccacosmetics #BECCAGlowGloss opal x jadeFoundation : @frankierosecosmetics #frankierosecosmetics shade "gold" coupon code for discount (paox) Brows : @benefitcosmetics #benefitbrows kabrow 04Bronzer : @benefitcosmetics #hoolabronzer Highlighter : @kikomilanousa glow fusion shade "03" used it on the inner corner of the eye as well #kikomilano #paox33 #hudabeauty #wakeupandmakeup #vegas_nay #motd #makeup #lillyghalichi139w'
post1


# In[143]:


#Lowercase text
post1 = post1.lower()

#Remove emojis
emoji = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)

#post1.decode('utf-8')
post1 = re.sub(emoji, " ", post1)
post1


# In[144]:


#Identify makeup categories; code for partitioning continuous strings in next section
re.findall(r"\w+\s\:+", post1)


# In[145]:


#Trim trailing whitespace (i.e. "foundation :" to "foundation:")
post1 = re.sub(r"(\s:\s)", ": ", post1)
post1


# In[146]:


#Insert new line breaks before category mention to mark ending of 'sentence' (i.e. category + brand + product + shade is one sentence)
#Couldn't figure out how to regexp_tokenize
post1 = re.sub(r"(?=\s\w+:)", ".",post1)
post1


# In[147]:


#Quickly scan sentences created
re.findall(r"(\w+\:+)\s(\@\w+)+\s(.+?)\.", post1)


# In[148]:


#Compile regex for category + brand + product + shade
r = re.compile(r'(?P<category>\w+\:+)\s+(?P<brand>\@\w+)\s[^."]*(?:"(?P<shade>.+?)")?[^."]*(?:\.\s+|$)')

#Convert matches into dictionary
for m in r.finditer(post1):
    print m.groupdict()
    
#Convert dictionary to dataframe
df = pd.DataFrame([m.group('category', 'brand', 'shade') for m in r.finditer(post1)], columns = ['Category', 'Brand', 'Shade'])
df['Category'] = df['Category'].str.replace(r"\:", "")
df['Brand'] = df['Brand'].str.replace(r"\@", "")
df


# # Practice on dataset with top six patterns

# **Key Questions:**
# 
# 1. How to best remove emojis
# 
# 2. How to deal with continuous strings (common continuous strings are in category mentions - i.e. jadeFoundation, 03concealer, whereby previous category's shade and next category phrase are bunched up)
# 
# 3. How to ensure category matches to related brand + product + shade in groupdict (for now, I inserted periods before each category mention to mimick sentences/keep the phrases 'together')
# 
# 4. How to capture groups of text with 2-4 regex patterns and when sometimes the groups of text don't exist
# 
# Note: I think category/product can be interchangable

# In[2]:


google_sheet_url = 'https://docs.google.com/spreadsheets/d/1KjMgV-tUFVRhYo81tQd87Za6xqGhWFFG3oIETUNybOs/export?format=csv&gid=340079439'
df = pd.read_csv(google_sheet_url)


# In[3]:


#Lowercase
df['Description'] = df['Description'].str.decode('utf-8')
df['Description'] = df['Description'].str.lower()
df


# **RegEx Pattern (1)**: [@brand + 'product'/'shade'] & [@brand + 'product'/'shade' + 'category'] &  [@brand + 'category' + 'shade']

# In[5]:


post0 = df['Description'][0]
post0


# In[ ]:


r=
re.compile(r'(?P<category>\w+\:+)\s+(?P<brand>\@\w+)\s[^."]*(?:"(?P<shade>.+?)")?[^."]*(?:\.\s+|$)')


r0=
re.compile(r')


# **RegEx Pattern (2)**: [@brand + 'shade' + 'category'] & [@brand + 'category' + 'shade'] & [@brand + 'product' & @brand + 'shade']

# In[212]:


df['Description'][1]


# **RegEx Pattern (3)**: [@brand + 'category'/'product' + 'shade'] & [@brand + 'product' + 'shade'] & [@brand + 'shade' + 'category'/'product']

# In[213]:


df['Description'][2]


# **RegEx Pattern (4)**: [@brand + 'shade(s)' + 'category'/'product'] & [@brand + 'product' + 'shade(s)'] & ['category: ' + @brand + 'product' + 'shade(s)']

# In[214]:


df['Description'][3]


# **RegEx Pattern (5)**: [@brand + 'shade' + 'category/product'] & [@brand + 'category']

# In[215]:


df['Description'][4]


# **RegEx Pattern**: 'category :'/'category@'/'category @' + brand + product/shade; brand + shade + category/product

# In[216]:


df['Description'][5]


# In[192]:


#Identify makeup categories
category = r"()"
[re.findall(category, row) for row in df]


# In[ ]:


#Identify continuous strings
continuous = r"\w+bronzer\s[@:]|\w+foundation\s[@:]|\w+lips\s[@:]|\w+lip\s[@:]|\w+lipgloss\s[@:]|\w+concealer\s[@:]|\w+blush\s[@:]|\w+corrector\s[@:]|\w+lipliner\s[@:]|\w+eye\s[@:]|\w+lipstick\s[@:]|\w+contour\s[@:]|\w+palette\s[@:]|\w+eyeshadow\s[@:]|\w+eyeliner\s[@:]|\w+brows\s[@:]|\w+highlight\s[@:]|\w+gloss\s[@:]|\w+stick\s[@:]|\w+glow\s[@:]"
continuous = [re.findall(continuous, row) for row in df]
continuous


# In[ ]:


#Partition continuous strings
categories = [
    "foundation", "bronzer", "lips", "lip", "lipliner", "lipliners", "liner", "lipstick", "lipgloss", 
    "eyes", "eyeshadow", "eyebrows", "eyeliner", "brows", "concealer", "blush", "contour", 
    "corrector", "palette", "highlight", "highlighter", "gloss", "stick", "glow"]

df = [re.sub(r"({seps})".format(seps='|'.join(categories)), r' \1', i) for i in df]


# In[ ]:





# # Practice on dataset (scraped data from one instagram account)

# In[172]:


google_sheet_url_pao = 'https://docs.google.com/spreadsheets/d/1AuyA_Q_12EOT8gJ7S2Lm4_j-JBPESeA8NQCuLkkjsmw/export?format=csv&gid=1775475691'
pao_df = pd.read_csv(google_sheet_url_pao)
pao_df['Description'] = pao_df['Description'].str.decode('utf-8')
pao_df['Description'] = pao_df['Description'].str.lower()
pao_df = pao_df['Description']
pao_df


# In[111]:


#Remove emojis
emoji = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)

pao_df = [re.sub(emoji, " ", row) for row in pao_df]
pao_df


# In[112]:


#Identify makeup categories
makeup = r"\w+\s+?[@:-]"
[re.findall(makeup, row) for row in pao_df]

# In[115]:

#Identify continuous strings
continuous = r"\w+bronzer\s[@:]|\w+foundation\s[@:]|\w+lips\s[@:]|\w+lip\s[@:]|\w+lipgloss\s[@:]|\w+concealer\s[@:]|\w+blush\s[@:]|\w+corrector\s[@:]|\w+lipliner\s[@:]|\w+eye\s[@:]|\w+lipstick\s[@:]|\w+contour\s[@:]|\w+palette\s[@:]|\w+eyeshadow\s[@:]|\w+eyeliner\s[@:]|\w+brows\s[@:]|\w+highlight\s[@:]|\w+gloss\s[@:]|\w+stick\s[@:]|\w+glow\s[@:]"
continuous = [re.findall(continuous, row) for row in pao_df]
continuous

# In[116]:

#Partition continuous strings
categories = [
    "foundation", "bronzer", "lips", "lip", "lipliner", "lipliners", "liner", "lipstick", "lipgloss", 
    "eyes", "eyeshadow", "eyebrows", "eyeliner", "brows", "concealer", "blush", "contour", 
    "corrector", "palette", "highlight", "highlighter", "gloss", "stick", "glow"]

pao_df = [re.sub(r"({seps})".format(seps='|'.join(categories)), r' \1', i) for i in pao_df]

#Approach B
#pao_df = [re.sub(r'(?=(?:foundation|bronzer|lips|lip|lipliner|liner|lipstick|lipgloss|eyes|eyeshadow|eyebrows|eyeliner|brows|concealer|blush|contour|corrector|palette|highlight|highlighter|gloss|stick|glow) )', " ", i) for i in pao_df]
#pao_df = [re.sub(r'(?=(?:foundation|bronzer|lips|lip|lipliner|liner|lipstick|lipgloss|eyes|eyeshadow|eyebrows|eyeliner|brows|concealer|blush|contour|corrector|palette|highlight|highlighter|gloss|stick|glow))', " ", i) for i in pao_df]
#pao_df


# In[117]:


#Trim trailing whitespace after category mention, before colon (i.e. "foundation :" to 'foundation:')
pao_df = [re.sub(r"(\s:\s)", ": ", i) for i in pao_df]

#Add space between colon and @ in category mentions (i.e. 'foundation:@' to 'foundation: @')
pao_df = [re.sub(r"(\w+\:@)", "\w+\: @", i) for i in pao_df]
pao_df


# In[118]:


#Encode dataset (result still has \xe2...)
pao_df = [i.encode('utf-8') for i in pao_df]
pao_df


# In[119]:


# Create regex patterns for each category, brand, product, shade
# Note sometimes product is mentioned, sometimes not

category = r"(\w+\?:s\[@:-]+\s)" #patterns ["eyes:", "eyes : ", "eyes @", "eyes-"]
brand = r"(\@\w+\s)" #pattern ["@urbandecaycosmetics "] #also comes after category
product = r"(\w+(?=\@\w+\s))" #typically text that comes after brand mention and before shade
shade = r"()" #patterns ["'gold'", "shade 8&9", "in number 4", ""] #typically mentioned after product and before category

# Compile regex and tokenize
[regexp_tokenize(i, r"(\w+\?:s\[@:]+\s\.+?\.)") for i in pao_df]


# In[33]:


#If sent_tokenize doesn't work, add periods

#pao_df = [re.sub(r"(?=\s+\w+\s+@)", ".", i) for i in pao_df]
#pao_df = [re.sub(r"(?=\s+\w+\:)", ".", i) for i in pao_df]
#pao_df

#Compile regex to find makeup categories
[re.findall(r"(\w+\?:s\[@:]+\s\@\w+\s.+?\?:w+@)", i) for i in pao_df]


# In[500]:


r3 = [re.findall(r'(?P<category>\w+\:+)\s+(?P<brand>\@\w+)\s[^."]*(?:"(?P<shade>.+?)")?[^."]*(?:\.\s+|$)', i) for i in pao_df]

#Convert matches into dictionary
for m in r3.finditer(pao_df):
    print m.groupdict()
    
#Convert dictionary to dataframe
df = pd.DataFrame([m.group('category', 'brand', 'shade') for m in r3.finditer(i) for i in pao_df], columns = ['Category', 'Brand', 'Shade'])
df['Category'] = df['Category'].str.replace(r"\:", "")
df['Brand'] = df['Brand'].str.replace(r"\@", "")
df


# In[ ]:




