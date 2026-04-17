import os

# Constants
INPUT_FILE = "raw_text.txt"
ENCRYPTED_FILE = "encrypted_text.txt"
DECRYPTED_FILE = "decrypted_text.txt"
ALPHABET_SIZE = 26

TAGS = {
    "LOWER_FIRST": "1",
    "LOWER_SECOND": "2",
    "UPPER_FIRST": "3",
    "UPPER_SECOND": "4"
}


# Utility Functions
def shift_char_forward(char, shift, base):
    return chr((ord(char) - ord(base) + shift) % ALPHABET_SIZE + ord(base))


def shift_char_backward(char, shift, base):
    return chr((ord(char) - ord(base) - shift) % ALPHABET_SIZE + ord(base))



# Validation Functions
def validate_input():
    while True:
        try:
            shift1 = int(input("Enter shift1 (non-negative integer): "))
            shift2 = int(input("Enter shift2 (non-negative integer): "))

            if shift1 < 0 or shift2 < 0:
                raise ValueError("Shift values must be non-negative.")

            return shift1, shift2

        except ValueError as e:
           print("Invalid input!, Please try again.\n")


def ensure_input_file_exists():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: '{INPUT_FILE}' not found.")
        return False
    return True


# Encryption Logic
def encrypt_character(char, shift1, shift2):
    if char.islower():
        if 'a' <= char <= 'm':
            shift = shift1 * shift2
            return TAGS["LOWER_FIRST"] + shift_char_forward(char, shift, 'a')
        else:
            shift = shift1 + shift2
            return TAGS["LOWER_SECOND"] + shift_char_backward(char, shift, 'a')

    elif char.isupper():
        if 'A' <= char <= 'M':
            return TAGS["UPPER_FIRST"] + shift_char_backward(char, shift1, 'A')
        else:
            shift = shift2 ** 2
            return TAGS["UPPER_SECOND"] + shift_char_forward(char, shift, 'A')

    return char


def encrypt_file(shift1, shift2):
    try:
        with open(INPUT_FILE, "r") as infile, open(ENCRYPTED_FILE, "w") as outfile:
            for line in infile:
                encrypted_line = ''.join(encrypt_character(ch, shift1, shift2) for ch in line)
                outfile.write(encrypted_line)
    except Exception as e:
        print(f"Encryption error: {e}")


# Decryption Logic
def decrypt_file(shift1, shift2):
    try:
        with open(ENCRYPTED_FILE, "r") as infile, open(DECRYPTED_FILE, "w") as outfile:
            for line in infile:
                decrypted_line = ""
                i = 0

                while i < len(line):
                    ch = line[i]

                    if ch in TAGS.values():
                        tag = ch
                        i += 1

                        if i >= len(line):
                            break

                        ch = line[i]

                        if tag == TAGS["LOWER_FIRST"]:
                            shift = shift1 * shift2
                            decrypted_line += shift_char_backward(ch, shift, 'a')

                        elif tag == TAGS["LOWER_SECOND"]:
                            shift = shift1 + shift2
                            decrypted_line += shift_char_forward(ch, shift, 'a')

                        elif tag == TAGS["UPPER_FIRST"]:
                            decrypted_line += shift_char_forward(ch, shift1, 'A')

                        elif tag == TAGS["UPPER_SECOND"]:
                            shift = shift2 ** 2
                            decrypted_line += shift_char_backward(ch, shift, 'A')

                    else:
                        decrypted_line += ch

                    i += 1

                outfile.write(decrypted_line)

    except Exception as e:
        print(f"Decryption error: {e}")


# Verification Logic

def verify_files():
    try:
        with open(INPUT_FILE, "r") as f1, open(DECRYPTED_FILE, "r") as f2:
            if f1.read() == f2.read():
                print("Decryption successful: Files match!")
            else:
                print("Decryption failed: Files do NOT match.")
    except Exception as e:
        print(f"Verification error: {e}")


# Main
def main():
    print("=== Encryption Program ===")

    if not ensure_input_file_exists():
        return

    shift1, shift2 = validate_input()

    encrypt_file(shift1, shift2)
    print(f"Encrypted -> {ENCRYPTED_FILE}")

    decrypt_file(shift1, shift2)
    print(f"Decrypted -> {DECRYPTED_FILE}")

    verify_files()


if __name__ == "__main__":
    main()