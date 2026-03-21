import numpy

def f(t):
    return t

def df(t):
    return t

def newton_raphson(f, df, t0, tol=1e-7, max_iter=100):

    t = t0
    for i in range(max_iter):
        ft = f(t)
        dft = df(t)
        
        if abs(dft) < 1e-10:
            print("Derivative too small; no convergence.")
            return None

        t_new = t - ft / dft

        if abs(t_new - t) < tol:
            return t_new
        
        t = t_new
        
    print("Maximum iterations reached; no convergence.")
    return t
