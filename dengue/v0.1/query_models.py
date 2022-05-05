# Libraries
import pickle
import pandas as pd

# Load a model
m = pickle.load(open('./models/xgb/model.p', 'rb'))

# Display model
print(m)

# Read dataset
query = pd.read_excel(r'./OUCRU_dengue_shock.xlsx', nrows=10)

# Compute prediction
pred = m.predict(query.iloc[:, :10])
prob = m.predict_proba(query.iloc[:, :10])

# Show
print(pred)
print(prob)