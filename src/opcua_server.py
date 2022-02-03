from opcua import Server
from src.service import Service


class Marshalling(object):
    def import_services(self, services):
        self.services = services

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)
        callback = self.find_set_callback(node)
        if callback is not None:
            callback(val)

    def find_set_callback(self, node_id):
        layers = node_id.nodeid.Identifier.split('.')
        if layers[0] == 'services':
            service_name = layers[1]
            if layers[2] == 'source_mode':
                var_name = layers[3]
                return self.services[service_name].source_mode.variables[var_name].callback


def run_opcua_server():
    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # common server structure
    idx = server.register_namespace('1')
    objects = server.get_objects_node()
    services_folder = objects.add_folder(idx, "services")

    services = {'data_collection':
                    Service(tag_name='data_collection', opcua_server=server, opcua_ns=idx)
                }

    subscription_list = []

    # Service data collection
    for service in services.values():
        service_folder = services_folder.add_folder(idx, service.tag_name)

        for folder in ['source_mode', 'operation_mode', 'procedure_control', 'command_control']:
            service_section_folder = service_folder.add_folder(idx, folder)
            for variable in eval(f'service.{folder}.variables.values()'):
                service_section_folder.add_variable(variable.opcua_node_obj.nodeid, variable.name, variable.init_value).\
                    set_writable(variable.writable)
                opcua_node = server.get_node(variable.opcua_node_obj)
                subscription_list.append(opcua_node)

    # starting!
    server.start()

    # Subscription
    handler = Marshalling()
    handler.import_services(services)
    sub = server.create_subscription(500, handler)
    handle = sub.subscribe_data_change(subscription_list)


run_opcua_server()
