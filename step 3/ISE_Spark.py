""""
ISE API
Authors:
-Chiara Pietra (cpietra@cisco.com)
-Mike Castellana (micastel@cisco.com)
Date: April 2017

The functions on this class allow to:
-Create a Spark room
-Add sponsors to the room
-Post messages on the room
-Get the last message from the room
-Receive a list of pending users from ISE and allow the sponsor to approve the access to the network (or not) from the Spark room

WARNING:
This script is meant for educational purposes only.
Any use of these scripts and tools is at
our own risk. There is no guarantee that
they have been through thorough testing in a
comparable environment and we are not
responsible for any damage or data loss
incurred with their use.

INFORMATION:
If you have further questions about this API and script, please contact GVE. Here are the contact details:
   For internal Cisco employees, please contact GVE at http://go2.cisco.com/gve
   For Cisco partners, please open a case at www.cisco.com/go/ph
"""

import requests
import json
import time
from ISE_Print import ISE_Print

class ISE_Spark:


    # The ACCESS_TOKEN belongs to the ISE-Guest Bot

    ACCESS_TOKEN = 'OTBhY2ExM2UtNmU4My00NzExLWI4OGQtNjgzNjAwNGM2MTg1NDk4YmVjMjQtZjY4'
    HEADERS = {"Content-type" : "application/json; charset=utf-8",
               "Authorization" : "Bearer " + ACCESS_TOKEN}


### Functions ###


    # ### Create a room with the sponsor
    # Function create_room(self, name)
    # (self, name) = sets the room's name

    def create_room(self, name):

        URL = 'https://api.ciscospark.com/v1/rooms'
        PAYLOAD = {"title" : name}

        room = requests.post(url=URL, json=PAYLOAD, headers=self.HEADERS)
    
    # Testing: check if the request was successful and return the ID assigned to the room
        if room.status_code == 200:
            print("Room %s was created successfully" % name)
            return room.json()['id']
        else:
            exit()
    

    # ### Add the sponsor
    # Function add_user(self, roomID, email)
    # (self, roomID, email) = ID returned when calling create_room(name) and sponsor's email address (other parameters could be included)

    def add_user(self, roomID, email):
    
        URL = "https://api.ciscospark.com/v1/memberships"
        PAYLOAD = {"roomId": roomID, "personEmail": email}

        user = requests.post(url=URL, json=PAYLOAD, headers=self.HEADERS)

    # Testing: check if the request was successful and return True or False
        if user.status_code == 200:
            print("User was successfully added to the room")
            return True
        else:
            # print(user.status_code)
            # print(user.json()['message'])
            return False


    # ### Post message on the Spark room
    # Function post_message(self, roomID, text)
    # (self, roomID, text) = ID returned when calling create_room(name) and text to post

    def post_message(self, roomID, text):

        URL = "https://api.ciscospark.com/v1/messages"
        PAYLOAD = {"roomId": roomID, "text": text}

        message = requests.post(url=URL, json=PAYLOAD, headers=self.HEADERS)

    # Testing: check if the request was successful and return True or False
        if message.status_code == 200:
            print("Message was successfully posted into the room")
            return True
        else:
            # print(message.status_code)
            # print(message.text)
            return False


    # ### Get message from the sponsor on Spark to make a decision on ISE
    # Function get_last_message(self, roomID) returns the last message posted by the SPONSOR on the room roomID
    # The room works with the Bot's token if the parameter "mentionedPeople": "me" is included on the request
    # The last message is obtained because of the ("max":1) on the request

    # The Bot needs to be mentioned on the message @ISE-Guest (requirement on a group room, where more than one sponsor may be needed)
    # The information about the message is inside "items"
    # The most recent message is number [0] in the dictionary called "response"
    # Inside "items" I can find the message "id" and "text" that contains

    def get_last_message(self, roomID):

        URL = "https://api.ciscospark.com/v1/messages"
        PAYLOAD = {"roomId": roomID, "mentionedPeople": 'me', "max": 1}

        message = requests.get(url=URL, params=PAYLOAD, headers=self.HEADERS)
        # get_last_message() --> params (get functions) instead of json (post functions)

    # Testing: check if the message was successfully obtained
        if message.status_code == 200:
            print("Message can be successfully obtained from the room")
            response = json.loads(message.text)
            try:                # If there is an answer from the sponsor refered to the Bot
                msg = {'id': response['items'][0]['id'], 'text': response['items'][0]['text']}
                print(msg['id'])
                return msg
            except:             # No messages yet to the Bot
                msg = {'id': '0', 'text': 'NO MESSAGES'}
                print(msg['id'])
                return msg      
        else:   
            # print(message.status_code)
            # print (message.text)
            exit() 


    # ### Ask the sponsor to approve or deny a guest that is in pending status
    # Function approve_pending(self, roomID, pendingUserList, pending_names, approved_users)
    # (self, roomID, pendingUserList, pending_names, approved_users) = ID returned when calling create_room(name),list of pending users on ISE ...
    # ... pending names = from the pending users, we can identify the user by its name and company on the Spark room
    # ... approved_users = list of users that the sponsor decided to approve

    def approve_pending(self, roomID, pendingUserList, pending_names, approved_users):

    # lastMessage is a variable where I save the last message in 

        lastMessage = self.get_last_message(roomID)
        # print lastMessage
        msg_ID = lastMessage['id']

    # The sponsor will be asked for every pending user if he decides to accept or deny access to the network.
    # Once it accepts the first user that asked accesing the network, it will move to next one and so.
        iter = 0
        for user in pendingUserList:
            message = "Approve user: " + pending_names[iter] + "?"
            self.post_message(roomID, message)
            answered = False
    
            while not(answered):            # While answered == False
                lastMessage = self.get_last_message(roomID)
                # print lastMessage
                if not(lastMessage['id'] == msg_ID):
                                            # If lastMessage['id']==msg_ID then the sponsor have not answer yet
                    msg_ID = lastMessage['id']
                    if lastMessage['text'].upper() == "ISE-GUEST Y":
                            # ISE has to approve this guest --> add it to approved_users
                        approved_users.append(user)
                        answered = True
                    elif lastMessage['text'].upper() == "ISE-GUEST N":
                            # ISE does not approve this guest (stays as pending, but the program moves on)
                        answered = True
                    else:
                        message = "Please decide if you want to approve this user (Y) or deny this user (N)"
                        self.post_message(roomID, message)
                else:
                    time.sleep(5)
            iter = iter+1
        pendingUserList = []
        pending_names = []
    # We remove the content from the pending list once the users have been accepted or not so that the Spark room does not ask again about the same user
