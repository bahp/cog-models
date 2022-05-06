#%%

import pandas as pd
import numpy as np

#%%

# 4131 patients admitted to hospital without shock
# Features are those collected over the initial 48 hours of admission


df = pd.read_excel(r'./OUCRU_dengue_shock.xlsx')

#%%

'''
Data dictionary:
---
day_of_illness: day of illness/fever onset starting from day 0
age: age in years
sex: 1=male, 0=female
weight: weight in kg
hctmin/median/max: haematocrit % summarised over first 48 hours of hospital admission
pltmin/median/max: platelet count x 10^6.L
Shock: dengue shock syndrome (WHO 2009 definitions)
'''

X_cat = ['sex']
X_num = [
    'day_of_illness',
    'hctmedian',
    'hctmax',
    'hctmin',
    'pltmax',
    'pltmedian',
    'pltmin',
    'age',
    'weight'
]

#%%

X = df.iloc[:,:-2]
y = df.iloc[:,-2]


# Show
print(X)

#%%

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

categorical_features =  X_cat
categorical_transformer = Pipeline([
    ('imputer_cat', SimpleImputer(strategy = 'most_frequent', fill_value = 'missing'))
])

numeric_features = X_num
numeric_transformer = Pipeline([
        ('imputer_num', SimpleImputer()),
        ('scaler', StandardScaler())
])

preprocessor = ColumnTransformer([
        ('categoricals', categorical_transformer, categorical_features),
        ('numericals', numeric_transformer, numeric_features)],
        remainder = 'drop')

# -----------------------------------------
# Define te models with optimise parameters
# -----------------------------------------
# Libraries
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

# Xgboost
xgb = XGBClassifier(eta=0.01,gamma=0.1,max_depth= 4,min_child_weight=0.005,
            n_estimators= 250, eval_metric='logloss')

# Artificial Neural Network
ann = MLPClassifier(activation='relu', alpha=0.1, batch_size='auto', beta_1=0.9,
            beta_2=0.999, early_stopping=False, epsilon=1e-08,
            hidden_layer_sizes=(100, 100), learning_rate='constant',
            learning_rate_init=0.001, max_fun=15000, max_iter=50,
            momentum=0.9, n_iter_no_change=10, nesterovs_momentum=True,
            power_t=0.5, random_state=None, shuffle=True, solver='adam',
            tol=0.0001, validation_fraction=0.1, verbose=False,
            warm_start=False)

# Random Forest Classifier
rfc = RandomForestClassifier(bootstrap=True, ccp_alpha=0.0, class_weight=None,
                    criterion='gini', max_depth=5, max_features='auto',
                    max_leaf_nodes=None, max_samples=None,
                    min_impurity_decrease=0.0,
                    min_samples_leaf=1, min_samples_split=3,
                    min_weight_fraction_leaf=0.0, n_estimators=500,
                    n_jobs=None, oob_score=False, random_state=42, verbose=0,
                    warm_start=False)


# --------------------------
# Fit the pipelines
# --------------------------
# Libraries
from sklearn.model_selection import cross_validate
from sklearn.model_selection import RepeatedStratifiedKFold

# Definitions
cv = RepeatedStratifiedKFold(n_splits=10,
                             n_repeats=1,
                             random_state=1)

# Storage variable
pipelines = {}
results = pd.DataFrame()

models = [
    (xgb,'xgb'),
    (ann,'ann'),
    (rfc,'rfc')
]

# For each model fit the pipeline
for model, name in models:
    # Information
    print("Computing... %s" % name)

    # Create pipeline
    pipe = Pipeline([
            ('preprocess', preprocessor),
            ('model', model)
        ]).fit(X, y)

    # Compute scores
    scores = cross_validate(pipe,
        X, y, scoring='roc_auc', cv=cv)

    # Save pipeline
    pipelines[name] = pipe
    results[name] = scores['test_score']


# --------------------------
# Save the models and scores
# --------------------------
# Libraries
import pickle
from pathlib import Path

# Save all the models
for name, model in pipelines.items():
    # Define path
    path = './models/%s/' % name
    # Create if it does not exist
    Path(path).mkdir(parents=True, exist_ok=True)
    # Save pickle file
    with open('%s/model.p' % path, 'wb') as file:
        pickle.dump(model, file)

# Save the scores
results.to_csv('./models/scores.csv')

# Show
print(results)