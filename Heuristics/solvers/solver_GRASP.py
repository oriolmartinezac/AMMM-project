'''
AMMM Lab Heuristics
GRASP solver
Copyright 2018 Luis Velasco.

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
'''

import random
import sys
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidateList, alpha, path):  # COMPLETED !!
        aux_candidate_list = candidateList[:]
        max_int = sys.maxsize

        if len(path) == self.instance.getNumCodes():
            new_index = 0
            selection = candidateList[0]
        else:
            for i in path:
                aux_candidate_list[i] = max_int

            sortedCandidateList = sorted(aux_candidate_list)  # Order the elements

            minF = sortedCandidateList[0]
            window = (len(path)+1)*-1
            maxF = sortedCandidateList[window]
            boundaryF = minF + (maxF - minF) * alpha

            # find elements that fall into the RCL
            maxIndex = 0
            for candidate in sortedCandidateList:
                if candidate <= boundaryF:
                    maxIndex += 1

            # create RCL and pick an element randomly
            rcl = sortedCandidateList[0:maxIndex]  # pick first maxIndex elements starting from element 0
            if not rcl:
                return None

            selection = random.choice(rcl)
            new_index = aux_candidate_list.index(selection)
        return new_index, selection  # pick a candidate from rcl at random

    def _greedyRandomizedConstruction(self, alpha):
        # get an empty solution for the problem
        solution = self.instance.createSolution()
        costCodes = self.instance.getF()

        path = []
        current = 0
        total_flips = 0

        path.append(current)

        for n in range(self.instance.getNumCodes()):
            new_index, value = self._selectCandidate(costCodes[current], alpha, path)

            total_flips += value
            path.append(new_index)
            current = new_index

        solution.setPathFollowed(path)
        solution.setTotalFlips(total_flips)

        return solution

    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()
        incumbent = self.instance.createSolution()
        bestTotalFlips = sys.maxsize
        #self.writeLogLine(bestTotalFlips, 0)

        iteration = 0
        while not self.stopCriteria():
            iteration += 1

            # force first iteration as a Greedy execution (alpha == 0)
            alpha = 0 if iteration == 1 else self.config.alpha

            solution = self._greedyRandomizedConstruction(alpha)
            if self.config.localSearch:
                localSearch = LocalSearch(self.config, None)
                endTime = self.startTime + self.config.maxExecTime
                solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

            solutionTotalFlips = solution.getTotalFlips()
            if solutionTotalFlips < bestTotalFlips:
                incumbent = solution
                bestTotalFlips = solutionTotalFlips
                self.writeLogLine(bestTotalFlips, iteration)

        incumbent.setIterations(iteration)

        self.writeLogLine(solution.getTotalFlips(), iteration)  # TOTAL_FLIPS AND NUMBER ITERATIONS
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent
