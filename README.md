# regex
Makeup recommender project

#Goal

Extract makeup category, brand, product name/line, and shade mentions from each makeup tutorial (of an instagram account) into a dataframe that I will perform exploratory data analysis on and/or use to build a basic recommender. Focusing on makeup because I'm curious about colors and their creative combinations (and if this thing we call a makeup color wheel is legit).

#Ideal output

Groupdict to convert into dataframe

{'category': foundation, 'brand': @hudabeauty, 'product': #fauxfilter, 'shade': 'tres leches'; 'category': concealer, 'brand': @lancomeofficial, 'product': 'teint idole ultra wear, 'shade': '220 buff'; 'category': bronzer, 'brand': @kikomilanousa, 'product': None, 'shade': 'bronze melange'; 'category': lips, 'brand': @ofracosmetics, 'product': None, 'shade':'mocha'}

#Notebook contents (regexcode.py)

1. Single tutorial post
2. Top six patterns across posts
3. Sample dataset of data scraped from an individual beauty blogger's account on instagram
