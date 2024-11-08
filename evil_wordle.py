"""
Student information for this assignment:

Replace <FULL NAME> with your name.
On my/our honor, <KAVYA CHOWTI> and <ETHAN MIKEL>, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1: kc45736
UT EID 2: etm693
"""

import random
import sys

# ANSI escape codes for text color
# These must be used by wrapping it around a single character string
# for the test cases to work. Please use the color_word function to format
# the feedback properly.

CORRECT_COLOR = "\033[3;1;92m"
WRONG_SPOT_COLOR = "\033[3;1;93m"
NOT_IN_WORD_COLOR = "\033[3;1m"
NO_COLOR = "\033[0m"

# Used for the explanation.
BOLD_COLOR = "\033[1m"

# If you are colorblind for yellow and green, please use these colors instead.
# Uncomment the two lines below. Commenting in and out can be done by
# highlighting the  lines you care about and using:
# on a windows/linux laptop: ctrl + /
# on a mac laptop: cmd + /

# CORRECT_COLOR = "\033[3;1;91m"
# WRONG_SPOT_COLOR = "\033[3;1;94m"

# The total number of letters allowed
NUM_LETTERS = 5

INVALID_INPUT = "Bad input detected. Please try again."


class Keyboard:
    """
    A class representing the on-screen keyboard for a word-guessing game. Each key
    has a color state that indicates feedback based on user guesses. The keyboard
    displays feedback colors for letters guessed in the word.

    Instance Variables:
        rows: A list of strings, each representing a row of letters on the keyboard.
        colors: A dictionary mapping each letter to its current feedback color.
    """

    def __init__(self):
        """
        Initializes the Keyboard object by setting up the rows of keys and initializing
        each key with a default 'NO_COLOR' state.

        pre: The `NO_COLOR` constant is defined and represents the default color for each letter.
        post: `self.colors` is a dictionary with each letter set to `NO_COLOR`.
        """
        self.rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
        self.colors = {letter: NO_COLOR for letter in "qwertyuiopasdfghjklzxcvbnm"}

    # Modify this method. You may delete this comment when you are done.
    def update(self, feedback_colors, guessed_word):
        """
        Updates the color of each letter on the keyboard based on feedback from a guessed word.

        If a letter's feedback color is `CORRECT_COLOR`, the color is updated. If the color
        is `WRONG_SPOT_COLOR`, the color updates only if the keyboard's current color for that
        letter is not `CORRECT_COLOR`. Letters marked with `NO_COLOR` retain that color unless any
        feedback changes it.

        Args:
            feedback_colors: A list/tuple of color codes indicating feedback for each letter.
            guessed_word: The word guessed by the user.

        pre: `feedback_colors` has the same length as `guessed_word`, and each item in
             `feedback_colors` is a valid color constant.
        post: The `colors` dictionary is updated based on feedback, with each letter's color
              reflecting the most accurate feedback from the guesses so far.
        """
        for i, letter in enumerate(guessed_word):
            feedback = feedback_colors[i]

            if feedback == CORRECT_COLOR:
                self.colors[letter] = CORRECT_COLOR
            elif feedback == WRONG_SPOT_COLOR:
                if self.colors[letter] != CORRECT_COLOR:
                    self.colors[letter] = WRONG_SPOT_COLOR
            elif feedback == NOT_IN_WORD_COLOR:
                if self.colors[letter] == NO_COLOR:
                    self.colors[letter] = NOT_IN_WORD_COLOR

    # Modify this method. You may delete this comment when you are done.
    def __str__(self):
        """
        Returns a string representation of the keyboard, showing each letter in its
        corresponding color. Each row of the keyboard is formatted for readability,
        with spacing adjusted for alignment. Color each individual letter using color_word()
        based on the colors in the dictionary.

        The first row has no leading spaces.
        The second keyboard row has 1 leading space.
        The third keyboard row has 3 leading spaces.

        Here is the print format (without the ANSI coloring):

        q w e r t y u i o p
         a s d f g h j k l
           z x c v b n m

        pre: `color_word` function is defined, accepting a color and a letter, and
             returning the letter wrapped in ANSI color codes.
        post: Returns a formatted string with each letter colored according to feedback
              and arranged to match a typical keyboard layout.
        """
        indentations = ["", " ", "   "]

        formatted_rows = []

        for i, row in enumerate(self.rows):
            row_str = indentations[i] + " ".join(
                color_word(self.colors[letter], letter) for letter in row
            )
            formatted_rows.append(row_str)


        return "\n".join(formatted_rows)


class WordFamily:
    """
    A class representing a group or 'family' of words that match a specific pattern
    of color feedback. Each word family has a difficulty level determined by the
    pattern's color difficulty and the number of words in the family.

    Class Variables:
        COLOR_DIFFICULTY: A dictionary mapping color codes to numeric difficulty levels.

    Instance Variables:
        pattern: The pattern of color codes representing the feedback for each letter.
        words: A list of words that match the given color pattern.
        difficulty: An integer representing the cumulative difficulty of this word family.
    """

    COLOR_DIFFICULTY = {CORRECT_COLOR: 0, WRONG_SPOT_COLOR: 1, NOT_IN_WORD_COLOR: 2}

    # Modify this method. You may delete this comment when you are done.
    def __init__(self, feedback_colors, words):
        """
        Initializes the WordFamily instance with a feedback color list and a list of corresponding
        words. The difficulty of the family is calculated based on the color difficulty of each
        character in the pattern.

        Args:
            feedback_colors (str): A string representing feedback colors for a guessed word.
            words (list): A list of words that match the feedback pattern.

        pre: `feedback_colors` consists of valid color codes, and `words` is a list of strings.
        post: `self.difficulty` is set based on the cumulative color difficulty, and
              `self.pattern` and `self.words` are initialized.
        """
        self.feedback_colors = feedback_colors
        self.words = words
        # implement the difficulty calculation here.
        self.difficulty = sum(self.COLOR_DIFFICULTY[color] for color in feedback_colors)
        self.difficulty += len(words)


    # Modify this method. You may delete this comment when you are done.
    def __lt__(self, other):
        """
        Compares this WordFamily object with another by prioritizing a larger
        number of words, higher difficulty, and lexicographical order of the pattern.
        Raises an error if other is not a WordFamily object.

        Args:
            other: Another object, most likely a WordFamily, to compare with.

        Raises:
            A NotImplementedError if other is not a WordFamily object with the message:
            "< operator only valid for WordFamily comparisons."

        Returns:
            bool: True if this instance is 'less than' the other, False otherwise.

        pre: `other` is a WordFamily object.
        post: Returns a boolean result of the comparison, raises NotImplementedError
              if `other` is not a WordFamily instance.
        """
        if not isinstance(other, WordFamily):
            raise NotImplementedError("< operator only valid for WordFamily comparisons.")

        if len(self.words) != len(other.words):
            return len(self.words) > len(other.words)

        if self.difficulty != other.difficulty:
            return self.difficulty > other.difficulty

        return self.feedback_colors < other.feedback_colors

    # DO NOT change this method.
    # You should use this for debugging!
    def __str__(self):
        return (
            f"({len(self.words)}, {self.difficulty}, "
            f"{color_word(self.feedback_colors, ['■'] * 5)})"
        )

    # DO NOT change this method.
    def __repr__(self):
        return str(self)


# DO NOT change this function
def print_explanation(attempts):
    """Prints the 'how to play' instructions on the official website"""

    print("Welcome to Command Line Evil Wordle!")
    print()

    print("".join([BOLD_COLOR + letter + NO_COLOR for letter in "How To Play"]))
    print(f"Guess the secret word in {attempts} tries.")
    print("Each guess must be a valid 5-letter word.")
    print("The color of the letters will change to show")
    print("how close your guess was.")
    print()

    print("Examples:")
    print(CORRECT_COLOR + "w" + NO_COLOR, end="")
    print("".join([NOT_IN_WORD_COLOR + letter + NO_COLOR for letter in "eary"]))
    print(BOLD_COLOR + "w" + NO_COLOR, end=" ")
    print("is in the word and in the correct spot.")

    print(NOT_IN_WORD_COLOR + "p" + NO_COLOR, end="")
    print(WRONG_SPOT_COLOR + "i" + NO_COLOR, end="")
    print("".join([NOT_IN_WORD_COLOR + letter + NO_COLOR for letter in "lls"]))
    print(BOLD_COLOR + "i" + NO_COLOR, end=" ")
    print("is in the word but in the wrong spot.")

    print("".join([NOT_IN_WORD_COLOR + letter + NO_COLOR for letter in "vague"]))
    print(BOLD_COLOR + "u" + NO_COLOR, end=" ")
    print("is not in the word in any spot.")
    print()


# DO NOT change this function
def color_word(colors, word):
    """
    Colors a given word using ANSI formatting then returns it as a new string.

    pre: colors is a list of strings, each representing an ANSI escape color,
        word is a string of equal length to colors.
    post: Returns a string where each character in word is wrapped in the
        corresponding color from colors, followed by NO_COLOR.
    """
    # Guarantee that colors is a list
    # Useful for if colors is a single color
    if isinstance(colors, str):
        colors = [colors]

    assert len(colors) == len(word), "The length of colors and word do not match."

    colored_word = [None] * len(word)
    for i, character in enumerate(word):
        colored_word[i] = f"{colors[i]}{character}{NO_COLOR}"

    return "".join(colored_word)


# DO NOT change this function
def get_attempt_label(attempt_number):
    """
    Generates the label for the given attempt number.

    pre: 1 < attempt_number < 100 and attempt_number is an integer.
    post: returns a string
    """
    if 11 <= attempt_number <= 12:  # Special case for teens (11th, 12th)
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(attempt_number % 10, "th")

    return f"{attempt_number}{suffix}"


# DO NOT change this function
def prepare_game():
    """
    Prepares the game by setting the number of attempts and loading the list of valid words. This
    list of valid words will be used as the initial pool of secret words as well. The function
    accepts an optional command-line argument for attempts and a "debug" mode flag.

    pre: The file valid_guesses.txt exists and contains valid guessable words, one per line. The
        file test_guesses.txt exists and contains secret words, one per line.
    post: Returns a tuple (attempts, valid_words) or raises a ValueError on invalid user attempts:
        The number of attempts the user gets before the game automatically ends.
        valid_words: A list of valid guess words and is the initial pool of secret words.
    """

    valid_words_file_name = "valid_guesses.txt"

    # Must have 1 or 2 arguments
    if len(sys.argv) > 3:
        raise ValueError()
    if sys.argv[-1] == "debug":
        valid_words_file_name = "test_guesses.txt"
        sys.argv.pop()

    if len(sys.argv) == 1:
        attempts = 6
    elif sys.argv[1].isnumeric():
        attempts = int(sys.argv[1])
        if not 1 < attempts < 100:
            raise ValueError()
    # Otherwise, must be bad input and returns None instead
    else:
        raise ValueError()

    # Specify "ascii" as its representation (encoding) since it's required by
    # pylint.
    with open(valid_words_file_name, "r", encoding="ascii") as valid_words:
        valid_words = [word.rstrip() for word in valid_words.readlines()]

    return attempts, valid_words


# Modify this function. You may delete this comment when you are done.
def fast_sort(lst):
    """
    Returns a new list with the same elements as lst sorted in ascending order. You MUST implement
    either merge sort or quick sort. You may not use selection sort, insertion sort, or any other
    sorting method such as the built-in sort() and sorted(). Your sorting function must be able to
    sort lists of WordFamily, integers, floats, and strings. See the test cases for an example.

    pre: lst must be a list

    post: Returns a new sorted list of the items in lst.

    """
    if len(lst) <= 1:
        return lst

    pivot = lst[len(lst) // 2]

    less = [x for x in lst if x < pivot]
    equal = [x for x in lst if x == pivot]
    greater = [x for x in lst if x > pivot]

    return fast_sort(less) + equal + fast_sort(greater)


# Modify this helper function. You may delete this comment when you are done.
def get_feedback_colors(secret_word, guessed_word):
    """
    Processes the guess and generates the colored feedback based on the potential secret word. This
    function should not call color_word and instead returns the list of colors used for the
    corresponding letters.

    This should be extremely similar to what you have from assignment 3: Wordle.

    pre: secret_word must be a string of exactly 5 lowercase alphabetic characters.
         guessed_word must be a string of exactly 5 lowercase alphabetic characters.
    post: the return value is a list where:
          - Correctly guessed letters are marked with CORRECT_COLOR.
          - Correct letters in the wrong position are marked with WRONG_SPOT_COLOR.
          - Letters not in secret_word are marked with NOT_IN_WORD_COLOR. The list will be of
            length 5 with the ANSI coloring in each index as the returned value.
    """
    feedback = [None] * NUM_LETTERS
    secret_word_used = [False] * NUM_LETTERS
    guessed_word_used = [False] * NUM_LETTERS

    # Modify this! This is just starter code.
    for i in range(NUM_LETTERS):
        if guessed_word[i] == secret_word[i]:
            feedback[i] = CORRECT_COLOR
            secret_word_used[i] = True
            guessed_word_used[i] = True

    for i in range(NUM_LETTERS):
        if feedback[i] is None:
            for j in range(NUM_LETTERS):
                if (not secret_word_used[j] and
                guessed_word[i] == secret_word[j] and
                not guessed_word_used[i]):
                    feedback[i] = WRONG_SPOT_COLOR
                    secret_word_used[j] = True
                    guessed_word_used[i] = True
                    break

    for i in range(NUM_LETTERS):
        if feedback[i] is None:
            feedback[i] = NOT_IN_WORD_COLOR

    return feedback


# Modify this function. You may delete this comment when you are done.
def get_feedback(remaining_secret_words, guessed_word):
    """
    Processes the guess and generates the colored feedback based on the hardest word family. Use
    get_feedback_colors to group the words based on their feedback, and then create word families
    based on these groups. The hardest word family is then chosen by sorting the families, where
    the 0th index is now the hardest word family.

    pre: remaining_secret_words is a list of strings.
         guessed_word must be a string of exactly 5 lowercase alphabetic characters.
    post: Returns a tuple (feedback_colors, new_remaining_secret_words) where:
          - feedback_colors: a list of feedback colors (CORRECT_COLOR, WRONG_SPOT_COLOR, or
            NOT_IN_WORD_COLOR) that correspond to the remaining secret words
          - new_remaining_secret_words: the remaining secret words, picked by choosing the hardest
            word family, where the hardest word family is decided by these tiebreakers:
            1. Largest word family (length of the word list)
            2. Difficulty of the feedback
            3. Lexicographical ordering of the feedback (ASCII value comparisons)
    """
    feedback_groups = {}

    for word in remaining_secret_words:
        feedback = tuple(get_feedback_colors(word, guessed_word))
        if feedback not in feedback_groups:
            feedback_groups[feedback] = []
        feedback_groups[feedback].append(word)

    def get_family_difficulty(feedback_pattern):
        return sum([WordFamily.COLOR_DIFFICULTY[color] for color in feedback_pattern])

    hardest_family = None
    hardest_feedback = None

    for feedback, words in feedback_groups.items():
        family_difficulty = get_family_difficulty(feedback)
        if hardest_family is None or (
            len(words) > len(hardest_family) or
            (
                len(words) == len(hardest_family) and
                family_difficulty > get_family_difficulty(hardest_feedback)
            ) or
            (
                len(words) == len(hardest_family) and
                family_difficulty == get_family_difficulty(hardest_feedback) and
                feedback < hardest_feedback
            )
        ):
            hardest_family = words
            hardest_feedback = feedback

    feedback_colors = list(hardest_feedback)
    return feedback_colors, sorted(hardest_family)

# DO NOT modify this function.
def main():
    """
    This function is the main loop for the game. It calls prepare_game() to set up the game,
    then it loops continuously until the game is over.
    """

    try:
        valid = prepare_game()
    except ValueError:
        print(INVALID_INPUT)
        return

    attempts, valid_guesses = valid
    secret_words = valid_guesses

    print_explanation(attempts)

    keyboard = Keyboard()
    attempt = 1

    while attempt <= attempts:
        attempt_number_string = get_attempt_label(attempt)
        prompt = f"Enter your {attempt_number_string} guess: "
        guess = input(prompt)

        # Mimics user typing out the guess when reading input from a file.
        if not sys.stdin.isatty():
            print(guess)

        if guess not in valid_guesses:
            print(INVALID_INPUT)
            continue

        feedback_colors, secret_words = get_feedback(secret_words, guess)
        feedback = color_word(feedback_colors, guess)
        print(" " * (len(prompt) - 1), feedback)

        keyboard.update(feedback_colors, guess)
        print(keyboard)
        print()

        if len(secret_words) == 1 and guess == secret_words[0]:
            print("Congratulations! ", end="")
            print("You guessed the word '" + feedback + "' correctly.")
            break

        attempt += 1

    if attempt > attempts:
        random.seed(0)
        secret_word = random.choice(fast_sort(secret_words))
        formatted_secret_word = "".join(
            [CORRECT_COLOR + c + NO_COLOR for c in secret_word]
        )
        print("Sorry, you've run out of attempts. The correct word was ", end="")

        print("'" + formatted_secret_word + "'.")


# DO NOT change these lines
if __name__ == "__main__":
    main()
