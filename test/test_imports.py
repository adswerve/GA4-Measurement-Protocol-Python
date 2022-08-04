import unittest
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestImports(unittest.TestCase):
    def test_import_ga4mp(self):
        test_pass = None
        try:
            from ga4mp import Ga4mp
            from ga4mp.ga4mp import Ga4mp

            test_pass = True
        except:
            test_pass = False
        self.assertEqual(test_pass, True)


if __name__ == "__main__":
    unittest.main()