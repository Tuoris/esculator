from datetime import date
from fractions import Fraction
from esculator.constants import DAYS_PER_YEAR, NPV_CALCULATION_DURATION


def calculate_contract_duration(
        contract_duration_years,
        contract_duration_days,
        days_per_year=DAYS_PER_YEAR):
    '''Calculate contract duration in days'''
    return contract_duration_years * days_per_year + contract_duration_days


def calculate_days_with_cost_reduction(
        announcement_date,
        days_per_year=DAYS_PER_YEAR,
        ):
    first_year_days = (date(announcement_date.year, 12, 31) - announcement_date).days
    return [first_year_days] + [days_per_year] * NPV_CALCULATION_DURATION


def calculate_days_for_discount_rate(days_with_cost_reduction):
    days = days_with_cost_reduction[:-1]
    days.append(DAYS_PER_YEAR - days[0])
    return days


def calculate_discount_rate(
        days_for_discount_rate,
        nbu_discount_rate,
        days_per_year=DAYS_PER_YEAR):
    '''Calculates discount rate according to the law'''

    return Fraction(str(nbu_discount_rate)) * Fraction(days_for_discount_rate, days_per_year)


def calculate_discount_rates(
        days_for_discount_rates,
        nbu_discount_rate,
        days_per_year=DAYS_PER_YEAR):
    '''Calculates discount rates from days_for_discount_rates list'''

    return [
        calculate_discount_rate(
            days_for_discount_rate,
            nbu_discount_rate,
            days_per_year,
        ) for days_for_discount_rate in days_for_discount_rates
    ]


def calculate_discount_coef(discount_rates):
    discount_coef = []
    coefficient = Fraction(1)
    for i in discount_rates:
        coefficient = Fraction(coefficient, (Fraction(1)+Fraction(i)))
        discount_coef.append(coefficient)
    return discount_coef


def calculate_days_with_payments(
        contract_duration,
        days_with_cost_reduction,
        days_per_year=DAYS_PER_YEAR):
    days = [min(contract_duration, days_with_cost_reduction[0])]
    contract_duration -= days[0]
    days += [days_per_year] * (contract_duration // days_per_year) + [contract_duration % days_per_year]
    if len(days) < NPV_CALCULATION_DURATION + 1:
        days += [0] * (NPV_CALCULATION_DURATION + 1 - len(days))
    return days


def calculate_payment(
        yearly_payments_percentage,
        client_cost_reduction,
        days_with_payments,
        days_for_discount_rate):
    '''Calculates client payment to a participant'''

    if days_with_payments > 0:
        # Transormation Fraction(str(float)) is done because of its
        # better precision than Fraction(float).
        #
        # For example:
        # >>> Fraction(str(0.2))
        # Fraction(1, 5)
        # >>> Fraction(0.2)
        # Fraction(3602879701896397, 18014398509481984)

        yearly_payments_percentage = Fraction(
            str(yearly_payments_percentage)
        )
        client_cost_reduction = Fraction(str(client_cost_reduction))

        return (yearly_payments_percentage * client_cost_reduction *
                Fraction(days_with_payments, days_for_discount_rate))
    return 0


def calculate_payments(
        yearly_payments_percentage,
        client_cost_reductions,
        days_with_payments,
        days_for_discount_rate):
    '''Calculates client payments to a participant'''

    payments = []

    for i, _ in enumerate(client_cost_reductions):
        payments.append(
            calculate_payment(
                yearly_payments_percentage,
                client_cost_reductions[i],
                days_with_payments[i],
                days_for_discount_rate[i],
            )
        )

    return payments


def calculate_income(client_cost_reductions, days_for_discount_rate, days_with_cost_reduction, client_payments):
    count = 0
    income = []
    for i in client_cost_reductions:
        income.append(Fraction(str(i)) * Fraction(Fraction(str(days_for_discount_rate[count])),
                      Fraction(str(days_with_cost_reduction[count]))) - Fraction(str(client_payments[count])))
        count += 1
    return income


def calculate_discounted_income(coef_discount, income_customer):
    count = 0
    discounted_income = []
    for i in coef_discount:
        discounted_income.append(i*income_customer[count])
        count += 1
    return discounted_income


def calculate_sum(data):
    return sum(data)


def calculate_amount_perfomance(data):
    contract_duration = calculate_contract_duration(data['contractDuration']['years'], data['contractDuration']['days'])
    days_with_cost_reduction = calculate_days_with_cost_reduction(data['announcementDate'])
    days_for_discount_rate = calculate_days_for_discount_rate(days_with_cost_reduction)
    discount_rates = calculate_discount_rates(days_for_discount_rate, data['NBUdiscountRate'])
    discount_coef = calculate_discount_coef(discount_rates)
    days_with_payments = calculate_days_with_payments(contract_duration,  days_for_discount_rate)
    payments = calculate_payments(data['yearlyPaymentsPercentage'], data['annualCostsReduction'], days_with_payments,
                                  days_for_discount_rate)
    income = calculate_income(data['annualCostsReduction'], days_for_discount_rate, days_with_cost_reduction, payments)
    discounted_income = calculate_discounted_income(discount_coef, income)
    npv = calculate_sum(discounted_income)
    return float(npv)


def calculate_amount_contract(data):
    contract_duration = calculate_contract_duration(data['contractDuration']['years'], data['contractDuration']['days'])
    days_with_cost_reduction = calculate_days_with_cost_reduction(data['announcementDate'])
    days_for_discount_rate = calculate_days_for_discount_rate(days_with_cost_reduction)
    days_with_payments = calculate_days_with_payments(contract_duration,  days_for_discount_rate)
    payments = calculate_payments(data['yearlyPaymentsPercentage'], data['annualCostsReduction'], days_with_payments,
                                  days_for_discount_rate)
    tcp = calculate_sum(payments)
    return float(tcp)
