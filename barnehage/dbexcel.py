# dbexcel module
import pandas as pd



kgdata = pd.ExcelFile(r'C:\Users\47939\Github\Obligatorisk5\barnehage\kgdata.xlsx')
barnehage = pd.read_excel(kgdata, 'barnehage', index_col=0)
forelder = pd.read_excel(kgdata, 'foresatt', index_col=0)
barn = pd.read_excel(kgdata, 'barn', index_col=0)
soknad = pd.read_excel(kgdata, 'soknad', index_col=0)




"""
Referanser
[] https://www.geeksforgeeks.org/list-methods-python/
"""