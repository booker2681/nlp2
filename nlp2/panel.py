import inspect


class Panel:
    def __init__(self):
        self.element_list = []
        self.key_list = []
        self.result_dict = {}

    def add_element(self, k, v, msg):
        if isinstance(v, float) and 0 < v < 1:  # probability
            msg += " (between 0-1)"
        elif isinstance(v, float) or isinstance(v, int):  # number
            msg += " (number)"

        if isinstance(v, list):
            inputted = ''
            while inputted not in [str(e) for e in v]:
                inputted = input(msg + ", input an item in the list " + str(v) + ": ")
            self.element_list.append(inputted)
        else:
            self.element_list.append(input(msg + ", [default=" + str(v) + "]: "))
        self.key_list.append(k)

    def get_result_dict(self):
        result_dict = dict(zip(self.key_list, self.element_list))
        return {k: v for k, v in result_dict.items() if
                v is not None and len(v) > 0}  # only return non empty result


def function_get_all_arg(func):
    if len(inspect.getfullargspec(func).args) > 0:
        arg_len = len(inspect.getfullargspec(func).args)
        def_len = len(inspect.getfullargspec(func).defaults)
        return inspect.getfullargspec(func).args[arg_len - def_len:]
    else:
        return []


def function_check_wrong_arg(func, input_arg):
    all_arg = function_get_all_arg(func)
    return [arg for arg in input_arg if arg not in all_arg]


def function_check_missing_arg(func, input_arg):
    all_arg = function_get_all_arg(func)
    return [arg for arg in all_arg if arg not in input_arg]


def function_argument_panel(func, inputted_arg={}, disable_input_panel=False, ignore_empty=False,
                            func_parent=None, show_func_name=False):
    """use inquirer panel to let user input function parameter or just use default value"""
    fname = func.__name__
    if len(inspect.getfullargspec(func).args) > 0 and inspect.getfullargspec(func).defaults is not None:
        arg_len = len(inspect.getfullargspec(func).args)
        def_len = len(inspect.getfullargspec(func).defaults)
        arg_w_def = zip(inspect.getfullargspec(func).args[arg_len - def_len:],
                        inspect.getfullargspec(func).defaults)
        # merge two dict
        def_arg = dict(arg_w_def)
        function_def_arg = {**def_arg, **inputted_arg}
        # panel
        panel = Panel()
        for k, v in def_arg.items():
            if v is not None and (not isinstance(v, str) or len(v) > 0 or not ignore_empty):
                msg = fname + " " + k if show_func_name else k
                if callable(v):
                    v = v(func_parent) if func_parent else v()
                    function_def_arg[k] = v[0]  # set default value
                elif isinstance(v, bool):
                    v = [True, False]
                if not disable_input_panel:
                    panel.add_element(k, v, msg)

        if not disable_input_panel:
            function_def_arg.update(panel.get_result_dict())
        return function_def_arg
    else:
        return inputted_arg
