from datetime import datetime

radar_number_map = {
    'castor-bay' : '07',
    'chenies' : '05',
    'clee-hill' : '03',
    'cobbacomebe' : '16',
    'crug-y-gorrllwyn' : '10',
    'deanhill' : '21',
    'druima-starraig' :'15',
    'dudwick' : '14',
    'hameldon-hill' : '4',
    'high-moorsley' : '23',
    'holehead' : '18',
    'ingham' : '09',
    'jersey' :'12',
    'munduff-hill' :'19',
    'predannack' : '18',
    'thurnham' :'20',
    'wardon-hill' :'11',
    
}

def get_date(year, file):
    file_end = file.split('/')[-1]
    string_date = file_end[4:8]
    #date = datetime.strptime(f'{string_date}{year}', '%m%d%Y').date()
    return f'{string_date}{year}'   


def get_radar_number(radar):

    if radar not in radar_number_map:
        raise ValueError('Not a valid radar name')

    return radar_number_map[radar]