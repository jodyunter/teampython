class RequestUtilities:

    @staticmethod
    def get_parameter_from_input(input_map, parameter, required):
        pass

    @staticmethod
    def get_boolean_from_form_input(input_map, parameter):
        if parameter not in input_map:
            return False
        else:
            if input == "on":
                return True
            else:
                return False
