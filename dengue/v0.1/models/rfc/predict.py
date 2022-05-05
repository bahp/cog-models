from cog import BasePredictor, Input, Path
import pickle

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory"""
        self.model = pickle.load(open('./model.p', 'rb'))

    # The arguments and types the model takes as input
    def predict(self, input):
        """Run a single prediction on the model"""
        print("INSIDE!")
        r = self.model.predict(input)
        return r


if __name__ == '__main__':

    print("MAIN")