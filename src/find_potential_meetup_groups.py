# Get key from https://secure.meetup.com/meetup_api/key/

# Using urllib2 in order to stick to core modules.

import urllib2
import datetime
import json
import argparse
import time

class FindPotentialMeetupGroups(object):
    LAT_CENTER = 34.022352
    LON_CENTER = -118.285117
    FAR_DISTANCE_KM = 250
    OLD_EVENT_DAYS = 150


    def __init__(self, api_key, contributor_name, get_member_ids):
        self.api_key = api_key
        self.contributor_name = contributor_name
        self.file_name = '/tmp/meetups_{}.txt'.format(self.contributor_name)
        self.get_member_ids = get_member_ids

    # Helper method - calc meetup distance
    def _distance_from_center(self, lat, lon):
        from math import sin, cos, sqrt, atan2, radians

        # approximate radius of earth in km
        R = 6373.0

        lat_center = radians(self.LAT_CENTER)
        lon_center = radians(self.LON_CENTER)
        lat_group = radians(lat)
        lon_group = radians(lon)

        dlon = lon_group - lon_center
        dlat = lat_group - lat_center

        a = sin(dlat / 2) ** 2 + cos(lat_center) * cos(lat_group) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance

    # Helper method - build API URL
    def _build_api_call_url(self, service_str, params_str=None):
        BASE_URL = 'https://api.meetup.com'
        full_params_str = 'key={}{}'.format(self.api_key, '&'+params_str if params_str else '')
        return '{}{}?{}'.format(BASE_URL, service_str, full_params_str)

    # Helper method - call API
    def _raw_api_call(self, url):
        jsn = ''
        sleep_time = 1
        while not jsn:
            try:
                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                code = response.getcode()
                res = response.read()
                jsn = json.loads(res)
            except Exception, e:
                print "Error: {}. Retrying in {} seconds...".format(e.message, sleep_time)
                time.sleep(sleep_time)
                sleep_time *= 2
        return jsn

    # Helper method - build URL and call API
    def _simple_api_call(self, service_str, params_str=None):
        return self._raw_api_call(self._build_api_call_url(service_str, params_str))

    # main method
    def run(self):

        members_pool = set()
        len_members = 0

        # Open file for write
        file_name = 'meetups_{}.txt'.format(self.contributor_name)
        print "Writing results to file: {}".format(file_name)
        with open(file_name, 'w') as f:

            # Groups
            fields = 'category,last_event,city,country,description,lat,lon,members,name,self'
            my_groups = self._simple_api_call('/self/groups','fields={}'.format(fields))

            for g in my_groups:
                distance_km = self._distance_from_center(g['lat'], g['lon'])
                last_event_days = 0 if 'last_event' not in g else (
                    datetime.datetime.now() - datetime.datetime.fromtimestamp(
                        int(str(g['last_event']['time'])[:-3]))).days

                # Filter irrelevant groups
                if g.get('category', {'name': 'Tech'})['name'] == 'Tech' \
                        and distance_km < self.FAR_DISTANCE_KM and last_event_days < self.OLD_EVENT_DAYS:

                    f.write('###Group:' + '\n')
                    group_txt = json.dumps({'actions': g['self']['actions'], 'id': g['id'], 'name': g['name'],
                                            'distance_km': int(distance_km), 'members': g['members'],
                                            'last_event_days': last_event_days})
                    print group_txt
                    f.write(group_txt + '\n')

                    # Members
                    if self.get_member_ids:

                        f.write('###Members:' + '\n')
                        res = self._simple_api_call('/2/members', 'group_id={}'.format(g['id']))

                        cont = (len(res['results']) > 0)
                        c = 0
                        while cont:
                            curr_batch = []
                            print 'reading...'
                            for x in res['results']:
                                curr_batch.append(x['id'])
                                if x['id'] not in members_pool:
                                    members_pool.add(x['id'])
                            # Get next batch
                            if 'next' in res['meta'] and res['meta']['next']:
                                res = self._raw_api_call(res['meta']['next'])
                            else:
                                cont = False
                            c += len(curr_batch)
                            print 'so far {} records.'.format(c)
                            f.write(json.dumps(list(curr_batch)) + '\n')

                        # Debug message
                        print "Group members: {} / Found members: {} / New members in pool: {} / New pct: {}%".format(g['members'], c,
                                                                                                       (len(members_pool) - len_members),
                                                                                                                      (float(len(members_pool) - len_members)/c*100)
                                                                                                       )
                        len_members = len(members_pool)


if __name__ == '__main__':
    # Get args
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', type=str, required=True)
    parser.add_argument('--contributor_name', type=str, required=True)
    parser.add_argument('--dont_list_member_ids', dest='get_member_ids', action='store_false')
    parser.set_defaults(get_member_ids=True)

    args = parser.parse_args()
    print args
    r = FindPotentialMeetupGroups(**vars(args))
    r.run()
