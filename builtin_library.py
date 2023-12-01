def split_list(list_in, split_col_num=1):
    return [list_in[col::split_col_num] for col in range(split_col_num)]