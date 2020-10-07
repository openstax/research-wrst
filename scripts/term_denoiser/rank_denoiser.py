# Implements a 3PL IRT model
# TODO: Set a type variable for the IRT for 1PL, 2PL, and 3PL models
# 1PL can have an additional routine for sampling beta more efficiently
# Fit method will call whatever appropriate fit construct given the type

import numpy as np
from scipy.stats import norm
from time import time

# Brief model description:
# This is a simple estimator that simply ranks terms in order of how often they were proposed
# It is left to the user to determine appopriate thresholding


class RankDenoiser(object):
    def __init__(self, **kwargs):
        pass

    def fit(self, data):
        # data: A numpy array of size Q (terms) x N (users)
        # A value of 1 indicates the term was selected by the user, 0 that it was not, with NA implying unobserved
        self.data = data
        
        observations_per_term = np.nansum(data, axis=1)
        self.observations_per_term = observations_per_term
