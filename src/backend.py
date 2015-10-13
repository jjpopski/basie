#coding=utf-8

#
#
#    Copyright (C) 2013  INAF -IRA Italian institute of radioastronomy, bartolini@ira.inaf.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
logger=logging.getLogger(__name__)

from persistent import Persistent

from errors import *


class Backend(Persistent):
    def __init__(self, name, backend_type = "INVALID"):
        self.name = name
        self.backend_type = backend_type
        self.can_activate_switching_mark = False

    def _get_backend_instructions(self):
        raise NotImplementedError

    def __str__(self):
        res = "%s:BACKENDS/%s{\n" % (self.name, self.backend_type)
        res += self._get_backend_instructions()
        res += "}\n"
        return res


class XBackend(Backend):
    def __init__(self, name, configuration):
        Backend.__init__(self, name, "XBackend")
        self.configuration = configuration
        self.can_activate_switching_mark = False

    def _get_backend_instructions(self):
        res = "\tinitialize=%s\n" % (self.configuration,)
        return res


class TotalPowerBackend(Backend):
    def __init__(self, name, integration, sampling, bandwidth):
        Backend.__init__(self, name, "TotalPower")
        self.integration = integration
        self.samplingInterval = sampling
        self.sections = []
        self.valid_filters = [300.0, 730.0, 1250.0, 2000.0]
        self.can_activate_switching_mark = True
        self.bandwidth = bandwidth

    def set_sections(self, nfeed, bandwidth):
        if not bandwidth in self.valid_filters:
            msg = "not a valid bandwidth: %f" % (bandwidth,)
            logger.error(msg)
            raise ScheduleError(msg)
        for i in range(nfeed):
            self.sections.append((i, float(bandwidth)))

    def _get_backend_instructions(self):
        res = "\tintegration=%d\n" % (self.integration,)
        enable_string = "\tenable="
        for i, (_id, _bw) in enumerate(self.sections):
            res += "\tsetSection=%d,*,%f,*,*,%f,*\n" % (_id, _bw,
                                                        self.samplingInterval,)
            if i > 0:
                enable_string += ";"
            enable_string += "1"
        enable_string += "\n"
        res += enable_string
        return res
            