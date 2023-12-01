def check_if_str(function):
    def new_func(input_str):
        if type(input_str) != str:
            raise TypeError
        return function(input_str)
    return new_func

#(check_if_str(convert_line_str))(input_str)
@check_if_str
def convert_line_str(input_str):
    def processing_line(line):
        if line.find('In [') != -1:
            return line[line.find(': ')+len(': '):]
        else:
            return None
    
    return '\n'.join(processing_line(line) for line in input_str.splitlines() if processing_line(line))