#include <stdio.h>
#include <cs50.h>

bool check_log(long cc);
int check_length(long cc);
int check_front(long cc);
void identify(long cc, int length, int front_digits);

int main(void)
{
    // request input
    long cc = get_long("Your CC-Number: ");

    // call functions, if Luhn's Algorithm equals true
    if (check_log(cc))
    {
        int length = check_length(cc);
        int front = check_front(cc);
        identify(cc, length, front);
    }
    else
    {
        printf("INVALID\n");
/*         printf("Invalid card number.\n"); */
    }
}

// Check Luhn's Algorithm
bool check_log(long cc)
{
    int sum = 0;
    bool straight_pos = false;
    while (cc > 0)
    {
        int last_digit = cc % 10;

        if (straight_pos == true)
        {
            if (last_digit >= 5)
            {
                int digits = last_digit * 2;
                while (digits > 0)
                {
                    int last = digits % 10;
                    sum += last;
                    digits = digits / 10;
                }
            }
            else
            {
                sum += last_digit * 2;
            }
        }
        else
        {
            sum += last_digit;
        }
        straight_pos = !straight_pos;
        cc = cc / 10;
    }

    if (sum % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Check Length of inserted Card Number
int check_length(long cc)
{
    int length = 0;
    while (cc > 0)
    {
        length++;
        cc = cc / 10;
    }
    return length;
}

// Check the first 2 digits
int check_front(long cc)
{
    int front_digits;
    while (cc > 0)
    {
        if (cc < 100 && cc > 10)
        {
            front_digits = cc;
        }
        cc = cc / 10;
    }
    return front_digits;
}

// Combine everything & give feedback
void identify(long cc, int length, int front_digits)
{
    if (length == 15 && (front_digits == 34 || front_digits == 37))
    {
        printf("AMEX\n");
    }
    else if (length == 16 && front_digits >= 51 && front_digits <= 55)
    {
        printf("MASTERCARD\n");
    }
    else if ((length == 13 || length == 16) && front_digits >= 40 && front_digits <= 49)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
