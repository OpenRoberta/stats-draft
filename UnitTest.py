#!/usr/bin/env python
# coding: utf-8

# In[18]:


import unittest
import DataAnalytics as fun


# In[34]:


comp_stat_error_dict_result={"Das ist ein Fehler":[{"time":"2019-07-01 00:00:01,000", "sessionId":"29371", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":"Das ist ein Fehler"},{"time":"2019-07-03 00:00:00,999", "sessionId":"29373", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":"Das ist 3in Fehler"}],"Das sind mehreree Fehler hier oder":[{"time":"2019-07-02 00:00:01,000", "sessionId":"29372", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":"Das sind mehreree Fehler hier oder"}]}
stat_error_dict_result={"Das ist ein Fehler":[{"time":"2019-07-01 00:00:01,000", "sessionId":"29371", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":"Das ist ein Fehler"}],"Das sind mehreree Fehler hier oder":[{"time":"2019-07-02 00:00:01,000", "sessionId":"29372", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":"Das sind mehreree Fehler hier oder"}],"Das ist 3in Fehler":[{"time":"2019-07-03 00:00:00,999", "sessionId":"29373", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":"Das ist 3in Fehler"}]}
json_list_fehler=[{"time":"2019-07-03 00:00:00,999", "sessionId":"29373", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":"Das ist 3in Fehler"},{"time":"2019-07-02 00:00:01,000", "sessionId":"29372", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":"Das sind mehreree Fehler hier oder"},{"time":"2019-07-01 00:00:01,000", "sessionId":"29371", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":"Das ist ein Fehler"}]
comp_list_actions_result=["RoboConnect","NewStart","Hola","ProgramRun","SimulationRun"]
json_list_actions=[{"time":"2019-07-05 00:00:00,000", "sessionId":"29375", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"RoboConnect","args":[{"LoggedIn":"false"}]}},{"time":"2019-07-04 00:00:01,001", "sessionId":"29374", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"NewStart","args":[{"LoggedIn":"false"}]}},{"time":"2019-07-03 00:00:00,999", "sessionId":"29373", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"Hola","args":[{"LoggedIn":"false"}]}},{"time":"2019-07-02 00:00:01,000", "sessionId":"29372", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"ProgramRun","args":[{"LoggedIn":"false"}]}},{"time":"2019-07-01 00:00:01,000", "sessionId":"29371", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"SimulationRun","args":[{"LoggedIn":"false"}]}}]
json_list_user=[{"time":"2019-07-03 00:00:02,999", "sessionId":"29372", "robotName":"ev3dev", "logLevel":"INFO", "message":{"action":"SimulationRun","args":[{"LoggedIn":"false"}]}},{"time":"2019-07-03 00:10:02,999", "sessionId":"29372", "robotName":"ev3dev", "logLevel":"INFO", "message":{"action":"SimulationRun","args":[{"LoggedIn":"false"}]}},{"time":"2019-07-01 00:00:01,000", "sessionId":"29371", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"SimulationRun","args":[{"LoggedIn":"false"}]}},{"time":"2019-07-01 00:00:01,000", "sessionId":"29372", "robotName":"ev3dev", "logLevel":"INFO", "message":{"action":"Initialization","args":[{"LoggedIn":"false"}]}}]
comp_list_action_user=["SimulationRun","Initialization"]
robot_user_count_result={"ev3dev":1,"ev3lejosv1":1}
list_session_id_user = {"2937203":[{"time":"2019-07-03 00:00:02,999", "sessionId":"29372", "robotName":"ev3dev", "logLevel":"INFO", "message":{"action":"SimulationRun","args":[{"LoggedIn":"false"}]}},{"time":"2019-07-03 00:10:02,999", "sessionId":"29372", "robotName":"ev3dev", "logLevel":"INFO", "message":{"action":"SimulationRun","args":[{"LoggedIn":"false"}]}}],"2937201":[{"time":"2019-07-01 00:00:01,000", "sessionId":"29372", "robotName":"ev3dev", "logLevel":"INFO", "message":{"action":"Initialization","args":[{"LoggedIn":"false"}]}}],"2937101":[{"time":"2019-07-01 00:00:01,000", "sessionId":"29371", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"SimulationRun","args":[{"LoggedIn":"false"}]}}]}
stat_dict_result={"ev3dev":{"SimulationRun":[{"time":"2019-07-03 00:00:02,999", "sessionId":"29372", "robotName":"ev3dev", "logLevel":"INFO", "message":{"action":"SimulationRun","args":[{"LoggedIn":"false"}]}},{"time":"2019-07-03 00:10:02,999", "sessionId":"29372", "robotName":"ev3dev", "logLevel":"INFO", "message":{"action":"SimulationRun","args":[{"LoggedIn":"false"}]}}],"Initialization":[{"time":"2019-07-01 00:00:01,000", "sessionId":"29372", "robotName":"ev3dev", "logLevel":"INFO", "message":{"action":"Initialization","args":[{"LoggedIn":"false"}]}}],"other":[]},"ev3lejosv1":{"SimulationRun":[{"time":"2019-07-01 00:00:01,000", "sessionId":"29371", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"SimulationRun","args":[{"LoggedIn":"false"}]}}],"Initialization":[],"other":[]}}
json_list_country=[{"time":"2019-07-05 00:00:10,000", "sessionId":"293475", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"Initialization","args":[{"LoggedIn":"false", "CountryCode":"De"}]}},{"time":"2019-07-05 00:00:00,000", "sessionId":"292375", "robotName":"ev3dev", "logLevel":"INFO", "message":{"action":"Initialization","args":[{"LoggedIn":"false", "CountryCode":"JP"}]}},{"time":"2019-07-05 00:00:00,100", "sessionId":"293751", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"Initialization","args":[{"LoggedIn":"false", "CountryCode":"De"}]}}]
country_dict_result ={"De":{"ev3lejosv1":[{"time":"2019-07-05 00:00:10,000", "sessionId":"293475", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"Initialization","args":[{"LoggedIn":"false", "CountryCode":"De"}]}},{"time":"2019-07-05 00:00:00,100", "sessionId":"293751", "robotName":"ev3lejosv1", "logLevel":"INFO", "message":{"action":"Initialization","args":[{"LoggedIn":"false", "CountryCode":"De"}]}}]},"JP":{"ev3dev":[{"time":"2019-07-05 00:00:00,000", "sessionId":"292375", "robotName":"ev3dev", "logLevel":"INFO", "message":{"action":"Initialization","args":[{"LoggedIn":"false", "CountryCode":"JP"}]}}]}}


# In[30]:


class myTest(unittest.TestCase):
    def test_line_validation_test(self):
        self.assertTrue(fun.validate_line("{\"time\":\"2019-07-01 00:00:01,000\", \"sessionId\":\"2937\", \"robotName\":\"ev3lejosv1\", \"logLevel\":\"INFO\", \"message\":{\"action\":\"SimulationRun\",\"args\":[{\"LoggedIn\":\"false\"}]}}")[0])
        self.assertFalse(fun.validate_line("{\"time\":\"2019-07-01 00:00:01,000\", sessionId\":\"2937\", \"robotName\":\"ev3lejosv1\", \"logLevel\":\"INFO\", \"message\":{\"action\":\"SimulationRun\",\"args\":[{\"LoggedIn\":\"false\"}]}}")[0])
        self.assertFalse(fun.validate_line("{\"time\":\"2019-07-01 00:00:01,000\", \"sessionId\":\"2937\", \"robotName\":\"ev3lejosv1\", \"logLvel\":\"INFO\", \"message\":{\"action\":\"SimulationRun\",\"args\":[{\"LoggedIn\":\"false\"}]}}")[0])

    def test_error_dict_test(self):
        self.assertEqual(fun.scan_input_list_actions(json_list_fehler)[1],stat_error_dict_result)
    def test_comp_error_dict_test(self):
        self.assertEqual(fun.filter_errors_and_sort(stat_error_dict_result),comp_stat_error_dict_result) 
    def test_list_action_test(self):
        self.assertEqual(fun.scan_input_list_actions(json_list_actions)[0],comp_list_actions_result)
    def test_robot_action_test(self):
        self.assertEqual(fun.scan_robot_names_userid_country_code(json_list_user,comp_list_action_user)[3],stat_dict_result)#Funktion, Ergebnis
    def test_robot_country_test(self):
        self.assertEqual(fun.country_codes_sort_robot(fun.scan_robot_names_userid_country_code(json_list_country,comp_list_action_user)[1]),country_dict_result)
    def test_robot_user_test(self):
        self.assertEqual(fun.create_robot_specific_user_num(list_session_id_user, fun.scan_robot_names_userid_country_code(json_list_user,comp_list_action_user)[4]),robot_user_count_result)
    def test_session_id_test(self):
        self.assertEqual(fun.scan_robot_names_userid_country_code(json_list_user,comp_list_action_user)[0],list_session_id_user)#funktion,ergebnis
    def test_verweildauer_test(self):
        self.assertEqual(fun.average_stay(list_session_id_user),10)
    def test_time_range_test(self):
        self.assertEqual(len(fun.reading_data_for_given_period("Zeitspannebetrachten",".txt","2019-07-02 00:00:00,000","2019-07-04 23:59:59,9990",True)),3)
    
if __name__ == "__main__":        
    unittest.main()


# In[ ]:




