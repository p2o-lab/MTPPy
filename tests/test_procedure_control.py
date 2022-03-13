from mtppy.procedure_control import ProcedureControl
from mtppy.procedure import Procedure
from test_operation_source_mode import init_op_source_mode


def init_procedure_control(op_mode='off', src_mode='int'):
    op_src_mode = init_op_source_mode(op_mode=op_mode, src_mode=src_mode)
    dummy_procedures = {0: Procedure(0, 'first'),
                        1: Procedure(1, 'second', is_default=True),
                        2: Procedure(2, 'third'),
                        3: Procedure(3, 'forth')}
    procedure_control = ProcedureControl(procedures=dummy_procedures, service_op_src_mode=op_src_mode)
    return procedure_control


def check_valid_states(procedure_control, set_function, change_allowed=False):
    for proc_id in range(4):
        set_function(proc_id)
        if change_allowed:
            assert procedure_control.attributes['ProcedureReq'].value == proc_id
        else:
            assert procedure_control.attributes['ProcedureReq'].value == 0


def check_invalid_states(procedure_control, set_function):
    set_function(0)
    set_function(10)
    assert procedure_control.attributes['ProcedureReq'].value == 0


def test_set_procedure_op():
    procedure_control = init_procedure_control(op_mode='off')
    check_valid_states(procedure_control, procedure_control.set_procedure_op, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_op)

    procedure_control = init_procedure_control(op_mode='op')
    check_valid_states(procedure_control, procedure_control.set_procedure_op, change_allowed=True)
    check_invalid_states(procedure_control, procedure_control.set_procedure_op)

    procedure_control = init_procedure_control(op_mode='aut')
    check_valid_states(procedure_control, procedure_control.set_procedure_op, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_op)


def test_set_procedure_int():
    procedure_control = init_procedure_control(op_mode='off', src_mode='ext')
    check_valid_states(procedure_control, procedure_control.set_procedure_int, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_int)

    procedure_control = init_procedure_control(op_mode='off', src_mode='int')
    check_valid_states(procedure_control, procedure_control.set_procedure_int, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_int)

    procedure_control = init_procedure_control(op_mode='op', src_mode='ext')
    check_valid_states(procedure_control, procedure_control.set_procedure_int, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_int)

    procedure_control = init_procedure_control(op_mode='op', src_mode='int')
    check_valid_states(procedure_control, procedure_control.set_procedure_int, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_int)

    procedure_control = init_procedure_control(op_mode='aut', src_mode='ext')
    check_valid_states(procedure_control, procedure_control.set_procedure_int, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_int)

    procedure_control = init_procedure_control(op_mode='aut', src_mode='int')
    check_valid_states(procedure_control, procedure_control.set_procedure_int, change_allowed=True)
    check_invalid_states(procedure_control, procedure_control.set_procedure_int)


def test_set_procedure_ext():
    procedure_control = init_procedure_control(op_mode='off', src_mode='ext')
    check_valid_states(procedure_control, procedure_control.set_procedure_ext, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_ext)

    procedure_control = init_procedure_control(op_mode='off', src_mode='int')
    check_valid_states(procedure_control, procedure_control.set_procedure_ext, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_ext)

    procedure_control = init_procedure_control(op_mode='op', src_mode='ext')
    check_valid_states(procedure_control, procedure_control.set_procedure_ext, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_ext)

    procedure_control = init_procedure_control(op_mode='op', src_mode='int')
    check_valid_states(procedure_control, procedure_control.set_procedure_ext, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_ext)

    procedure_control = init_procedure_control(op_mode='aut', src_mode='ext')
    check_valid_states(procedure_control, procedure_control.set_procedure_ext, change_allowed=True)
    check_invalid_states(procedure_control, procedure_control.set_procedure_ext)

    procedure_control = init_procedure_control(op_mode='aut', src_mode='int')
    check_valid_states(procedure_control, procedure_control.set_procedure_ext, change_allowed=False)
    check_invalid_states(procedure_control, procedure_control.set_procedure_ext)


def test_set_procedure_cur():
    procedure_control = init_procedure_control(op_mode='op')
    for proc_id in range(4):
        procedure_control.set_procedure_op(proc_id)
        procedure_control.set_procedure_cur()
        assert procedure_control.attributes['ProcedureCur'].value == proc_id

    procedure_control.set_procedure_op(0)
    procedure_control.set_procedure_cur()
    procedure_control.set_procedure_op(10)
    procedure_control.set_procedure_cur()
    assert procedure_control.attributes['ProcedureCur'].value == 0
    
