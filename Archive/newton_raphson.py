import numpy as np
import constants

def f_func(t):
    sigma = sigma_calc(t)
    return t*np.sqrt(1+sigma**2) - sigma*np.sqrt(1+t**2) - df_func(t)

def df_func(t):
    sigma = sigma_calc(t)
    return (np.sqrt(1+sigma**2)*np.sqrt(1+t**2) - sigma*t)*(((1-constants.epsilon**2)*(np.sqrt(1+t**2)))/(1 + (1-constants.epsilon**2)*t**2))

def sigma_calc(t):
    return np.sinh(constants.epsilon*np.arctanh(constants.epsilon*t/(np.sqrt(1+t**2))))

def newton_raphson(t0, tol=1e-7, max_iter=100):

    t = t0
    for i in range(max_iter):
        ft = f_func(t)
        dft = df_func(t)
        
        if abs(dft) < 1e-10:
            print("Derivative too small; no convergence.")
            return None

        t_new = t - ft / dft

        if abs(t_new - t) < tol:
            return t_new
        
        t = t_new
        
    print("Maximum iterations reached; no convergence.")
    return t
