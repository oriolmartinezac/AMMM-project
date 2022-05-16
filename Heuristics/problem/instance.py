"""
AMMM Lab Heuristics
Representation of a problem instance
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

from Heuristics.problem.Task import Task
from Heuristics.problem.CPU import CPU
from Heuristics.problem.solution import Solution

class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        self.numCodes = inputData.n
        self.numElementsCodes = inputData.m
        self.S = inputData.S

        # Distance matrix
        self.F = [[0] * self.numCodes for i in range(self.numCodes)]

        for i in range(self.numCodes):
            for j in range(self.numElementsCodes):
                for k in range(self.numCodes):
                    if i != k:
                        if self.S[i][j] != self.S[k][j]:
                            self.F[i][k] += 1

    def getNumCodes(self):
        return len(self.numCodes)

    def getNumElementsCodes(self):
        return len(self.numElementsCodes)

    def getS(self):
        return self.S

    def getF(self):
        return self.F

    def getCode(self, idx):
        return self.S[idx]

    def createSolution(self):
        solution = Solution(self.S, self.F)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        return True
