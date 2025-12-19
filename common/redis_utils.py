from django.core.cache import cache


class RedisConfirmationCode:
    @staticmethod
    def generate_key(user_id):
        return f"confirmation_code:{user_id}"
    
    @staticmethod
    def set_code(user_id, code, timeout=300):
        key = RedisConfirmationCode.generate_key(user_id)
        cache.set(key, code, timeout=timeout)
        return True
    
    @staticmethod
    def get_code(user_id):
        key = RedisConfirmationCode.generate_key(user_id)
        return cache.get(key)
    
    @staticmethod
    def delete_code(user_id):
        key = RedisConfirmationCode.generate_key(user_id)
        cache.delete(key)
        return True
    
    @staticmethod
    def verify_code(user_id, code):
        stored_code = RedisConfirmationCode.get_code(user_id)
        if stored_code and stored_code == code:
            RedisConfirmationCode.delete_code(user_id)
            return True
        return False