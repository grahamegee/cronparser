import sys


def parse(cron_line):
    return {cron_line}


if __name__ == '__main__':
    cron_line = sys.argv[1]
    print(parse(cron_line))