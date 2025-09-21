from textblob import TextBlob

while True:
    a = input("Enter the word to be checked: ")
    print("Original text:", a)

    b = TextBlob(a)
    print("Corrected text:", b.correct())

    again = input("Try Again? (1 = Yes, 0 = No): ")
    if again.strip() != "1":
        print("Goodbye!")
        break