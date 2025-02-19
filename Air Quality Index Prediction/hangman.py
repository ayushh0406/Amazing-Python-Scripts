import random

def hangman():
    words = ['python', 'java', 'kotlin', 'javascript']
    word = random.choice(words)
    guessed_word = ["_"] * len(word)
    attempts = 6
    guessed_letters = set()

    print("H A N G M A N")
    
    while attempts > 0:
        print("\n" + "".join(guessed_word))
        guess = input("Input a letter: ").lower()

        if guess in guessed_letters:
            print("You've already guessed this letter.")
        elif guess in word:
            guessed_letters.add(guess)
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed_word[i] = guess
        else:
            guessed_letters.add(guess)
            attempts -= 1
            print("That letter doesn't appear in the word.")
        
        if "_" not in guessed_word:
            print("You guessed the word! You survived!")
            break
    else:
        print("You lost. The word was:", word)

hangman()
