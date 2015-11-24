#!/usr/bin/python

from bs4 import BeautifulSoup as Soup
from _util import compose

PERIOD_TIMES = {
    "08:00AM" : 1,
    "08:55AM" : 2,
    "10:20AM" : 3,
    "11:15AM" : 4,
    "12:10PM" : 5,
    "01:05PM" : 6,
    "02:00PM" : 7,
}

def parse_sched(schedule):
    raw = Soup(schedule, 'html.parser')
    raw = raw.table.contents
    student_info = dict(zip(
        ("name", "id", "cuts", "year", "cluster",
        "rm", "hoco", "advisor", "phone_ext"),
        map(compose(str.strip, Soup.get_text), raw[5].find_all('b'))
    ))
    # 7 potential courses, work duty, sport, potential 9th period
    courses = [None for i in range(10)]
    for i in range(9, 29, 2):
        course_info = dict(zip(
            ("course_code", "course_name", "null", "inst", "time", "loc"),
            map(compose(str.strip, Soup.get_text), raw[i].find_all('font'))
        ))
        code = course_info['course_code']
        # If it's not an actual character, it's probably not a real course
        if not code or not code[0].isalpha(): continue
        time = course_info['time']
        # Work duty
        if 'WD' in code:
            courses[7] = course_info
        # Athletic
        # My favorite bug was matching the 'ATH' in 'MATH'
        elif code.startswith('ATH'):
            courses[8] = course_info
        elif time in PERIOD_TIMES:
            courses[PERIOD_TIMES[time]-1] = course_info
        # Otherwise, it's probably a 9th period class
        else:
            courses[9] = course_info
    return student_info, courses

if __name__ == '__main__':
    with open('Student Schedules.html') as f: print(parse_sched(f))
