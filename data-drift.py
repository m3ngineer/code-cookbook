# Automatically checks for changes in data upon code changes

# Inputs: 2 dataframes for comparison. 1 dataframe could be the data used to train a model. The other is the current data used to make predictions

# Ouput: A series of tests that dectect statistical differences and changes in the dataset

class DriftTest():

    def __init__(self):
        pass

    def test(self):
        pass

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
