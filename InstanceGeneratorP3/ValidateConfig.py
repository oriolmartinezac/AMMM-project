'''
AMMM P3 Instance Generator v2.0
Config attributes validator.
Copyright 2020 Luis Velasco

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

from AMMMGlobals import AMMMException


class ValidateConfig(object):
    # Validate config attributes read from a DAT file.

    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        paramList = ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',
                      'numCPUs', 'minNumCoresPerCPU', 'maxNumCoresPerCPU', 'minCapacityPerCore', 'maxCapacityPerCore',
                      'numTasks', 'minNumThreadsPerTask', 'maxNumThreadsPerTask', 'minResourcesPerThread', 'maxResourcesPerThread']
        for paramName in paramList:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter(%s) has not been not specified in Configuration' % str(paramName))

        instancesDirectory = data.instancesDirectory
        if len(instancesDirectory) == 0: raise AMMMException('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if len(fileNamePrefix) == 0: raise AMMMException('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if len(fileNameExtension) == 0: raise AMMMException('Value for fileNameExtension is empty')

        numInstances = data.numInstances
        if not isinstance(numInstances, int) or (numInstances <= 0):
            raise AMMMException('numInstances(%s) has to be a positive integer value.' % str(numInstances))

        numCPUs = data.numCPUs
        if not isinstance(numCPUs, int) or (numCPUs <= 0):
            raise AMMMException('numCPUs(%s) has to be a positive integer value.' % str(numCPUs))

        minNumCoresPerCPU = data.minNumCoresPerCPU
        if not isinstance(minNumCoresPerCPU, int) or (minNumCoresPerCPU <= 0):
            raise AMMMException('minNumCoresPerCPU(%s) has to be a positive integer value.' % str(minNumCoresPerCPU))

        maxNumCoresPerCPU = data.maxNumCoresPerCPU
        if not isinstance(maxNumCoresPerCPU, int) or (maxNumCoresPerCPU <= 0):
            raise AMMMException('maxNumCoresPerCPU(%s) has to be a positive integer value.' % str(maxNumCoresPerCPU))

        if maxNumCoresPerCPU < minNumCoresPerCPU:
            raise AMMMException('maxNumCoresPerCPU(%s) has to be >= minNumCoresPerCPU(%s).' % (str(maxNumCoresPerCPU), str(minNumCoresPerCPU)))

        minCapacityPerCore = data.minCapacityPerCore
        if not isinstance(minCapacityPerCore, (int, float)) or (minCapacityPerCore <= 0):
            raise AMMMException('minCapacityPerCore(%s) has to be a positive float value.' % str(minCapacityPerCore))

        maxCapacityPerCore = data.maxCapacityPerCore
        if not isinstance(maxCapacityPerCore, (int, float)) or (maxCapacityPerCore <= 0):
            raise AMMMException('maxCapacityPerCore(%s) has to be a positive float value.' % str(maxCapacityPerCore))

        if maxCapacityPerCore < minCapacityPerCore:
            raise AMMMException('maxCapacityPerCore(%s) has to be >= minCapacityPerCore(%s).' % (str(maxCapacityPerCore), str(minCapacityPerCore)))

        numTasks = data.numTasks
        if not isinstance(numTasks, int) or (numTasks <= 0):
            raise AMMMException('numTasks(%s) has to be a positive integer value.' % str(numTasks))

        minNumThreadsPerTask = data.minNumThreadsPerTask
        if not isinstance(minNumThreadsPerTask, int) or (minNumThreadsPerTask <= 0):
            raise AMMMException('minNumThreadsPerTask(%s) has to be a positive integer value.' % str(minNumThreadsPerTask))

        maxNumThreadsPerTask = data.maxNumThreadsPerTask
        if not isinstance(maxNumThreadsPerTask, int) or (maxNumThreadsPerTask <= 0):
            raise AMMMException('maxNumThreadsPerTask(%s) has to be a positive integer value.' % str(maxNumThreadsPerTask))

        if maxNumThreadsPerTask < minNumThreadsPerTask:
            raise AMMMException('maxNumThreadsPerTask(%s) has to be >= minNumThreadsPerTask(%s).' % (str(maxNumThreadsPerTask), str(minNumThreadsPerTask)))

        minResourcesPerThread = data.minResourcesPerThread
        if not isinstance(minResourcesPerThread, (int, float)) or (minResourcesPerThread <= 0):
            raise AMMMException('minResourcesPerThread(%s) has to be a positive float value.' % str(minResourcesPerThread))

        maxResourcesPerThread = data.maxResourcesPerThread
        if not isinstance(maxResourcesPerThread, (int, float)) or (maxResourcesPerThread <= 0):
            raise AMMMException('maxResourcesPerThread(%s) has to be a positive float value.' % str(maxResourcesPerThread))

        if maxResourcesPerThread < minResourcesPerThread:
            raise AMMMException('maxResourcesPerThread(%s) has to be >= minResourcesPerThread(%s).' % (str(maxResourcesPerThread), str(minResourcesPerThread)))
