"""
Transform Coords V1.0
Made by A.Chhabra

Convert any MGA94/GDA2020 grid coordinate into WGS84 geographic coordinate. Applicable for most Australian airports that supply an AD Survey/AOC.

Script uses EPSG API to convert.

"""

from pyproj import Proj

def throwError():
    raise ValueError("An error occurred: invalid input provided.")

def check_line(line):
    ## Check if line can be split and two arguments exist 
    try:
        x, y = line.split("\t")
        y = y.replace("\n", "")
    except ValueError:
        throwError()
    return x, y

def check_float(lat,long):
    ## Check if x, y coords are numbers 
    try:
        lat = float(lat)
        long = float(long)
    except ValueError:
        throwError()
    return lat, long

def check_grid(grid_sys, zone):
    ## Check type of grid system and use corresponding ESPG value
    if grid_sys == "MGA94" and zone >= 48 and zone <= 58:
        grid = "EPSG:283" + str(zone)
    elif grid_sys == "GDA2020" and zone >= 48 and zone <= 58:
        grid = "EPSG:78" + str(zone)
    else:
        throwError()
    return grid

def main(file_path, grid_sys, zone):
    filename = file_path#.split("/")[-1]
    #file2write = 'Coords_Output.txt'
    #filewrite = open(file2write, 'w')

    grid = check_grid(grid_sys, int(zone))

    results= []

    with open(filename, 'r') as file:
        for line in file:
            try:
                x, y = check_line(line)

                p = Proj(grid)
                long, lat = p(x,y,inverse=True)

                results.append((lat,long))

                #filewrite.write(f"{lat}\t{long}")
                #filewrite.write('\n')
            except ValueError:
                throwError()
    
    return results