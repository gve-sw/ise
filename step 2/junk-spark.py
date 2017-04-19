from ISE_Spark import ISE_Spark
from ISE_Print import ISE_Print
from lxml import etree

user = 'sponsor'
pwd  = 'Csap1'
ip="198.18.133.27"


ise=ISE_Print()

obj = ISE_Spark()


# roomID = obj.create_room('ISE Room')
# obj.add_user(roomID, 'micastel@cisco.com')
# listPendingUsers = ['Guest1', 'Guest2']
# obj.approve_pending(roomID, listPendingUsers)
idlist=['c012ca70-2057-11e7-b088-005056aabed5']
ise.all_guest_users(user, pwd, ip)
ise.guest_user_by_id(user, pwd, ip, idlist)