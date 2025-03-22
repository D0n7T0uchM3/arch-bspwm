from logger import Logger, LoggerStatus
from configuration.software import AurBuilder

from installation import packages
from installation.installation_tools import Executer
from installation.drivers import GraphicDrivers
from installation.patches import PatchSystemBugs
from installation.daemons import Daemons

logger = Logger()

class SystemConfiguration:
    @staticmethod
    def install_packages(package_names: list, aur: bool = False):
        installer = "yay -S --noconfirm" if aur else "sudo pacman -S --noconfirm"

        for package in package_names:
            Executer.execute_command([installer, package], f"Installation of {package}")

    @staticmethod
    def start(*args):
        logger.add_record(f"[+] Starting assembly. Options {args}", status=LoggerStatus.SUCCESS)
        if args[0]: SystemConfiguration.__start_option_1()
        if args[1]: SystemConfiguration.__start_option_2()
        if args[2]: SystemConfiguration.__start_option_3()
        if args[3]: GraphicDrivers.install()

        Daemons.enable_all_daemons()
        PatchSystemBugs.enable_all_patches()

    @staticmethod
    def __start_option_1():
        SystemConfiguration.__create_default_folders()
        SystemConfiguration.__copy_bspwm_dotfiles()

    @staticmethod
    def __start_option_2():
        Executer.execute_command(["sudo", "pacman", "-Sy"], f"Updates")

    @staticmethod
    def __start_option_3():
        AurBuilder.build()
        SystemConfiguration.install_packages(packages.PACKAGES)
        logger.add_record("[+] Installed BSPWM Dependencies", status=LoggerStatus.SUCCESS)

    @staticmethod
    def __create_default_folders():
        default_folders = "~/Videos ~/Documents ~/Downloads ~/Music ~/Desktop"
        Executer.execute_command(["mkdir", "-p", "~/.config", default_folders], f"Creating all default folders")
        Executer.execute_command(["cp", "-r", "../Images", "~/"], f"Images copying")
        logger.add_record("[+] Create default directories", status=LoggerStatus.SUCCESS)

    @staticmethod
    def __copy_bspwm_dotfiles():
        Executer.execute_command(["cp", "../Xresources", "~/.Xresources"], f"Xresources folder copying")
        Executer.execute_command(["cp", "../gtkrc-2.0", "~/.gtkrc-2.0"], f"gtkrc-2.0 folder copying")
        Executer.execute_command(["cp", "-r", "../local", "~/.local"], f"local folder copying")
        Executer.execute_command(["cp", "../xinitrc", "~/.xinitrc"], f"xinitrc folder copying")
        Executer.execute_command(["cp", "-r", "../bin/", "~/"], f"bin folder copying") # TODO if it is bin or .bin
        logger.add_record("[+] Copy Dotfiles & GTK", status=LoggerStatus.SUCCESS)