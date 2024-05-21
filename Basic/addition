def add_numbers(n):
    total = 0
    for i in range(n):
        num = float(input("Enter number {}: ".format(i+1)))
        total += num
    return total

def main():
    try:
        n = int(input("How many numbers do you want to add? "))
        if n < 1:
            print("Please enter a positive integer.")
            return
        result = add_numbers(n)
        print("The sum of the {} numbers is: {}".format(n, result))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
