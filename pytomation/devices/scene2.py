from .interface2 import Interface2Device
from .interface import Command
from .state2 import State2

class Scene2(Interface2Device):
    STATES = [State2.UNKNOWN, State2.ACTIVE, State2.INACTIVE]
    COMMANDS = [Command.ACTIVATE, Command.DEACTIVATE, Command.LEVEL, Command.PREVIOUS, Command.TOGGLE, Command.INITIAL]

    def __init__(self, address=None, *args, **kwargs):
        devices = kwargs.get('devices', [])
        super(Scene2, self).__init__(address=address, *args, **kwargs)
        
        self._get_controlled_devices(devices)

    def _initial_vars(self, *args, **kwargs):
        super(Scene2, self)._initial_vars(*args, **kwargs)
        self._can_update = kwargs.get('update', False)
        self._controlled_devices={}
        self.mapped(command=Command.ON, mapped=Command.ACTIVATE)
        self.mapped(command=Command.OFF, mapped=Command.DEACTIVATE)

    def _get_controlled_devices(self, devices):
        for device in devices:
            try:
                for k, v in device.iteritems():
                    self._controlled_devices.update({k: v})
            except Exception, ex:
                pass

        if self._can_update:
            try:
                for interface in self._interfaces:
                    interface.update_scene(self.address, devices=self._controlled_devices )
            except Exception, ex:
                self._logger.warning("{name} Interface {interface} does not support updating scenes for {address}".format(
                                                                        name=self.name,
                                                                        interface=interface.name,
                                                                        address=self.address,
                                                                        ))


