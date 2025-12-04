import logging


def get_log_level(stage: str) -> int:
    if stage == "prod":
        return logging.INFO
    elif stage == "dev":
        return logging.INFO
    elif stage == "local":
        return logging.DEBUG
    else:
        return logging.WARNING


def log_setting(stage: str) -> logging.RootLogger:
    logging.basicConfig(
        level=get_log_level(stage),
        format="%(levelname)-9s  %(asctime)s [%(filename)s:%(lineno)d] %(message)s",
        # handlers=[logging.StreamHandler(encoding='utf-8')]
    )
    logger = logging.getLogger(__name__)
    return logger
