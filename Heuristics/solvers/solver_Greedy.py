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
            max_int = sys.maxsize
            if len(path) == self.instance.getNumCodes():
                new_index = 0
                min_value = candidateList[0]
            else:
                for i in path:
                    candidateList[i] = max_int

                min_value = min(candidateList)
                # new_index = sortedCandidateList.index(min_value) + (index+1)
                new_index = candidateList.index(min_value)
            return new_index, min_value  # Return position next node

        return random.choice(candidateList)

    def construction(self):
        # get an empty solution for the problem
        solution = self.instance.createSolution()

        # get tasks and sort them by their total required resources in descending order
        costCodes = self.instance.getF()

        # TAKE the codes to feasible assignments
        # select the best candidate
        path = []
        current = 0
        total_flips = 0

        path.append(current)

        for n in range(self.instance.getNumCodes()):

            new_index, value = self._selectCandidate(costCodes[current], path)

            total_flips += value
            path.append(new_index)
            current = new_index

        solution.add(path, total_flips)

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
        self.writeLogLine(solution.getFitness(), 1)
        self.numSolutionsConstructed = 1
        self.printPerformance()

        return solution


