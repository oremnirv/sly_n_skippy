import scipy.stats as scst
import numpy as np

def mean_revert_rand_walk_gausian_step(temp = [17], temp_steps = 500):
    '''
    This random walk prevents variance from exploding to infinity. For each temperature value
    check where it falls in the cumulative distribution function with mean equlas to temp[0]. 
    Toss a coin w/ prob heads = p_right. If it falls on heads then we sample a truncated normal 
    r.v from [0, inf) else we sample from truncated normal (-inf, 0]. The long running mean will still be 17
    with variance approx. scale^2.
    
    -------------------
    Parameters:
    temp (list of float): a list of one element with an intial tempertaure value (mean) in its first element 
    temp_steps (int): # days to run the function where 1e-3 is one day
    -------------------
    Returns: 
    temp (list of floats): the temperatures observed during the random walk
    probs (list of floats): each temperature value is converted to a score between 0 to 1/10
    which indicates the mingling probability of foxes (higher temperature, more mingling). 
    This argument will be an input to mort_prey function.   
    '''
    dts = []
    
    while True:
        dt = np.random.beta(1, 300) + 0.00001
        dts.append(dt)
        curr_val = temp[-1] - temp[0]
        cdf_val = scst.norm.cdf(curr_val, loc = 0, scale = 3)    
        p_right = 1 - cdf_val
        
        p = 'R' if (np.random.uniform(0, 1) <= p_right) else 'L'
        
        if p=='R':
            temp.append(temp[-1] + scst.truncnorm.rvs(a = 0, b = np.inf ,loc = 0, scale = 3 * dt * 1000 / 9))

        else:
            temp.append(temp[-1] + scst.truncnorm.rvs(a = - np.inf , b = 0, loc = 0, scale = 3 * dt * 1000 / 9))


        if (sum(dts) >= (temp_steps * 1e-3)):
            break
    shifted_temp = np.array(temp)  - (min(temp))
    return temp,  shifted_temp / (max(shifted_temp) * 10), dts