![Static Badge](https://img.shields.io/badge/python-v3.13-blue)

###### Compatible with Windows 11

# CoordShift

This program was developed to handle geodetic transformations, specifically MGA94 & GDA2020 grid coordinate conversions
to WGS84 geographic coordinates. Australian Aeronautical Information Publications (AIPs) publish data in grid format hence
this program converts this data into a processable format.

Using EPSG's API via Pyproj, the coordinate transformation was computed under the assertion of appropriate
input parameters. Inputs required to run this program include the grid coordinate system, zone of analysis and the
corresponding Easting and Northing data.

| V1.0.0             |                               |
| ------------------ | ----------------------------- |
| [CoordShift.exe]() | Windows x64 Version Installer |
