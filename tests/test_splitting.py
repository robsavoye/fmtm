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
import shapely
#from shapely.geometry import Polygon, shape, GeometryCollection
from shapely.geometry import shape
from shapely.prepared import prep
from shapely import wkt
import geojson
from geojson import Polygon, Feature, FeatureCollection, dump


boundary = open("test_boundary.geojson", 'r')
coords = geojson.load(boundary)
#print(coords)
poly = shape(coords['features'][0]['geometry'])
# xmin,ymin,xmax,ymax =  boundary.total_bounds

minx, miny, maxx, maxy = poly.bounds
delta = 0.005
nx = int((maxx - minx)/delta)
ny = int((maxy - miny)/delta)
gx, gy = np.linspace(minx,maxx,nx), np.linspace(miny,maxy,ny)
grid = list()
json = open("tmp.geojson", 'w')
id = 0
for i in range(len(gx)-1):
    for j in range(len(gy)-1):
        poly = Polygon([[
            [gx[i],gy[j]],
            [gx[i],gy[j+1]],
            [gx[i+1],gy[j+1]],
            [gx[i+1],gy[j]],
            [gx[i],gy[j]]],
        ])
        feature = Feature(geometry=poly, properties={'id': str(id)})
        id += 1
        grid.append(feature)
collection = FeatureCollection(grid)

dump(collection, json)

# def partition(geom, delta):
#     prepared_geom = prep(geom)
#     grid = list(filter(prepared_geom.intersects, grid_bounds(geom, delta)))
#     return grid
