from passlib.context import CryptContext

password = "admin"

def get_password_hash(password):
    return pwd_context.hash(password)

if __name__ == "__main__":
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    hashed_password = get_password_hash(password)
    print(hashed_password)