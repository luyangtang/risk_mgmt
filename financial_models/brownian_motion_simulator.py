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


def plot_paths(paths, num_paths_shown = 10):
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
    plot_paths(gen_path(S0 = 100,
            r = 0.05,
            sigma = 0.25,
            T = 10,
            M = 50,
            I = 100))
    '''

    fig, ax = plt.subplots()
    ax.plot(paths[:,:num_paths_shown])
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

r = 0.05 # constant riskless short value
sigma = 0.25 # constant volatility
I = 2000 # number of paths
M = 50 # number of steps
T = 10 # max time
S0 = 100 # initial state

paths = gen_path(S0, r, sigma, T, M, I)
print(paths)
plot_paths(paths)
