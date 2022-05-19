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

from Heuristics.problem.solution import Solution
import numpy as np

class Instance(object):

    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        self.numCodes = inputData.n
        self.numElementsCodes = inputData.m
        self.S = inputData.S

        # Distance matrix
        self.F = np.zeros((int(self.numCodes), int(self.numCodes))).astype(int)

        for i in range(self.numCodes):  # Selection of the code i
            for j in range(i + 1, self.numCodes):  # Selection of the code j to compare
                f = 0
                for k in range(self.numElementsCodes):
                    if self.S[i][k] != self.S[j][k]:
                        f += 1

                self.F[i][j] = f
                self.F[j][i] = f

        self.F = self.F.tolist()

    def getNumCodes(self):
        return self.numCodes

    def getNumElementsCodes(self):
        return self.numElementsCodes

    def getS(self):
        return self.S

    def getF(self):
        return self.F

    def getCode(self, idx):
        return self.S[idx]

    def getCodes(self):
        return self.S

    def createSolution(self):
        solution = Solution(self.S, self.F)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        return True
