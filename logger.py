from flask import request, g
import logging

def log_access(page):
    logger = logging.getLogger()
    if (g.user):
        logger.info(f"Acceess {page} from {request.remote_addr}, User: {g.user['username']}")
    else:
        logger.info(f"Acceess {page} from {request.remote_addr}, User: Unknown")