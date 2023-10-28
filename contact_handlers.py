from constants import (
    YES_CHOICE,
    NO_CHOICE,
    YES_NO_CHOICE,
    ABORTED,
    INVALID_COMMAND,
    EMPTY_PHONEBOOK,
    NO_CONTACT
)
from classes import Record, AddressBook
from exceptions_handler import input_error


@input_error()
def add_contact(args, book: AddressBook):
    name, phone = args
    record: Record = book.find(name)
    if record:
        record.add_phone(phone)
        return f"{phone} was added to {name}'s phone list."
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return f"Contact {name} was added."


@input_error()
def change_contact(args, book: AddressBook):
    name, phone, new_phone = args
    record: Record = book.find(name)
    if record:
        record.edit_phone(phone, new_phone)
        return record
    else:
        return NO_CONTACT


@input_error()
def delete_contact(args, book: AddressBook):
    name = args[0]
    record: Record = book.find(name)
    if record:
        user_input = input(
            f"Do you really want to delete {name} from contacts?{YES_NO_CHOICE}"
        )
        user_input = user_input.strip().lower()
        if user_input == YES_CHOICE:
            book.delete(name)

        elif user_input == NO_CHOICE:
            return ABORTED
        else:
            return INVALID_COMMAND
    else:
        return NO_CONTACT


@input_error()
def show_phone_numbers(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return record
    else:
        return NO_CONTACT

@input_error()    
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record: Record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"{name} birthday was added."
    else:
       return NO_CONTACT
    
@input_error()    
def show_birthday(args, book: AddressBook):
    name = args[0]
    record: Record = book.find(name)
    if record:
        if record.birthday:
            return record.birthday
        return f"No birthday for {name}. You can add it"
    else:
       return NO_CONTACT

def show_all_birthdays_per_week(args, book: AddressBook):
    birthdays=book.get_birthdays_per_week()
    if birthdays:
        return birthdays
    return "No birthdays for the next week"


def show_all_contacts(args, book):
    records = []
    book_items=book.data.items()
    if len(book_items):
        for name, record in book_items:
            records.append(str(record))
        records_string = "\n".join(records)
        return f"{'*'*15}\n{records_string}\n{'*'*15}"
    else:
        return EMPTY_PHONEBOOK
