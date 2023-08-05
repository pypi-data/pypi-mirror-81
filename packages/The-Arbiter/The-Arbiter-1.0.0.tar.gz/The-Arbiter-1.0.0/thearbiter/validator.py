import re


class Arbiter:
    """
    The arbiter validates arguments of various kinds. It can be used in functions, or perhaps at command line parsing!
    It is very flexible. And pretty simple.
    """

    def __init__(self, required_args: list or dict):
        if not (isinstance(required_args, list) or isinstance(required_args, dict)):
            raise TypeError(f"required_args must be a list or dict. Got {type(required_args).__name__}.")
        self.required_args = required_args
        self.__missing = []

    @property
    def required_args(self):
        """
        Getter for the required args object.
        :return: The required parameters object.
        """
        return self._required_args

    @required_args.setter
    def required_args(self, required_args: dict or list):
        """
        Sets the required arguments object.
        :param required_args: Required arguments object.
        :return: None
        :raises: TypeError for invalid types (anything other than list or dict)
        """
        if isinstance(required_args, list) or isinstance(required_args, dict):
            self._required_args = required_args
        else:
            raise TypeError(f"Expected dict or list. Got {type(required_args).__name__}")

    @property
    def missing_arguments(self):
        return self.__missing

    def validate_args(self, **arguments):
        """
        Validates named arguments against the Arbiter's required_args pattern.
        :param arguments: The named arguments to validate.
        :return: True if everything checks out.
        :raises: AttributeError on failure.
        """
        # Reset missing args in case missing stuff was found on another call.
        self.__missing.clear()

        try:
            if self.__validate(self.required_args, **arguments):
                return True

            raise AttributeError(f"Missing {len(self.missing_arguments)} "
                                 f"argument{'s' if len(self.missing_arguments) > 1 else ''}: "
                                 f"{', '.join(self.missing_arguments)}")
        except Exception:
            raise

    def __validate(self, arbitrate: list or dict or str, **arguments) -> bool:
        """
        Handles the next section of requirements to arbitrate. Happy iteration!
        :param arbitrate: The next requirement.
        :param arguments: The arguments to check
        :return: True if the arguments are happy.
        :raises: AttributeError or TypeError on failure.
        """

        return {
            'str': lambda required, **args: self.__handle_str(required, **args),
            'list': lambda required, **args: self.__handle_list(required, **args),
            'dict': lambda required, **args: self.__handle_dict(required, **args)
        }.get(type(arbitrate).__name__,
              TypeError(f'Expected str, list or dict. Got {type(arbitrate).__name__}'))(arbitrate, **arguments)

    def __handle_dict(self, required_args: dict, **arguments) -> bool:
        """
        Iterates over dictionary objects using "OR", or "XOR" logic depending on the object key.
        Keys must start with OR for non-exclusive handling. Or... XOR for exclusive-or handling. They can be suffixed
        for clarity if desired.

        The value must be a list. That list can contain nested dicts, lists or strings.
        If multiple key-value pairs are given, they are combined using "AND" logic.

        :param required_args: The required arguments dict.
        :param arguments: Arguments to verify.
        :return: True if all is happy and bright.
        :raises: AttributeError if something is missing or incorrect.
        :raises: TypeError if the required_args argument isn't a dict or a key isn't a str.
        :raises: KeyError if the dictionary "operator" key is invalid (not 'or' or 'xor').
        """

        if not isinstance(required_args, dict):
            raise TypeError(f"Expected a dict, got {type(required_args).__name__}.")

        results = []

        for key in required_args:
            if not isinstance(key, str):  # Pretty important for the key to be a string.
                raise TypeError(f"Invalid key type: {type(key).__name__}. Must be str.")

            if not (isinstance(required_args[key], list)):  # Yes... the value must be a list.
                raise TypeError(f"The value for {key} must be a list. Got {type(required_args[key]).__name__}")

            operation = re.match('^x?or', key, re.IGNORECASE)  # Look for a valid operator in the key name.
            if operation is not None:
                results.append({'or': lambda r, **a: self.__or_path(r, **a),
                                'xor': lambda r, **a: self.__xor_path(r, **a)
                                }.get(operation.group(), False)(required_args[key], **arguments))
            else:
                raise KeyError('Invalid key name. Must start with "or" or "xor".')

        return any(results)

    def __or_path(self, required_args: list, **arguments) -> bool:
        """
        Handles "OR" logic for a dictionary. It uses short-circuit logic. Once the first True validation is found, it
        returns.
        :param required_args: The set of required arguments to validate.
        :return: True if an argument is validated. False if not.
        """

        for required_arg in required_args:
            if self.__validate(required_arg, **arguments):  # Short circuit on first validated arg.
                return True

        # No required argument was found at this point.
        return False

    def __xor_path(self, required_args: list, **arguments):
        """
        Handles "XOR" logic for a dictionary. Only 1 argument can resolve to True.
        :param required_args: The set of required arguments to validate.
        :return: True if only one validates.
        :raises: TooManyArgumentsError if multiple validations are True.
        """
        args_validated = []  # Keep track of True validations. There can be only one!

        for required_arg in required_args:
            if self.__validate(required_arg, **arguments):
                args_validated.append(str(required_arg))

            if len(args_validated) > 1:
                raise TooManyArgumentsError(f"Too many arguments given: {','.join(args_validated)}. "
                                            "Only one is allowed.")

        return len(args_validated) == 1  # 0 means none were found.

    def __handle_list(self, required_args: list, **arguments):
        """
        Iterates over every list item with "AND" logic. It expects all the items to resolve to True.
        :param required_args: The set of required arguments to validate.
        :param arguments: The arguments given.
        :return: True if all resolve.
        :raises: TypeError if the required_args aren't a list.
        """

        if not isinstance(required_args, list):
            raise TypeError(f"Expected a list, got {type(required_args).__name__}.")

        return all([self.__validate(required_arg, **arguments) for required_arg in required_args])

    def __handle_str(self, required_arg: str, **arguments):
        """
        This is the lowest level. It compares a string against the provided arguments.
        :param required_arg: The required argument to check for.
        :param arguments: The list of arguments to validate.
        :return: True if the required arg is found. False if not.
        :raises: TypeError if the required_arg value isn't a string.
        """
        if not isinstance(required_arg, str):
            raise TypeError(f"Expected a str, got {type(required_arg).__name__}.")

        if required_arg in arguments:
            return True

        # Keep track of missing arguments for logging later.
        self.__missing.append(required_arg)
        return False


class TooManyArgumentsError(Exception):
    """
    An error for those times where coexisting is bad.
    """

    def __init(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"TooManyArgumentsError: {self.message}."
        else:
            return "TooManyArgumentsError: Too many arguments were given."
