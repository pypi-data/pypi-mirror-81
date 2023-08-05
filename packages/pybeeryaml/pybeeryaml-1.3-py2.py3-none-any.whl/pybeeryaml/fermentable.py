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


class Fermentable(BeerComponent):
    """Fermentable class"""

    def __init__(self, name, type, amount, color, beeryaml_yield, **kwargs):
        super().__init__()

        self.name = name
        self.type = type
        self.amount = amount
        self.color = color
        self.beeryaml_yield = beeryaml_yield

        self.set(kwargs)
