from conductor.airfinder.messages import DownlinkMessageSpec
from conductor.airfinder.devices.node import Node
from conductor.util import Version


class TestTagDownlinkMessageSpecV1(DownlinkMessageSpec):
    """ Message Spec for Location Beacon v1.1.

    Caution:
        Internal Object
    """

    header = {
        'def': ['msg_type', 'msg_spec_vers'],
        'struct': '>BB',
        'defaults': [0x00, 0x01]
    }

    msg_types = {
        'Configuration': {
            'def': ['mask', 'event_delay', 'msgs_per_event', 'msg_delay'],
            'struct': '>BIBI',
            'defaults': [0x00, 0x0000012C, 0x02, 0x0000000F]
        },
        'Reset': {
            'def': ['reset_code'],
            'struct': '>I',
            'defaults': [0xd5837ed6]
        },
        'MakeLocation': {
            'def': ['test_tag_code'],
            'struct': '>I',
            'defaults': [0xd5837ed6]
        }
    }


class TestTag(Node):
    """ Represents an Airfinder Location. """

    @property
    def symble_version(self):
        pass

    @property
    def event_delay(self):
        return self._make_prop('eventDelay', int)

    @property
    def msgs_per_event(self):
        return self._make_prop('msgPerEvent', int)

    @property
    def msg_delay(self):
        return self._make_prop('messageDelay', int)

    subject_name = ''
    af_subject_name = ''
    application = '9a6d019a9385b231f658'

    @property
    def version(self):
        val = self._md.get("fwVersion")
        return Version(int(val[:2]), int(val[2:]), 0) if val else None

    @property
    def msg_spec_version(self):
        val = self._md.get("msgSpecVersion")
        return Version(0, int(val)) if val else None

    @classmethod
    def _get_spec(cls, vers):
        """ Returns: The Message Spec of the Test Tag. """
        return TestTagDownlinkMessageSpecV1()
