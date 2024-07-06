import re


def get_str(text):
    while True:
        try:
            return input(text)
        except:
            print("Please enter text")


# Count letters, and only lettersa
def count_letters(txt):
    count = 0
    for letter in txt:
        if letter.isalpha():
            count += 1
    return count


# Count all words
def count_words(txt):
    return len(txt.split())


# Count sentences via re.split / txt.count(". ") ...
def count_sentences(txt):
    return len(re.split(r'[.!?]+', txt)) - 1


def main():
    while True:
        txt = get_str("Text: ")
        if len(txt) > 0:
            break
        else:
            print("Please type in some text")
            continue

    letters = count_letters(txt)
    words = count_words(txt)
    sentences = count_sentences(txt)

    l = (letters / words) * 100
    s = (sentences / words) * 100
    cl = round(0.0588 * l - 0.296 * s - 15.8)

    if cl < 1:
        print("Before Grade 1")
    elif cl > 16:
        print("Grade 16+")
    else:
        print(f"Grade {cl}")


if __name__ == "__main__":
    main()
