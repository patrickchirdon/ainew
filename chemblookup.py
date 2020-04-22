import pandas as pd
from pandas import DataFrame

def lookup(target):
	chemblframe=pd.read_csv('chembl.csv')
	
	print(chemblframe[chemblframe['2'].str.match(target)])
lookup('CDK4')		