import Service_Logic_2
import Dummy_Service

class Service_1_Handler(object):
    def datachange_notification(self,node,val,data):
        i=1
        #Service_1.Sync_and_execute(node,val)

class Service_2_Handler(object):
    def datachange_notification(self, node, val, data):
        Service_2.Sync_and_execute(node, val)

address='opc.tcp://localhost:4840'

#Service_1=Service_Logic_2.Sync_Class(Dummy_Service.D_Service(),2,Service_1_Handler(),address)
Service_2=Service_Logic_2.Sync_Class(Dummy_Service.D_Service(),1,Service_2_Handler(),address)