def divide_numbers(n):
    quotient = None
    for i in range(n):
        num = float(input("Enter number {}: ".format(i+1)))
        if i == 0:
            quotient = num  # Assign the first number as the initial quotient
        else:
            if num == 0:
                print("Error: Cannot divide by zero.")
                return None
            quotient /= num  # Divide the current quotient by the next number
    return quotient

def main():
    try:
        n = int(input("How many numbers do you want to divide? "))
        if n < 1:
            print("Please enter a positive integer.")
            return
        result = divide_numbers(n)
        if result is not None:
            print("The result of dividing {} numbers is: {}".format(n, result))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
