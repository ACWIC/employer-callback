import hashlib
import uuid


class Random:
    @staticmethod
    def get_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def get_str_hash(text):
        hash_object = hashlib.md5(str.encode(text))
        return hash_object.hexdigest()
