from parse_input import parse_input
from general_handlers import read_contacts, show_command_list, close_assistant
from classes import AddressBook


def main():
    book = read_contacts()
    if not book:
        print(show_command_list())
        book = AddressBook()

    while True:
        user_input = input("---> Enter a command: >>> ")
        handler, args = parse_input(user_input)

        print(handler(args, book=book))

        if handler == close_assistant:
            break


if __name__ == "__main__":
    main()
