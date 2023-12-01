from datetime import datetime

def split_list(list_in, split_col_num=1):
    return [list_in[col::split_col_num] for col in range(split_col_num)]

def transpose_list(list_in,default_val=None):
    list_temp = list_in.copy()
    if len(list_temp[-1])-len(list_temp[0]) != 0:
        for l in list_temp:
            l.append(default_val)
    return list(map(list, zip(*list_temp)))

def date_only_month_and_day(str_date,spearator='.'):
    month,day = map(int,str_date.split(spearator))
    now_date = datetime.utcnow()
    year = now_date.year
    comp_date = datetime(year,month,day)
    if comp_date > now_date:
        year -= 1
    return datetime(year,month,day)

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