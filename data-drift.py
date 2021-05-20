'''

Data Drift automatically checks for statistical differences in data upon code changes.

Inputs: 2 dataframes for comparison. 1 dataframe could be the data used to train a model. The other is the current data used to make predictions
Ouput: A series of tests that dectect statistical differences and changes in the dataset

ML partially substitutes the role of data stewards by flagging the data points based on probabilistic ratings as per learning from training set of past data steward decisions and categorizing duplicate, vacant, incorrect or suspicious entries. This reduces manual effort and governance activities.

'''

import pandas as pd
from scipy.stats import ttest_ind

class DriftTest():

    def __init__(self):
        self.tests = {
            'shape_rows': self.test_shape_rows,
            'shape_cols': self.test_shape_cols,
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

        result = pd.Series(dtype='float64')
        stats = ['shape_rows', 'shape_cols', 'mean', 'median', 'null', 'min', 'max', 'uniqueness', 'completeness']
        for stat in stats:
            result.loc[stat] = self.tests[stat](data)

        return result

    def compare(self, datasets, names=None, ttest=False):
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

        if ttest:
            for i, dataset in enumerate(datasets):
                if i > 0:
                    print('T-test statistic ({} vs {}): {}'.format(names[i-1], names[i], stat_ttest(dataset[i-1], dataset[i]))

        return result

    def test_mean(self, data):
        return data.mean()

    def test_shape_rows(self, data):
        return data.shape[0]

    def test_shape_cols(self, data):
        if len(data.shape) > 1:
            return data.shape[1]
        return None

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

    def stat_ttest(self, data1, data2):
        return ttest_ind(data1, data2, equal_var=False)

data1 = pd.Series(list(range(1,10)))
data2 = pd.Series(list(range(1,12)) + [None])
drift = DriftTest()
print(drift.compare([data1, data2]))
