from settings import UserInterface
from logger import Logger, LoggerStatus


def main():
    logger = Logger()

    try:
        logger.add_record("Starting User Interface", status=LoggerStatus.SUCCESS)
        UserInterface.start()
        logger.add_record("Installation Completed Successfully", status=LoggerStatus.SUCCESS)
        print("Installation Completed!")
    except Exception as e:
        logger.add_record(f"Error during installation: {str(e)}", status=LoggerStatus.FAILURE)
        print(f"Installation failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
