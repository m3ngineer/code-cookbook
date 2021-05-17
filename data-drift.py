# Automatically checks for changes in data upon code changes

# Inputs: 2 dataframes for comparison. 1 dataframe could be the data used to train a model. The other is the current data used to make predictions

# Ouput: A series of tests that dectect statistical differences and changes in the dataset
import pandas as pd

class DriftTest():

    def __init__(self):
        self.tests = {
            'mean': self.test_mean,
            'median': self.test_median,
            'null': self.test_null,
            'min': self.test_min,
            'max': self.test_max,
            'uniqueness': self.test_uniqueness,
            'completeness': self.test_completeness,
        }

    def test(self):
        pass

    def profile(self, data):
        ''' Create a profile comparing 2 dataframes '''

        result = pd.DataFrame()
        stats = ['mean', 'median', 'null', 'min', 'max', 'uniqueness', 'completeness']
        for stat in stats:
            for i in range(0,1):
                print(stat, i)
                result.loc[stat, i] = self.tests[stat](data)

        return result

    def test_mean(self, data):
        return data.mean()

    def test_median(self, data):
        return data.median()

    def test_mean(self, data):
        return data.mean()

    def test_null(self, data):
        return data.isnull().shape[0]

    def test_max(self, data):
        return max(data)

    def test_min(self, data):
        return min(data)

    def test_uniqueness(self, data):
        return data.duplicated().shape[0]

    def test_completeness(self, data):
        return ( data.shape[0] - data.isnull().sum() ) / data.shape[0]

data = pd.Series(list(range(1,10)))
drift = DriftTest()
print(drift.profile(data))
