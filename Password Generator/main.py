import string
import secrets

def generate_password(length=28):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

if __name__ == "__main__":
    print("Welcome to the Password Generator!")
    try:
        length = int(input("Enter password length (default 28): ") or 28)
    except ValueError:
        length = 28
    password = generate_password(length)
    print("\nGenerated password:")
    print(password)