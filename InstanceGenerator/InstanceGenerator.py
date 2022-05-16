'''
AMMM P2 Instance Generator v2.0
Instance Generator class.
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

import os, random
from AMMMGlobals import AMMMException


class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        n = self.config.n
        m = self.config.m

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')


            S = []
            # First code init
            S.append([0]*m)
            aux_s = []

            inserted = False
            for n_items in range(1, n):
                while not inserted:
                    for m_items in range(m):
                        aux_s.append(random.randint(0, 1))
                    if aux_s not in S:
                        S.append(aux_s)
                        inserted = True
                    aux_s = []
                inserted = False

            fInstance.write('n=%d;\n' % n)
            fInstance.write('m=%d;\n' % m)

            # translate vector of floats into vector of strings and concatenate that strings separating them by a single space character
            fInstance.write('S=\n[\n')
            for row in S:
                fInstance.write("  [")
                for column in row:
                    fInstance.write(' %d' % column)
                fInstance.write(" ]\n")
            fInstance.write("];\n")

            fInstance.close()