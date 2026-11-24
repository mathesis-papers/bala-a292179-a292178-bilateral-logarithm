import argparse
from fractions import Fraction
import json
from math import comb
from pathlib import Path


def positive(parameter_x, parameter_a, index):
    return (parameter_x - parameter_a ** index) ** index / index


def negative(parameter_x, parameter_a, index):
    return ((-1) ** (index + 1) * parameter_a ** (index * index)
            / (index * (1 - parameter_x * parameter_a ** index) ** index))


def positive_bound(radius_x, radius_a, cutoff):
    ratio = radius_x + radius_a ** (cutoff + 1)
    assert 0 <= ratio < 1
    return ratio ** (cutoff + 1) / ((cutoff + 1) * (1 - ratio))


def negative_bound(radius_x, radius_a, cutoff):
    ratio = radius_a ** (cutoff + 1) / (1 - radius_x * radius_a ** (cutoff + 1))
    assert 0 <= ratio < 1
    return ratio ** (cutoff + 1) / ((cutoff + 1) * (1 - ratio))


def enclosure(lower, upper, places=60):
    endpoint_scale = 10 ** 72
    lower = Fraction(lower.numerator * endpoint_scale // lower.denominator, endpoint_scale)
    upper = Fraction(-((-upper.numerator * endpoint_scale) // upper.denominator), endpoint_scale)
    scale = 10 ** places
    lower_digits = lower.numerator * scale // lower.denominator
    upper_digits = upper.numerator * scale // upper.denominator
    assert lower_digits == upper_digits
    decimal = str(lower_digits).zfill(places + 1)
    return {'lower': str(lower), 'upper': str(upper),
            'decimal_prefix': decimal[:-places] + '.' + decimal[-places:],
            'certified_decimal_places': places}


def outward_upper(value):
    scale = 10 ** 90
    return Fraction(-((-value.numerator * scale) // value.denominator), scale)


def paired_enclosures(parameter_x, parameter_a, positive_cutoff):
    negative_cutoff = 16
    positive_sum = sum((positive(parameter_x, parameter_a, index)
                        for index in range(1, positive_cutoff + 1)), Fraction(0))
    negative_sum = sum((negative(parameter_x, parameter_a, index)
                        for index in range(1, negative_cutoff + 1)), Fraction(0))
    positive_error = positive_bound(parameter_x, parameter_a, positive_cutoff)
    negative_error = negative_bound(parameter_x, parameter_a, negative_cutoff)
    logarithm_sum = sum((parameter_x ** index / index
                         for index in range(1, positive_cutoff + 1)), Fraction(0))
    logarithm_error = (parameter_x ** (positive_cutoff + 1)
                       / ((positive_cutoff + 1) * (1 - parameter_x)))
    assert positive_sum + negative_sum - negative_error <= logarithm_sum + logarithm_error
    assert logarithm_sum <= positive_sum + positive_error + negative_sum + negative_error
    return {
        'positive': enclosure(positive_sum, positive_sum + positive_error),
        'negative': enclosure(negative_sum - negative_error, negative_sum + negative_error),
        'logarithm': enclosure(logarithm_sum, logarithm_sum + logarithm_error),
        'positive_cutoff': positive_cutoff, 'negative_cutoff': negative_cutoff,
        'positive_error_bound': str(outward_upper(positive_error)),
        'negative_error_bound': str(outward_upper(negative_error)),
        'logarithm_error_bound': str(outward_upper(logarithm_error)),
        'interval_compatibility': True}


def root_bracket():
    lower = Fraction(5471802439661624, 10 ** 16)
    upper = Fraction(5471802439661625, 10 ** 16)
    cutoff = 80
    error = Fraction(1, 81 * 2 ** 80)
    lower_sum = sum((positive(Fraction(1, 2), lower, index)
                     for index in range(1, cutoff + 1)), Fraction(0))
    upper_sum = sum((positive(Fraction(1, 2), upper, index)
                     for index in range(1, cutoff + 1)), Fraction(0))
    assert lower_sum > 0 and upper_sum + error < 0
    scale = 10 ** 36
    def rounded_interval(value):
        minimum = Fraction(value.numerator * scale // value.denominator, scale)
        maximum_value = value + error
        maximum = Fraction(-((-maximum_value.numerator * scale)
                             // maximum_value.denominator), scale)
        return {'lower': str(minimum), 'upper': str(maximum)}
    lower_interval = rounded_interval(lower_sum)
    upper_interval = rounded_interval(upper_sum)
    assert Fraction(lower_interval['lower']) > 0
    assert Fraction(upper_interval['upper']) < 0
    return {'bracket_lower': str(lower), 'bracket_upper': str(upper),
            'strict_bracket': True, 'positive_tail_cutoff': cutoff,
            'positive_tail_error_bound': str(error),
            'value_at_lower': lower_interval, 'value_at_upper': upper_interval,
            'decimal_prefix': '0.5471802439661624', 'certified_decimal_places': 16,
            'interval_for_uniqueness': ['1/2', '3/5'],
            'contraction_bound': '363/490', 'averaged_contraction_bound': '1/2'}


def calculate():
    coefficient_checks = 0
    for row_index in range(1, 81):
        for column_index in range(1, row_index + 1):
            assert column_index * comb(row_index, column_index) == (
                row_index * comb(row_index - 1, column_index - 1))
            coefficient_checks += 1
    parameters = [(Fraction(0), Fraction(0)),
                  (Fraction(1, 2), Fraction(0)),
                  (Fraction(1, 2), Fraction(1, 2)),
                  (Fraction(-2, 3), Fraction(3, 4)),
                  (Fraction(3, 4), Fraction(-2, 3)),
                  (Fraction(-3, 4), Fraction(-3, 4))]
    row_checks = 0
    negative_checks = 0
    zero_checks = 0
    for parameter_x, parameter_a in parameters:
        for index in range(1, 25):
            correction = sum(((-1) ** column_index * comb(index, column_index)
                              * parameter_a ** (index * column_index)
                              * parameter_x ** (index - column_index) / index
                              for column_index in range(1, index + 1)), Fraction(0))
            assert positive(parameter_x, parameter_a, index) - parameter_x ** index / index == correction
            row_checks += 1
            if parameter_a:
                ordinary_negative = (parameter_x - parameter_a ** (-index)) ** (-index) / (-index)
                assert ordinary_negative == negative(parameter_x, parameter_a, index)
                negative_checks += 1
            else:
                assert negative(parameter_x, parameter_a, index) == 0
                assert positive(parameter_x, parameter_a, index) == parameter_x ** index / index
                zero_checks += 1
    boundary_row_checks = 0
    boundary_negative_checks = 0
    boundary_parameters = [Fraction(0), Fraction(1, 2), Fraction(-1, 2),
                           Fraction(3, 4), Fraction(-3, 4)]
    for boundary_x in [Fraction(-1), Fraction(1)]:
        for boundary_a in boundary_parameters:
            radius = abs(boundary_a)
            for index in range(1, 41):
                row_norm = sum((comb(index, column_index) * radius ** (index * column_index)
                                / index for column_index in range(1, index + 1)), Fraction(0))
                difference = positive(boundary_x, boundary_a, index) - boundary_x ** index / index
                assert abs(difference) <= row_norm
                assert row_norm == ((1 + radius ** index) ** index - 1) / index
                assert row_norm <= radius ** index * (1 + radius ** index) ** (index - 1)
                boundary_row_checks += 1
                if boundary_a:
                    ordinary_negative = (boundary_x - boundary_a ** (-index)) ** (-index) / (-index)
                    assert ordinary_negative == negative(boundary_x, boundary_a, index)
                    boundary_negative_checks += 1
    half = Fraction(1, 2)
    positive_cutoff = 220
    negative_cutoff = 16
    positive_sum = sum((positive(half, half, index)
                        for index in range(1, positive_cutoff + 1)), Fraction(0))
    negative_sum = sum((negative(half, half, index)
                        for index in range(1, negative_cutoff + 1)), Fraction(0))
    positive_error = positive_bound(half, half, positive_cutoff)
    negative_error = negative_bound(half, half, negative_cutoff)
    log_sum = sum((half ** index / index
                  for index in range(1, positive_cutoff + 1)), Fraction(0))
    log_error = half ** (positive_cutoff + 1) / ((positive_cutoff + 1) * (1 - half))
    positive_interval = enclosure(positive_sum, positive_sum + positive_error)
    negative_interval = enclosure(negative_sum - negative_error, negative_sum + negative_error)
    logarithm_interval = enclosure(log_sum, log_sum + log_error)
    assert positive_sum + negative_sum - negative_error <= log_sum + log_error
    assert log_sum <= positive_sum + positive_error + negative_sum + negative_error
    assert positive_interval['decimal_prefix'] == '0.066511041770508969698008004177213908831416795925918353857547'
    assert negative_interval['decimal_prefix'] == '0.626636138789436339719224117280962659244083338434336900263132'
    first_pair = paired_enclosures(Fraction(1, 2), Fraction(1, 3), 220)
    second_pair = paired_enclosures(Fraction(2, 3), Fraction(1, 2), 400)
    off_diagonal_checks = 0
    for index in range(1, 25):
        assert positive(Fraction(1, 2), Fraction(1, 3), index) == Fraction(
            (3 ** index - 2) ** index, index * 2 ** index * 3 ** (index * index))
        assert negative(Fraction(1, 2), Fraction(1, 3), index) == Fraction(
            (-1) ** (index + 1) * 2 ** index, index * (2 * 3 ** index - 1) ** index)
        assert positive(Fraction(2, 3), Fraction(1, 2), index) == Fraction(
            (2 ** (index + 1) - 3) ** index, index * 3 ** index * 2 ** (index * index))
        assert negative(Fraction(2, 3), Fraction(1, 2), index) == Fraction(
            (-1) ** (index + 1) * 3 ** index,
            index * 2 ** index * (3 * 2 ** (index - 1) - 1) ** index)
        off_diagonal_checks += 4
    return {
        'arithmetic': 'Exact integers and fractions; outward rational bounds; decimal prefixes truncated.',
        'scope': 'Finite coefficient and term identities, and certified decimal enclosures; infinite identities have written proofs.',
        'binomial_coefficient_identity': {'rows': [1, 80], 'checks': coefficient_checks},
        'binomial_row_identities': {'indices': [1, 24], 'parameter_pairs': len(parameters), 'checks': row_checks},
        'ordinary_negative_term_identities': {'indices': [1, 24], 'checks': negative_checks},
        'regular_zero_values': {'indices': [1, 24], 'checks': zero_checks},
        'boundary_row_estimates': {'indices': [1, 40], 'parameter_pairs': 10,
                                   'checks': boundary_row_checks},
        'boundary_negative_term_identities': {'indices': [1, 40], 'parameter_pairs': 8,
                                               'checks': boundary_negative_checks},
        'positive_tail_cutoff': positive_cutoff,
        'negative_tail_cutoff': negative_cutoff,
        'positive_tail_error_bound': str(outward_upper(positive_error)),
        'negative_tail_error_bound': str(outward_upper(negative_error)),
        'logarithm_tail_error_bound': str(outward_upper(log_error)),
        'A292179': positive_interval, 'A292178': negative_interval,
        'log_2': logarithm_interval,
        'constant_relation_interval_compatibility': True,
        'A293381': first_pair['positive'], 'A293382': first_pair['negative'],
        'A293383': second_pair['positive'], 'A293384': second_pair['negative'],
        'log_3': second_pair['logarithm'],
        'off_diagonal_enclosures': {
            'A293381_A293382': {key: value for key, value in first_pair.items()
                                if key not in ['positive', 'negative', 'logarithm']},
            'A293383_A293384': {key: value for key, value in second_pair.items()
                                if key not in ['positive', 'negative', 'logarithm']}},
        'off_diagonal_term_identities': {'indices': [1, 24], 'checks': off_diagonal_checks},
        'A293380_root': root_bracket(),
        'result': 'All finite identities and rational enclosure checks passed.'}


def main():
    parser = argparse.ArgumentParser(description='Exact finite checks and rational enclosures for the bilateral logarithm identity.')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    output = json.dumps(calculate(), indent=2) + '\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
