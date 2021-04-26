import re


def is_dictionary_empty(input_dict):
    """
    Checking if dictionary is empty recursively
    :return: True if dictionary is empty, False if not
    """
    checked_dictionary = []

    def dictionary_check(dict_for_checking):
        for key, value in dict_for_checking.items():
            if isinstance(value, dict):
                dictionary_check(value)
            else:
                checked_dictionary.append(bool(value))

    dictionary_check(input_dict)

    return not any(checked_dictionary)


def find_all(a_str, sub):
    return [m.start() for m in re.finditer(sub, a_str)]  # [0, 5, 10, 15]
