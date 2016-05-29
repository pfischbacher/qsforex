#from test import Test
from datetime import datetime, date, time, timedelta
from collections import defaultdict

def defaultdict_testing():
    d = defaultdict(list)
    d['test'].append('a')
    d['test'].append('b')
    d['test'].append('c')
    d['test'].append('d')
    d['test'].append('e')
    d['test'].append('f')
    d['test 2'].append('ab')
    d['test 2'].append('bc')
    
    del[d['test'][1]]
    del[d['test'][1]]
    print('Default Dict', d)
    for a, b in enumerate(d['test']):
        print a, b

def round_time(dt=None, date_delta=timedelta(seconds=1), to='average'):
    """
    Round a datetime object to a multiple of a timedelta
    dt : datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    from:  http://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object-python
    """

    round_to = date_delta.total_seconds()
    print('Round To', round_to)
    if dt is None:
        dt = datetime.now()
    seconds = (dt - dt.min).seconds
    print('to', to)
    if to == 'up':
        # // is a floor division, not a comment on following line (like in javascript):
        rounding = (seconds + round_to) // round_to * round_to
    elif to == 'down':
        rounding = seconds // round_to * round_to
        print('rounding', rounding)
    else:
        rounding = (seconds + round_to / 2) // round_to * round_to
		
	print('rounding', rounding)
    return dt + timedelta(0, rounding - seconds, -dt.microsecond )



print("Hello World!")
print("This is a Python program.")
defaultdict_testing()
#input_variable = raw_input("Enter your name: ")
#test = Test('test')
#print(test)
"""now = datetime.now()
time2 = datetime(2010, 6, 10, 3, 56, 23)
date_delta=timedelta(minutes=15)
rounded_time = round_time(time2, date_delta, "down")
print('Time Now',str(time2))
print('Time Rounded', str(rounded_time))"""
