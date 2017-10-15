import sys
import re

# 5 non whitespace sequences separated by at least 1 space.
TIME_DATE_FIELDS = re.compile(
    r' *([^\s]+) +([^\s]+) +([^\s]+) +([^\s]+) +([^\s]+) +(.*)')


def parse(cron_line):
    *time_data_fields, command = re.search(TIME_DATE_FIELDS, cron_line).groups()
    print(time_data_fields)
    print(command)
    return {cron_line}


if __name__ == '__main__':
    cron_line = sys.argv[1]
    print(parse(cron_line))