import numpy as np

def reproduce(γ, mort_p, foxes):
    '''
    reproduction rate per prey eaten by pairs of foxes
    ---------------------
    Parameters:
    γ (float): constant reproduction rate per prey eaten 
    mort_p (int): # rabbits eaten at a previous timestamp t - i
    foxes (int):  # foxes at timestamp t 
    ---------------------
    Returns:
    int additional foxes born 
    
    '''
    rep_rate = 2 * (mort_p / max(foxes, 1)) * γ if ((mort_p / max(foxes, 1)) * γ <= 0.5) else 1
    if (foxes <= 1):
        return 0
    else: 
        ## assume every fox gets equal share from prey
        return np.random.binomial(np.floor(foxes / 2), rep_rate)


def spieces_mort(a, idx, θ):
    '''
    Mortality rate of a spieces
    -----------------------
    Parameters:
    a (array of int): # of animals at each idx (timestamp) 
    idx (int): index of the timestamp to be affected by mortality
    θ (float): mortality rate 
    -----------------------
    Returns:
    int # animals which died
    '''
    n = 0 if a[idx - 1] < 0 else a[idx - 1]
    return np.random.binomial(n, θ)  


def mort_prey(probs, θ, idx, rabbit, fox):
    '''
    Each rabbit could be killed by the mingled foxes (which are determined by the temperature)
    Each fox has the same chance to kill independently each living rabbit. But once a rabbit has 
    been killed by a fox it can't die again. Also, we can't have more dead rabbits than rabbits alive.
    ----------------------
    Parameters:
    probs (list of floats): probability for foxes to mingle with rabbits 
    θ (float): mortality rate 
    idx (int): index of the timestamp to be affected by mortality
    rabbit (list of ints):
    fox (list of ints):
    ---------------------
    Returns:
    int # of rabbits which died 
    
    '''
    temp_l = rabbit[:]
    temp = rabbit[idx - 1]
    n = 0 if fox[idx - 1] < 0 else fox[idx - 1]
    mingled_foxes = np.random.binomial(n, probs[idx - 1])
    for fox in range(mingled_foxes):
#         print('fox num: ', fox)
        temp =  temp - spieces_mort(temp_l, idx, θ)
        temp_l[idx - 1] = temp
#         print('rabbits left: ', temp)
        if temp <= 0:
            return rabbit[idx - 1]
    return rabbit[idx - 1] - temp

def growth_abs(rabbit, idx, δ):
    '''
    -----------------
    Parameters:
    rabbit (list of ints): # of rabbits per idx (timestamp)
    idx (int): index of the timestamp to be affected by growth
    δ (float):
    -----------------
    Returns:
    int number of additional rabbits born
    '''
    n = 0 if rabbit[idx - 1] <= 1 else rabbit[idx - 1]
    return np.random.binomial(np.floor(n / 2), δ)