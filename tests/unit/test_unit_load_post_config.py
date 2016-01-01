''' Unit test for load_post_config function for hamerkop '''
from hamerkop import load_post_config

import mock
import unittest

class LoadPostConfigTest(unittest.TestCase):
    ''' Run a unit test against load_post_config() '''

    def setUp(self):
        ''' Setup basic config '''
        self.config = {
            'articles' : {
                'config' : '/tmp/'
            }
        }
        self.desired_return = {
            1 : {
                'post_id' : 1
            }
        }

    def tearDown(self):
        ''' Destroy basic config '''
        self.config = None
        self.desired_return = None

class RunWithDirResult(LoadPostConfigTest):
    ''' Verify function tests discovered files from os.listdir '''
    @mock.patch('hamerkop.os')
    @mock.patch('hamerkop.os.path')
    @mock.patch('hamerkop.open')
    def runTest(self, mock_os, mock_path, mock_open):
        ''' Execute Test '''
        mock_os.listdir = ['directory']
        mock_path.isfile = False
        self.assertEqual(load_post_config(self.config), {})
        self.assertFalse(mock_open.called, "Failed to test if file existed")

class RunWithEmptyDir(LoadPostConfigTest):
    ''' Verify function tests discovered files from os.listdir '''
    @mock.patch('hamerkop.os')
    @mock.patch('hamerkop.open')
    def runTest(self, mock_os, mock_open):
        ''' Execute Test '''
        mock_os.listdir = []
        self.assertEqual(load_post_config(self.config), {})
        self.assertFalse(mock_open.called, "Failed to handle empty directories")
