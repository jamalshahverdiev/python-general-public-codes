
def return_mutliple_type_logs(current_app):
    current_app.logger.info("Info from logger")
    current_app.logger.error("Error from logger")
    current_app.logger.warning("Warning from logger")
