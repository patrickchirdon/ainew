import pandas as pd # uses pandas python module to view and analyse data
import requests # this is used to access json files

f2=open('output.txt', 'w+')

#====================================================================#

# using a list of known targets, find compounds that are active on these targets:

def find_bioactivities_for_targets(targets):

    targets = ",".join(targets) # join the targets into a suitable string to fulfil the search conditions of the ChEMBL api
    assay_type = 'B' # only look for binding assays
    pchembl_value = 5 # xxx specify a minimum threshold of the pCHEMBL activity value. Greater than or equal to 5 (10 microM) is a typical minimum rule of thumb for binding activity between a compound and a protein target
    limit = 100 # limit the number of records pulled back for each url call xxx

    # set up the call to the ChEMBL 'activity' API.
    # Remember that there is a limit to the number of records returned in any one API call (default is 20 records, maximum is 1000 records).
    # So we need to iterate over several pages of results to gather all relevant information together.
    url_stem = "https://www.ebi.ac.uk" #This is the stem of the url
    url_full_string = url_stem + "/chembl/api/data/activity.json?target_chembl_id__in={}&assay_type={}&pchembl_value__gte={}&limit={}".format(targets
, assay_type, pchembl_value, limit) #This is the full url with the specified input parameters
    url_full = requests.get( url_full_string ).json() 
    url_activities = url_full['activities'] #This is a list of the results for activities

    # This 'while' loop iterates over several pages of records (if required), and collates the list of results
    while url_full['page_meta']['next']:
        url_full = requests.get(url_stem + url_full['page_meta']['next']).json()
        url_activities = url_activities + url_full['activities'] #Add result (as a list) to previous list of results

    # Convert the list of results into a Pandas dataframe:
    act_df = pd.DataFrame(url_activities)

   


    return act_df

# Extract the list of compounds from the previous dataframe ('act_df'), and call the 'molecule' API to find their molecular properties etc, so that this list can be refined

def find_properties_of_compounds(act_df):

    #First find the list of compounds that are within the act_df dataframe:
    
    cmpd_chembl_ids = list(set(act_df['molecule_chembl_id']))
    print("There are {} compounds initially identified as active on the known targets. e.g.".format(len(cmpd_chembl_ids)))
    print(cmpd_chembl_ids[0:2])

    
   
    #For the identified compounds, extract their molecular properties and other information from the 'molecule' ChEMBL API
    #Specify the input parameters:
    cmpd_chembl_ids = ",".join(cmpd_chembl_ids[0:]) #Amend the format of the text string of compounds so that it is suitable for the API call
    limit = 100 #Limit the number of records pulled back for each url call

    # Set up the call to the ChEMBL 'molecule' API
    # Remember that there is a limit to the number of records returned in any one API call (default is 20 records, maximum is 1000 records)
    # So need to iterate over several pages of records to gather all relevant information together!
    url_stem = "https://www.ebi.ac.uk" #This is the stem of the url
    url_full_string = url_stem + "/chembl/api/data/molecule.json?molecule_chembl_id__in={}&limit={}".format(cmpd_chembl_ids, limit) #This is the full

    url_full = requests.get( url_full_string ).json() #This calls the information back from the API using the 'requests' module, and converts it to j

    url_molecules = url_full['molecules'] #This is a list of the results for activities

    # This 'while' loop iterates over several pages of records (if required), and collates the list of results
    while url_full['page_meta']['next']:
        url_full = requests.get(url_stem + url_full['page_meta']['next']).json()
        url_molecules = url_molecules + url_full['molecules'] #Add result (as a list) to previous list of results
    
    mol_df = pd.DataFrame(url_molecules)
    mol_df = mol_df[[ 'molecule_chembl_id']]
    return mol_df 
#====================================================================#

import chembl_webresource_client
from chembl_webresource_client.new_client import new_client
def main(target):

     # using a list of known targets, find compounds that are active on these targets:
    targets = [target] # xxx
    act_df = find_bioactivities_for_targets(targets)
    mol_df=find_properties_of_compounds(act_df)
    chembl_list = mol_df.values.tolist()
    flattened = [val for sublist in chembl_list for val in sublist]
    chemblid=[]
    smilesid=[]
    for x in flattened:
        chemblid.append(x)
        chembl_id=str(x)
        records = new_client.activity.filter(molecule_chembl_id=chembl_id)
        molecule=records[0]['canonical_smiles']
        smilesid.append(molecule)
    df = pd.DataFrame(list(zip(chemblid, smilesid)), 
               columns =['ChemblID', 'smiles'])
    df.to_csv('output.txt')
    #====================================================================#
    

#====================================================================#
