import logging as log
class Report:
    """Class that is used to store multiple reports, by level of gravity
    and can display them nicely"""
    DEBUG = 0
    INFO = 1
    ERROR = 2
    CRITICAL = 3

    def __init__(self):
        self.messages = { key: [] for key in (Report.DEBUG,Report.INFO,Report.ERROR,Report.CRITICAL) }

    def store(self,level, message):
        if level not in self.messages: level = Report.INFO
        self.messages[level].append(message)
    
    def summary(self,tolog=True,tofile=None):
        """Return a summary of the reports. Basically all reports organized by level of 
        gravity. You can pass it a log = False to NOT print on the log output, and file
        name to where to write this report (append)."""
        if tolog is False and tofile is None:
            log.warning("Requested a summary without logging or file output. Weirdo !")
            return
        log.info("-" * 50)
        self.summary_log()
        if tofile: self.summary_file(tofile)
        log.info("-" * 50)
            

    def summary_log(self):
        for mess in self.messages[Report.DEBUG]:
            log.debug(mess)
        for mess in self.messages[Report.INFO]:
            log.info(mess)
        for mess in self.messages[Report.ERROR]:
            log.warning(mess)
        for mess in self.messages[Report.CRITICAL]:
            log.critical(mess)

    def summary_file(self,file):
        pass

