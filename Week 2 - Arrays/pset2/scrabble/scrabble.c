#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int gamelogic(string word);

int main(void)
{
    string word_p1 = get_string("Player 1: ");
    string word_p2 = get_string("Player 2: ");
    int p1 = gamelogic(word_p1);
    int p2 = gamelogic(word_p2);

    if (p1 > p2)
    {
        printf("Player 1 wins!\n");
    }
    else if (p1 < p2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
    return 0;
}

int gamelogic(string word)
{
    int scores[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    int score = 0;

    for (int i = 0, len = strlen(word); i < len; i++)
    {
        if isupper(word[i])
        {
            score += scores[word[i] - 'A'];
        }
        else if islower(word[i])
        {
            score += scores[word[i] - 'a'];
        }
    }
    return score;
}