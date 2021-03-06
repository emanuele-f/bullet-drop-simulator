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
SIMULATION_FPS = 40
# Skip some frame visualization when simulation is running slow
FRAME_SKIP = False

# List of initial obstacles, in the form (x, y, w, h)
#~ INITIAL_OBSTACLES = ((7,0,2,1), (3,0,3,3))
INITIAL_OBSTACLES = ()

# Color "theme"
THEME = {
    "arrow" : (255,0,0),
    "arrow_width" : 2,
    "track" : (255,50,50),
    "ramp" : (50,50,50),
    "ground" : (0,0,255),
    "obstacles" : (0,100,0),
    "units" : (255,0,0),
    "ball" : (255,0,0),
    "ball_ray" : 10,
    "stats" : (0,0,0),
    "target" : (0,255,0),
    "target_width" : 5,
    "target_height" : 15,
    "maxrange" : (255,0,0),
    "line" : 2,
    "background" : (255, 255, 255)
}

# Size stuff
class Measures:
    PANEL_BOX_PADDING = 10
    PANEL_BOX_MARGIN = 3
    PANEL_INNER_PADDING = 7
    PANEL_INNER_PADDING_SMALL = 3
