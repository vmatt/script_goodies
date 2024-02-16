import math

# Function to count the number of divisors of a number
def count_divisors(n):
    count = 0
    sqrt_n = int(math.sqrt(n))
    for i in range(1, sqrt_n + 1):
        if n % i == 0:
            count += 2 if n // i != i else 1
    return count
# Here's how the function works step by step:
#
# Initialize a variable count to zero. This variable will keep track of the number of divisors found.
#
# Compute the square root of n and store it in a variable sqrt_n.
# This is because we only need to check for divisors up to the square root of n. Any factor larger than the square root of n will be paired with a factor smaller than the square root.
#
# Use a loop to iterate over all integers i from 1 up to and including sqrt_n. For each i:
#
# Check if i is a divisor of n by performing the modulus operation n % i. If the result is zero, it means i is a divisor.
#
# If i is a divisor, there is another divisor n // i which, when multiplied by i, gives n.
#
# Increase the count by 2 to account for both i and n // i as divisors of n.
#
# However, if i is such that i and n // i are the same (which can only happen if i is the square root of a perfect square n), we only want to count it once. So in this special case, we increase the count by 1 instead of 2.
#
# After the loop finishes, return the count variable, which now contains the total number of divisors of n.
# Input parsing
elements = input()
elements_arr = elements.split(" ")

if len(elements_arr) != 2:
    raise Exception("Input must consist of exactly 2 numbers")

# Convert input to integers and check constraints
int_elements_arr = []
for x in elements_arr:
    numeric_x = int(x)
    if numeric_x < 1 or numeric_x > pow(10, 12):
        raise ValueError("Any number must be between 1 and 10^12")
    int_elements_arr.append(numeric_x)

x, y = int_elements_arr

# Find the GCD of x and y
gcd_value = math.gcd(x, y)

# Count the number of divisors of the GCD
common_factors_count = count_divisors(gcd_value)

# Output the number of common factors
print(common_factors_count)
