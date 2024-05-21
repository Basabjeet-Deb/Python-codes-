def fibonacci(n):
    fib_sequence = [0, 1]  # Initialize Fibonacci sequence with first two terms
    while len(fib_sequence) < n:
        next_term = fib_sequence[-1] + fib_sequence[-2]  # Calculate the next Fibonacci term
        fib_sequence.append(next_term)
    return fib_sequence[:n]  # Return the Fibonacci sequence up to the nth term

def main():
    try:
        n = int(input("Enter the number of Fibonacci terms: "))
        if n <= 0:
            print("Please enter a positive integer.")
            return
        result = fibonacci(n)
        print("The first {} Fibonacci numbers are: {}".format(n, result))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
