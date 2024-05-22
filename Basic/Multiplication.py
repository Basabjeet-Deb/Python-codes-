def multiply_numbers(n):
    product = 1  # Initialize product to 1 for multiplication
    for i in range(n):
        num = float(input("Enter number {}: ".format(i+1)))
        product *= num  # Multiply each number with the product
    return product

def main():
    try:
        n = int(input("How many numbers do you want to multiply? "))
        if n < 1:
            print("Please enter a positive integer.")
            return
        result = multiply_numbers(n)
        print("The product of {} numbers is: {}".format(n, result))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
