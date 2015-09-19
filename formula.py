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
        return x0 + vx0 * t + 0.5 * a * t*t

    @staticmethod
    def vx(vx0, a, t):
        return vx0 + a * t

class BulletDrop:
    """Calcola la y massima della traiettoria del proiettile"""
    @staticmethod
    def max_height(v0, teta):
        sinteta = math.sin(teta)
        return (v0 * v0) * sinteta * sinteta / (-2. * GRAVITY_ACCELERATION)

    """Calcola v0 e teta0 in modo tale che la parabola con punto finale xf
       passi per il punto x,y.

       NB. torna uno solo dei due angoli possibili, (teta e pi/2 - teta)
    """
    @staticmethod
    def v0_teta_pass_by(x, y, y0, xf):
        teta = math.atan(xf * (y - y0) / (1. * x * (xf - x)))
        v0 = math.sqrt(- GRAVITY_ACCELERATION * xf / math.sin(2*teta))
        return v0, teta

__all__ = ["UniformMotion", "UniformAccelleration", "BulletDrop"]
