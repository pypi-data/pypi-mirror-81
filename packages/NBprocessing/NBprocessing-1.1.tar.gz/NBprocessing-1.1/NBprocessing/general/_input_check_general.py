"""
This file contain wraps function that will check the input of the general function.
will raise exceptions if the input is not valid.
This file is using the generic check input class 'CheckInput' that contains all the
input validation to all the functions

Created by: Nir Barazida
Good luck
"""

from functools import wraps
from NBprocessing.src._check_input import _CheckInput

class _InputCheckGeneral(object):
    """
    This class contain wraps function that will check the input of the general function.
    will raise exceptions if the input is not valid.
    This class is using the generic check input class 'CheckInput' that contains all the
    input validation to all the functions

    """
    @staticmethod
    def _missing_values_checker(func):
        """
        Wrapper function to validate the input for method 'missing_values'
        Will raise Exception if input incorrect
        """

        @wraps(func)
        def wrapper_checker(database):
            _CheckInput._check_database_input(database)
            return func(database)
        return wrapper_checker

    @staticmethod
    def _split_and_check_checker(func):
        """
        Wrapper function to validate the input for method 'split_and_check'
        Will raise Exception if input incorrect
        """

        @wraps(func)
        def wrapper_checker(database, column_name, test_size=0.3):
            _CheckInput._check_database_input(database)
            _CheckInput._check_column_in_database(column_name, database)
            _CheckInput._check_threshold(test_size)
            return func(database, column_name, test_size=0.3)
        return wrapper_checker