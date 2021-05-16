# Automatically checks for changes in data upon code changes

# Inputs: 2 dataframes for comparison. 1 dataframe could be the data used to train a model. The other is the current data used to make predictions

# Ouput: A series of tests that dectect statistical differences and changes in the dataset

class DriftTest():

    def __init__(self):
        self.tests = {
            'mean': self.test_mean(),
            'median': self.test_median(),
            'null': self.test_null(),
            'range': self.test_range(),
            'uniqueness': self.test_uniqueness(),
            'completeness': self.test_completeness,
        }

    def test(self):
        pass

    def profile(self):
        ''' Create a profile comparing 2 dataframes '''

        result = pd.DataFrame()
        stats = ['mean', 'median', 'null', 'range', 'uniqueness', 'completeness']
        for stat in stats:
            for i in range(0,1):
                result.loc[stat, i] = self.tests[stat]

        return result

    def test_mean(self, data):
        return data.mean()

    def test_median(self, data):
        return data.median()

    def test_mean(self, data):
        return data.mean()

    def test_null(self, data):
        return data.isnull().shape

    def test_range(self, data):
        return max(data), min(data)

    def test_unique(self, data):
        return data.duplicated()

    def test_completeness(self, data):
        return ( data.shape[0] - data.isnull().sum() ) / data.shape[0]
