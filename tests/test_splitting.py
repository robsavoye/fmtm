#!/usr/bin/python3

# Copyright (c) 2022, 2023 Humanitarian OpenStreetMap Team
# This file is part of FMTM.
#
#     FMTM is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     FMTM is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with FMTM.  If not, see <https:#www.gnu.org/licenses/>.
#

import pytest
import numpy as np
from shapely.geometry import shape
import shapely
# from shapely.prepared import prep
import geojson
from geojson import Polygon, Feature, FeatureCollection, dump

file = open("test_boundary.geojson", 'r')
coords = geojson.load(file)
boundary = shape(coords['features'][0]['geometry'])

minx, miny, maxx, maxy = boundary.bounds
delta = 0.005
nx = int((maxx - minx)/delta)
ny = int((maxy - miny)/delta)
gx, gy = np.linspace(minx,maxx,nx), np.linspace(miny,maxy,ny)
grid = list()
json = open("tmp.geojson", 'w')
id = 0
for i in range(len(gx)-1):
    for j in range(len(gy)-1):
        poly = shapely.geometry.Polygon([
            [gx[i],gy[j]],
            [gx[i],gy[j+1]],
            [gx[i+1],gy[j+1]],
            [gx[i+1],gy[j]],
            [gx[i],gy[j]],
        ])
        if boundary.contains(poly):
            feature = Feature(geometry=poly, properties={'id': str(id)})
            id += 1
            grid.append(feature)
collection = FeatureCollection(grid)
dump(collection, json)

