'''

Data Drift automatically checks for statistical differences in data upon code changes.

Inputs: 2 dataframes for comparison. 1 dataframe could be the data used to train a model. The other is the current data used to make predictions
Ouput: A series of tests that dectect statistical differences and changes in the dataset

ML partially substitutes the role of data stewards by flagging the data points based on probabilistic ratings as per learning from training set of past data steward decisions and categorizing duplicate, vacant, incorrect or suspicious entries. This reduces manual effort and governance activities.

'''

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from itertools import combinations

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
            print(data.head())
            print(data.shape)
            result.loc[stat] = self.tests[stat](data)

        return result

    def compare(self, datasets, dataset_names=None, ttest=False, join_cols=[]):
        '''
        Generates comparison statistics for list of datasets
        datasets :: list of dataframes
        names :: list of strings
        '''

        dataset_names = dataset_names[i] if dataset_names else ['data_{}'.format(i) for i in range(len(datasets))]
        result = pd.DataFrame(index=self.tests.keys())
        kwargs = {}
        for i, dataset in enumerate(datasets):
            kwargs[names[i]] = self.profile(dataset).values
        result = result.assign(**kwargs)

        # Get matches for all combinations of datasets
        for (dset1, dset2) in pairs:
            result['match_{}-{}'.format(dset1,dset2)] = result[dset1].eq(result[dset2])

        if ttest:
            for i, dataset in enumerate(datasets):
                if i > 0:
                    print('T-test statistic ({} vs {}): {}'.format(names[i-1], names[i], stat_ttest(dataset[i-1], dataset[i])))

        if join_cols:
            self.find_col_differences(datasets, dataset_names, join_cols)

        return result

    def find_col_differences(datasets, dataset_names, join_cols):
        ''' Finds rows unique to given datasets '''

        df = datasets[0].copy()
        for i in range(0, len(datasets)):
            if i > 0:
                df = df.join(datasets[i], on=join_cols, how='outer')

        print('Row discrepancies')
        print('----------')
        for (dset1, dset2) in pairs:
            # Get num columns unique to each dataset

            merged_df = dset1.merge(dset2, indicator=True)
            num_equal = (merged_df['_merged'] == 'both').sum()
            num_left = (merged_df['_merged'] == 'left_only').sum()
            num_right = (merged_df['_merged'] == 'right_only').sum()
            print('Number of rows in both datsets: {}'.format(num_equal))
            print('Number of rows in {0} not in {1}: '.format(dataset_names[0], dataset_names[1], num_left))
            print('Number of rows in {1} not in {2}: '.format(dataset_names[1], dataset_names[0], num_right))



    def test_mean(self, data):
        return data.mean()

    def test_shape_rows(self, data):
        return data.shape[0]

    def test_columns(self, datal, datar):
        ''' Returns unique columns for each dataset '''

        return [col for col in datal.columns if col not in datar.columns],
            [col for col in datar.columns if col not in datal.columns]

    def test_shape_cols(self, data):
        if len(data.shape) > 1:
            return data.shape[1]
        return None

    def test_median(self, data):
        return data.median()[0]

    def test_mean(self, data):
        return data.mean()[0]

    def test_null(self, data):
        return data.isnull().shape[0]

    def test_max(self, data):
        return data.max()[0]

    def test_min(self, data):
        return data.min()[0]

    def test_uniqueness(self, data):
        return data.duplicated().shape[0]

    def test_completeness(self, data):
        return ( data.shape[0] - data.isnull().sum()[0] ) / data.shape[0]

    def stat_ttest(self, data1, data2):
        return ttest_ind(data1, data2, equal_var=False)

data = pd.read_csv('../../Projects/xray-healthcare/data/Medicare_Provider_Utilization_and_Payment_Data__Physician_and_Other_Supplier_PUF_CY2017.csv', nrows=300000)
print(data.columns)
data1 = data[data['Provider Type'] == 'Hematology-Oncology']
data2 = data1[data1['Number of Medicare Beneficiaries'] > 15]

# data1 = pd.Series(list(range(1,10)))
# data2 = pd.Series(list(range(1,12)) + [None])
drift = DriftTest()
cols = ['HCPCS Drug Indicator', 'Number of Services',
       'Number of Medicare Beneficiaries',
       'Number of Distinct Medicare Beneficiary/Per Day Services',
       'Average Medicare Allowed Amount', 'Average Submitted Charge Amount',
       'Average Medicare Payment Amount',
       'Average Medicare Standardized Amount']
cols = ['Average Medicare Payment Amount']
print(drift.compare([data1[cols], data2[cols]]))
