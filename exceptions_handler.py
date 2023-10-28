from constants import INVALID_COMMAND


class PhoneValidationError(Exception):
    pass


class BirthdayValidationError(Exception):
    pass


def input_error(default_response=INVALID_COMMAND):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except PhoneValidationError:
                return (
                    "Phone number should consists of 10 digits in international format"
                )
            except BirthdayValidationError:
                return "Birthday should be in DD.MM.YYYY format"
            except ValueError:
                return "Please provide all arguments"
            except IndexError:
                return "Please provide contact's name"
            except KeyError:
                return "Please provide the right key"
            except:
                return default_response

        return wrapper

    return decorator
