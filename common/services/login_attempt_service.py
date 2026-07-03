from django.core.cache import cache


class LoginAttemptService:

    MAX_ATTEMPS = 5
    BLOCK_TIME = 60 * 15

    @classmethod
    def get_cache_key(cls, email):
        return f"login_attempt: {email.lower()}"
    

    @classmethod
    def is_blocked(cls, email):

        attempts = cache.get(cls.get_cache_key(email), 0)

        return attempts >= cls.MAX_ATTEMPS
    

    @classmethod
    def register_failure(cls, email):

        key = cls.get_cache_key(email)

        attempts = cache.get(key, 0)

        attempts += 1

        cache.set(
            key,
            attempts,
            timeout=cls.BLOCK_TIME
        )

        return attempts
    

    @classmethod
    def reset(cls, email):

        cache.delete(
            cls.get_cache_key(email)
        )