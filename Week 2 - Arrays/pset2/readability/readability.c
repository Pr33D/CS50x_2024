#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

// init functions
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Get user input
    string text = get_string("Text: ");

    float letters = count_letters(text);
    float words = count_words(text);
    float sentences = count_sentences(text);
    
    float l = (letters / words) * 100;
    float s = (sentences / words) * 100;
    int cl_index = round(0.0588 * l - 0.296 * s - 15.8);

    if (cl_index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (cl_index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", cl_index);
    }
}

int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        // Count only letter, no numbers oder other chars
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    int words = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    // Check, if there is a single word, or nothing
    if (strlen(text) != 0)
    {
        words++;
    }
    return words++;
}

int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }
    }
    // Check, if there is only one sentence without punctuation
    if (sentences == 0 && strlen(text) != 0)
    {
        sentences++;
    }
    return sentences;
}
