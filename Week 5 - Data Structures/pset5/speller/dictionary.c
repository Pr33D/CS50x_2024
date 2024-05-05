// Implements a dictionary's functionality
#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];
int words = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // hash the word
    int h = hash(word);
    node *cursor = table[h];
    // search table for word
    while (cursor != NULL)
    {
        // compare words
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        // jump to next node for looping through
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Open file failed");
        return false;
    }

    // Scan dictionary
    char buffer[LENGTH + 1];
    while (fscanf(dict, "%s", buffer) != EOF)
    {
        // Space for a new hash table node
        node *new = malloc(sizeof(node));
        if (new == NULL)
        {
            printf("Cannot allocate memory for this word.");
            return false;
        }
        // Copy buffered word into node
        strcpy(new->word, buffer);
        // hash buffered word
        int h = hash(buffer);
        // nodes next pointer = actual list head's pointer
        new->next = table[h];
        // list head = actual node
        table[h] = new;
        // increase wordcounter
        words++;
    }
    // close dictionary
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // return value of words counted via load function
    return words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // iterate over hole hash table
    for (int i = 0; i < N; i++)
    {
        // set actual cursor
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            // bring cursor to next node
            cursor = cursor->next;
            free(temp);
        }

        if (i == N - 1 && cursor == NULL)
        {
            // if cursor is NULL and i on end of table return true
            return true;
        }
    }
    return false;
}
