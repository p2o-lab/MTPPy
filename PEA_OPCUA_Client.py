from opcua import Client
import Dummy_Service
from time import sleep


#TODO Valentin fragen ob man dem handler auch ein object übergeben kann ansonsten muss für jeden Service etc
# eine eigene Handler classer erstellt werden anstatt immer die gleicher zu verwenden vllt mithilfe einer weiteren klasse ?

#Test_Service=Dummy_Service.D_Service()
class SM_Handler(object):
    def datachange_notification(self,node,val,data):
        Gate2.gateway(node,val)

class Gate():
    def __init__(self,Service,ns):
        self.Service=Service
        self.ns=ns
        client = Client('opc.tcp://localhost:4840')
        client.connect()

        handler = SM_Handler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(client.get_node(f'ns={self.ns};s=Service_Control').get_children())

    def gateway(self,node,val):
        client2=Client('opc.tcp://localhost:4840')
        client2.connect()
        #curr_nsi = node.nodeid.NamespaceIndex
        curr_nsi = self.ns
        curr_name = node.nodeid.Identifier
        print(f'{curr_name}: {val}')
        # TODO nachdenke von wo und wie der automatische state im falle der bedienung vor ort laufen soll da hier lediglich
        # die kommunikation von pea zu server stattfindet und nicht subskr basiert gearbeitet werden kann (warsch while
        # var xy true akt server within seconds...)

        if curr_name in ['StateAutOp', 'StateOpOp', 'StateOffOp'] and client2.get_node(
                f'ns={curr_nsi};s=StateChannel').get_value() == False and val == True:

            if curr_name == 'StateAutOp':
                self.Service.Service.StateAutOp = True
                self.Service.Service.StateOpOp = False
                self.Service.Service.StateOffOp = False

            if curr_name == 'StateOpOp':
                self.Service.Service.StateAutOp = False
                self.Service.Service.StateOpOp = True
                self.Service.Service.StateOffOp = False

            if curr_name == 'StateOffOp':
                self.Service.Service.StateAutOp = False
                self.Service.Service.StateOpOp = False
                self.Service.Service.StateOffOp = True

            self.Service.Service.Service_operation_mode()
            self.Service.Service.update_feedback()

            client2.get_node(f'ns={curr_nsi};s=StateAutOp').set_value(self.Service.Service.StateAutOp)
            client2.get_node(f'ns={curr_nsi};s=StateOpOp').set_value(self.Service.Service.StateOpOp)
            client2.get_node(f'ns={curr_nsi};s=StateOffOp').set_value(self.Service.Service.StateOffOp)

            client2.get_node(f'ns={curr_nsi};s=StateAutAut').set_value(self.Service.Service.StateAutAut)
            client2.get_node(f'ns={curr_nsi};s=StateOpAut').set_value(self.Service.Service.StateOpAut)
            client2.get_node(f'ns={curr_nsi};s=StateOffAut').set_value(self.Service.Service.StateOffAut)

            client2.get_node(f'ns={curr_nsi};s=StateOpAct').set_value(self.Service.Service.StateOpAct)
            client2.get_node(f'ns={curr_nsi};s=StateAutAct').set_value(self.Service.Service.StateAutAct)
            client2.get_node(f'ns={curr_nsi};s=StateOffAct').set_value(self.Service.Service.StateOffAct)

        if curr_name in ['CommandOp', 'CommandInt', 'CommandExt']:
        #if curr_name in ['CommandOp']:
            if curr_name == 'CommandOp' and self.Service.Service.StateOpAct == True:
                self.Service.Service.Service_SM.ex_command(val)
                self.Service.Service.update_feedback()

            if curr_name == 'CommandInt' and self.Service.Service.StateAutAct == True \
                    and self.Service.Service.SrcIntAct == True:
                self.Service.Service.Service_SM.ex_command(val)
                self.Service.Service.update_feedback()

            if curr_name == 'CommandExt' and self.Service.Service.StateAutAct == True \
                    and self.Service.Service.SrcExtAct == True:
                self.Service.Service.Service_SM.ex_command(val)
                self.Service.Service.update_feedback()

            client2.get_node(f'ns={curr_nsi};s=StateCur').set_value(self.Service.Service.StateCur)
            client2.get_node(f'ns={curr_nsi};s=CommandEn').set_value(self.Service.Service.CommandEn)
            client2.disconnect()




Gate2=Gate(Dummy_Service.D_Service(),1)
