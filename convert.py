def check_if_str(function):
    def new_func(input_str,**kwarg):
        if type(input_str) != str:
            raise TypeError("Must be str")
        return function(input_str,**kwarg)
    return new_func

#(check_if_str(convert_line_str))(input_str)
@check_if_str
def convert_line_str(input_str,include_in_line = ''):
    def processing_line(line):
        if line.find(include_in_line) != -1:
            return line[line.find(': ')+len(': '):]
        else:
            return None
    
    return '\n'.join(processing_line(line) for line in input_str.splitlines() if processing_line(line))