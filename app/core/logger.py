import logging


logger = logging.getLogger("ai-platform")

logger.setLevel(logging.INFO)


handler = logging.StreamHandler()

logger.addHandler(handler)