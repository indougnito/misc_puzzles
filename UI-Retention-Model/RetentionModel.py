import csv
from datetime import datetime, timedelta

DATE_FORMAT = '%Y-%m-%d'
DELIM = '-'

class RetentionModel(object):

    ''' construct model from csv file '''
    def __init__(self, filepath):

        # model data
        data = dict()

        # csv file reader
        csvfile = open(filepath, 'rb')
        rdr = csv.reader(csvfile, delimiter=',')

        # parse column names
        labels = rdr.next()
        idx_event_name  = labels.index('event_name')
        idx_event_time  = labels.index('event_time')
        idx_os_name     = labels.index('os_name')
        idx_sdk_version = labels.index('sdk_version')
        idx_user_id     = labels.index('user_id')

        for row in rdr:
            # parse field names
            event_name  = row[idx_event_name]
            if event_name != 'UI_OPEN_COUNT':
                continue # irrelevant event
            event_time  = row[idx_event_time]
            os_name     = row[idx_os_name]
            sdk_version = row[idx_sdk_version]
            user_id     = row[idx_user_id]

            # parse date from timestamp
            dt = datetime.strptime(event_time.split()[0], DATE_FORMAT)

            # generate user identifier from user_id, os name, and sdk version
            full_user_id = user_id + DELIM + os_name + DELIM + sdk_version

            # parse fields
            year = dt.year
            month = dt.month
            day = dt.day
            if year not in data:
                data[year] = dict()
            if month not in data[year]:
                data[year][month] = dict()
                data[year][month]['user_activity'] = dict()
            if full_user_id not in data[year][month]['user_activity']:
                data[year][month]['user_activity'][full_user_id] = set()

            # 'user_activity' is a mapping of <user_id> to <set of dates>, where
            # the set contains all dates on which the UI was opened this month.
            data[year][month]['user_activity'][full_user_id].add(day)

            # keep track of dates for which we have data. will be handy later.
            if dt.day not in data[year][month]:
                data[year][month][day] = dict()
                data[year][month][day]['retention'] = dict()

        self.data = data

    ''' compute user retention for day n after acquisition, using optional filters. '''
    def computeRetentionForDay(self, n, os=None, version=None):
        data = self.data
        for year in data:
            for month in data[year]:

                # for each day, clear any existing retention counts
                for day in data[year][month]:
                    if day is 'user_activity':
                        continue
                    data[year][month][day]['retention'][n] = 0
                
                # for each user, determine if that user was active n days after acquisition
                for user_id, active_days in data[year][month]['user_activity'].iteritems():
                    if os and not self.matchesFilter(user_id, os):
                        continue # filter criterion not met
                    if version and not self.matchesFilter(user_id, version):
                        continue # filter criterion not met
                    day0 = list(active_days)[0] # user's first day (acquisition)
                    dt0 = datetime(year, month, day0)
                    dtn = dt0 + timedelta(n) # n-th day after acquisition
                    try:
                        if dtn.day in data[dtn.year][dtn.month]['user_activity'][user_id]:
                            # hooray, this user was active n days after acquisition
                            data[year][month][day0]['retention'][n] += 1
                    except KeyError:
                        pass # no data for day n; assume this user was not retained

    ''' returns True if the user_id contains the filter string '''
    def matchesFilter(self, user_id, filtr):
        # note that i'm (ab-)using the user_id field to perform filtering
        return filtr in user_id.split(DELIM)
