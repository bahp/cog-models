import cog
import pickle
import pandas as pd

from cog import BasePredictor

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory"""
        self.model = pickle.load(open('./model.p', 'rb'))

    def predict(self, day_of_illness: int=None,
                      age: float=None,
                      sex: int=None,
                      weight: float=None,
                      hctmin: float=None,
                      hctmedian: float=None,
                      hctmax: float=None,
                      pltmin: float=None,
                      pltmedian: float=None,
                      pltmax: float=None
                ) -> float:
        """Run a single prediction on the model

        .. note: It needs to create a dataframe with the name of the
                 features because the model has been trained using a
                 dataframe.
        """
        # Get all function parameters (remove self)
        aux = locals().copy()
        del aux['self']

        # Create dataframe
        q = pd.DataFrame(
            columns=aux.keys(),
            data=[aux.values()]
        )

        # Return prediction
        return self.model.predict_proba(q)[:, 1]



if __name__ == '__main__':

    print("Executing main....")