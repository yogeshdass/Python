def check_prime(number):
    if (int(number)%2):
        print("Not prime")
    else:
        print("Prime")

if __name__ == "__main__":
    check_prime(input("Enter the number : "))