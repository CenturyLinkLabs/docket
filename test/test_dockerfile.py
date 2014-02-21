import unittest
import os
import shutil
from docket.dockerfile import Dockerfile

class TestDockerfile(unittest.TestCase):

    def setUp(self):
        self.dfile = Dockerfile("sample")
        
    def test_extraction(self):
        self.dfile.parse()
        self.assertEqual(self.dfile.parent, "ubuntu:12.10")
        self.assertEqual(self.dfile.cmd, '["python", "-V"]')
        self.assertEqual(self.dfile.volumes, ['/tmp'])
        self.assertEqual(self.dfile.ports, ['80', '512'])
        self.assertEqual(self.dfile.command, 'python -V')
        


class TestResolveFetch(unittest.TestCase):

    def setUp(self):
        pass

    def test_recognized(self):
        pass
        # test
        #  - username/repo => dir[username]/dir[repo]
        #  - https://github.com/username/repo => "" 
        #  - https://non-github.foobar/path/234 => dir[234]


if __name__ == '__main__':
    unittest.main()
