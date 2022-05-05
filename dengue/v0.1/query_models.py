#from cog import BasePredictor, Input, Path
#import torch

"""
class Predictor(BasePredictor):
    def setup(self):
        #Load the model into memory.
        self.model = pickle.load(open('./rfc.pkl', 'rb'))

    # The arguments and types the model takes as input
    def predict(self,
          input: Path = Input(title="Grayscale input image")
    ) -> Path:
        Run a single prediction on the model
        processed_input = preprocess(input)
        output = self.model(processed_input)
        return postprocess(output)
"""


import pickle
import pandas as pd

m = pickle.load(open('./models/rfc.p', 'rb'))

print(m)

query = pd.read_excel(r'./OUCRU_dengue_shock.xlsx', nrows=10)

r = m.predict(query)
print(r)