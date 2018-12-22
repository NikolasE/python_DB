#! /usr/bin/python3

import requests

# https://developer.deutschebahn.com/store/apis/info?name=FaSta-Station_Facilities_Status&version=v2&provider=DBOpenData

class Facility:
    # TODO: named tuple?
    # from collections import namedtuple
    # d_named = namedtuple("Employee", j.keys())(*j.values())

    type_strings = ['ELEVATOR', 'ESCALATOR']
    state_strings = ['ACTIVE', 'INACTIVE', 'UNKNOWN']

    def __init__(self, j):
        self.equipmentnumber = j['equipmentnumber']
        self.stationnumber = j['stationnumber']

        self.description = j['description']
        self.lat = j['geocoordY']
        self.lng = j['geocoordX']

        self.type = self.type_strings.index(j['type'])
        self.state = self.state_strings.index(j['state'])
        self.stateExplanation = j['stateExplanation']

        self.with_position = bool(self.lat)

    def file_string(self):
        lat = self.lat if self.with_position else -1
        lng = self.lng if self.with_position else -1

        return ("%s,%s,%s,%i,%i,%f,%f" % (self.state_strings[self.state], self.type_strings[self.type],
                                          self.description,
                                        self.equipmentnumber, self.stationnumber, lat, lng))

    def __str__(self):
        if not self.with_position:
            return ("%s %s (no position)" % (self.state_strings[self.state].capitalize(),
                                        self.type_strings[self.type].lower()))

        return ('%s %s at %.5f %.5f' % (self.state_strings[self.state].capitalize(),
                                        self.type_strings[self.type].lower(),
                                        self.lat, self.lng))


def write_state_file(facality_list, filename):
    out_file = open(filename, 'w')
    for f in facality_list:
        if not f.with_position:
            print("Facility without position")
            continue
        print(f.file_string())
        out_file.write(f.file_string() + '\n')
    out_file.close()


facility_url = "https://api.deutschebahn.com/fasta/v2/facilities"

headers = dict()
headers['Authorization'] = 'Bearer 94be553af10bed31932217dbd705338b'
headers['Accept'] = 'application/json'

payload = dict()
payload['state'] = 'ACTIVE,INACTIVE,UNKNOWN'  # no space(!)
payload['type'] = 'Elevator'

r = requests.get(facility_url, payload, headers=headers)
r.raise_for_status()
facilities = [Facility(f) for f in r.json()]

write_state_file(facilities, '/home/engelhard/Documents/python_DB/data/db_facilities.txt')
