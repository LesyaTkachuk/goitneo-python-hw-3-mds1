import re
from constants import WEEKDAYS, WEEKENDS
from collections import UserDict, defaultdict
from datetime import datetime
from exceptions_handler import PhoneValidationError, BirthdayValidationError


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        # acceptable formats 1111111111, (111)-111-1-111, 111-111-11-11, (111)111-11-11
        valid_phone_number = re.match(
            r"(^[(]?[\d]{3}[)\-]?[\d]{3}[-]?[\d]{2}[-]?[\d]{2}$)|(^[(]?[\d]{3}[)\-]?[\d]{3}[-]?[\d]{1}[-]?[\d]{3}$)",
            phone,
        )
        if not valid_phone_number:
            raise PhoneValidationError()
        super().__init__(phone)


class Birthday(Field):
    def __init__(self, birthday):
        valid_format = re.match(
            r"^(0[1-9]|1\d|2\d|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}$", birthday
        )
        if not valid_format:
            raise BirthdayValidationError()
        super().__init__(birthday)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join([p.value for p in self.phones])}"

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number.value:
            self.phones.append(phone_number)

    def find_phone(self, phone_number):
        for phone in self.phones:
            if str(phone) == phone_number:
                return phone
        print(
            f"There is no phone number {phone_number} in the {self.name}'s phone list"
        )
        return None

    def edit_phone(self, phone_to_change, new_phone):
        new_phone_number = Phone(new_phone)
        phone = self.find_phone(phone_to_change)
        if phone and new_phone_number.value:
            self.phones = [
                number
                for number in map(
                    lambda i: new_phone_number if str(i) == phone_to_change else i,
                    self.phones,
                )
            ]

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)

    def add_birthday(self, value):
        birthday = Birthday(value)
        if birthday.value:
            self.birthday = birthday


class AddressBook(UserDict):
    def __str__(self):
        records_string = "\n".join([str(r) for r in self.data.values()])
        return f"{records_string}"

    def add_record(self, record):
        self[str(record.name)] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        record = self.find(name)
        if record:
            self.data.pop(name)

    def get_birthdays_per_week(self):
        today_date = datetime.today().date()
        grouped_birthdays = defaultdict(list)

        for name, contact in self.data.items():
            birthday = datetime.strptime(str(contact.birthday), "%d.%m.%Y").date()
            birthday_this_year = birthday.replace(year=today_date.year)

            if birthday_this_year < today_date:
                birthday_this_year = birthday.replace(year=today_date.year + 1)

            delta_days = (birthday_this_year - today_date).days

            if delta_days < 7:
                birthday_weekday = birthday_this_year.strftime("%A")
                if birthday_weekday in WEEKENDS:
                    grouped_birthdays["Monday"].append(name)
                else:
                    grouped_birthdays[birthday_weekday].append(name)

        sorted_keys = sorted(grouped_birthdays.keys(), key=WEEKDAYS.index)

        formatted_birthdays = []
        for key in sorted_keys:
            formatted_birthdays.append(
                "{:<10}:  {}".format(key, ", ".join(grouped_birthdays[key]))
            )
        return "\n".join(formatted_birthdays)
