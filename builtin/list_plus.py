def swap_in_list(list_,index1,index2,mutable=False):
    if mutable:
        temp = list_[index1]
        list_[index1] = list_[index2]
        list_[index2] = temp
    else:
        ret = list_.copy()
        ret[index1] = list_[index2]
        ret[index2] = list_[index1]
        return ret
    
def list_change_position(list_,index_from,index_to,mutable=False):
    if mutable:
        raise Exception("No implementation")
    else:
        temp = list_.copy()
        temp_val = temp[index_from]
        ret = temp[:index_from]+temp[index_from+1:]
        ret.insert(index_to,temp_val)
        return ret