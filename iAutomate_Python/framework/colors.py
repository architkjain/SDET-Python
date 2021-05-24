from colorama import Fore, Style


def print_black(message):
    """
    :param message:
    :return:
    """
    print(Fore.BLACK + message)
    print(Style.RESET_ALL)


def print_red(message):
    """
    :param message:
    :return:
    """
    # print(Fore.LIGHTRED_EX + message)
    print(message)
    # print(Style.RESET_ALL)


def print_green(message):
    """
    :param message:
    :return:
    """
    print(Fore.GREEN + message)
    print(Style.RESET_ALL)


def print_yellow(message):
    """
    :param message:
    :return:
    """
    # print(Fore.YELLOW + message)
    print(message)
    # print(Style.RESET_ALL)


def print_blue(message):
    """
    :param message:
    :return:
    """
    print(Fore.BLUE + message)
    print(Style.RESET_ALL)


def print_magenta(message):
    """
    :param message:
    :return:
    """
    print(Fore.MAGENTA + message)
    print(Style.RESET_ALL)


def print_cyan(message):
    """
    :param message:
    :return:
    """
    print(Fore.CYAN + message)
    print(Style.RESET_ALL)


def print_white(message):
    """
    :param message:
    :return:
    """
    print(Fore.WHITE + message)
    print(Style.RESET_ALL)

