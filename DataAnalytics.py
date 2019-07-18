import re
import json
import csv
import datetime
from datetime import timedelta
from difflib import SequenceMatcher
import time
import argparse

use_console = False

if use_console:
    parser = argparse.ArgumentParser(prog="Statistics Analytics",description="Analyse the statisticLog. Process arguments to specify the analysis")
    parser.add_argument("input_file_name", help="enter the name of the file here")
    parser.add_argument("output_file_name",help="enter name of output file here")
    parser.add_argument("--start_date",help="analysing only a specific period: enter start date here (%Y-%m-%d %H:%M:%S,%f). Default: None",default=0)
    parser.add_argument("--end_date",help="for analysing a specific period: enter the end date here (%Y-%m-%d %H:%M:%S,%f). Default: None",default=0)
    parser.add_argument("--checker",help="Boolean value that enables a checker, whether correct data is used. Default: False",default=False)
    parser.add_argument("--err_stat",help="boolean value, whether an error statistics file shall be created. Default: False",type=bool,default=False)
    parser.add_argument("--normal_stat_creation",help="boolean value whether a statistics file shall be generated or not. Default: True",type=bool,default=True)
    parser.add_argument("--normal_stat_action",help="boolean value whether the statistics file contains the robot action per robot. Default: True",type=bool,default=True)
    parser.add_argument("--normal_stat_country",help="boolean value whether the statistics file contains the country per robot. Default: True",type=bool,default=True)
    parser.add_argument("--normal_stat_rest",help="boolean value whether the statistics file contains every action taken place. Default: False",type=bool,default=False)
    args = parser.parse_args()
    print(args)
    FILE_INPUT = args.input_file_name
    FILE_OUTPUT = args.output_file_name
    DATA_START = args.start_date
    DATA_END = args.end_date
    ERR_STAT = args.err_stat
    NORMAL_STAT_CREATION = args.normal_stat_creation
    NoSt_Action= args.normal_stat_action
    NoSt_Country=args.normal_stat_country
    NoSt_Rest =args.normal_stat_rest
    CHECKER = args.checker
else:
    FILE_INPUT = "stat-2019-06.txt"  
    FILE_OUTPUT = "oolas"
    DATA_START = "2019-06-09 00:00:00,001"
    DATA_END = 0 #"2019-06-10 23:59:59,999"
    ERR_STAT = False
    NORMAL_STAT_CREATION = True
    NoSt_Action=True
    NoSt_Country=True
    NoSt_Rest=False
    CHECKER=False


def check_bracket(json_string):
    counter, counter2, counter3 = 0, 0, 0
    counter += json_string.count("{")
    counter -= json_string.count("}")
    counter2 += json_string.count("[")
    counter2 -= json_string.count("]")
    counter3 += json_string.count("(")
    counter3 -= json_string.count(")")
    if counter == 0 and counter2==0 and counter3 == 0:
        return True
    print("SyntaxError: Bracket")
    return False

def check_syntax(json_string):
    try:
        json_str = json.loads(json_string)
        return True
    except:
        print("SyntaxError")
        return False

def check_elements(json_string):
    if json_string.find("\", \"sessionId\":\"")>=0:
        if json_string.find("\", \"robotName\":\"") >=0:
            if json_string.find("\", \"logLevel\":\"")>=0:
                if json_string.find("\", \"message\":")>=0:
                    return True
    print("Error: Element is missing or broken")
    return False

def validate_line(line):
    data_group = re.search("({.*})",line)
    try:
        json_string = data_group.group()
    except:
        return False, ""
    if data_group and check_bracket(json_string) and check_syntax(json_string) and check_elements(json_string):
        json_dict = json.loads(data_group.group())
        return True, json_dict
    return False, ""

def more_than_2_days(date_two, date_one):
    datetimeFormat = '%Y-%m-%d %H:%M:%S,%f'
    diff = datetime.datetime.strptime(date_one, datetimeFormat)\
    - datetime.datetime.strptime(date_two, datetimeFormat)
    if diff.days >=2:
        return True
    return False

def get_time_difference(date_two, date_one):
    datetimeFormat = '%Y-%m-%d %H:%M:%S,%f'
    diff = datetime.datetime.strptime(date_one, datetimeFormat)\
    - datetime.datetime.strptime(date_two, datetimeFormat)
    return (diff.days/(24*60*60)+diff.seconds)/60

def average_stay(dicti_user):
    time_sum = 0
    user = 0
    for x in dicti_user:
        if len(dicti_user[x])>=2:
            time_sum =time_sum + get_time_difference(dicti_user[x][0]["time"],dicti_user[x][-1]["time"])
            user = user + 1
    if user >= 1:
        return (time_sum / user)
    return 0

def date_later(date_expect_later,date_expect_earlier):
    datetimeFormat = '%Y-%m-%d %H:%M:%S,%f'
    return datetime.datetime.strptime(date_expect_later, datetimeFormat)>=datetime.datetime.strptime(date_expect_earlier, datetimeFormat)

def similarity_ratio(string_a, string_b, value):
    return SequenceMatcher(None, string_a, string_b).ratio()>=value

def append_or_new_list(element, key, dicti):
    if key not in dicti:
        dicti[key]=[]
    dicti[key].append(element)
    
def reduce_list_unique_elements(liste):
    new_set = {0,1}
    return_list =[]
    for x in liste:
        if x not in new_set:
            new_set.add(x)
            return_list.append(x)
    return return_list

def reading_data_for_given_period(name,dstart,dend,checker):
    json_list = []
    start = time.time()
    
    #1
    with open((name),"rt") as data_file: 
        if checker:
            for line in data_file:
                val_line=validate_line(line)
                if val_line[0]:
                    json_list.append(validate_line(line)[1])
        else:
            for line in data_file:
                try:
                    a=re.search("({.*})",line).group()
                    json_list.append(json.loads(a))
                except:
                    pass
                
    end = time.time()
    print(end-start, "checker")
    
    #2
    json_list = sorted(json_list, key = lambda i: i['time'])
    begin,end = 0,-1
    def date_checker(dend,dstart):
        if dend!=0 and dstart!=0:
            return date_later(dend,dstart)
        else:
            return True
    
    if dstart != 0 or dend !=0:
        b_not_found = True
        if date_checker:
            for counter, element in enumerate(json_list):
                if dstart!=0:
                    if date_later(element["time"],dstart) and b_not_found:
                        print("ja")
                        begin=counter
                        b_not_found = False
                        if dend==0:
                            json_list.append(0)
                            return json_list[begin:end]
                if dend!=0:
                    if date_later(element["time"],dend):
                        print("ne")
                        end = counter
                        return json_list[begin:end]
        else:
            print("Check entered dates. Try switch them")
    else:
        print("No date entered. I will use everything")
    json_list.append(0)
    return json_list[begin:end]

def scan_input_list_actions(input_list):
    stat_error_dict = {}
    list_actions=[]
    for element in input_list:
        #1
        if not "action" in element["message"]:
            append_or_new_list(element, element["message"],stat_error_dict)
        else: 
            list_actions.append(element["message"]["action"])
    return reduce_list_unique_elements(list_actions),stat_error_dict

def scan_robot_names_userid_country_code(input_list,comp_list_actions):
    list_session_id={}
    country_codes_dict={}
    robot_names =[]
    stat_dict ={}
    robot_user_count = {}
    #1
    for element in input_list:   
        if element["robotName"] not in robot_names:
            robot_user_count[element["robotName"]]=[]
            robot_names.append(element["robotName"])
            stat_dict[element["robotName"]]={}
            for action in comp_list_actions:
                stat_dict[element["robotName"]][action]=[]
            stat_dict[element["robotName"]]["other"]=[] 
        try:
            stat_dict[element["robotName"]][element["message"]["action"]].append(element)
        except:
            stat_dict[element["robotName"]]["other"].append(element)

        #2

        s_id = str(element["sessionId"])+element["time"][8:10]
        case_a =s_id not in list_session_id
        case_b = str(int(s_id)-1) not in list_session_id
        case_c = str(int(s_id)-2) not in list_session_id
        s_id = str(s_id)
        if case_a and case_b and case_c:
            list_session_id[s_id]= [element]

        elif not case_a:
            list_session_id[s_id].append(element)
        elif not case_b:
            list_session_id[str(int(s_id)-1)].append(element)
        elif not case_c:
            if more_than_2_days(list_session_id[str(int(s_id)-2)][0]["time"],element["time"]):
                list_session_id[s_id]=[element]

            else:
                list_session_id[str(int(s_id)-2)].append(element)
        #3
        try:
            append_or_new_list(element, element["message"]["args"][0]["CountryCode"], country_codes_dict)   
        except:
            pass
    return list_session_id, country_codes_dict, robot_names, stat_dict, robot_user_count

def create_robot_specific_user_num(user_id_list,robot_user_count):
    for element in user_id_list:
        robot_name_set={0,1}
        for i in user_id_list[element]:
            if "action" in i["message"]:
                if not i["robotName"] in robot_name_set and i["message"]["action"] != "Initialization":
                    robot_user_count[i["robotName"]].append(1)
                    robot_name_set.add(i["robotName"])
            
    for x in robot_user_count:
        robot_user_count[x]= len(robot_user_count[x])
    return robot_user_count

def filter_errors_and_sort(error_dict):
    comp_stat_error_dict = {}
    error_messages_list = []
    t = True
    for x in error_dict:
        if len(error_messages_list)>0:
            for y in error_messages_list:
                t=True
                if similarity_ratio(y[0],x,0.85):
                    y.append(x)
                    t=False
                    break
            if t:
                error_messages_list.append([x])              
        else:
            error_messages_list.append([x])

    for x in error_messages_list:
        comp_stat_error_dict[x[0]]=[]
        for y in x:
            comp_stat_error_dict[x[0]].extend(error_dict[y])
    return comp_stat_error_dict


def country_codes_sort_robot(country_codes_dict):
    for country_code in country_codes_dict:
        c_dict={}
        for i in country_codes_dict[country_code]:
            append_or_new_list(i, i["robotName"], c_dict)
        country_codes_dict[country_code]=c_dict
    return country_codes_dict


def write_csv_normal_stat(create_nor_stat, start,end,name,comp_list_actions,list_session_id,robot_user_count,stat_dict,country_codes_dict,robot_names,nor_action,nor_country,nor_rest):
    with open(name+'_stat_analysis.csv','w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["durchschnittliche Verweildauer: ", average_stay(list_session_id),"Zeitraum von: ",start,"bis: ",end])
        writer.writerow(["Gesamtnutzer:", len(list_session_id)])
        writer.writerow([""]+robot_names)
        robot_user_count_list=["User"]
        for x in robot_user_count:
            robot_user_count_list.append(robot_user_count[x])
        writer.writerow(robot_user_count_list)
        if nor_action:   
            writer.writerow([])
            for action in comp_list_actions:
                action_count_list = []
                action_count_list.append(action)
                for i in robot_names:
                    action_count_list.append(len(stat_dict[i][action]))
                writer.writerow(action_count_list)
        if nor_country:
            writer.writerow([])
            for country_code in country_codes_dict:
                country_write_list = []
                country_write_list.append(country_code)
                for i in robot_names:
                    if i in country_codes_dict[country_code]:
                        country_write_list.append(len(country_codes_dict[country_code][i]))
                    else:
                        country_write_list.append(0)
                writer.writerow(country_write_list)

        
        if nor_rest:
            writer.writerow([])
            writer.writerow(["UserId","Uhrzeit","Roboter Name","Action/Fehler","CountryCode"])

            for element in list_session_id:
                for i in list_session_id[element]:
                    liste = [element]
                    liste.append(i["time"])
                    liste.append(i["robotName"])
                    if "action" in i["message"]:
                        liste.append(i["message"]["action"])
                    else:
                        liste.append(i["message"])
                    if "action" in i["message"]:
                        if i["message"]["action"] == "Initialization":
                            if "CountryCode" in i["message"]["args"][0]:
                                liste.append(i["message"]["args"][0]["CountryCode"])
                    writer.writerow(liste)
          
def write_csv_error_stat(robot_names,comp_stat_error_dict,name):
    err_ticket_robot = {}
    with open(name+'_stat_error_analysis.csv','w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([""]+robot_names)
        for x in comp_stat_error_dict:
            error_list = [x]
            for name in robot_names:
                count = 0
                for i in comp_stat_error_dict[x]:
                    if i["robotName"]==name:
                        count = count +1
                error_list.append(count)
            writer.writerow(error_list)
        for x in comp_stat_error_dict:
            if similarity_ratio(x,"Exception. Error ticket: E-",0.7):
                for i in comp_stat_error_dict[x]:

                    append_or_new_list(re.sub("\D", "", i["message"]),i["robotName"],err_ticket_robot)
        #print(err_ticket_robot)
        fin_list=[""]
        for name in robot_names:
            if name in err_ticket_robot:
                fin_list.append(','.join(err_ticket_robot[name]))
            else:
                fin_list.append("")
        writer.writerow(fin_list)    

        
def main(name,output_name,create_err_stat,create_nor_stat,nor_action,nor_country,nor_rest,checker,start,end):
    json_list = reading_data_for_given_period(name,start,end,checker)
    comp_list_actions,stat_error_dict = scan_input_list_actions(json_list)
    list_session_id, country_codes_dict, robot_names, stat_dict, robot_user_count = scan_robot_names_userid_country_code(json_list,comp_list_actions)
    robot_user_count_fin = create_robot_specific_user_num(list_session_id,robot_user_count)
    comp_stat_error_dict = filter_errors_and_sort(stat_error_dict)
    country_codes_dict_sorted = country_codes_sort_robot(country_codes_dict)
    if create_nor_stat:
        write_csv_normal_stat(create_nor_stat,start,end,output_name,comp_list_actions,list_session_id,robot_user_count_fin,stat_dict,country_codes_dict_sorted, robot_names,nor_action,nor_country,nor_rest)
    if create_err_stat:
        write_csv_error_stat(robot_names,comp_stat_error_dict,output_name)

start = time.time()
main(FILE_INPUT,FILE_OUTPUT,ERR_STAT,NORMAL_STAT_CREATION,NoSt_Action,NoSt_Country,NoSt_Rest,CHECKER,DATA_START,DATA_END)
end = time.time()
print(end-start, "gesamt")


