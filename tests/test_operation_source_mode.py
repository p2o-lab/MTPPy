from src.mtppy.operation_elements import OperationSourceMode


def init_op_source_mode(op_mode='off',
                        state_channel=False,
                        src_mode='int',
                        src_channel=False,
                        allow_switch_to_offline=True):

    op_src_mode = OperationSourceMode()

    if allow_switch_to_offline:
        op_src_mode.allow_switch_to_offline_mode(True)

    if op_mode == 'op':
        op_src_mode.attributes['StateOpOp'].set_value(True)
    elif op_mode == 'aut':
        op_src_mode.attributes['StateAutOp'].set_value(True)
    elif op_mode == 'off':
        pass
    else:
        raise ValueError(f'Operation mode {op_mode} is unknown')

    if src_mode == 'ext':
        op_src_mode.attributes['SrcExtOp'].set_value(True)
    elif src_mode == 'int':
        pass
    else:
        raise ValueError(f'Source mode {src_mode} is unknown')

    if state_channel:
        op_src_mode.attributes['StateChannel'].set_value(True)

    if src_channel:
        op_src_mode.attributes['SrcChannel'].set_value(True)

    return op_src_mode


def is_initial_state(op_src_mode):
    return all([op_src_mode.attributes['StateChannel'].value == False,
                op_src_mode.attributes['StateOffAut'].value == False,
                op_src_mode.attributes['StateOpAut'].value == False,
                op_src_mode.attributes['StateAutAut'].value == False,
                op_src_mode.attributes['StateOffOp'].value == False,
                op_src_mode.attributes['StateOpOp'].value == False,
                op_src_mode.attributes['StateAutOp'].value == False,
                op_src_mode.attributes['StateOpAct'].value == False,
                op_src_mode.attributes['StateAutAct'].value == False,
                op_src_mode.attributes['StateOffAct'].value == True,
                op_src_mode.attributes['SrcChannel'].value == False,
                op_src_mode.attributes['SrcExtAut'].value == False,
                op_src_mode.attributes['SrcIntOp'].value == False,
                op_src_mode.attributes['SrcIntAut'].value == False,
                op_src_mode.attributes['SrcExtOp'].value == False,
                op_src_mode.attributes['SrcIntAct'].value == False,
                op_src_mode.attributes['SrcExtAct'].value == False])


def test_initial_state():
    op_src_mode = init_op_source_mode(op_mode='off', state_channel=False, src_mode='int', src_channel=False)
    assert is_initial_state(op_src_mode) == True


def test_state_channel_change():
    op_src_mode = init_op_source_mode()
    op_src_mode.attributes['StateChannel'].set_value(True)
    assert op_src_mode.attributes['StateChannel'].value == True
    op_src_mode.attributes['StateChannel'].set_value(False)
    assert op_src_mode.attributes['StateChannel'].value == False
    assert is_initial_state(op_src_mode) == True


def test_off_to_op_state_channel_false():
    op_src_mode = init_op_source_mode(op_mode='off', state_channel=False)
    op_src_mode.attributes['StateOpOp'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == False
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == True
    assert op_src_mode.attributes['StateAutAct'].value == False
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == False
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_off_to_op_state_channel_true():
    op_src_mode = init_op_source_mode(op_mode='off', state_channel=True)
    op_src_mode.attributes['StateOpAut'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == True
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == True
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == True
    assert op_src_mode.attributes['StateAutAct'].value == False
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == False
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_op_to_off_state_channel_false():
    op_src_mode = init_op_source_mode(op_mode='op', state_channel=False)
    op_src_mode.attributes['StateOffOp'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == False
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == False
    assert op_src_mode.attributes['StateOffAct'].value == True

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == False
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_op_to_off_state_channel_true():
    op_src_mode = init_op_source_mode(op_mode='op', state_channel=True)
    op_src_mode.attributes['StateOffAut'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == True
    assert op_src_mode.attributes['StateOffAut'].value == True
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == False
    assert op_src_mode.attributes['StateOffAct'].value == True

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == False
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_off_to_aut_state_channel_false():
    op_src_mode = init_op_source_mode(op_mode='off', state_channel=False)
    op_src_mode.attributes['StateAutOp'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == False
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == True
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == True
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_off_to_aut_state_channel_true():
    op_src_mode = init_op_source_mode(op_mode='off', state_channel=True)
    op_src_mode.attributes['StateAutAut'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == True
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == True
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == True
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == True
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_aut_to_off_state_channel_false():
    op_src_mode = init_op_source_mode(op_mode='aut', state_channel=False)
    op_src_mode.attributes['StateOffOp'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == False
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == False
    assert op_src_mode.attributes['StateOffAct'].value == True

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == False
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_aut_to_off_state_channel_true():
    op_src_mode = init_op_source_mode(op_mode='aut', state_channel=True)
    op_src_mode.attributes['StateOffAut'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == True
    assert op_src_mode.attributes['StateOffAut'].value == True
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == False
    assert op_src_mode.attributes['StateOffAct'].value == True

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == False
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_aut_to_op_state_channel_false():
    op_src_mode = init_op_source_mode(op_mode='aut', state_channel=False)
    op_src_mode.attributes['StateOpOp'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == False
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == True
    assert op_src_mode.attributes['StateAutAct'].value == False
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == False
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_aut_to_op_state_channel_true():
    op_src_mode = init_op_source_mode(op_mode='aut', state_channel=True)
    op_src_mode.attributes['StateOpAut'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == True
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == True
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == True
    assert op_src_mode.attributes['StateAutAct'].value == False
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == False
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_op_to_aut_state_channel_false():
    op_src_mode = init_op_source_mode(op_mode='op', state_channel=False)
    op_src_mode.attributes['StateAutOp'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == False
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == True
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == True
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_op_to_aut_state_channel_true():
    op_src_mode = init_op_source_mode(op_mode='op', state_channel=True)
    op_src_mode.attributes['StateAutAut'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == True
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == True
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == True
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == True
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_source_channel_change():
    op_src_mode = init_op_source_mode()
    op_src_mode.attributes['SrcChannel'].set_value(True)
    assert op_src_mode.attributes['SrcChannel'].value == True
    op_src_mode.attributes['SrcChannel'].set_value(False)
    assert op_src_mode.attributes['SrcChannel'].value == False
    assert is_initial_state(op_src_mode) == True


def test_int_to_ext_src_channel_false():
    op_src_mode = init_op_source_mode(op_mode='aut', src_channel=False)
    op_src_mode.attributes['SrcExtOp'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == False
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == True
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == False
    assert op_src_mode.attributes['SrcExtAct'].value == True


def test_int_to_ext_src_channel_true():
    op_src_mode = init_op_source_mode(op_mode='aut', src_channel=True)
    op_src_mode.attributes['SrcExtAut'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == False
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == True
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == True
    assert op_src_mode.attributes['SrcExtAut'].value == True
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == False
    assert op_src_mode.attributes['SrcExtAct'].value == True


def test_ext_to_int_src_channel_false():
    op_src_mode = init_op_source_mode(op_mode='aut', src_mode='ext', src_channel=False)
    op_src_mode.attributes['SrcIntOp'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == False
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == True
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == False
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == False
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == True
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_ext_to_int_src_channel_true():
    op_src_mode = init_op_source_mode(op_mode='aut', src_mode='ext', src_channel=True)
    op_src_mode.attributes['SrcIntAut'].set_value(True)

    assert op_src_mode.attributes['StateChannel'].value == False
    assert op_src_mode.attributes['StateOffAut'].value == False
    assert op_src_mode.attributes['StateOpAut'].value == False
    assert op_src_mode.attributes['StateAutAut'].value == False
    assert op_src_mode.attributes['StateOffOp'].value == False
    assert op_src_mode.attributes['StateOpOp'].value == False
    assert op_src_mode.attributes['StateAutOp'].value == False
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == True
    assert op_src_mode.attributes['StateOffAct'].value == False

    assert op_src_mode.attributes['SrcChannel'].value == True
    assert op_src_mode.attributes['SrcExtAut'].value == False
    assert op_src_mode.attributes['SrcIntOp'].value == False
    assert op_src_mode.attributes['SrcIntAut'].value == True
    assert op_src_mode.attributes['SrcExtOp'].value == False
    assert op_src_mode.attributes['SrcIntAct'].value == True
    assert op_src_mode.attributes['SrcExtAct'].value == False


def test_allowance_change_op_to_off_state_channel_false():
    op_src_mode = init_op_source_mode(op_mode='op', state_channel=False, allow_switch_to_offline=False)
    op_src_mode.attributes['StateOffOp'].set_value(True)
    assert op_src_mode.attributes['StateOpAct'].value == True
    assert op_src_mode.attributes['StateAutAct'].value == False
    assert op_src_mode.attributes['StateOffAct'].value == False


def test_allowance_change_op_to_off_state_channel_true():
    op_src_mode = init_op_source_mode(op_mode='op', state_channel=True, allow_switch_to_offline=False)
    op_src_mode.attributes['StateOffAut'].set_value(True)
    assert op_src_mode.attributes['StateOpAct'].value == True
    assert op_src_mode.attributes['StateAutAct'].value == False
    assert op_src_mode.attributes['StateOffAct'].value == False


def test_allowance_change_aut_to_off_state_channel_false():
    op_src_mode = init_op_source_mode(op_mode='aut', state_channel=False, allow_switch_to_offline=False)
    op_src_mode.attributes['StateOffOp'].set_value(True)
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == True
    assert op_src_mode.attributes['StateOffAct'].value == False


def test_allowance_change_aut_to_off_state_channel_true():
    op_src_mode = init_op_source_mode(op_mode='aut', state_channel=True, allow_switch_to_offline=False)
    op_src_mode.attributes['StateOffAut'].set_value(True)
    assert op_src_mode.attributes['StateOpAct'].value == False
    assert op_src_mode.attributes['StateAutAct'].value == True
    assert op_src_mode.attributes['StateOffAct'].value == False


class TestValue:
    def __init__(self):
        self.value = 0


def test_exit_offline_callback_off_to_op():
    test_value = TestValue()

    def callback_function():
        test_value.value = 10

    op_src_mode = init_op_source_mode(op_mode='off')
    op_src_mode.attributes['StateOpOp'].set_value(True)
    assert test_value.value == 0

    op_src_mode = init_op_source_mode(op_mode='off')
    op_src_mode.add_exit_offline_callback(callback_function)
    op_src_mode.attributes['StateOpOp'].set_value(True)
    assert test_value.value == 10


def test_exit_offline_callback_off_to_aut():
    test_value = TestValue()

    def callback_function():
        test_value.value = 10

    op_src_mode = init_op_source_mode(op_mode='off')
    op_src_mode.attributes['StateAutOp'].set_value(True)
    assert test_value.value == 0

    op_src_mode = init_op_source_mode(op_mode='off')
    op_src_mode.add_exit_offline_callback(callback_function)
    op_src_mode.attributes['StateAutOp'].set_value(True)
    assert test_value.value == 10
