'''
AMMM Lab Heuristics
Greedy solver
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
'''

import random, time
import sys

from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_Greedy(_Solver):

    def _selectCandidate(self, candidateList, path):
        if self.config.solver == 'Greedy':
            aux_candidate_list = candidateList[:]
            max_int = sys.maxsize
            if len(path) == self.instance.getNumCodes():
                new_index = 0
                min_value = candidateList[0]
            else:
                for i in path:
                    aux_candidate_list[i] = max_int

                min_value = min(aux_candidate_list)
                new_index = aux_candidate_list.index(min_value)
            return new_index, min_value

        # RANDOM selection
        new_index = 0
        min_value = candidateList[0]
        if len(path) != self.instance.getNumCodes():
            while True:
                choice = random.choice(candidateList)
                if choice not in path:
                    min_value = choice
                    new_index = candidateList.index(min_value)
                    break
        return new_index, min_value

    def construction(self):
        # get an empty solution for the problem
        solution = self.instance.createSolution()

        costCodes = self.instance.getF()

        path = []
        current = 0
        total_flips = 0

        path.append(current)

        for n in range(self.instance.getNumCodes()):
            new_index, value = self._selectCandidate(costCodes[current], path)

            total_flips += value
            path.append(new_index)
            current = new_index

        solution.setPathFollowed(path)
        solution.setTotalFlips(total_flips)

        return solution

    def solve(self, **kwargs):
        self.startTimeMeasure()

        solver = kwargs.get('solver', None)
        if solver is not None:
            self.config.solver = solver
        localSearch = kwargs.get('localSearch', None)
        if localSearch is not None:
            self.config.localSearch = localSearch
        self.writeLogLine(float('inf'), 0)

        solution = self.construction()
        if self.config.localSearch:
            localSearch = LocalSearch(self.config, None)
            endTime= self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

        self.elapsedEvalTime = time.time() - self.startTime
        self.writeLogLine(solution.getTotalFlips(), solution.getIterations()) #TOTAL_FLIPS AND NUMBER ITERATIONS
        self.numSolutionsConstructed = 1
        self.printPerformance()

        return solution


