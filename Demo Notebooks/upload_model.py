import pandas as pd
import mosqlient as mosq

challenge_year = 2026
validation_indices = [1, 2, 3, 4] # None (forecast), or [1, 2, 3, 4] (validation)

##########################
## Put the API key here ##
##########################

api_key = 'bentolab_diseasedynamics:d14d8f46-1763-422f-a944-656ef6268d69'

# Retrieve API key from Ana's Mosqclimate account.
## Log into https://mosqlimate.org using GH of @anabento.
## Go to "Auth" tab in profile overview.

##################
## Upload model ##
##################

# Function `upload_model` of `mosqlient` deprecated (IMDC 2026)
# Upload model by logging into https://mosqlimate.org with the BentoLab-DiseaseDynamics GH account and adding a new model

#####################
## Upload forecast ##
#####################

# validation
if validation_indices:

    for validx in validation_indices:
        # set correct ID and description
        ID = f"endemic_channel-validation_{validx}"
        description = f"Validation {validx} (Cornell_BentoLab - NegBinom Endemic Channel). Authored by Tijs W. Alleman & Ana I. Bento."
        commit = "9c2d82f14e438680918a3f1304de9fe2bade62b5"
        # load validation experiment data
        forecast = pd.read_csv(f'../data/interim/model_output/sprint_{challenge_year}/{ID}.csv', index_col=0)
        # get the ufs..
        ufs = forecast['adm_1'].unique().tolist()
        # ..and loop over them
        for uf in ufs:
            # slice data
            df = forecast[forecast['adm_1'] == uf].reset_index()
            # push the prediction
            res = mosq.upload_prediction(
                api_key = api_key,
                repository = 'BentoLab-DiseaseDynamics/3rd_imdc_cornell_bentolab',
                description = description, 
                commit = commit,
                disease = 'A90', # dengue
                case_definition = 'probable',
                adm_level=1,
                adm_1=uf,
                published = True,
                prediction = df,
                ) 
            
# forecast
else:

    # set correct ID and description
    ID = f"endemic_channel-forecast"
    description = f"Forecast (Cornell_BentoLab - NegBinom Endemic Channel). Authored by Tijs W. Alleman & Ana I. Bento."
    commit = "cc763c9bcc4a46d93ef32d97f5e8c1de4af6e3b5"
    # load validation experiment data
    forecast = pd.read_csv(f'../data/interim/model_output/sprint_{challenge_year}/{ID}.csv', index_col=0)
    # get the ufs..
    ufs = forecast['adm_1'].unique().tolist()
    # ..and loop over them
    for uf in ufs:
        # slice data
        df = forecast[forecast['adm_1'] == uf].reset_index()
        # push the prediction
        res = mosq.upload_prediction(
            api_key = api_key,
            repository = 'BentoLab-DiseaseDynamics/3rd_imdc_cornell_bentolab',
            description = description, 
            commit = commit,
            disease = 'A90', # dengue
            case_definition = 'probable',
            adm_level=1,
            adm_1=uf,
            published = True,
            prediction = df,
            ) 

    pass