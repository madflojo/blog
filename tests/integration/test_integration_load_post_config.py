from hamerkop import load_post_config

import mock
import unittest
import os
import sys

class LoadPostConfigTest(unittest.TestCase):
    ''' Run a unit test against load_post_config() '''

    def setUp(self):
        ''' Create a pseudo environment for function to run '''

        # Set config dictionary
        self.config = {
            'articles' : {
                'config' : '/tmp/'
            }
        }

        # Put desired outcome of a full run in an object
        self.desired_return = {
            1 : {
                'post_id' : 1
            }
        }

        # Create some sample test directories and files
        testdirs = [
            '/tmp/testcase1',
            '/tmp/testcase2',
            '/tmp/testcase3',
        ]
        for directory in testdirs:
            if os.path.isdir(directory) is False:
                try:
                    os.makedirs(directory)
                except OSError:
                    pass
        fh = open("/tmp/testcase2/file.yml", "w")
        fh.write("post_id: 1\n")
        fh.close()

    def tearDown(self):
        ''' Destroy pseudo environment for next run '''
        self.config = None
        self.desired_return = None
        try:
            os.remove("/tmp/testcase2/file.yml")
        except:
            pass
        try:
            os.rmdir("/tmp/testcase1")
            os.rmdir("/tmp/testcase2")
            os.rmdir("/tmp/testcase3")
        except:
            pass

class RunWithEmptyDir(LoadPostConfigTest):
    ''' Verify function tests discovered files from os.listdir '''
    def runTest(self):
        self.config['articles']['config'] = "/tmp/testcase1"
        self.assertEqual(load_post_config(self.config), {})

class RunWithYMLFile(LoadPostConfigTest):
    ''' Verify function returns good data '''
    def runTest(self):
        self.config['articles']['config'] = "/tmp/testcase2"
        self.assertEqual(load_post_config(self.config), self.desired_return)

class RunWithDirResult(LoadPostConfigTest):
    ''' Verify function tests discovered files from os.listdir '''
    def runTest(self):
        self.config['articles']['config'] = "/tmp/testcase3"
        self.assertEqual(load_post_config(self.config), {})

