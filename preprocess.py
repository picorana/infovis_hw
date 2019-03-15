import csv
from collections import defaultdict
from pprint import pprint
import json

EVENT_DATE = 3
FATALITIES = 23
COUNTRY = 5
STEP = 28
AIRPORT_NAME = 9
LOCATION = 4
WEATHER_CONDITION = 27
MAKE = 14
MODEL = 15
AMATEUR = 16
CARRIER = 22

def read_csv():
    with open('AviationData.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        linecount = 0
        output_dict = {}
        output_dict["Plane Crashes"] = list()
        year_dict = defaultdict(int)
        fatalities_dict = defaultdict(int)
        steps_dict = defaultdict(int)
        phase_dict = {}
        country_dict = {}
        phase_dict["Crash Phases"] = list()
        fatal_phase = defaultdict(int)

        for line in csv_reader:
            linecount += 1

            year_dict[line[EVENT_DATE].split('-')[0]] += 1
            if line[STEP] != 'Broad.Phase.of.Flight' and line[STEP] != '':
                steps_dict[line[STEP]] += 1
                if line[FATALITIES]!= '' and int(line[FATALITIES]) > 0:
                    fatal_phase[line[STEP]] += 1

            if line[FATALITIES] != 'Total.Fatal.Injuries' and line[FATALITIES] != '':
                fatalities_dict[line[EVENT_DATE].split('-')[0]] += int(line[FATALITIES])

        for elem in year_dict:
            new_dict = {}
            output_dict["Plane Crashes"].append(new_dict)
            new_dict["Crashes"] = year_dict[elem]
            new_dict["Date"] = elem
            new_dict["Fatalities"] = fatalities_dict[elem]

        for elem in steps_dict:
            new_dict = {}
            phase_dict["Crash Phases"].append(new_dict)
            new_dict["Phase"] = elem
            new_dict["Instances"] = steps_dict[elem]
            new_dict["Fatal"] = fatal_phase[elem]

        print(output_dict)
        print(phase_dict)

def read_causes():
    with open('AviationData2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        linecount = 0
        accidents_dict = defaultdict(int)
        accidents_dict2 = defaultdict(int)

        for line in csv_reader:
            linecount += 1
            print line[12]
            if line[12] != '':
                accidents_dict[line[12]] += 1

        s = 0
        for elem in accidents_dict:
            if accidents_dict[elem] > 1:
                s += 1
                accidents_dict2[elem] = accidents_dict[elem]

        print s
        print accidents_dict2


def create_for_scatterplots():
    f = open('AviationData.csv', 'r')
    csv_reader = csv.reader(f, delimiter=',')
    res = []

    linecount = 0
    outfile = open("air.json", 'w')

    for line in csv_reader:
        if linecount == 0:
            linecount+=1 
            continue
        linecount += 1

        new_dict = {}
        new_dict['Country'] = line[COUNTRY]
        
        new_dict['Weather_Condition'] = line[WEATHER_CONDITION].encode('utf-8').strip()
        new_dict['Phase'] = line[STEP].encode('utf-8').strip()
        
        try:
            new_dict['Airport_Name'] = line[AIRPORT_NAME].encode('utf-8').strip()
            new_dict['Location'] = line[LOCATION].encode('utf-8').strip()
        except:
            #print(line[AIRPORT_NAME])
            #print(line[LOCATION])
            continue
        new_dict['Make'] = line[MAKE].encode('utf-8').strip()
        new_dict['Model'] = line[MODEL].encode('utf-8').strip()
        new_dict['Carrier'] = line[CARRIER].encode('utf-8').strip()
        new_dict['Date'] = line[EVENT_DATE].encode('utf-8').strip()

        if line[AMATEUR] == 'Yes': continue
        if line[CARRIER] == '': continue


        res.append(new_dict)

        #if linecount == 20:
        #    break 

    #pprint(res)
    print(len(res))
    json.dump({'data':res}, outfile, indent=4)


create_for_scatterplots()

