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
