"""
AMMM Lab Heuristics
Instance file validator v2.0
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

from AMMMGlobals import AMMMException


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['n', 'm', 'S']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        n = data.n
        if not isinstance(n, int) or (n <= 0):
            raise AMMMException('n(%s), number of codes, has to be a positive integer value.' % str(n))

        m = data.m
        if not isinstance(m, int) or (m <= 0):
            raise AMMMException('m(%s), length of the codes, has to be a positive integer value.' % str(m))

        # Validate S
        data.n_val = list(data.S)
        n_val = data.n_val
        if len(n_val) != n:
            raise AMMMException('Size of (%d) does not match with value of nTasks(%d).' % (len(n_val), n))

        for value in n_val:
            if value > 1 or value < 0:
                raise AMMMException(
                    'Invalid parameter value(%s) in S. Should be an int equal to 0 or 1.' % str(value))
