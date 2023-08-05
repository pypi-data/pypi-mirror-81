#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Pybeeryaml
# Copyright (C) 2018  TROUVERIE Joachim <joachim.trouverie@linoame.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from pybeeryaml.meta import BeerComponent


class Water(BeerComponent):
    """Water class"""

    def __init__(
        self,
        name,
        amount,
        calcium,
        bicarbonate,
        sulfate,
        chloride,
        sodium,
        magnesium,
        ph,
        **kwargs
    ):
        super().__init__()

        self.name = name
        self.amount = amount
        self.calcium = calcium
        self.bicarbonate = bicarbonate
        self.sulfate = sulfate
        self.chloride = chloride
        self.magnesium = magnesium
        self.ph = ph

        self.set(kwargs)
