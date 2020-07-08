import numpy as np


def create_dt_feature(t, standardize=False, normalize=False):
    '''

    '''
    cum_t = np.cumsum(t)
    if standardize:
        cum_t = (cum_t - np.mean(cum_t)) / np.std(cum_t)
        return cum_t
    elif normalize:
        cum_t = cum_t - np.min(cum_t) / (np.max(cum_t) - np.min(cum_t))

    return cum_t


def seq_max_len_w_o_padding(arr):
    '''

    '''
    cc = []
    for i in range(pro_foxes.shape[0]):
        try:
            cc.append(np.where(pro_foxes[i, :] == 0)[0][0])
        except:
            cc.append(pro_foxes.shape[1])
            break
    return max(cc)


def data_combination(foxes_ode, rabbits_ode, foxes_prob, rabbits_prob, ode_t, prob_t):
    '''

    '''

    n_columns = seq_max_len_w_o_padding(
        foxes_ode) + seq_max_len_w_o_padding(foxes_prob)
    combined_array = np.zeros((foxes_ode.shape[0] * 5, n_columns))
    for idx in range(foxes_ode.shape[0]):
        ode_m = np.where(foxes_ode[idx, :] != 0)[0][-1] + 1
        prob_m = np.where(foxes_prob[idx, :] != 0)[0][-1] + 1
        m = ode_m + prob_m
        combined_array[idx, :m] = np.concatenate(
            (foxes_ode[idx, :ode_m], foxes_prob[idx, :prob_m]))
        combined_array[idx + 1, :m] = np.concatenate(
            (rabbits_ode[idx, :ode_m], rabbits_prob[idx, :prob_m]))
        combined_array[idx + 2,
                       :m] = np.concatenate((ode_t[idx, :ode_m], prob_t[idx, :prob_m]))
        combined_array[idx + 3,
                       :m] = np.concatenate((np.ones(ode_m), np.ones(prob_m) * 2))
        combined_array[idx + 4,
                       :m] = np.concatenate((np.ones(ode_m) * 3, np.ones(prob_m) * 4))
    return combined_array
