import yaml
from datetime import datetime, timedelta

def save_time_direct(datetime_file):
    with open(datetime_file,mode='w') as f:
        f.write(datetime.utcnow().strftime("%Y%m%d %H%M%S"))
    
def save_value_direct(value_file,val='0'):
    with open(value_file,mode='w') as f:
        f.write(val)


def load_time_direct(datetime_file):
    with open(datetime_file,mode='r') as f:
        waketime_str = f.read()
        waketime = datetime.strptime(waketime_str, "%Y%m%d %H%M%S")
        return waketime

def load_value_direct(value_file):
    with open(value_file,mode='r') as f:
        value_file_str = f.read()
        return value_file_str


def open_yaml_data(datafile):
    def _open_data_no_check(datafile):
        y_data = None
        with open(datafile,'r') as datas:
            y_data = yaml.load(datas,Loader=yaml.FullLoader)

        return y_data

    y_data = None
    try:
        y_data = _open_data_no_check(datafile)
    except FileNotFoundError:
        with open(datafile,'w') as datas:
            datas.write('')
    finally:
        y_data = _open_data_no_check(datafile)

    return y_data

def save_yaml_data(filename,datas):
    with open(filename,'w') as datafile:
        yaml.dump(datas,datafile)