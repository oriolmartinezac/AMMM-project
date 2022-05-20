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
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidateList, alpha): # COMPLETED !!

        sortedCandidateList = sorted(candidateList) # Order the elements

        minF = sortedCandidateList[0]
        maxF = sortedCandidateList[-1]
        boundaryF = minF + (maxF - minF) * alpha
        
        # find elements that fall into the RCL
        maxIndex = 0
        for candidate in sortedCandidateList:
            if candidate <= boundaryF:
                maxIndex += 1

        # create RCL and pick an element randomly
        rcl = sortedCandidateList[0:maxIndex]          # pick first maxIndex elements starting from element 0
        if not rcl: return None
        return random.choice(rcl)          # pick a candidate from rcl at random
    
    def _greedyRandomizedConstruction(self, alpha): #TODO: function
        # get an empty solution for the problem
        solution = self.instance.createSolution()
        
        # get tasks and sort them by their total required resources in descending order
        tasks = self.instance.getTasks()
        sortedTasks = sorted(tasks, key=lambda t: t.getTotalResources(), reverse=True)


        # for each task taken in sorted order
        for task in sortedTasks:
            taskId = task.getId()
            
            # compute feasible assignments
            candidateList = solution.findFeasibleAssignments(taskId)

            # no candidate assignments => no feasible assignment found
            if not candidateList:
                solution.makeInfeasible()
                break
            
            # select an assignment
            candidate = self._selectCandidate(candidateList, alpha)

            # assign the current task to the CPU that resulted in a minimum highest load
            solution.assign(taskId, candidate.cpuId)
            
        return solution
    
    def stopCriteria(self): #TODO: function
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs): #TODO: function
        self.startTimeMeasure()
        incumbent = self.instance.createSolution()
        incumbent.makeInfeasible()
        bestTotalFlips = incumbent.getTotalFlips()
        self.writeLogLine(bestTotalFlips, 0)

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

            if solution.isFeasible():
                solutionHighestLoad = solution.getFitness()
                if solutionHighestLoad < bestTotalFlips :
                    incumbent = solution
                    bestTotalFlips = solutionHighestLoad
                    self.writeLogLine(bestTotalFlips, iteration)

        self.writeLogLine(bestTotalFlips, iteration)
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent

