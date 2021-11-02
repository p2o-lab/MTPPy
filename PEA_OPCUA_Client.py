from opcua import Client
import Dummy_Service
from time import sleep



Test_Service=Dummy_Service.D_Service()

class SM_Handler():
    def datachange_notification(self,node,val,data):
        #Test_Service.Service.Service_SM.ex_command(val)
        print(val)


client=Client('opc.tcp://localhost:4840')
client.connect()
Current_state=client.get_node('ns=1;s=ns=1;s=D_Service_StateAutAut')
Current_command=client.get_node('ns=1;s=D_Service_StateAutAct')

handler=SM_Handler()
sub=client.create_subscription(500,handler)
handle=sub.subscribe_data_change(Current_command)

