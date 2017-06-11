
#---Sunset and sunrise times come from "https://sunrise-sunset.org/api"---
#
#Parameters:
#   -> lat: Latitude in decimal degrees. Required.
#   -> lng: Longitude in decimal degrees. Required.
#   -> date: Date in YYYY-MM-DD format. Also accepts other date formats and even relative date formats.
#      If not present, date defaults to current date. Optional.
#   -> callback: Callback function name for JSONP response. Optional.
#   -> formatted: 0 or 1 (1 is default). Time values in response will be expressed following ISO 8601
#      and day_length will be expressed in seconds. Optional.
#
#Sample requests:
# -> https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400
# -> https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400&date=today
# -> https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400&date=2017-06-04
#
#-------------------------------------------------------------------------
#
#---def returnSunInfo(day)------------------------------------------------
#
#Parameters:
#   ->day: either 'today'/'yesterday'/etc. or 'yyyy-mm-dd'
#
#Return format:
# function returns a json string:
#   '{
#        "status":{
#                "successful": bool , "message": string
#               },
#        "details":{
#               "sunrise"   : str ,
#               "sunset"    : str ,
#               "civil_twilight_rise"   : str ,
#               "civil_twilight_set"    : str ,
#               "nautical_twilight_rise": str ,
#               "nautical_twilight_set" : str ,
#           }
#   }'
#
#-------------------------------------------------------------------------

import urllib3
import json
import datetime

class sunInfo(object):
    
    def __init__(self, latitude, longitude, time_zone):
        self.GMT_timeShift = time_zone
        self.lat = latitude
        self.long = longitude

    def convCorrectTimeZone(self, s_time, shift):
        temp = datetime.datetime.strptime(s_time,"%I:%M:%S %p").time()
        return temp.replace(hour=temp.hour+shift)

    def changeLocation(self, latitude, longitude, GMT_zone):
        self.lat = latitude
        self.long = longitude
        self.GMT_timeShift = GMT_zone    


    def getSunDetails(self, day="today"):
        self.result = {}
        urllib3.disable_warnings()
        self.http = urllib3.PoolManager()
        self.r = self.http.request('GET','https://api.sunrise-sunset.org/json?lat='+self.lat+'&lng='+self.long+'&date='+day)
        self.r_json = json.loads(self.r.data.decode('utf-8'))
        

        if(self.r.status != 200):
            self.result['status'] = {
                    'successful':False,
                    'message':'check date format, request failed. Status code: '+str(r.status)
                }
        else:
            self.result['status'] = {
                    'successful':True,
                    'message':'request was successful'
                }


        self.response = self.r_json['results']

        self.sunrise = self.convCorrectTimeZone(self.response['sunrise'],self.GMT_timeShift)
        self.sunset = self.convCorrectTimeZone(self.response['sunset'],self.GMT_timeShift)
        self.civil_twilight_rise = self.convCorrectTimeZone(self.response['civil_twilight_begin'],self.GMT_timeShift)
        self.civil_twilight_set = self.convCorrectTimeZone(self.response['civil_twilight_end'],self.GMT_timeShift)
        self.nautical_twilight_rise = self.convCorrectTimeZone(self.response['nautical_twilight_begin'],self.GMT_timeShift)
        self.nautical_twilight_set = self.convCorrectTimeZone(self.response['nautical_twilight_end'],self.GMT_timeShift)

        #convert datetime.time to string for compatability with other languages
        self.result['details'] = {
                'sunrise'   :str(self.sunrise),
                'sunset'    :str(self.sunset),
                'civil_twilight_rise'   :str(self.civil_twilight_rise),
                'civil_twilight_set'    :str(self.civil_twilight_set),
                'nautical_twilight_rise':str(self.nautical_twilight_rise),
                'nautical_twilight_set' :str(self.nautical_twilight_set)
            }

        #convert result to json string format
        return json.dumps(self.result)



#-------------------------------------------------------------------------


































    
