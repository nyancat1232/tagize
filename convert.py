#post_process(convert_line)(...)

def convert_line(input_file,out_file):
    with open(out_file,mode='w',encoding='UTF-8') as ouf:
        with open(input_file,mode='r',encoding='UTF-8') as inf:
            while line := inf.readline() :
                rrr = line.split('\t')
                ouf.writelines(rrr[1]+'\n')