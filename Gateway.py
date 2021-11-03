import Service_Logic
import Dummy_Service_2
import Dummy_Service

class Service_1_Handler(object):
    def datachange_notification(self,node,val,data):
        Service_1.Logic_sync(node,val)

class Service_2_Handler(object):
    def datachange_notification(self, node, val, data):
        Service_2.Logic_sync(node, val)

Service_1=Service_Logic.Logic_Class(Dummy_Service.D_Service(),2,Service_1_Handler())
Service_2=Service_Logic.Logic_Class(Dummy_Service.D_Service(),1,Service_2_Handler())