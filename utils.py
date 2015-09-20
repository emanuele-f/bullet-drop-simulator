#!/bin/env python2
# -*- coding: utf-8 -*-
#
# Emanuele Faranda                         <black.silver@hotmail.it>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import math

def ToRadians(degrees):
    return 2. * math.pi * degrees / 360

def ToDegrees(radians):
    return radians * 360. / (2 * math.pi)

def RectCollidePoint(rectf, point):
    return point[0] >= rectf[0] and\
        point[0] <= rectf[2] and\
        point[1] >= rectf[1] and\
        point[1] <= rectf[3]

__all__ = ["ToRadians", "ToDegrees", "RectCollidePoint"]
