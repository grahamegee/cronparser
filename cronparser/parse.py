import sys
import re


# 5 non whitespace sequences separated by at least 1 space.
TIME_DATE_FIELDS_RE = re.compile(
    r' *([^\s]+) +([^\s]+) +([^\s]+) +([^\s]+) +([^\s]+) +(.*)')

PREFIXES_RE = re.compile(r'[A-z]{3}')

RANGE_RE = re.compile(r'(\d{1,2})-(\d{1,2})')
RANGE_WITH_STEP_RE = re.compile(r'(\d{1,2})-(\d{1,2})/(\d{1,2})')
SINGLE_NUMBER_RE = re.compile(r'(\d{1,2})')

ID_TO_NAME = {
    0: 'minute',
    1: 'hour',
    2: 'day of month',
    3: 'month',
    4: 'day of week'
}
RANGES = {
    0: (0, 59),
    1: (0, 23),
    2: (1, 31),
    3: (1, 12),
    4: (0, 7)
}
MONTH_TO_INT = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12
}
DAY_TO_INT = {
    'sun': 0,
    'mon': 1,
    'tue': 2,
    'wed': 3,
    'thu': 4,
    'fri': 5,
    'sat': 6
}


def _expand_stars(field_id, string):
    '''
    turn and '*' into it's expanded form:
    for example with day of week:
        * -> 0-7
    '''
    return string.replace('*', '{}-{}'.format(*RANGES[field_id]))


def _replace_prefixes_with_ints(field_id, string):
    prefixes = re.findall(PREFIXES_RE, string)
    if field_id == 3:
        mapping = MONTH_TO_INT
    elif field_id == 4:
        mapping = DAY_TO_INT
    for prefix in prefixes:
        replacement = str(mapping[prefix.lower()])
        string = string.replace(prefix, replacement)
    return string


def _create_subschedule(field_id, start, end, step):
    min_val, max_val = RANGES[field_id]
    if start < min_val or end > max_val or start > end:
        raise SyntaxError('Bad {}'.format(ID_TO_NAME[field_id]))
    return {i for i in range(start, end + 1, step)}


def parse(cron_line):
    *time_data_fields, command = re.search(TIME_DATE_FIELDS_RE, cron_line).groups()
    full_schedule = {'command': command}
    
    for field_id, field_string in enumerate(time_data_fields):
        field_string = _expand_stars(field_id, field_string)
        if field_id == 3 or field_id == 4:
            field_string = _replace_prefixes_with_ints(field_id, field_string)
        field_items = field_string.split(',')

        schedule = set()
        # ranges with step, ranges, and ints are the only valid options left
        for item in field_items:
            m = re.match(RANGE_WITH_STEP_RE, item)
            if m:
                start, end, step = (int(i) for i in m.groups())
                schedule.update(
                    _create_subschedule(field_id, start, end, step))
                continue
            m = re.match(RANGE_RE, item)
            if m:
                start, end = (int(i) for i in m.groups())
                schedule.update(
                    _create_subschedule(field_id, start, end, 1))
                continue
            m = re.match(SINGLE_NUMBER_RE, item)
            if m:
                start = end = int(item)
                schedule.update(
                    _create_subschedule(field_id, start, end, 1))
                continue

            raise SyntaxError('Bad {}'.format(ID_TO_NAME[field_id]))

        full_schedule[ID_TO_NAME[field_id]] = sorted(list(schedule))
    return full_schedule


if __name__ == '__main__':
    arg = sys.argv[1]
    print(parse(arg))
