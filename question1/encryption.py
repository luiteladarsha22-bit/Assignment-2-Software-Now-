import os


# Constants
INPUT_FILE = "raw_text.txt"
ENCRYPTED_FILE = "encrypted_text.txt"
DECRYPTED_FILE = "decrypted_text.txt"
ALPHABET_SIZE = 26


# Utility Functions
def shift_forward(char, shift, base):
    return chr((ord(char) - ord(base) + shift) % ALPHABET_SIZE + ord(base))


def shift_backward(char, shift, base):
    return chr((ord(char) - ord(base) - shift) % ALPHABET_SIZE + ord(base))



# NOTE FOR LECTURER
# The given encryption rules divide characters into ranges (a-m, n-z, etc.)
# and apply different transformations.
#
# However, after encryption, characters may move across these ranges.
# This creates ambiguity during decryption because:
#
#   Different original characters can produce the same encrypted character.
#
# Example:
#   'm' → 'o' (forward shift)
#   'r' → 'o' (backward shift)
#
# Both result in 'o', so during decryption we cannot uniquely determine
# the original character.
#
# Therefore, this implementation applies the reverse rules based on the
# encrypted character's range, but perfect reconstruction of the original
# text is NOT guaranteed for all inputs.
#
# A fully reliable solution would require storing additional metadata
# (e.g., tags -> to store the rules information used during encryption), which is not used here to strictly follow the assignment rules.
# (but i have implemented it in the other file named encryptionWithTags.py)


# Validation Functions
def validate_input():
    while True:
        try:
            shift1 = int(input("Enter shift1 (non-negative integer): "))
            shift2 = int(input("Enter shift2 (non-negative integer): "))

            if shift1 < 0 or shift2 < 0:
                raise ValueError("Shift values must be non-negative.")

            return shift1, shift2

        except ValueError :
            print("Invalid input!, Please try again.\n")

def check_input_file():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: '{INPUT_FILE}' not found.")
        return False
    return True



# Encryption
def encrypt_file(shift1, shift2):
    try:
        with open(INPUT_FILE, "r") as infile, open(ENCRYPTED_FILE, "w") as outfile:
            for line in infile:
                encrypted_line = ""

                for ch in line:
                    if ch.islower():
                        if 'a' <= ch <= 'm':
                            shift = shift1 * shift2
                            encrypted_line += shift_forward(ch, shift, 'a')
                        else:
                            shift = shift1 + shift2
                            encrypted_line += shift_backward(ch, shift, 'a')

                    elif ch.isupper():
                        if 'A' <= ch <= 'M':
                            encrypted_line += shift_backward(ch, shift1, 'A')
                        else:
                            shift = shift2 ** 2
                            encrypted_line += shift_forward(ch, shift, 'A')

                    else:
                        encrypted_line += ch

                outfile.write(encrypted_line)

    except Exception as e:
        print(f"Encryption error: {e}")


# Decryption
def decrypt_file(shift1, shift2):
    try:
        with open(ENCRYPTED_FILE, "r") as infile, open(DECRYPTED_FILE, "w") as outfile:
            for line in infile:
                decrypted_line = ""

                for ch in line:
                    if ch.islower():
                        if 'a' <= ch <= 'm':
                            shift = shift1 * shift2
                            decrypted_line += shift_backward(ch, shift, 'a')
                        else:
                            shift = shift1 + shift2
                            decrypted_line += shift_forward(ch, shift, 'a')

                    elif ch.isupper():
                        if 'A' <= ch <= 'M':
                            decrypted_line += shift_forward(ch, shift1, 'A')
                        else:
                            shift = shift2 ** 2
                            decrypted_line += shift_backward(ch, shift, 'A')

                    else:
                        decrypted_line += ch

                outfile.write(decrypted_line)

    except Exception as e:
        print(f" Decryption error: {e}")



# Verification
def verify_files():
    try:
        with open(INPUT_FILE, "r") as f1, open(DECRYPTED_FILE, "r") as f2:
            if f1.read() == f2.read():
                print(" Decryption successful: Files match!")
            else:
                print("Decryption failed: Files do not match.")
    except Exception as e:
        print(f"Verification error: {e}")


# Main
def main():
    print("=== Encryption Program ===")

    if not check_input_file():
        return

    shift1, shift2 = validate_input()

    encrypt_file(shift1, shift2)
    print(f"Encrypted -> {ENCRYPTED_FILE}")

    decrypt_file(shift1, shift2)
    print(f"Decrypted -> {DECRYPTED_FILE}")

    verify_files()


if __name__ == "__main__":
    main()