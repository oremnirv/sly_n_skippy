###########################
# Author: Omer Nivron
###########################
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def multi_phase_plot_rabbit_fox(rabbits, foxes, xs, ys):
    '''
    Phase plot for foxes and rabbits model.
    -------------------
    Parameters:
    rabbits (list of lists of floats): first output from rmulti_init_rabbit_fox_env
    foxes (list of lists of floats): second output from multi_init_rabbit_fox_env
    xs (list of int): initial value for prey (Rabbits)
    ys (list of int): initial value for Predator (Foxes)
    -------------------
    '''
    fig, ax = plt.subplots(figsize=(9,5))
    ax.set_xlabel('Rabbit population')
    ax.set_ylabel('Fox population')
    ax.set_title('Phase space of Rabbits vs. Foxes population')
    ## Phase space is a plot ignoring time, so we only care what will be
    ## the rabbits vs. foxes population. 
    ## "This corresponds to eliminating time from the two differential equations above to produce a single differential equation"
    for rabbit, fox, x0, y0 in zip(rabbits, foxes, xs, ys):
        ax.scatter(rabbit, fox, label = "init prey: {}, pred: {}".format(str(x0), str(y0)))
    ax.legend()
    plt.show()


def multi_probs_worlds(rabbits, foxes):
    '''

    '''
    for r,f in zip(rabbits, foxes):
        fig, ax = plt.subplots(figsize=(9,5))
        ax.plot(range(len(r)), r, label='Prey')
        ax.plot(range(len(f)), f, '--', label='Predator')
        ax.grid(True)
        ax.legend()
        ax.set_ylabel('population')
        ax.set_xlabel('time index')
        plt.show()