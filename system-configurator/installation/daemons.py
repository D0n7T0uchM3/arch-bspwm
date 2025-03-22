from installation.installation_tools import Executer
from logger import Logger
import os
from typing import NamedTuple

logger = Logger()

class ServiceConfig(NamedTuple):
    """Represents a system service configuration to be enabled and/or started."""
    name: str
    start: bool

class Daemons:
    @staticmethod
    def enable_all_daemons():
        """Enables and starts essential system daemons/services."""
        services_to_enable = [
            ServiceConfig("NetworkManager", True),
            ServiceConfig("bluetooth.service", True),
            # TODO: Add usb mount daemon,...
        ]

        for service in services_to_enable:
            Daemons.__manage_service(
                service_name=service.name,
                enable=True,
                start=service.start
            )

    @staticmethod
    def __manage_service(service_name: str, enable: bool = False, start: bool = False):
        """
        Manages system services using systemctl with optimal command execution.
        
        Args:
            service_name: Name of the service to manage
            enable: Whether to enable the service to start on boot
            start: Whether to immediately start the service
        """
        # Determine if sudo is needed based on current user
        sudo_required = os.geteuid() != 0
        base_cmd = ["sudo"] if sudo_required else []

        try:
            if enable and start:
                # Most efficient: single command to enable and start
                command = base_cmd + ["systemctl", "enable", "--now", service_name]
                Executer.execute_command(command, f"Enabling and starting {service_name}")
            elif enable:
                command = base_cmd + ["systemctl", "enable", service_name]
                Executer.execute_command(command, f"Enabling {service_name}")
            elif start:
                command = base_cmd + ["systemctl", "start", service_name]
                Executer.execute_command(command, f"Starting {service_name}")
            else:
                logger.warning(f"No action specified for service {service_name}. Skipping.")
                
        except Exception as e:
            logger.error(f"Failed to manage service {service_name}: {str(e)}")
            raise  # Re-raise to allow caller handling if needed
