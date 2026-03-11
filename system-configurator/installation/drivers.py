from installation.installation_tools import Executer
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
            logger.add_record("This script requires root privileges. Please run with sudo.", status=LoggerStatus.FAILURE)
            sys.exit(1)

    def install(self):
        """Main entry point for driver installation"""
        try:
            self._enable_multilib()
            self._update_repositories()
            self._install_drivers()
            self._configure_mkinitcpio()
            self._configure_grub()
            self._post_install_checks()
        except Exception as e:
            logger.add_record(f"Installation failed: {str(e)}", status=LoggerStatus.FAILURE) 
            sys.exit(1)

    def _enable_multilib(self):
        """Safely enables multilib repository"""
        logger.add_record("[1/6] Configuring multilib repository...", status=LoggerStatus.SUCCESS)
        
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
                    logger.add_record("Multilib repository successfully enabled", status=LoggerStatus.SUCCESS)
                else:
                    logger.add_record("Multilib was already active", status=LoggerStatus.SUCCESS)
                    
        except Exception as e:
            logger.add_record(f"Failed to configure multilib: {str(e)}", status=LoggerStatus.FAILURE)
            raise

    def _update_repositories(self):
        """Refresh package databases"""
        logger.add_record("[2/6] Updating package databases...", status=LoggerStatus.SUCCESS)
        Executer.execute_command(["pacman", "-Syy"], "Repository update")

    def _install_drivers(self):
        """Install required driver packages"""
        logger.add_record("[3/6] Installing drivers...", status=LoggerStatus.SUCCESS)
        
        packages = [
            # NVIDIA (64-bit)
            "nvidia",
            "nvidia-utils",
            "nvidia-settings",
            # NVIDIA (32-bit multilib)
            "lib32-nvidia-utils",
            # Intel integrated GPU
            "xf86-video-intel",
            "vulkan-intel",
            # Optimus manager (AUR) for hybrid GPU switching
            "optimus-manager-git",
        ]
        
        Executer.execute_command(
            ["yay", "-S", "--needed", "--noconfirm"] + packages,
            "Driver packages installation"
        )
        
        Executer.execute_command(
            ["systemctl", "enable", "optimus-manager"],
            "Enable optimus-manager service"
        )

    def _configure_mkinitcpio(self):
        """Add NVIDIA modules to mkinitcpio so they load early at boot"""
        logger.add_record("[4/6] Configuring mkinitcpio for NVIDIA early KMS...", status=LoggerStatus.SUCCESS)
        
        nvidia_modules = "nvidia nvidia_modeset nvidia_uvm nvidia_drm"
        
        try:
            with open("/etc/mkinitcpio.conf", "r+") as f:
                content = f.read()
                
                # Replace MODULES=() or existing MODULES=(...) with nvidia modules
                import re
                updated = re.sub(
                    r"^MODULES=\(.*?\)",
                    f"MODULES=({nvidia_modules})",
                    content,
                    flags=re.MULTILINE
                )
                
                if updated != content:
                    f.seek(0)
                    f.write(updated)
                    f.truncate()
                    logger.add_record("NVIDIA modules added to mkinitcpio", status=LoggerStatus.SUCCESS)
                else:
                    logger.add_record("mkinitcpio MODULES already configured", status=LoggerStatus.SUCCESS)
                    
            Executer.execute_command(["mkinitcpio", "-P"], "Regenerate initramfs")
            
        except Exception as e:
            logger.add_record(f"Failed to configure mkinitcpio: {str(e)}", status=LoggerStatus.FAILURE)
            raise

    def _configure_grub(self):
        """Add NVIDIA DRM modeset parameters to GRUB kernel cmdline"""
        logger.add_record("[5/6] Configuring GRUB for NVIDIA DRM...", status=LoggerStatus.SUCCESS)
        
        nvidia_params = "nvidia_drm.modeset=1 nvidia_drm.fbdev=1"
        
        try:
            with open("/etc/default/grub", "r+") as f:
                content = f.read()
                
                import re
                # Add nvidia params to GRUB_CMDLINE_LINUX_DEFAULT if not present
                def add_params(match):
                    existing = match.group(1)
                    if "nvidia_drm.modeset" not in existing:
                        return f'GRUB_CMDLINE_LINUX_DEFAULT="{existing.rstrip()} {nvidia_params}"'
                    return match.group(0)
                
                updated = re.sub(
                    r'GRUB_CMDLINE_LINUX_DEFAULT="(.*?)"',
                    add_params,
                    content
                )
                
                if updated != content:
                    f.seek(0)
                    f.write(updated)
                    f.truncate()
                    logger.add_record("GRUB cmdline updated with NVIDIA DRM params", status=LoggerStatus.SUCCESS)
                else:
                    logger.add_record("GRUB cmdline already configured for NVIDIA DRM", status=LoggerStatus.SUCCESS)
                    
            Executer.execute_command(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"], "Regenerate GRUB config")
            
        except Exception as e:
            logger.add_record(f"Failed to configure GRUB: {str(e)}", status=LoggerStatus.FAILURE)
            raise

    def _post_install_checks(self):
        """Verify installation success"""
        logger.add_record("[6/6] Running post-install checks...", status=LoggerStatus.SUCCESS)
        
        Executer.execute_command(
            ["nvidia-smi"],
            "NVIDIA driver verification"
        )
        
        Executer.execute_command(
            ["glxinfo", "-B"],
            "Intel/Mesa driver verification"
        )
