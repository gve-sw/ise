import requests
import json
import ISE_Spark

### Run test ###

# To call the functions to create a room, add a user, post a first message on the room

"""
if not ACCESS_TOKEN:
        print("ACCESS_TOKEN variable needs to be populated before proceeding")
        exit()
"""

roomName = 'ISE-Test'
roomID = ISE_Spark.ISE_Spark().create_room(roomName)
# print(roomID)

# roomID of the Test room created, called ISE-PendingGuest
#roomID = 'Y2lzY29zcGFyazovL3VzL1JPT00vNDlmMTU4ZDAtMTFhMS0xMWU3LTllNjMtYWY1YTJhNDRmYjcw'


if roomID:
    # email = 'cpietra@cisco.com'
    email = 'micastel@cisco.com'
    user = ISE_Spark.ISE_Spark().add_user(roomID, email)   #add_user() can be True or False
    
#Testing adding a user to the room (sponsor already in the room)
    #if not user:
        #print("Error adding sponsor to the room. Exiting...")
        #exit()

# First message in the room:

    text = 'List of guests that are waiting the approval from the sponsor to have access to the wireless network'
"""
    message = post_message(roomID, text)
    if not message:
        print("Error posting message to the room. Exiting...")
        exit()
"""

# If there is any user that is waiting to be approved, call the function: approve_pending(roomID,pendingUserList)

listPendingUsers = ['Guest1', 'Guest2']
listApproved = []

ISE_Spark.ISE_Spark().approve_pending(roomID, listPendingUsers)
