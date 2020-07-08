import numpy as np

def rabbit_fox_env(x0, y0, α, β, γ, δ, dt = 1e-3, len_t = 1/8):
    '''
    Simple loteka-volterra differential equation model - see https://en.wikipedia.org/wiki/Lotka–Volterra_equations
    for details of the underlying assumptions.
    
    ------
    Parameters:
    x0 (int): initial value for prey (Rabbits)
    y0 (int): initial value for Predator (Foxes)
    α  (float): intrinsic rate of prey population increase
    β  (float): predation rate coefficient
    γ  (float): predator mortality rate  
    δ  (float): reproduction rate of predators per prey eaten
    dt (float): time interval between events
    len_t (int): # of events
    ------------
    Returns:
    rabbit (list of floats): # of rabbits at time t
    fox (list of floats): # foxes at time t
    t (numpy array):  time intervals 
    x0 (int): initial value for prey (Rabbits)
    y0 (int): initial value for Predator (Foxes)
    
    '''
    rabbit = []; fox = []
    rabbit.append(x0); fox.append(y0)
    dt_multiplier = np.random.randint(1, 9) 
    t = np.arange(0, len_t, dt_multiplier * dt)
    for idx, _ in enumerate(t):
        if (idx == 0):
            continue
        r = rabbit[-1] ; f = fox[-1]
        # The term β * (f * r)  - reminds a binomial experiment.  
        rabbit.append(r + dt * (α * r - β * (f * r)))
        fox.append(f + dt * (δ * (f * r) - γ * f))
    return rabbit, fox, t, x0, y0


def multi_init_rabbit_fox_env(xs, ys, α, β, γ, δ):
    '''
    ------------
    Parameters:
    xs (list of int): initial values for prey (Rabbits)
    ys (list of int): initial values for Predator (Foxes)
    α  (float): intrinsic rate of prey population increase
    β  (float): predation rate coefficient
    γ  (float): reproduction rate of predators per 1 prey eaten
    δ  (float): predator mortality rate
    -----------
    Returns:
    rabbits (list of lists): each list contains # of rabbits according to init state xs
    foxes (list of lists): each list contains # of foxes according to init state ys
    xs (list of int): initial values for prey (Rabbits)
    ys (list of int): initial values for Predator (Foxes)
    
    '''
    n = len(xs)
    rabbits = np.zeros((n, 125))
    foxes = np.zeros((n, 125))
    for idx, (x0, y0) in enumerate(zip(xs, ys)):
        rabbit, fox, t, x0, y0 = rabbit_fox_env(x0, y0, α, β, γ, δ)
        rabbits[idx, :len(rabbit)] = rabbit
        foxes[idx, :len(fox)] = fox
    
    
    return rabbits, foxes