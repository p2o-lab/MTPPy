class OPCUACommunicationObject:
    def __init__(self, opcua_node_obj, node_id):
        self.opcua_node_obj = opcua_node_obj
        self.node_id = node_id
        self.write_value_callback = opcua_node_obj.set_value
