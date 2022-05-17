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


# This class stores the load of the highest loaded CPU
# when a task is assigned to a CPU.
class Assignment(object):
    def __init__(self, taskId, cpuId, highestLoad):
        self.taskId = taskId
        self.cpuId = cpuId
        self.highestLoad = highestLoad

    def __str__(self):
        return "<t_%d, c_%d>: highestLoad: %.2f%%" % (self.taskId, self.cpuId, self.highestLoad * 100)


# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    def __init__(self, S, F):
        self.S = S
        self.F = F
        self.total_flips = 0
        self.path_followed = []
        super().__init__()

    def add(self, path, total_flips):
        try:
            self.total_flips = total_flips
            self.path_followed = path
            return True
        except:
            return False

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
