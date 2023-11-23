import logging



class logsMain():
    def __init__(self,  loggerName):
        from app import useLogs
        self.useLogs = useLogs
        self.log = logging.getLogger(loggerName)

    def logInfo(self, msg):
        if self.useLogs:
            self.log.info(msg)
    def logWarning(self, msg):
        if self.useLogs:
            self.log.warning(msg)
    def logError(self, msg):
        if self.useLogs:
            self.log.error(msg)