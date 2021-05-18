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

    def profile(self, data):
        ''' Create a profile comparing 2 dataframes '''

        result = pd.Series()
        stats = ['mean', 'median', 'null', 'min', 'max', 'uniqueness', 'completeness']
        for stat in stats:
            result.loc[stat] = self.tests[stat](data)

        return result

    def compare(self, datasets, names=None):
        '''
        Generates comparison statistics for list of datasets
        datasets :: list of dataframes
        names :: list of strings
        '''

        result = pd.DataFrame(index=self.tests.keys())
        kwargs = {}
        for i, dataset in enumerate(datasets):
            name = names[i] if names else 'data_{}'.format(i)
            kwargs[name] = self.profile(dataset).values
        result = result.assign(**kwargs)

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

data1 = pd.Series(list(range(1,10)))
data2 = pd.Series(list(range(1,12)) + [None])
drift = DriftTest()
print(drift.compare([data1, data2]))
