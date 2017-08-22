import unittest
from esculator.tests.base import snitch
from esculator.tests.npv_blanks import (
    contract_duration_change,
    announcement_date_change,
    payments_percentage_change,
)


class NPVCalculationTest(unittest.TestCase):
    """ NPV Calculation Test
        based on data from https://docs.google.com/spreadsheets/d/1kOz6bxob4Nmb0Es_W0TmbNznoYDcnwAKcSgxfPEXYGQ/edit#gid=1469973930
    """

    test_contract_duration_change = snitch(contract_duration_change)
    test_announcement_date_change = snitch(announcement_date_change)
    test_payments_percentage_change = snitch(payments_percentage_change)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NPVCalculationTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
