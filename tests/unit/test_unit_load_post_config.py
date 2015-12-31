from hamerkop import load_post_config

import io
import mock
import unittest

class LoadPostConfigTest(unittest.TestCase):
    ''' Run a unit test against load_post_config() '''

    def setUp(self):
        self.config = {
            'articles' : {
                'config' : '/tmp/'
            }
        }
        self.file_data = io.StringIO(u'post_id: 1')
        self.yaml_data = { 'post_id' : 1 }
        self.desired_return = {
            1 : {
                'post_id' : 1
            }
        }

    def tearDown(self):
        self.config = None
        self.file_data = None
        self.yaml_data = None
        self.desired_return = None

class RunWithDirResult(LoadPostConfigTest):
    ''' Verify function tests discovered files from os.listdir '''
    @mock.patch('hamerkop.os')
    @mock.patch('hamerkop.os.path')
    @mock.patch('hamerkop.open')
    @mock.patch('hamerkop.yaml')
    def runTest(self, mock_os, mock_path, mock_open, mock_yaml):
        mock_os.listdir = [ 'directory' ]
        mock_path.isfile = False
        self.assertEqual(load_post_config(self.config), {})
        self.assertFalse(mock_open.called, "Failed to test if file existed")

class RunWithEmptyDir(LoadPostConfigTest):
    ''' Verify function tests discovered files from os.listdir '''
    @mock.patch('hamerkop.os')
    @mock.patch('hamerkop.os.path')
    @mock.patch('hamerkop.open')
    @mock.patch('hamerkop.yaml')
    def runTest(self, mock_os, mock_path, mock_open, mock_yaml):
        mock_os.listdir = []
        self.assertEqual(load_post_config(self.config), {})
        self.assertFalse(mock_open.called, "Failed to handle empty directories")
