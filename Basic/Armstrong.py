def is_armstrong(number):
    # Convert the number to a string to count its digits
    num_str = str(number)
    num_digits = len(num_str)
    
    # Calculate the sum of digits raised to the power of num_digits
    sum_of_digits = sum(int(digit) ** num_digits for digit in num_str)
    
    # Check if the sum equals the original number
    return sum_of_digits == number

def main():
    try:
        number = int(input("Enter a number to check if it's an Armstrong number: "))
        if number < 0:
            print("Please enter a non-negative integer.")
            return
        if is_armstrong(number):
            print("{} is an Armstrong number.".format(number))
        else:
            print("{} is not an Armstrong number.".format(number))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
