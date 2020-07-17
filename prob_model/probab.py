###########################
# Author: Omer Nivron
###########################
import numpy as np
from prob_model import random_walk

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


def multi_init_rabbit_fox_env(xs, ys):
    '''

    '''
    θ = np.random.beta(1, 10)
    δ = np.random.beta(1, 5)
    χ = np.random.beta(1, 10)
    # reproduction rate per 1 prey eaten
    γ = np.random.beta(1, 10)
    n = len(xs)
    
    rabbits = np.zeros((n, 500)); foxes = np.zeros((n, 500)); times = np.zeros((n, 500))
    for idx, (x0, y0) in enumerate(zip(xs, ys)):
        temp, probs, dts = random_walk.mean_revert_rand_walk_gausian_step(temp = [17], temp_steps = 499)
        rabbit = []; fox = []
        rabbit.append(x0); fox.append(y0)
        for idd, _ in enumerate(temp, start=1):
#           print('rabbit population: ', rabbit[-1])

            rab_growth = growth_abs(rabbit, idd, δ)
#           print('rabbit growth: ', rab_growth)
            rab_mort = mort_prey(probs, θ, idd, rabbit, fox)  
#           print('rabbit mortality: ', rab_mort)

            rabbit.append(rabbit[idd - 1]
                          + rab_growth
                          - rab_mort)

            if (rabbit[-1] <= 1):
                break

#           print('fox population: ', fox[-1])

            fox_rep = reproduce(γ, rab_mort, fox[idd - 1])
            fox_mort = spieces_mort(fox, idd, χ)

            fox.append(fox[idd - 1]   
                       + fox_rep
                       - fox_mort)

            if (fox[-1] <= 1):
                break
        rabbits[idx, :len(rabbit)] = np.array(rabbit); foxes[idx, :len(fox)] = np.array(fox); times[idx, :len(dts)] = np.cumsum(dts)
    return rabbits, foxes, times

