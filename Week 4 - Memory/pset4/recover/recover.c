#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK 512

int main(int argc, char *argv[])
{
    // check number of arguments
    if (argc != 2)
    {
        printf("Usage: ./recover <card.raw>\n");
        return 1;
    }
    // open input file
    char *image = argv[1];
    FILE *input = fopen(image, "r");
    // set output to NULL
    FILE *output = NULL;
    if (input == NULL)
    {
        printf("File could not be opened\n");
        return 1;
    }

    uint8_t buffer[BLOCK];
    int counter = 0;
    char *imgName = malloc(8);

    // Read block = True?
    while (fread(buffer, BLOCK, 1, input) == 1)
    {
        // find signature for jpg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && buffer[3] >= 0xe0 &&
            buffer[3] <= 0xef)
        {
            // first, check if file already exists & close connection
            if (output != NULL)
            {
                fclose(output);
            }
            // init file
            sprintf(imgName, "%03d.jpg", counter);
            output = fopen(imgName, "w");
            // check output
            if (output == NULL)
            {
                printf("Could not create file");
                return 1;
            }
            // increase counter
            counter++;
        }
        // Write to new file
        if (output != NULL)
        {
            fwrite(buffer, BLOCK, 1, output);
        }
    }
    // free allocated memory & close file connections
    free(imgName);
    fclose(output);
    fclose(input);
}
