import pandas as pd
import numpy
from keras.models import load_model 


def predictor(myinput, mymodel):
    smile=myinput
        
    themol=Chem.MolFromSmiles(smile)
    estimator = load_model(mymodel)
    
    fp = AllChem.GetMorganFingerprintAsBitVect(themol,2,nBits=2048)
    res = numpy.zeros(len(fp),numpy.int32)
    DataStructs.ConvertToNumpyArray(fp,res)
    probas = list(estimator.predict(res.reshape(1,-1))[0])
    return probas
    
    
from rdkit import Chem
import numpy as np
from rdkit.Chem import AllChem, DataStructs

def testmodels(themodel, thedata):
    newdf=pd.read_csv(thedata, sep='\t', names=['smiles', 'value'])
    validate=newdf['smiles']
    testvalidate=newdf['value']
    mypreds=[]
    mysmiles=[]
    for y in validate:
        a=predictor(y, themodel)
        mypreds.append(a)
        mysmiles.append(y)
        zippedList = list(zip(mysmiles, mypreds))
    mydf=pd.DataFrame(zippedList, columns=['My Smiles', 'My Prediction'])
    mydf.to_csv('output.txt')



