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

GRAVITY_ACCELERATION = - 9.81

INITIAL_ANGLE = 45
INITIAL_VELOCITY = 8
GROUND_HEIGHT = 50

UNITSIZE = 40
SIMULATION_FPS = 60

# List of initial obstacles, in the form (x, y, w, h)
INITIAL_OBSTACLES = ()

# Color "theme"
THEME = {
    "track" : (255,50,50),
    "ramp" : (50,50,50),
    "ground" : (0,0,255),
    "obstacles" : (0,100,0),
    "units" : (255,0,0),
    "ball" : (255,0,0),
    "ball_ray" : 10,
    "stats" : (0,0,0),
    "target" : (0,255,0),
    "range" : (255,0,0),
    "line" : 2,
    "background" : (255, 255, 255)
}
