"""
AMMM Lab Heuristics
Local Search algorithm
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
import time
from Heuristics.solver import _Solver
from AMMMGlobals import AMMMException


# A change in a solution in the form: move taskId from curCPUId to newCPUId.
# This class is used to perform sets of modifications.
# A new solution can be created based on an existing solution and a list of
# changes using the createNeighborSolution(solution, moves) function.

# Implementation of a local search using two neighborhoods and two different policies.
class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy
        self.maxExecTime = config.maxExecTime
        super().__init__(config, instance)

    def solve(self, **kwargs):
        initialSolution = kwargs.get('solution', None)
        if initialSolution is None:
            raise AMMMException('[local search] No solution could be retrieved')

        if not initialSolution.isFeasible(): return initialSolution
        self.startTime = kwargs.get('startTime', None)
        endTime = kwargs.get('endTime', None)

        incumbent = initialSolution
        incumbentFlips = incumbent.getTotalFlips()
        iterations = 0

        # keep iterating while improvements are found
        while time.time() < endTime:
            iterations += 1

            neighbor = self.LS_2opt(incumbent)
            if neighbor is None: break
            neighborFlips = neighbor.getTotalFlips()
            if incumbentFlips <= neighborFlips: break
            incumbent = neighbor
            incumbentFlips = neighborFlips

        incumbent.setIterations(iterations)
        return incumbent

    def LS_2opt(self, solution): # Flips is F matrix, path is solution from greedy
        path = solution.getPathFollowed()
        result_path = path
        flips = solution.getFMatrix()
        current_total_flips = solution.getTotalFlips()
        changed = False

        for i in range(len(path)): # CHECK IF IT IS GETTING OUT OF INDEX
            for j in range(i+2, len(path) - 1): # CHECK IF IT IS GETTING OUT OF INDEX
                current_cost = flips[path[i]][path[i+1]] + flips[path[j]][path[j+1]]
                new_cost = flips[path[i]][path[j]] + flips[path[i+1]][path[j+1]]

                if new_cost < current_cost:
                    changed = True
                    total_cost = current_cost - new_cost
                    current_total_flips -= total_cost
                    min_i = i
                    min_j = j
                    result_path[min_i + 1: min_j + 1] = path[min_i + 1: min_j + 1][::-1]  # Change in the path

                    if self.policy == 'FirstImprovement':
                        break
            if self.policy == 'FirstImprovement' and changed:
                break

        solution.setPathFollowed(result_path)
        solution.setTotalFlips(current_total_flips)

        return solution
