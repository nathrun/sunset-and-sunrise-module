
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


#times from here are GMT time
GMT_timeShift = 0
lat = "00.0000000"
long = "00.0000000"

def convCorrectTimeZone(s_time, shift):
    temp = datetime.datetime.strptime(s_time,"%I:%M:%S %p").time()
    return temp.replace(hour=temp.hour+shift)
    

def getSunDetails(day="today"):
    result = {}
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    r = http.request('GET','https://api.sunrise-sunset.org/json?lat='+lat+'&lng='+long+'&date='+day)
    r_json = json.loads(r.data.decode('utf-8'))
    

    if(r.status != 200):
        result['status'] = {
                'successful':False,
                'message':'check date format, request failed. Status code: '+str(r.status)
            }
    else:
        result['status'] = {
                'successful':True,
                'message':'request was successful'
            }


    response = r_json['results']

    sunrise = convCorrectTimeZone(response['sunrise'],GMT_timeShift)
    sunset = convCorrectTimeZone(response['sunset'],GMT_timeShift)
    civil_twilight_rise = convCorrectTimeZone(response['civil_twilight_begin'],GMT_timeShift)
    civil_twilight_set = convCorrectTimeZone(response['civil_twilight_end'],GMT_timeShift)
    nautical_twilight_rise = convCorrectTimeZone(response['nautical_twilight_begin'],GMT_timeShift)
    nautical_twilight_set = convCorrectTimeZone(response['nautical_twilight_end'],GMT_timeShift)

    #convert datetime.time to string for compatability with other languages
    result['details'] = {
            'sunrise'   :str(sunrise),
            'sunset'    :str(sunset),
            'civil_twilight_rise'   :str(civil_twilight_rise),
            'civil_twilight_set'    :str(civil_twilight_set),
            'nautical_twilight_rise':str(nautical_twilight_rise),
            'nautical_twilight_set' :str(nautical_twilight_set)
        }

    #convert result to json string format
    return json.dumps(result)


if __name__ == '__main__':
    print('today:')
    print(getSunDetails('today'))
    print('tomorrow:')
    print(getSunDetails('tomorrow'))
