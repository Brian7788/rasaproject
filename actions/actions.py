# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sqlite3

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

# class ActionDisplayOrder(Action):
#
#     def name(self) -> Text:
#         return "action_medicine"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         medicine_name = tracker.get_slot("name")
#         dispatcher.utter_message("{} is good.".format(medicine_name))
#
#         return []

class DbQueryingMethods:
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
        return conn

    def select_by_slot(conn,slot_value):

        cur = conn.cursor()
        cur.execute(f'''SELECT information from medicine WHERE name="{slot_value}"''')

        rows = cur.fetchall()

        if len(list(rows))<1:
            return  "There is no such medicine."
        else:
            for row in rows:
                message = "This kind of medicine" + row[0]
        return(message)



    # def select_by_slot1(conn,slot_value):
    #
    #     cur = conn.cursor()
    #     cur.execute(f'''SELECT * from appointmentlist WHERE username="{slot_value}"''')
    #
    #     rows = cur.fetchall()
    #
    #     if len(list(rows))<1:
    #         return  "There is no such medicine."
    #     else:
    #         for row in rows:
    #             message = "This kind of medicine" + row[0]
    #     return(message)

class QueryOrderDetails(Action):
    def name(self) -> Text:
        return "action_medicine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = DbQueryingMethods.create_connection(db_file="sarcdb/medicine.db")

        slot_value = tracker.get_slot("name")
        get_query_results = DbQueryingMethods.select_by_slot(conn=conn,slot_value=slot_value)
        dispatcher.utter_message(text=str(get_query_results))

        return

class appointment_setting(Action):
    def name(self) -> Text:
        return "action_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = sqlite3.connect("sarcdb/appointment.db")
        cu = conn.cursor()
        userName = tracker.get_slot("username")
        hospitalName = tracker.get_slot("hospitalname")
        appointmentTime = tracker.get_slot("appointmenttime")

        hospital_name_c =cu.execute(f'''SELECT hospitalname from appointmentlist Where hospitalname = "{hospitalName}"''')
        appointment_time_c = cu.execute(f'''SELECT appointmenttime from appointmentlist ''')

        if hospitalName == hospital_name_c.fetchone()[0]:
            dispatcher.utter_message(text="At that time, this hospital dental appointments were already full")
        else:
            s = "insert into appointmentlist(username, hospitalname, appointmenttime) values (?, ?, ?)"
            conn.execute(s, (userName, hospitalName,appointmentTime))

            conn.commit()
            dispatcher.utter_message(text="You have successfully made an appointment!")

        return []

class QueryAppointmentDetail(Action):
    def name(self) -> Text:
        return "action_queryappointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = DbQueryingMethods1.create_connection(db_file="sarcdb/appointment.db")

        slot_value = tracker.get_slot("username")
        get_query_results = DbQueryingMethods1.select_by_slot(conn=conn,slot_value=slot_value)
        dispatcher.utter_message(text=str(get_query_results))

        return

class DbQueryingMethods1:
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
        return conn

    def select_by_slot(conn,slot_value):

        cur = conn.cursor()
        cur.execute(f'''SELECT * from appointmentlist WHERE username="{slot_value}"''')
        # appo = cur.execute(f'''SELECT appointmenttime from appointmentlist WHERE username="{slot_value}"''')
        rows = cur.fetchall()

        if len(list(rows))<1:
            return  "There is no reservation information for you."
        else:
            for row in rows:
                message = "Your appointment information: " + row[0] +" booked hospital "+row[1]+ ", The scheduled time is "+ row[2]
        return(message)