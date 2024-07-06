from sys import exit

# CS50 Problem set 1's "credit"


# get_int function (-> no import of cs50 needed)
def get_num(text):
    while True:
        try:
            return int(input(text))
        except:
            print("Please type in a number!")


# check length and luhn's algorithm
def check(num, length):
    # check cardnumber length
    if length < 13 or length > 16:
        print("INVALID")
        exit(f"Invalid card length. Was {length} (Min 13, max 16 digits)")
    # else calc luhn's algorithm
    else:
        sum = 0
        for i in range(length):
            if i % 2 == 0:
                sum += num % 10
            else:
                odd = (num % 10) * 2
                sum += odd // 10 + odd % 10
            num //= 10
        if sum % 10 == 0:
            return True
        else:
            print("INVALID")
            exit("Card number did not match algorithm.")


# identify company
def identify(card, length):
    # str for iteration and back to int for calculation
    dig1 = int(str(card)[0])
    dig2 = int(str(card)[1])

    if length == 15 and dig1 == 3 and (dig2 == 4 or dig2 == 7):
        return "AMEX"
    elif length == 16 and dig1 == 5 and dig2 >= 1 and dig2 <= 5:
        return "MASTERCARD"
    elif (length == 13 or length == 16) and dig1 == 4 and dig2 >= 0 and dig2 <= 9:
        return "VISA"
    else:
        print("INVALID")
        exit("No company matches found.")


# define main function
def main():
    card = get_num("Your Card Number: ")
    length = len(str(card))
    # everything is okay? -> Print company name
    if check(card, length):
        print(identify(card, length))
    # exit() = code 0
    exit()


# call main function if it's not a module
if __name__ == "__main__":
    main()
