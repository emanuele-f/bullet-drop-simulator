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
from constraints import GRAVITY_ACCELERATION

class UniformMotion:
    @staticmethod
    def x(v, t):
        return v * t

    @staticmethod
    def v(x, t):
        return x * 1. / t

    @staticmethod
    def t(v, x):
        return x * 1. / v

class UniformAccelleration:
    @staticmethod
    def x(x0, vx0, a, t):
        return x0 + vx0 * t + 0.5 * a * t**2

    @staticmethod
    def vx(vx0, a, t):
        return vx0 + a * t

class BulletDrop:
    """Calcola la y massima della traiettoria del proiettile"""
    @staticmethod
    def max_height(v0, teta):
        sinteta = math.sin(teta)
        return v0**2 * sinteta**2 / (-2. * GRAVITY_ACCELERATION)

    """Calcola la gittata massima del moto."""
    @staticmethod
    def max_distance(v0):
        return 1.*v0*v0/(- GRAVITY_ACCELERATION)

    """Calcola v0 necessario a fornire la gittata xf"""
    @staticmethod
    def v0_by_distance(xf):
        return math.sqrt(- GRAVITY_ACCELERATION * xf)

    """Calcola v0 e teta0 in modo tale che la parabola con punto finale xf
       passi per il punto x,y.

       NB. torna uno solo dei due angoli possibili, (teta, pi/2 - teta)
    """
    @staticmethod
    def v0_teta_pass_by(x, y, y0, xf):
        teta = math.atan(xf * (y - y0) / (1. * x * (xf - x)))
        v0 = math.sqrt(- GRAVITY_ACCELERATION * xf / math.sin(2*teta))
        return v0, teta

    """Calcola teta, in modo tale che il punto finale del moto di velocità
       iniziale v0 sia xf. Torna None se la gittata è inferiore ad xf.

       NB. torna uno solo dei due angoli possibili, (teta, pi/2 - teta)
    """
    @staticmethod
    def teta_by_v0_xf(v0, xf):
        sin2teta = -GRAVITY_ACCELERATION * 1. * xf / (v0*v0)
        if sin2teta >= 1 or sin2teta <= 0:
            # not enough power
            return None
        teta = 0.5 * math.asin(sin2teta)
        return teta

    """Calcola, dati v0 e teta, il punto finale della traiettoria."""
    @staticmethod
    def xf_by_v0_teta(v0, teta):
        return 1. * v0**2 * math.sin(2*teta) / (-GRAVITY_ACCELERATION)

__all__ = ["UniformMotion", "UniformAccelleration", "BulletDrop"]
