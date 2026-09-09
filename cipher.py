"""
Assignment 2
# Group name: DAN/EXT-31

# Group members:
# Xuan Vinh Do - S407011
# Andy Tran - s401280
# Hynaro Eang - s400654
"""

""" Question 1"""


# SHIFT CHARACTER
def shift_character(character, start, end, shift):
    range_size = ord(end) - ord(start) + 1
    position = ord(character) - ord(start)
    new_position = (position + shift) % range_size
    return chr(ord(start) + new_position)


# ENCRYPTED TEXT
def encrypt_file(shift1, shift2, input_path, output_path):
    with open(input_path, "r") as file:
        text = file.read()

    encrypted_text = ""

    for character in text:

        if "a" <= character <= "n":
            encrypted_character = shift_character(
                character, "a", "n", shift1 * shift2
            )

        elif "o" <= character <= "z":
            encrypted_character = shift_character(
                character, "o", "z", -(shift1 + shift2)
            )

        elif "A" <= character <= "M":
            encrypted_character = shift_character(
                character, "A", "M", -shift1
            )

        elif "N" <= character <= "Z":
            encrypted_character = shift_character(
                character, "N", "Z", shift2 ** 2
            )

        elif "0" <= character <= "9":
            encrypted_character = shift_character(
                character, "0", "9", shift1 - shift2
            )

        else:
            encrypted_character = character

        encrypted_text += encrypted_character

    with open(output_path, "w") as file:
        file.write(encrypted_text)


# DECRYPTED TEXT
def decrypt_file(shift1, shift2, input_path, output_path):
    with open(input_path, "r") as file:
        text = file.read()

    decrypted_text = ""

    for character in text:

        if "a" <= character <= "n":
            decrypted_character = shift_character(
                character, "a", "n", -(shift1 * shift2)
            )

        elif "o" <= character <= "z":
            decrypted_character = shift_character(
                character, "o", "z", shift1 + shift2
            )

        elif "A" <= character <= "M":
            decrypted_character = shift_character(
                character, "A", "M", shift1
            )

        elif "N" <= character <= "Z":
            decrypted_character = shift_character(
                character, "N", "Z", -(shift2 ** 2)
            )

        elif "0" <= character <= "9":
            decrypted_character = shift_character(
                character, "0", "9", -(shift1 - shift2)
            )

        else:
            decrypted_character = character

        decrypted_text += decrypted_character

    with open(output_path, "w") as file:
        file.write(decrypted_text)


# VERIFY TEXT
def verify_files(original_path, decrypted_path):
    with open(original_path, "r") as file:
        original_text = file.read()

    with open(decrypted_path, "r") as file:
        decrypted_text = file.read()

    if original_text == decrypted_text:
        print("Verification successful: Files match.")
        return True
    else:
        print("Verification failed: Files do not match.")
        return False

def get_non_negative_integer(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value < 0:
                print("Invalid input. Please enter a non-negative integer.")
            else:
                return value

        except ValueError:
            print("Invalid input. Please enter a whole number.")

def main():
    shift1 = get_non_negative_integer("Enter shift1: ")
    shift2 = get_non_negative_integer("Enter shift2: ")
    
    encrypt_file(
        shift1,
        shift2,
        "raw_text.txt",
        "encrypted_text.txt"
    )

    print("Encryption completed.")
    
    decrypt_file(
        shift1,
        shift2,
        "encrypted_text.txt",
        "decrypted_text.txt"
    )

    print("Decryption completed.")


    verify_files(
        "raw_text.txt",
        "decrypted_text.txt"
    )
    
main()


