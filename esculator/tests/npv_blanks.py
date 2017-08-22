from copy import deepcopy
from esculator.npv_calculation import (
    calculate_amount_perfomance,
    calculate_amount_contract,
)
from esculator.tests.npv_test_data import (
    CONTRACT_DURATION_CHANGING,
    ANNOUNCEMENT_DATE_CHANGING,
    PAYMENTS_PERCENTAGE_CHANGING,
)


def _str(number, max_length=15):
    number_str = '{:.{}f}'.format(number, max_length)
    integer_part, _ = number_str.split('.')
    precision = max_length - len(integer_part)
    return '{:.{}f}'.format(number, precision)


def contract_duration_change(self):
    data = deepcopy(CONTRACT_DURATION_CHANGING)
    contract_durations = data.pop('contractDuration')

    for i, contract_duration in enumerate(contract_durations):
        data['contractDuration'] = contract_duration

        amount_perfomance = calculate_amount_perfomance(data)
        self.assertEqual(
            _str(amount_perfomance),
            _str(CONTRACT_DURATION_CHANGING
                 ['calculated'][i]['amountPerformance'])
        )

        amount_contract = calculate_amount_contract(data)
        self.assertEqual(
            _str(amount_contract),
            _str(CONTRACT_DURATION_CHANGING
                 ['calculated'][i]['amountContract'])
        )


def announcement_date_change(self):
    data = deepcopy(ANNOUNCEMENT_DATE_CHANGING)
    announcement_dates = data.pop('announcementDate')

    for i, announcement_date in enumerate(announcement_dates):
        data['announcementDate'] = announcement_date

        amount_perfomance = calculate_amount_perfomance(data)
        self.assertEqual(
            _str(amount_perfomance),
            _str(ANNOUNCEMENT_DATE_CHANGING
                 ['calculated'][i]['amountPerformance'])
        )
        amount_contract = calculate_amount_contract(data)
        self.assertEqual(
            _str(amount_contract),
            _str(ANNOUNCEMENT_DATE_CHANGING
                 ['calculated'][i]['amountContract'])
        )


def payments_percentage_change(self):
    data = deepcopy(PAYMENTS_PERCENTAGE_CHANGING)
    payments_percentages = data.pop('yearlyPaymentsPercentage')

    for i, payments_percentage in enumerate(payments_percentages):
        data['yearlyPaymentsPercentage'] = payments_percentage

        amount_perfomance = calculate_amount_perfomance(data)
        self.assertEqual(
            _str(amount_perfomance),
            _str(PAYMENTS_PERCENTAGE_CHANGING
                 ['calculated'][i]['amountPerformance'])
        )

        amount_contract = calculate_amount_contract(data)
        self.assertEqual(
            _str(amount_contract),
            _str(PAYMENTS_PERCENTAGE_CHANGING
                 ['calculated'][i]['amountContract'])
        )
