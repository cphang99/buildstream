#!/usr/bin/env python3
#
#  Copyright (C) 2016 Codethink Limited
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library. If not, see <http://www.gnu.org/licenses/>.
#
#  Authors:
#        Tristan Van Berkom <tristan.vanberkom@codethink.co.uk>

"""The BuildElement class is a convenience element one can derive from for
implementing the most common case of element.
"""

import os
from . import Element, Scope, ElementError


_command_steps = ['bootstrap-commands',
                  'configure-commands',
                  'build-commands',
                  'test-commands',
                  'install-commands',
                  'strip-commands']
_command_prefixes = ['pre-', '', 'post-']


class BuildElement(Element):

    def configure(self, node):

        self.commands = {}

        for step in _command_steps:
            for prefix in _command_prefixes:
                command_name = prefix + step
                self.commands[command_name] = self._get_commands(node, command_name)

    def preflight(self):
        pass

    def get_unique_key(self):
        dictionary = {}

        for command_name, command_list in self.commands.items():
            dictionary[command_name] = command_list

        # Specifying notparallel for a given element effects the
        # cache key, while having the side effect of setting max-jobs to 1,
        # which is normally automatically resolved and does not effect
        # the cache key.
        variables = self._get_variables()
        if self.node_get_member(variables.variables, bool, 'notparallel', default_value=False):
            dictionary['notparallel'] = True

        return dictionary

    def assemble(self, sandbox):

        # Stage deps in the sandbox root
        for dep in self.dependencies(Scope.BUILD):
            dep.stage(sandbox)

        # Run any integration commands provided by the dependencies
        # once they are all staged and ready
        for dep in self.dependencies(Scope.BUILD):
            dep.integrate(sandbox)

        # Stage sources in /buildstream/build
        self.stage_sources(sandbox, '/buildstream/build')

        # Ensure builddir and installdir
        os.makedirs(os.path.join(sandbox.executor.fs_root,
                                 'buildstream',
                                 'build'), exist_ok=True)
        os.makedirs(os.path.join(sandbox.executor.fs_root,
                                 'buildstream',
                                 'install'), exist_ok=True)

        # And set the sandbox work directory too
        sandbox.set_cwd('/buildstream/build')

        # Run commands
        for step in _command_steps:
            for prefix in _command_prefixes:
                command_name = prefix + step
                commands = self.commands[command_name]
                for cmd in commands:
                    with self.timed_activity("Running %s" % command_name):
                        self.status("Running %s" % command_name, detail=cmd)

                        # Note the -e switch to 'sh' means to exit with an error
                        # if any untested command fails.
                        #
                        exitcode, _, _ = sandbox.run(['sh', '-c', '-e', cmd + '\n'])
                        if exitcode != 0:
                            raise ElementError("Command '{}' failed with exitcode {}".format(cmd, exitcode))

        # Return the payload (XXX TODO: expand 'install-root' variable)
        return '/buildstream/install'

    def _get_commands(self, node, name):
        list_node = self.node_get_member(node, list, name, default_value=[])
        commands = []

        for i in range(len(list_node)):
            command = self.node_subst_list_element(node, name, [i])
            commands.append(command)

        return commands
