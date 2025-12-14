# Function to calculate the sum of calibration values from a file
def sum_calibration_values_from_file(file_path):
    total_sum = 0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Find the first digit
                for char in line:
                    if char.isdigit():
                        first_digit = int(char)
                        break
                else:
                    # No digit found, set to 0
                    first_digit = 0

                # Find the last digit
                for char in reversed(line):
                    if char.isdigit():
                        last_digit = int(char)
                        break
                else:
                    # No digit found, set to 0
                    last_digit = 0

                # Combine the digits to form a two-digit number
                calibration_value = first_digit * 10 + last_digit

                # Add the calibration value to the total sum
                total_sum += calibration_value

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

    return total_sum

# Specify the path to your calibration data file
file_path = 'AoC_Day01.txt'

# Calculate and print the sum of calibration values from the file
result = sum_calibration_values_from_file(file_path)

if result is not None:
    print(result)
