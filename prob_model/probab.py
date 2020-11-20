###########################
# Author: Omer Nivron
###########################
import numpy as np
import time
from prob_model import random_walk
from scipy.stats import lognorm

def reproduce(δ, mort_prey, foxes, delta):
    '''
    reproduction rate per prey eaten by pairs of foxes
    ---------------------
    Parameters:
    δ (float): constant reproduction rate per prey eaten 
    mort_p (int): # rabbits eaten at a previous timestamp t - i
    foxes (int):  # foxes at timestamp t 
    ---------------------
    Returns:
    int additional foxes born 
    
    '''
    # that is per couple rep_rate
    if (foxes <= 1):
        return 0
    if (mort_prey <= 10):
        return 0
    else:
        delta_prime = δ * delta * (mort_prey) * (2 / 5)
        # print('delta: ', delta)
        # print('mort_prey: ', mort_prey)
        # print('δ: ', δ)
        # print('delta_prime: ', delta_prime)
        ## assume every fox gets equal share from prey
        return np.random.binomial(5 * np.floor(foxes / 2), min(1, delta_prime))


def spieces_mort(a, γ, delta):
    '''
    Mortality rate of a spieces
    -----------------------
    Parameters:
    a (array of int): # of animals at each idx (timestamp) 
    β (float): mortality rate 
    -----------------------
    Returns:
    int # animals which died
    '''
    n = 0 if a[- 1] < 0 else a[- 1]
    γ_prime = γ * delta

    return np.random.binomial(n, γ_prime)  


def mort_prey(probs, β, rabbit, fox, idx, delta):
    '''
    Each rabbit could be killed by the mingled foxes (which are determined by the temperature)
    Each fox has the same chance to kill independently each living rabbit. But once a rabbit has 
    been killed by a fox it can't die again. Also, we can't have more dead rabbits than rabbits alive.
    ----------------------
    Parameters:
    probs (list of floats): probability for foxes to mingle with rabbits 
    β (float): mortality rate 
    idx (int): index of the timestamp to be affected by mortality
    rabbit (list of ints):
    fox (list of ints):
    ---------------------
    Returns:
    int # of rabbits which died 
    
    '''
    n = 0 if fox[- 1] < 0 else fox[- 1]
    # print("prob: ", probs[idx])
    constrain = 0.3 + probs[idx]
    mingled_foxes = np.random.binomial(n, constrain)

    # print("rabbits at t: ", rabbit[-1])
    # print("mingled_foxes at t: ", mingled_foxes)

    if ((mingled_foxes == 0) or (rabbit[-1] <= 0)):
        trials = 0
        beta_prime = β 
    elif(rabbit[-1] < (20 * mingled_foxes)): 
        trials = rabbit[-1]
        beta_prime = (β * delta * mingled_foxes)
    else:
        trials = 20 * mingled_foxes
        beta_prime = (β * delta * rabbit[-1]) / 20

    if (trials <= 10):
        return 0


    # print("trials: ", trails)
    # print('rabbits: ', rabbit[-1])


    return np.random.binomial(trials, min(beta_prime, 1))

def growth_abs(rabbit, α, delta = 0.1):
    '''
    -----------------
    Parameters:
    rabbit (list of ints): # of rabbits per idx (timestamp)
    α (float):
    -----------------
    Returns:
    int number of additional rabbits born
    '''
    n = 0 if rabbit[- 1] <= 1 else rabbit[- 1]
    if ((rabbit[-1] == 1) or (rabbit[-1] == 0)):
        return 1
    # print('α: ', α)
    return np.random.binomial(5 * np.floor(n / 2), min(1, α * delta * (2 / 5)))


def multi_init_rabbit_fox_env(xs, ys, steps, delta = 0.1):
    '''

    '''
    α = np.random.lognormal(0, 0.01)  # expected value 1 # prey population increase
    β = np.random.lognormal(-1.61, 0.01)  # expected value 0.2
    γ = np.random.lognormal(-0.31, 0.01) # expected value 0.1 predator mortality rate
    δ = np.random.lognormal(-1.61, 0.01) # expected value around 0.2 # reproduction rate per 1 prey eaten and general 
    n = len(xs)
    
    rabbits = np.zeros((n, steps + 1)); foxes = np.zeros((n, steps + 1))
    for idx, (x0, y0) in enumerate(zip(xs, ys)):
        print('init rabbits: ', x0)
        print('init foxes: ', y0)
        t0 = time.time()
        temp, probs, dts = random_walk.mean_revert_rand_walk_gausian_step(temp = [17], readings = steps, delta_bw_reads = delta)
        # print(probs)
        # print("time to complete random walk: ", time.time() - t0)
        rabbit = []; fox = []; rab_mort =[0]
        rabbit.append(x0); fox.append(y0)
        for idd, _ in enumerate(temp):
#           print('rabbit population: ', rabbit[-1])

            rab_growth = growth_abs(rabbit, α)

            print('rabbit growth: ', rab_growth)
            rab_mort.append(mort_prey(probs, β, rabbit, fox, idd, delta))  
            print('rabbit mortality: ', rab_mort[-1])
            # print('idd : ', idd)

            rabbit.append(rabbit[-1]
                          + rab_growth
                          - rab_mort[-1])

            print('current rabbits: ', rabbit[-1])



#           print('fox population: ', fox[-1])

            fox_rep = reproduce(δ, rab_mort[-1], fox[- 1], delta)
            fox_mort = spieces_mort(fox, γ, delta)
            # fox_growth = growth_abs(fox, α / 20)

            fox.append(fox[- 1]   
                       + fox_rep
                       # + fox_growth
                       - fox_mort)
            print('current foxes: ', fox[-1])


            if ((fox[-1] <= 0) or (rabbit[-1] <= 0)):
                break
        # print(len(rabbit))

        rabbits[idx, :len(rabbit)] = np.array(rabbit); foxes[idx, :len(fox)] = np.array(fox); 
    return rabbits, foxes

