

class Status:
    PASS = 'Pass'
    FAIL = 'Fail'
    SKIP = 'Skip'
    ERROR = 'Error'
    PENDING = 'Pending'
    EXECUTING = 'Executing'

    @staticmethod
    def get_ordered_status():
        """
        :return:
        """
        return [Status.PENDING, Status.EXECUTING, Status.SKIP, Status.ERROR, Status.FAIL, Status.PASS]
