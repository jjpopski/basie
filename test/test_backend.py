#coding=utf-8

import unittest2 as unittest

from basie.backend import *

class TestRoachBackend(unittest.TestCase):
    def setUp(self):
        self.name = "prova"
        self.configuration = "RCONFIG"
        self.roach_backend = RoachBackend(self.name, self.configuration)

    def test_roach_backend_instructions(self):
        backend_instructions = ""
        self.assertEqual(self.roach_backend._get_backend_instructions(), 
                         backend_instructions)

    def test_roach_backend_bck_file(self):
        bck_file = "%s:BACKENDS/Roach{\n}\n" % (self.name,)
        self.assertEqual(str(self.roach_backend),
                         bck_file)
