import pickle
from pathlib import Path
from constants import EMPTY_PHONEBOOK, INVALID_COMMAND

CONTACTS_FILE_PATH = Path(__file__).parent / "contacts.bin"


def show_command_list(*args, **kwargs):
    return """
    *****************************
    hello                   --> to greet an assistant
    help                    --> to get the list of possible commands
    add <name> <phone>      --> to add a contact with the provided phone number to the phonebook
    change <name> <phone> <new_phone>   --> to change the existing contact's phone number
    phone <name>            --> to display the existing contact's phone number
    delete <name>           --> to delete provided contact with a phone number from the phonebook
    all                     --> to display the whole phone book
    add-birthday <name> <birthday> --> to add the bithday date for the contact
    show-birthdays <name>   --> to show the bithday date for the contact
    birthdays               --> to show all birthdays for the next week
    exit | close            --> to exit and store contacts
    ******************************
    """


def show_unknown_command(*args, **kwargs):
    return INVALID_COMMAND


def greet_user(*args, **kwargs):
    return "Hello! How can I help you?"


def read_contacts():
    book = {}
    try:
        with open(CONTACTS_FILE_PATH, "rb") as fh:
            book = pickle.load(fh)

    except FileNotFoundError:
        print(EMPTY_PHONEBOOK)
    except:
        print("There was an error while reading the phonebook")

    return book


def close_assistant(*args, book):
    if book:
        with open(CONTACTS_FILE_PATH, "wb") as fh:
            pickle.dump(book, fh)

    return "Good bye!"
