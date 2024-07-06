import csv
from sys import argv, exit


def main():

    # TODO: Check for command-line usage
    if len(argv) != 3:
        exit("Usage: python dna.py [database].csv [output].txt")
    else:
        if not argv[1].lower().endswith(".csv") or not argv[2].lower().endswith(".txt"):
            exit("Not correct file types")
        else:

            # TODO: Read database file into a variable
            list = []
            with open(f"{argv[1]}", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                sequences = reader.fieldnames[1:]
                for row in reader:
                    list.append(row)

            # TODO: Read DNA sequence file into a variable
            with open(f"{argv[2]}", "r") as dnafile:
                dna = dnafile.read()

            # TODO: Find longest match of each STR in DNA sequence
            matches = {}
            for seq in sequences:
                matches[seq] = longest_match(dna, seq)

            # TODO: Check database for matching profiles
            for person in list:
                personmatches = 0
                for seq in sequences:
                    if int(person[seq]) == matches[seq]:
                        personmatches += 1
                if personmatches == len(sequences):
                    print(f"{person["name"]}")
                    return

        print("No match")
        return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
