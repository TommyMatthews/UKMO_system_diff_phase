import sys
from datetime import date, timedelta

from config import radars, years, times


def get_total_tasks():
    return sum(
        (366 if date(int(year), 12, 31).timetuple().tm_yday == 366 else 365)
        * len(radars)
        * len(times)
        for year in years
    )


def get_task(task_id):

    for radar in radars:
        for year in years:

            start_date = date(int(year), 1, 1)

            days_in_year = (
                366 if date(int(year), 12, 31).timetuple().tm_yday == 366
                else 365
            )

            tasks_in_year = days_in_year * len(times)

            if task_id >= tasks_in_year:
                task_id -= tasks_in_year
                continue

            day_index, time_index = divmod(task_id, len(times))

            current_date = start_date + timedelta(days=day_index)

            return (
                radar,
                year,
                current_date.strftime('%m%d'),
                times[time_index]
            )

            # Note: task order is radar, year, day, time

    raise ValueError("Task ID outside valid range")


if __name__ == '__main__':

    if sys.argv[1] == '--count':
        print(get_total_tasks())

    else:
        print(*get_task(int(sys.argv[1])))