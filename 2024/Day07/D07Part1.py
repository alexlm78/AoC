from itertools import product


def evaluate_expression(numbers, operators):
    result = numbers[0]
    for i in range(len(operators)):
        if operators[i] == '+':
            result += numbers[i + 1]
        elif operators[i] == '*':
            result *= numbers[i + 1]
    return result


def is_valid_equation(test_value, numbers):
    operator_combinations = product('+-*', repeat=len(numbers) - 1)
    for operators in operator_combinations:
        if evaluate_expression(numbers, operators) == test_value:
            return True
    return False


def total_calibration_result(input_data):
    total_result = 0
    for line in input_data.strip().split('\n'):
        test_value, numbers = line.split(':')
        test_value = int(test_value)
        numbers = list(map(int, numbers.split()))
        if is_valid_equation(test_value, numbers):
            total_result += test_value
    return total_result


input_data = open("day07.txt", "r", encoding="utf-8").read()

# Example input
# input_data = """
# 190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20
# """

# Calculate the total calibration result
result = total_calibration_result(input_data)
print(f"Total calibration result: {result}")
