#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // take average of red, green and blue
            int bw =
                round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            // update pixel values
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = bw;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // initialize new colors with given formula, rounded to integer
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen +
                                 .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen +
                                   .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen +
                                  .131 * image[i][j].rgbtBlue);

            // Be sure not to exceed 255 per color
            if (sepiaRed > 255)
                sepiaRed = 255;
            if (sepiaGreen > 255)
                sepiaGreen = 255;
            if (sepiaBlue > 255)
                sepiaBlue = 255;

            // update pixel color values
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        // if width is even
        if (width % 2 == 0)
        {
            for (int j = 0, scan = width / 2; j < scan; j++)
            {
                // swap
                RGBTRIPLE temp = image[i][j];
                image[i][j] = image[i][width - (j + 1)];
                image[i][width - (j + 1)] = temp;
            }
        }
        // if width is odd
        else
        {
            for (int j = 0, scan = (width - 1) / 2; j < scan; j++)
            {
                // swap
                RGBTRIPLE temp = image[i][j];
                image[i][j] = image[i][width - (j + 1)];
                image[i][width - (j + 1)] = temp;
            }
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // copy image array
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // change colors
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // initialize variables for math
            double pixels = 0;
            int avgRed, avgGreen, avgBlue;
            avgRed = avgGreen = avgBlue = 0;

            // count each pixel in i-1, i and i+1, on pos j-1, j and j+1
            // if exists and safe color values
            for (int k = (i - 1); k < (i + 2); k++)
            {
                for (int l = (j - 1); l < (j + 2); l++)
                {
                    if (k >= 0 && k < height && l >= 0 && l < width)
                    {
                        avgRed += copy[k][l].rgbtRed;
                        avgGreen += copy[k][l].rgbtGreen;
                        avgBlue += copy[k][l].rgbtBlue;
                        pixels++;
                    }
                }
            }
            // update original image
            image[i][j].rgbtRed = round(avgRed / pixels);
            image[i][j].rgbtGreen = round(avgGreen / pixels);
            image[i][j].rgbtBlue = round(avgBlue / pixels);
        }
    }
}
