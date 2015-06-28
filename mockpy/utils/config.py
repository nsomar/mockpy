from termcolor import colored

global verbose
verbose = False


def error(msg):
    print(colored(msg, "red"))


def warn(msg):
    print(colored(msg, "yellow"))


def success(msg):
    print(colored(msg, "green"))


def info(msg):
    print(msg)
