from mnemonic import Mnemonic
from werkzeug.security import generate_password_hash, check_password_hash

class CryptoService:
    @staticmethod
    def generate_mnemonic():
        mnemo = Mnemonic("english")
        return mnemo.generate(strength=160)

    @staticmethod
    def hash_value(value):
        return generate_password_hash(value, method='pbkdf2:sha256')

    @staticmethod
    def verify_value(stored_hash, provided_value):
        return check_password_hash(stored_hash, provided_value)
