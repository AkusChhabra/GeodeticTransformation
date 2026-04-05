import numpy as np

a = 6378137.0 # metres [Semi-Major Axis]
f = 1/298.257222101 # 1/f [Reciprocal of Flattening]


## TM Definition
E0 = 500000 # metres [false_easting] #500000 # 200000
N0 = 10000000 # metres [false_northing] #10000000 # 4510193.494
m0 = 0.9996 # [central meridian scale factor]
zone_width = 6 # degrees
Long_central_meridian_zone_1 = -177 # degrees

b = a/(1-f) # [Semi-minor axis]

epsilon_sqr = f*(2-f)
epsilon = np.sqrt(f*(2-f))
n = f/(2-f)