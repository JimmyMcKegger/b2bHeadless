import logging
import colorama

colorama.init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "INFO": colorama.Fore.GREEN,
        "WARNING": colorama.Fore.YELLOW,
        "ERROR": colorama.Fore.RED,
        "CRITICAL": colorama.Fore.MAGENTA,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, colorama.Fore.WHITE)
        message = super().format(record)
        level_name = f"{log_color}{record.levelname}{colorama.Fore.RESET}"
        return message.replace(record.levelname, level_name)


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter("%(levelname)s:\t%(message)s - %(asctime)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

"""
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
 """
