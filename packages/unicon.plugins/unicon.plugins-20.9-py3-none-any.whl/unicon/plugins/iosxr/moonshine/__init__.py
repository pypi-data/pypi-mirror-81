__author__ = "Isobel Ormiston <iormisto@cisco.com>"

from unicon.plugins.iosxr.moonshine.settings import MoonshineSettings
from unicon.plugins.iosxr.moonshine.statemachine import MoonshineSingleRpStateMachine, MoonshineDualRpStateMachine
from unicon.plugins.iosxr.__init__ import IOSXRServiceList, IOSXRHAServiceList, IOSXRSingleRpConnection, IOSXRDualRpConnection
from unicon.plugins.iosxr.moonshine.connection_provider import MoonshineSingleRpConnectionProvider, MoonshineDualRpConnectionProvider
from unicon.plugins.iosxr.moonshine.pty_backend import MoonshineSpawn

class MoonshineSingleRpConnection(IOSXRSingleRpConnection):
    os = 'iosxr'
    series = 'moonshine'
    chassis_type = 'single_rp'    
    state_machine_class = MoonshineSingleRpStateMachine
    connection_provider_class = MoonshineSingleRpConnectionProvider
    subcommand_list = IOSXRServiceList
    settings = MoonshineSettings()

    def setup_connection(self):
        """ Creates a Session and spawns a connection
        """

        # Spawn a connection to the device
        self.spawn = MoonshineSpawn(self.parse_spawn_command(self.start[0]),
                                    settings=self.settings,
                                    log=self.log,
                                    logfile=self.logfile)

        # Instantiate connection provider
        self.connection_provider = self.connection_provider_class(self)


class MoonshineDualRpConnection(IOSXRDualRpConnection):
    os = 'iosxr'
    series = 'moonshine'
    chassis_type = 'dual_rp'
    state_machine_class = MoonshineDualRpStateMachine
    connection_provider_class = MoonshineDualRpConnectionProvider
    subcommand_list = IOSXRHAServiceList
    settings = MoonshineSettings()

    def setup_connection(self):
        """ Initializes the session and spawns connection
        to each RP
        """

        # Spawn each handle
        self.a.spawn = MoonshineSpawn(self.parse_spawn_command(self.a.start),
                                      settings=self.settings,
                                      log=self.log,
                                      logfile=self.logfile)
        self.b.spawn = MoonshineSpawn(self.parse_spawn_command(self.b.start),
                                      settings=self.settings,
                                      log=self.log,
                                      logfile=self.logfile)

        # Instantiate connection provider
        self.connection_provider = self.connection_provider_class(self)
