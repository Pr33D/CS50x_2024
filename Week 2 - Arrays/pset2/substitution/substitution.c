 #include <cs50.h>
 #include <stdio.h>
 #include <string.h>
 #include <ctype.h>

bool check_key(string key);
void cipher(string plaintext, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Use: ./substitution [key]");
        return 1;
    }

    if (!check_key(argv[1]))
    {
        printf("Invalid key\n");
        return 1;
    }
    string plaintext = get_string("Plaintext:  ");
    printf("ciphertext: ");
    cipher(plaintext, argv[1]);
    return 0;
}

bool check_key(string key)
{
    int len = strlen(key);
    if (len != 26)
    {
        return false;
    }

    for (int i = 0; i < len; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }
        for (int j = 0; j < len; j++)
            {
                if (i != j)
                {
                    if (tolower(key[i]) == tolower(key[j]))
                    {
                        return false;
                    }
                }
            }
    }
    return true;
}

void cipher(string plaintext, string key)
{
    int len = strlen(plaintext);
    string alphabet = "abcdefghijklmnopqrstuvwxyz";
    string ciphertext = "";

    for (int i = 0; i < len; i++)
    {
        if (isalpha(plaintext[i]))
        {
            for (int j = 0, al = strlen(alphabet); j < al; j++)
            {
                    if (tolower(plaintext[i]) == alphabet[j])
                    {
                        char add;
                        if (isupper(plaintext[i]))
                        {
                            add = toupper(key[j]);
                        }
                        else
                        {
                            add = tolower(key[j]);
                        }
                        printf("%c", add);
                    }
            }
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}
