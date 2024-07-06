# own get_int function with endless loop
# alternatively use from cs50 import get_int at the top
def get_int(text):
    while True:
        try:
            return int(input(text))
        except:
            print("This is not an integer.")


def main():
    # loop for int in range
    while True:
        height = get_int("Height (1-8): ")

        # range of 1 - 9 (9 not included)
        if height in range(1, 9):
            for i in range(height):
                # print out pyramid
                print(" " * ((height - 1) - i), end="")
                print("#" * (i + 1), end="")
                print("  ", end="")
                print("#" * (i + 1))
            break
        else:
            print("Type in a number between 1 and 8")


# call main function
if __name__ == "__main__":
    main()
