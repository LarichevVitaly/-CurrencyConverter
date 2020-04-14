import logging


def configure_logger(logging_level=logging.INFO):
    logger = logging.getLogger("server")

    logger.setLevel(logging_level)

    base_logger = logging.getLogger("root")
    base_logger.disabled = True
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    main_handler = logging.StreamHandler()
    main_handler.setFormatter(formatter)

    logger.addHandler(main_handler)
