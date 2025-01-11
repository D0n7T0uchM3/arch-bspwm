import subprocess
from configuration.system_initializer import SystemConfiguration
from logger import Logger, LoggerStatus

logger = Logger()


class UserInterface:
    @staticmethod
    def start():
        UserInterface.welcome_banner()
        install_params = UserInterface.get_params()
        logger.add_record("Installation parameters collected successfully.", status=LoggerStatus.SUCCESS)
        SystemConfiguration.start(*install_params)

    @staticmethod
    def welcome_banner():
        try:
            subprocess.run(["sh", "assets/startup.sh"], check=True)
            logger.add_record("Displayed welcome banner successfully.", status=LoggerStatus.SUCCESS)
        except subprocess.CalledProcessError as e:
            logger.add_record(f"Failed to display welcome banner: {e}", status=LoggerStatus.ERROR)
        except Exception as e:
            logger.add_record(f"Unexpected error during welcome banner: {str(e)}", status=LoggerStatus.ERROR)

    @staticmethod
    def is_verify_response(text: str) -> bool:
        return "y" in text.strip().lower()

    @staticmethod
    def get_params():
        options = [
            "Install all dotfiles?",
            "Update Arch DataBase?",
            "Install BSPWM Dependencies?",
            "Install Nvidia & Intel Drivers?"
        ]

        install_params = []
        for index, option in enumerate(options, start=1):
            response = UserInterface.prompt_user(f"{index}) {option} [Y/n]: ")
            install_params.append(response)

        logger.add_record(f"User responses: {install_params}", status=LoggerStatus.SUCCESS)
        return install_params

    @staticmethod
    def prompt_user(prompt: str) -> bool:
        while True:
            try:
                response = input(prompt).strip()
                if response == "":
                    return True  # Default to 'yes' if nothing is entered
                return UserInterface.is_verify_response(response)
            except Exception as e:
                logger.add_record(f"Error getting user input: {str(e)}", status=LoggerStatus.ERROR)
                print("Invalid input, please try again.")
