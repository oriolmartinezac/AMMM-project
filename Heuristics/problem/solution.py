"""
AMMM Lab Heuristics
Representation of a solution instance
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import copy
from Heuristics.solution import _Solution

class Solution(_Solution):
    def __init__(self, S, F):
        self.S = S
        self.F = F
        self.total_flips = 0
        self.path_followed = []
        super().__init__()

    def setFMatrix(self, matrix):
        self.F = matrix

    def getFMatrix(self):
        return self.F

    def setTotalFlips(self, total_flips):
        self.total_flips = total_flips

    def getTotalFlips(self):
        return self.total_flips

    def setPathFollowed(self, path_followed):
        self.path_followed = path_followed

    def getPathFollowed(self):
        return self. path_followed

    def __str__(self):

        strSolution = 'OBJECTIVE: %d;\n' % self.total_flips
        if self.fitness == float('inf'):
            return strSolution

        for index, code_index in enumerate(self.path_followed):
            if index == 0:
                strSolution += str(code_index)
            else:
                strSolution += '-->'+str(code_index)

        return strSolution

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
