def subtract_numbers(n):
    total = 0
    for i in range(n):
        num = float(input("Enter number {}: ".format(i+1)))
        if i == 0:
            total = num  # Assign the first number as the initial total for subtraction
        else:
            total -= num  # Subtract subsequent numbers from the total
    return total

def main():
    try:
        n = int(input("How many numbers do you want to subtract? "))
        if n < 1:
            print("Please enter a positive integer.")
            return
        result = subtract_numbers(n)
        print("The result of subtracting {} numbers is: {}".format(n, result))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
