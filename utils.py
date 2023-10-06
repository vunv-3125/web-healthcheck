from time import sleep


def max_retry(max_times):
    def retry(func):
        def wrapper(*args, **kwargs):
            for _ in range(max_times):
                try:
                    return func(*args, **kwargs)
                except:
                    sleep(3)

            raise Exception()

        return wrapper

    return retry


def is_executed_without_exception(func):
    def wrapper(*args, **kwargs) -> bool:
        try:
            func(*args, **kwargs)

            return True
        except:
            return False

    return wrapper
