#   Property of Akus Chhabra
#   
#   Script established to transform between ellipsoid and grid coordinates
#   Tailored towards Australia's method of displaying coordinates in easting-northing

import numpy as np
import constants
from newton_raphson import *

### Inputs

E = 367478.9    # East Grid Coordinate
N = 8131831.3   # North Grid Coordinate

n = constants.n

#A = (a/(1+n))*((n**2)*((n**2)*((n**2)*(25*n**2 + 64) + 256) + 16384))/16384
A = (constants.a/(1+n))*(1 + (1/4)*n**2 + (1/64)*n**4 + (1/256)*n**6 + (25/16384)*n**8)

## Alpha Coefficients

alpha_2 = (1/2)*n - (2/3)*n**2 + (5/16)*n**3 + (41/180)*n**4 - (127/288)*n**5 + (7891/37800)*n**6 
+ (72161/387072)*n**7 - (18975107/50803200)*n**8

alpha_4 = (13/48)*n**2 - (3/5)*n**3 + (557/1440)*n**4 + (281/630)*n**5 - (1983433/1935360)*n**6 
+ (13769/28800)*n**7 + (148003883/174182400)*n**8

alpha_6 = (61/240)*n**3 - (103/140)*n**4 + (15061/26880)*n**5 + (167603/181440)*n**6 
- (67102379/29030400)*n**7 + (79682431/79833600)*n**8

alpha_8 = (49561/161280)*n**4 - (179/168)*n**5 + (6601661/7257600)*n**6 + (97445/49896)*n**7 
- (40176129013/7664025600)*n**8

alpha_10 = (34729/80640)*n**5 - (3418889/1995840)*n**6 + (14644087/9123840)*n**7 + (2605413599/622702080)*n**8

alpha_12 = (212378941/319334400)*n**6 - (30705481/10378368)*n**7 + (175214326799/58118860800)*n**8

alpha_14 = (1522256789/1383782400)*n**7 - (16759934899/3113510400)*n**8

alpha_16 = (1424729850961/743921418240)*n**8

alpha = [alpha_2, alpha_4, alpha_6, alpha_8, alpha_10, alpha_12, alpha_14, alpha_16]


## Beta Coefficients

beta_2 = -(1/2)*n + (2/3)*n**2 - (37/96)*n**3 + (1/360)*n**4 + (81/512)*n**5 - (96199/604800)*n**6 
+ (5406467/38707200)*n**7 - (7944359/67737600)*n**8

beta_4 = -(1/48)*n**2 - (1/15)*n**3 + (437/1440)*n**4 +-(46/105)*n**5 + (1118711/3870720)*n**6 
- (51841/1209600)*n**7 - (24749483/348364800)*n**8

beta_6 = -(17/480)*n**3 + (37/840)*n**4 + (209/4480)*n**5 - (5569/90720)*n**6 - (9261899/58060800)*n**7 
+ (6457463/17740800)*n**8

beta_8 = -(4397/161280)*n**4 + (11/54)*n**5 + (830251/7257600)*n**6 - (466511/2494800)*n**7 
- (324154477/7664025600)*n**8

beta_10 = -(4583/161280)*n**5 + (108847/3991680)*n**6 + (8005831/63866880)*n**7 - (22894433/124540416)*n**8

beta_12 = -(20648693/638668800)*n**6 + (16363163/518918400)*n**7 + (2204645983/12915302400)*n**8

beta_14 = -(219941297/5535129600)*n**7 + (497323811/12454041600)*n**8

beta_16= -(191773887257/3719607091200)*n**8

beta = [beta_2, beta_4, beta_6, beta_8, beta_10, beta_12, beta_14, beta_16]


## Compute Transverse Mercator X, Y coordinates

X = (E - constants.E0)/constants.m0 # East coordinate
Y = (N - constants.N0)/constants.m0 # North coordinate

## Transverse Mercator (TM) ratios zeta and eta

zeta = Y/A
eta = X/A

## Gauss-Schreiber ratios

zeta_prime = zeta
eta_prime = eta

for k in range(0, 8):
    zeta_prime += beta[k]*np.sin(2*k*zeta)*np.cosh(2*k*eta)
    eta_prime += beta[k]*np.cos(2*k*zeta)*np.sinh(2*k*eta)


## Compute t' = tan(phi')

t_prime = np.sin(zeta_prime)/(np.sqrt(np.sinh(eta_prime)**2 + np.cos(zeta_prime)**2))

lat_phi = np.arctan(newton_raphson(t_prime))*180/np.pi

## Compute Long diff omega and long lambda

omega = np.arctan(np.sinh(eta_prime)/np.cos(zeta_prime))
longitude_lambda = constants.Long_central_meridian_zone_1 + omega 


# p and q factors

p, q = 0, 0
for k in range(0,8):
    p += 1 + 2*k*alpha[k]*np.cos(2*k*zeta_prime)*np.cosh(2*k*eta_prime)
    q += -2*k*alpha[k]*np.sin(2*k*zeta_prime)*np.sinh(2*k*eta_prime)

# Point scale factor m

phi_prime = np.arctan(t_prime)
m = constants.m0*(A/constants.a)*np.sqrt(p**2 + q**2)*((np.sqrt(1 + np.tan(lat_phi)**2)*(np.sqrt(1-constants.epsilon_sqr*np.sin(lat_phi)**2)))/(np.sqrt(np.tan(phi_prime**2) + np.cos(omega))**2))


## Grid Convergence, gamma

gamma = np.arctan(np.abs(q/p)) + np.arctan(np.abs(np.tan(phi_prime)*np.tan(omega))/np.sqrt(1 + np.tan(phi_prime)**2))


print(f"\nRectifying Radius, A: ", A)
print(f"Semi-Minor Axis, b: ", constants.b)
print(f"eccentricity squared: ", constants.epsilon_sqr)
print(f"n: ", n)
print(f"X: ", X)
print(f"Y: ", Y)
print(f"zeta: ", zeta)
print(f"eta: ", eta)
print(f"zeta_prime: ", zeta_prime)
print(f"eta_prime: ", eta_prime)
print(f"t_prime: ", t_prime)
print(f"lat_phi: ", lat_phi)
print(f"omega: ", omega)
print(f"longitude_lambda: ", longitude_lambda)
print(f"Scalar Factor, p: ", p)
print(f"Scalar Factor, q: ", q)
print(f"Point Scale Factor, m: ", m)
print(f"Grid Convergence, gamma: ", gamma)