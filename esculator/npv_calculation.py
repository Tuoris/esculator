from datetime import date
from fractions import Fraction


def calculate_contract_duration(
        contract_duration_years,
        contract_duration_days,
        days_per_year):
    '''Calculate contract duration in days'''
    return contract_duration_years * days_per_year + contract_duration_days


def calculate_days_with_cost_reduction(
        announcement_date,
        days_per_year,
        npv_calculation_duration):
    first_year_days = (
        date(announcement_date.year, 12, 31) - announcement_date).days
    return [first_year_days] + [days_per_year] * npv_calculation_duration


def calculate_days_for_discount_rate(days_with_cost_reduction, days_per_year):
    days = days_with_cost_reduction[:-1]
    days.append(days_per_year - days[0])
    return days


def calculate_discount_rate(
        days_for_discount_rate,
        nbu_discount_rate,
        days_per_year):
    '''Calculates discount rate according to the law'''

    return Fraction(str(nbu_discount_rate)) * Fraction(days_for_discount_rate, days_per_year)


def calculate_discount_rates(
        days_for_discount_rates,
        nbu_discount_rate,
        days_per_year):
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
        coefficient = Fraction(coefficient, (Fraction(1) + Fraction(i)))
        discount_coef.append(coefficient)
    return discount_coef


def calculate_days_with_payments(
        contract_duration,
        days_with_cost_reduction,
        days_per_year,
        npv_calculation_duration):

    first_period_duration = min(contract_duration, days_with_cost_reduction[0])
    full_periods_count, last_period_duration = divmod(
        contract_duration - first_period_duration,
        days_per_year,
    )

    # The empty periods count is equal to npv_calculation_duration + 1 without
    # all non empty period count (full, first and last periods)
    empty_periods_count = npv_calculation_duration + 1 - full_periods_count - 2

    days_with_payments = [first_period_duration]
    days_with_payments += [days_per_year] * full_periods_count
    days_with_payments += [last_period_duration]
    days_with_payments += [0] * empty_periods_count

    return days_with_payments


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
        income.append(
            Fraction(str(i)) * Fraction(
                Fraction(str(days_for_discount_rate[count])),
                Fraction(str(days_with_cost_reduction[count]))
            ) - Fraction(str(client_payments[count])))
        count += 1
    return income


def calculate_discounted_income(coef_discount, income_customer):
    count = 0
    discounted_income = []
    for i in coef_discount:
        discounted_income.append(i * income_customer[count])
        count += 1
    return discounted_income


def calculate_amount_perfomance(
        data,
        days_per_year=365,
        npv_calculation_duration=20):

    contract_duration = calculate_contract_duration(data['contractDuration']['years'], data['contractDuration']['days'], days_per_year)
    days_with_cost_reduction = calculate_days_with_cost_reduction(data['announcementDate'], days_per_year, npv_calculation_duration)
    days_for_discount_rate = calculate_days_for_discount_rate(days_with_cost_reduction, days_per_year)
    discount_rates = calculate_discount_rates(days_for_discount_rate, data['NBUdiscountRate'], days_per_year)
    discount_coef = calculate_discount_coef(discount_rates)
    days_with_payments = calculate_days_with_payments(contract_duration,  days_for_discount_rate, days_per_year, npv_calculation_duration)
    payments = calculate_payments(data['yearlyPaymentsPercentage'], data['annualCostsReduction'], days_with_payments,
                                  days_for_discount_rate)
    income = calculate_income(data['annualCostsReduction'], days_for_discount_rate, days_with_cost_reduction, payments)
    discounted_income = calculate_discounted_income(discount_coef, income)
    return sum(discounted_income)


def calculate_amount_contract(
        data,
        days_per_year=365,
        npv_calculation_duration=20):

    contract_duration = calculate_contract_duration(data['contractDuration']['years'], data['contractDuration']['days'], days_per_year)
    days_with_cost_reduction = calculate_days_with_cost_reduction(data['announcementDate'], days_per_year, npv_calculation_duration)
    days_for_discount_rate = calculate_days_for_discount_rate(days_with_cost_reduction, days_per_year)
    days_with_payments = calculate_days_with_payments(contract_duration,  days_for_discount_rate, days_per_year, npv_calculation_duration)
    payments = calculate_payments(data['yearlyPaymentsPercentage'], data['annualCostsReduction'], days_with_payments,
                                  days_for_discount_rate)
    return sum(payments)
