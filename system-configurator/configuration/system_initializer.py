import subprocess

from logger import Logger, LoggerStatus
from configuration.software import AurBuilder

from installation import packages
from installation.drivers import GraphicDrivers
from installation.patches import PatchSystemBugs
from installation.daemons import Daemons

logger = Logger()

class SystemConfiguration:

    @staticmethod
    def run_command(command: str):
        try:
            subprocess.run(command, check=True, shell=True)
            logger.add_record(f"Executed: {command}", status=LoggerStatus.SUCCESS)
        except subprocess.CalledProcessError as e:
            logger.add_record(f"Command failed: {command}, Error: {e}", status=LoggerStatus.ERROR)

    @staticmethod
    def install_packages(package_names: list, aur: bool = False):
        installer = "yay -S --noconfirm" if aur else "sudo pacman -S --noconfirm"
        for package in package_names:
            SystemConfiguration.run_command(f"{installer} {package}")
            logger.add_record(f"Installed: {package}", status=LoggerStatus.SUCCESS)

    @staticmethod
    def start(*args):
        logger.add_record(f"[+] Starting assembly. Options {args}", status=LoggerStatus.SUCCESS)
        if args[0]: SystemConfiguration.__start_option_1()
        if args[1]: SystemConfiguration.__start_option_2()
        if args[2]: SystemConfiguration.__start_option_3()
        if args[3]: SystemConfiguration.__start_option_4()
        if args[4]: GraphicDrivers.build()

        Daemons.enable_all_daemons()
        PatchSystemBugs.enable_all_patches()

    @staticmethod
    def __start_option_1():
        SystemConfiguration.__create_default_folders()
        SystemConfiguration.__copy_bspwm_dotfiles()

    @staticmethod
    def __start_option_2():
        SystemConfiguration.run_command("sudo pacman -Sy")
        logger.add_record("[+] Updates Enabled", status=LoggerStatus.SUCCESS)

    @staticmethod
    def __start_option_3():
        AurBuilder.build()
        SystemConfiguration.install_packages(packages.BASE_PACKAGES)
        SystemConfiguration.install_packages(packages.AUR_PACKAGES, aur=True)
        logger.add_record("[+] Installed BSPWM Dependencies", status=LoggerStatus.SUCCESS)

    @staticmethod
    def __start_option_4():
        SystemConfiguration.install_packages(packages.DEV_PACKAGES)
        SystemConfiguration.install_packages(packages.GNOME_OFFICIAL_TOOLS)
        logger.add_record("[+] Installed Dev Dependencies", status=LoggerStatus.SUCCESS)

    @staticmethod
    def __create_default_folders():
        default_folders = "~/Videos ~/Documents ~/Downloads ~/Music ~/Desktop"
        SystemConfiguration.run_command("mkdir -p ~/.config")
        SystemConfiguration.run_command(f"mkdir -p {default_folders}")
        SystemConfiguration.run_command("cp -r ../Images/ ~/")
        logger.add_record("[+] Create default directories", status=LoggerStatus.SUCCESS)

    @staticmethod
    def __copy_bspwm_dotfiles():
        SystemConfiguration.run_command("cp -r ../config/* ~/.config/")
        SystemConfiguration.run_command("cp ../Xresources ~/.Xresources")
        SystemConfiguration.run_command("cp ../gtkrc-2.0 ~/.gtkrc-2.0")
        SystemConfiguration.run_command("cp -r ../local ~/.local")
        SystemConfiguration.run_command("cp -r ../themes ~/.themes")
        SystemConfiguration.run_command("cp ../xinitrc ~/.xinitrc")
        SystemConfiguration.run_command("cp -r ../bin/ ~/")
        logger.add_record("[+] Copy Dotfiles & GTK", status=LoggerStatus.SUCCESS)