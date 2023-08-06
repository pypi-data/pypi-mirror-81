# Project name here
> Summary description here.


This file will become your README and also the index of your documentation.

## Install

`pip install your_project_name`

## Usage

very simple usage, 
init the search object then call sortedSearch()


```python
from cloudsearch.cloudsearch import Search
searchEndpoint = 'https://search-villa-cloudsearch-2-4izacsoytzqf6kztcyjhssy2ti.ap-southeast-1.cloudsearch.amazonaws.com'
searcher = Search(searchTerm = 'banana', key=USER, pw= PW , endpoint=searchEndpoint)
result = searcher.search(size=1000)
print(f'found {len(list(result))} results, the first item is \n{next(iter(result))}')
```

    found 455 results, the first item is 
    {'pr_country_en': 'Thailand', 'psqty': '1.0', 'ordertype': 'Y', 'pstype': '1', 'pr_abb': 'BANANA', 'pr_puqty': '1.0', 'pr_engname': 'BANANA', 'pr_name': 'BANANA', 'pr_dpcode': '19', 'pr_keyword_en': 'banana,bananas,Cavendish Banana,Cavendish,,Fresh fruit', 'cprcode': '0226238', 'pr_ggcode': '191', 'pr_market': 'BANANA', 'pr_sucode1': 'CM1906', 'prtype': 'I', 'villa_category_l2_en': 'Fresh Produce', 'content_en': '0226238 BANANA banana,bananas,Cavendish Banana,Cavendish,,Fresh fruit', 'iprcode': '0226238', 'oprcode': '0226238', 'villa_category_l3_en': 'Fruits & Vegetable Local', 'pr_keyword_th': 'กล้วย,กล้วยหอม,กล้วยไข่,กล้วยออร์แกนิก,กล้วออร์แกนิค,Fresh fruit', 'pr_cgcode': '26', 'pr_code': '0226238', 'villa_category_l4_en': 'Local Fruit', 'pr_sa_method': '1', 'content_th': 'BANANA กล้วย,กล้วยหอม,กล้วยไข่,กล้วยออร์แกนิก,กล้วออร์แกนิค,Fresh fruit', 'pr_active': 'Y', 'pr_suref3': 'A', 'villa_category_l1_en': 'Fresh'}


## For a more complex requirement
You can extend the class, please have a look at sortedSearch example

```python
_ = searcher.sortedSearch()
```

    raw search result is     villa_category_l1_en villa_category_l2_en      villa_category_l3_en  \
    0                  Fresh        Fresh Produce  Fruits & Vegetable Local   
    1                    NaN                  NaN                       NaN   
    2                  Fresh        Fresh Produce                    Bakery   
    3                  Fresh        Fresh Produce                    Bakery   
    4                  Fresh        Fresh Produce                    Bakery   
    ..                   ...                  ...                       ...   
    450                Fresh        Seafood Fresh                Crustacean   
    451                Fresh        Seafood Fresh                Crustacean   
    452                Fresh        Seafood Fresh                Crustacean   
    453                Fresh               Frozen                   Seafood   
    454                Fresh        Seafood Fresh             Local Seafood   
    
        villa_category_l4_en  
    0            Local Fruit  
    1                    NaN  
    2          Cake category  
    3          Cake category  
    4         Pasty category  
    ..                   ...  
    450                Local  
    451                Local  
    452                Local  
    453                  NaN  
    454                  NaN  
    
    [455 rows x 4 columns]

