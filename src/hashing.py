from passlib.context import CryptContext

# Inicjalizacja obiektu CryptContext
pwd_cxt = CryptContext(schemes=['sha256_crypt'], deprecated='auto')


class Hash:
    # Funkcja do haszowania haseł
    @staticmethod
    def encrypt(password: str):
        return pwd_cxt.hash(password)

    # Funkcja do weryfikacji haseł
    @staticmethod
    def verify(hashed_password: str, plain_password: str):
        return pwd_cxt.verify(plain_password, hashed_password)
