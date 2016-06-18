import numpy
import pandas
import datetime
import time
# Binning delta

#delta = datetime.timedelta(hours=1)
delta = datetime.timedelta(seconds=1)

# Sample data

sample = [
    ['2014-08-09 16:30:00', 'label1'],
    ['2014-08-09 15:30:00', 'label2'],
    ['2014-08-09 14:30:00', 'label3'],
    ['2014-08-09 14:00:00', 'label4']
]

sample_1 = [
    ['2016.02.01 00:00:00.728', 1.08253, 1.08261, 3, 10.67],
    ['2016.02.01 00:00:01.032', 1.08253, 1.08259, 5.62, 1],
    ['2016.02.01 00:00:01.366',1.08257, 1.0826, 1.87, 1],
    ['2016.02.01 00:00:01.620',1.08258, 1.08263, 1.5, 1.12],
    ['2016.02.01 00:00:02.125',1.08259, 1.08263, 1, 1],
    ['2016.02.01 00:00:02.651',1.0826, 1.08263, 4.5, 1],
    ['2016.02.01 00:00:02.803',1.08258, 1.08263, 2.25, 1],
    ['2016.02.01 00:00:02.905',1.0826, 1.08263, 1, 1],
    ['2016.02.01 00:00:03.057',1.08258, 1.08263, 3.75, 1],
    ['2016.02.01 00:00:03.210',1.0826, 1.08263, 1, 1],
    ['2016.02.01 00:00:03.722',1.08259, 1.08263, 1.5, 1],
    ['2016.02.01 00:00:04.388',1.08258, 1.08263, 2.25, 1],
    ['2016.02.01 00:00:04.896',1.08259, 1.08263, 1.5, 1],
    ['2016.02.01 00:00:05.436',1.08258, 1.08263, 1.5, 1],
    ['2016.02.01 00:00:05.740',1.0826, 1.08263, 3, 1],
    ['2016.02.01 00:00:05.842',1.0826, 1.08267, 6, 3.45],
    ['2016.02.01 00:00:06.350',1.08261, 1.08266, 1.5, 1],
    ['2016.02.01 00:00:06.452',1.08262, 1.08266, 3.37, 1],
    ['2016.02.01 00:00:07.876',1.08264, 1.08266, 1.5, 1],
    ['2016.02.01 00:00:08.396',1.08264, 1.08267, 1.5, 1],
    ['2016.02.01 00:00:09.905',1.08263, 1.08268, 1.5, 1]
]

# Create dataframe and append UNIX timestamp column

df = pandas.DataFrame(sample_1)

df.columns = ['Datetime', 'Ask', 'Bid', 'Ask Volume', 'Bid Volume']
#df.columns = ['Datetime', 'Label']
df['Datetime'] = pandas.to_datetime(df['Datetime'])
df['UnixStamp'] = df['Datetime'].apply(lambda d: time.mktime(d.timetuple()))
print(df)
df = df.set_index('Datetime')
df.index.map(lambda x: x.strftime("%Y%m%d"))
# Calculate bins
print('df.index', df.index)
bins = numpy.arange(min(df['UnixStamp']), max(df['UnixStamp']) + delta.seconds, delta.seconds)
print('bins', bins)
# Group columns by datetime bin

def bin_from_tstamp(tstamp):
    print('tstamp', tstamp)
    diffs = [abs(tstamp - bin) for bin in bins]
    print('diffs',diffs)
    return bins[diffs.index(min(diffs))]

grouped = df.groupby(df['UnixStamp'].map(
    lambda t: bin_from_tstamp(t)
))
print('df-UnixStamp', df['UnixStamp'].map(
    lambda t: bin_from_tstamp(t)
))
#At this point grouped contains the dataset grouped by datetime bins.

"""The following is the result of printing grouped.groups (where the keys are the datetime bins and the values are the grouped datetimes):"""
print('GROUPED', grouped.groups)
"""{
    numpy.datetime64('2014-08-09T18:00:00.000000000+0200'): [
        Timestamp('2014-08-09 16:30:00')
    ], 
    numpy.datetime64('2014-08-09T17:00:00.000000000+0200'): [
        Timestamp('2014-08-09 15:30:00')
    ], 
    numpy.datetime64('2014-08-09T16:00:00.000000000+0200'): [
        Timestamp('2014-08-09 14:30:00'), 
        Timestamp('2014-08-09 14:00:00'
    ]
}"""

