

def rename_duplicate(column_names):
    def check_duplicate(temp_buffer,s,index):
        if s in temp_buffer:
            return s+str(index)
        temp_buffer.append(s)
        return ""

    temp_buffer=[]
    return [f"{s}{check_duplicate(temp_buffer,s,i)}"for i,s in enumerate(column_names)]

def divide_by_column(list_lines,row_num=1,sep='\t'):
    new_list = []
    for i in range(0,len(list_lines),row_num):
        concat_line = []
        for ii in range(row_num):
            concat_line.append(list_lines[i+ii])
        new_list.append(sep.join(concat_line).split(sep))
    return new_list



def filter_by_exact_length(words,query):
    return [word for word in words if len(word)==len(query)]

def count_trues(li):
    return len([element for element in li if element==True])
               
def check_match(word,query):
    if len(word)!=len(query):
        raise IndexError("Not exact length")
    
    results = [any([char1==char2,char2=="?"]) for char1,char2 in zip(word,query) ]
    count = (count_trues(results)==len(word))
    return {'count':count,'results':results}
