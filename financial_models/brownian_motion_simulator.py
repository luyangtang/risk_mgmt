import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt

def gen_path(S0, r, sigma, T, M, I):
    '''
        Generates Monte Carlo paths for geometric Brownian motion

        Paramaters
        ==========
        S0: float
            initial stock/index value
        r: float
            constant short rate
        sigma: float
            constant volatility
        T: float
            final time horizon
        M: int
            number of time steps/ intervals
        I: int
            number of paths to be simulated

        Returns
        =======
        paths: ndarray, shape(M + 1,I)

        Examples
        ========
        gen_path(S0 = 100,
                r = 0.05,
                sigma = 0.25,
                T = 10,
                M = 50,
                I = 100)
    '''
    dt = T/M # interval width
    paths = np.zeros((M,I))
    paths[0][:] = S0

    for i in range(1,M):
        z = npr.standard_normal(I)
        paths[i] = paths[i-1] \
            * np.exp((r-0.5*sigma**2)*dt + sigma * np.sqrt(dt)*z)

    return paths


def log_return(paths):
    '''
    Returns the log_return log(S[t]/S[t-1])

    Parameters
    ==========
    paths: ndarray, shape(M,I)
        trajectories simulated

    Returns
    =======
    log_return: ndarray, shape(M-1,I)
        log returns of the paths
    '''
    return np.log(paths[1:]/paths[0:-1])

r = 0.05 # constant riskless short value
sigma = 0.25 # constant volatility
I = 2000 # number of paths
M = 50 # number of steps
T = 10 # max time
S0 = 100 # initial state
#
# paths = gen_path(S0, r, sigma, T, M, I)
# print(paths)
# plot_paths(paths)

class brownian_motion(object):
    '''
    Generates Monte Carlo paths for geometric Brownian motion

    Paramaters
    ==========
    S0: float
        initial stock/index value
    r: float
        constant short rate
    sigma: float
        constant volatility
    T: float
        final time horizon
    M: int
        number of time steps/ intervals
    I: int
        number of paths to be simulated

    Returns
    =======
    paths: ndarray, shape(M + 1,I)

    Examples
    ========
    bm = brownian_motion(S0 = 100,
            r = 0.05,
            sigma = 0.25,
            T = 10,
            M = 50,
            I = 100)
    bm.paths
    bm.plot()
    '''

    def __init__(self,
                S0 = 100,
                r = 0.05,
                sigma = 0.25,
                T = 10,
                M = 50,
                I = 100):
        self.paths = gen_path(S0, r, sigma, T, M, I)
        self.log_return = log_return(self.paths)

    def __repr__(self):
        return str(self.paths)

    def plot(self, num_paths_shown = 10):
        '''
        Plots the paths

        Parameters
        ==========
        paths: ndarray, shape(M,I)
            paths as matrix (each row being states at a time)
        num_paths_shown: int
            number of paths to be plotted

        Returns
        =======
        Plot the paths

        Examples
        ========
        bm = brownian_motion(S0 = 100,
                r = 0.05,
                sigma = 0.25,
                T = 10,
                M = 50,
                I = 100)
        bm.plot(20)
        '''
        fig, ax = plt.subplots()
        ax.plot(self.paths[:,:num_paths_shown])
        '''
        ax.set_title("Simulation of %d paths from Brownian motion\n\
                        with r = %1.2f, sigma = %1.2f at dt = %1.2f\n\
                        (only the first 10 paths shown)" % \
                        (I, r, sigma, dt))
        ax.set_xlabel("Time steps at dt = %1.2f" % dt)
        '''
        ax.set_ylabel("Index level")
        plt.grid(True)
        plt.show()



bm = brownian_motion()
flat_log_return = bm.log_return.flatten()
import scipy.stats as scs

print(scs.describe(bm.log_return.flatten()))


def print_statistics(array):
    '''
    Prints selected statistics

    Parameters
    ==========
    array: ndarray
        object to generate statistics on

    '''

    sta = scs.describe(array)
    print("%14s %15s" % ("statistic","value"))
    print(30*"-")
    print("%14s %15.5f" % ("size",sta[0]))
    print("%14s %15.5f" % ("min",sta[1][0]))
    print("%14s %15.5f" % ("max",sta[1][1]))
    print("%14s %15.5f" % ("mean",sta[2]))
    print("%14s %15.5f" % ("std",sta[3]))
    print("%14s %15.5f" % ("skew",sta[4]))
    print("%14s %15.5f" % ("kurosis",sta[5]))

# print_statistics(flat_log_return)

fig, ax = plt.subplots()
bins = 70
label = "frequency"
ax.hist(flat_log_return, bins = bins, density = True, label = label)
ax.set_ylabel(label)
x = np.linspace(ax.axis()[0], ax.axis()[1])
ax.plot(x,scs.norm.pdf(x, loc = r / M, \
                        scale = sigma/np.sqrt(M)),\
                        "r",lw = 2,label = 'pdf')
ax.legend()
plt.grid(True)
plt.show()
