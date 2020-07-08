import numpy as np

def create_dt_feature(t, standardize = False, normalize = False):
    '''
    
    '''
    cum_t = np.cumsum(t)
    if standardize:
        cum_t = (cum_t - np.mean(cum_t)) / np.std(cum_t)
        return cum_t
    elif normalize:
        cum_t = cum_t - np.min(cum_t) / (np.max(cum_t) -  np.min(cum_t))
    
    return cum_t