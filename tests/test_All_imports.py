import unittest
import logging
import os, sys

sys.path.append(
    os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
)

class TestAllImports(unittest.TestCase):
    def test_import_GtagMP(self):
        test_pass = None
        
        try:
            from ga4mp.ga4mp import GtagMP
            test_pass = True
        except:
            test_pass = False

        self.assertEqual(test_pass, True)

    def test_import_FirebaseMP(self):
        test_pass = None
        
        try:
            from ga4mp.ga4mp import FirebaseMP
            test_pass = True
        except:
            test_pass = False

        self.assertEqual(test_pass, True)

if __name__ == "__main__":
    unittest.main()