import numpy as np
from scipy.stats import beta
        
class BetaBandit(object):
    def __init__(self, num_options=2, weights = None, prior=(1.0,1.0)):
        self.trials = np.zeros(shape=(num_options,), dtype=int)
        self.successes = np.zeros(shape=(num_options,), dtype=int)
        self.num_options = num_options
        self.weights = weights
        self.prior = prior

    def update(self, trial_id, success):
        self.trials[trial_id] = self.trials[trial_id] + 1
        if (success):
            self.successes[trial_id] = self.successes[trial_id] + 1

    def recommend(self):
        samples = []
        for i in range(self.num_options):
            #Construct beta distribution for posterior
            dist = beta(self.prior[0]+self.successes[i],
                        self.prior[1]+self.trials[i]-self.successes[i])
            #Draw sample from beta distribution
            samples += [ dist.rvs() ]
        # Multiply samples with weights if specified
        if self.weights is not None:
            samples = [x*y for (x,y) in zip(samples, self.weights)]
        # Return the index of the sample with the largest value
        return samples.index( max(samples) )  

class MeanBandit():
    def __init__(self, num_options=2, weights = None):
        # Initialize random means
        self.means = np.random.random((num_options,))
        self.counts = np.zeros(shape=(num_options,), dtype=int)
        self.num_options = num_options
        self.weights = weights

    def update(self, trial_id, reward):
        # Add new trial to running mean
        mean = self.means[trial_id]
        count = self.counts[trial_id] + 1.0
        self.means[trial_id] = mean + (reward-mean)/count
        self.counts[trial_id] = count

    def recommend(self):
        # Multiply samples with weights if specified
        if self.weights is not None:
            samples = [x*y for (x,y) in zip(self.means, self.weights)]
        else:
            samples = self.means
        # Return the index of the sample with the largest value
        return np.argmax(samples)
        
class SampleMean():
    def __init__(self, n_models = 1000, num_options = 2, weights = None, modelType = MeanBandit):
        self.models = [modelType(num_options = num_options, weights = weights) for _ in range(n_models)]

    def recommend(self):
        return np.random.choice(self.models).recommend()

    def update(self, trial_id, reward):
        for model in self.models:
            if np.random.rand(1) > 0.5:
                model.update(trial_id, reward)  

class LinearBandit():
    def __init__(self, num_variables = 2, batch_size = 10):
        self.num_variables = num_variables
        self.batch_size = batch_size
        self.weights = np.zeros(1+num_variables)
        self.data = []
        self.results = []
        self.count = 0
            
    def update(self, variables, success):
        if len(variables)==self.num_variables:
            # Add data
            self.data.append([1]+variables)
            self.results.append(success)
        else:
            print("update: wrong list size")
        if self.count % self.batch_size == 0 and self.count > 0:
            # Update weights
            X = np.asarray(self.data)
            y = np.asarray(self.results)
            self.weights = (np.linalg.pinv(X.T.dot(X)).dot(X.T)).dot(y)
        self.count += 1
    
    def recommend(self, variables):
        if self.count <= self.batch_size:
            return np.random.random()
        # Predict
        X = np.asarray([1]+variables)
        return X.dot(self.weights)
        
class SampleLinear():
    def __init__(self, n_models = 1000, num_variables = 2, batch_size=10, modelType = LinearBandit):
        self.models = [modelType(num_variables = num_variables, batch_size = batch_size) for _ in range(n_models)]

    def recommend(self, variables):
        return np.random.choice(self.models).recommend(variables)

    def update(self, variables, success):
        for model in self.models:
            if np.random.rand(1) > 0.5:
                model.update(variables, success)  
