class OPCUACommunicationObject:
    def __init__(self, opcua_node_obj, node_id):
        """
        Represents a communication object for OPC UA for an attribute instance.
        :param opcua_node_obj: OPC UA node object.
        :param node_id: OPCUA node id.
        """
        self.opcua_node_obj = opcua_node_obj
        self.node_id = node_id
        self.write_value_callback = opcua_node_obj.set_value
