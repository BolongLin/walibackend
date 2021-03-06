from base.exceptions import WLException
from .order_protocol_sm import order_protocol_operate_sm
from ordersys.models import OrderProtocol


def execute_order_protocol_state_machine(user, order, action, parameter):

    def state_dealer(state_next, **kwargs):
        protocol.p_operate_status = state_next
        # Let log system aware of operator
        protocol.operator = user
        protocol.save()

    try:
        protocol = order.current_protocol
    except OrderProtocol.DoesNotExist:
        raise WLException(403, "Protocol does not exist")
    except OrderProtocol.MultipleObjectsReturned:
        raise AssertionError("Multiple processing protocol")

    try:
        order_protocol_operate_sm.execute_transition(
            protocol.p_operate_status,
            action,
            {"order": order, "protocol": protocol, "parameter": parameter, "user": user},
            state_dealer
        )
    except order_protocol_operate_sm.ActionError:
        raise WLException(403, "Action error")
    except order_protocol_operate_sm.StateDoesNotExist:
        raise
