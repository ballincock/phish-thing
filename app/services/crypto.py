from mnemonic import Mnemonic
from werkzeug.security import generate_password_hash, check_password_hash

class CryptoService:
    @staticmethod
    def generate_mnemonic():
        mnemo = Mnemonic("english")
        return mnemo.generate(strength=160)

    @staticmethod
    def secure_hash(data):
        from werkzeug.security import generate_password_hash
        return generate_password_hash(data, method='pbkdf2:sha256')

    hash_value = secure_hash 

    @staticmethod
    def verify_value(stored_hash, provided_data):
        from werkzeug.security import check_password_hash
        return check_password_hash(stored_hash, provided_data)
