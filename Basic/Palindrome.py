def is_palindrome(input_str):
    # Convert input to lowercase and remove non-alphanumeric characters
    input_str = ''.join(char.lower() for char in input_str if char.isalnum())
    
    # Check if the input string is equal to its reverse
    return input_str == input_str[::-1]

def main():
    input_str = input("Enter a string or number to check if it's a palindrome: ")
    if is_palindrome(input_str):
        print("{} is a palindrome.".format(input_str))
    else:
        print("{} is not a palindrome.".format(input_str))

if __name__ == "__main__":
    main()
