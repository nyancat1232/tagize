def convert_line_file(input_file,out_file):
    with open(out_file,mode='w',encoding='UTF-8') as ouf:
        with open(input_file,mode='r',encoding='UTF-8') as inf:
            while line := inf.readline() :
                rrr = line.split('\t')
                ouf.writelines(rrr[1]+'\n')

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