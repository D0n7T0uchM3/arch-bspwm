from installation_tools import Executer
import sys
import os
from logger import Logger, LoggerStatus

logger = Logger()

class GraphicDrivers:
    def __init__(self):
        self._check_root_privileges()
        logger.add_record("Initializing graphic drivers installation...", status=LoggerStatus.SUCCESS)

    def _check_root_privileges(self):
        if os.getuid() != 0:
            logger.add_record("This script requires root privileges. Please run with sudo.", LoggerStatus.FAILURE)
            sys.exit(1)

    def install(self):
        """Main entry point for driver installation"""
        try:
            self._enable_multilib()
            self._update_repositories()
            self._install_drivers()
            self._post_install_checks()
        except Exception as e:
            logger.add_record(f"Installation failed: {str(e)}", LoggerStatus.FAILURE)
            sys.exit(1)

    def _enable_multilib(self):
        """Safely enables multilib repository"""
        logger.add_record("[1/4] Configuring multilib repository...", LoggerStatus.SUCCESS)
        
        try:
            with open("/etc/pacman.conf", "r+") as f:
                lines = f.readlines()
                f.seek(0)
                
                multilib_active = False
                changed = False
                
                for line in lines:
                    if line.strip().startswith("#[multilib]"):
                        f.write(line.lstrip("#"))
                        changed = True
                        multilib_active = True
                    elif multilib_active and line.strip().startswith("#Include"):
                        f.write(line.lstrip("#"))
                        changed = True
                        multilib_active = False
                    else:
                        f.write(line)
                
                f.truncate()
                
                if changed:
                    logger.add_record("Multilib repository successfully enabled", LoggerStatus.SUCCESS)
                else:
                    logger.add_record("Multilib was already active", LoggerStatus.SUCCESS)
                    
        except Exception as e:
            logger.add_record(f"Failed to configure multilib: {str(e)}", LoggerStatus.FAILURE)
            raise

    def _update_repositories(self):
        """Refresh package databases"""
        logger.add_record("[2/4] Updating package databases...", LoggerStatus.SUCCESS)
        Executer.execute_command(["pacman", "-Syy"], "Repository update")

    def _install_drivers(self):
        """Install required driver packages"""
        logger.add_record("[3/4] Installing drivers...", LoggerStatus.SUCCESS)
        
        packages = [
            # 64-bit
            "mesa", 
            "nvidia", 
            "nvidia-utils",
            "xf86-video-intel", 
            "vulkan-intel",
            "optimus-manager",

            # 32-bit (multilib) - for 32-bit systems only
            # "lib32-mesa",          
            # "lib32-nvidia-utils",  
            # "lib32-vulkan-intel"
        ]
        
        Executer.execute_command(
            ["pacman", "-S", "--needed", "--noconfirm"] + packages,
            "Driver packages installation"
        )
        
        # Enable optimus-manager service
        Executer.execute_command(
            ["systemctl", "enable", "optimus-manager"],
            "Enable optimus-manager service"
        )

    def _post_install_checks(self):
        """Verify installation success"""
        logger.add_record("[4/4] Running post-install checks...", LoggerStatus.SUCCESS)
        
        # Check NVIDIA driver
        Executer.execute_command(
            ["nvidia-smi"],
            "NVIDIA driver verification"
        )
        
        # Check Intel driver
        Executer.execute_command(
            ["glxinfo", "-B"],
            "Intel driver verification"
        )
