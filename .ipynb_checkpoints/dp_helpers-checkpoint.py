from datetime import datetime

def get_date(year, file):
    file_end = file.split('/')[-1]
    string_date = file_end[4:8]
    date = datetime.strptime(f'{string_date}{year}', '%m%d%Y').date()
    return date    