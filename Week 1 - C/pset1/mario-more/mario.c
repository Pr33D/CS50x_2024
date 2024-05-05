#include <cs50.h>
#include <stdio.h>

void printp(int height);

int main(void)
{
    int h;
    do
    {
        h = get_int("Height of pyramid: ");
    }
    while (h < 1 || h > 8);
    printp(h);
}

void printp(int height)
{
    for (int i = 0; i < height; i++)
    {
        int hashes = i + 1;
        int spaces = height - hashes;

        for (int j = 0; j < spaces; j++)
        {
            printf(" ");
        }
        for (int k = 0; k < hashes; k++)
        {
            printf("#");
        }
        printf("  ");
        for (int l = 0; l < hashes; l++)
        {
            printf("#");
        }
        printf("\n");
    }
}
