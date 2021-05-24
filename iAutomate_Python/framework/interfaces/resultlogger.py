import abc


class IDefaultResultLogger(metaclass=abc.ABCMeta):
    """ Interface for creating Logger Classes """

    @classmethod
    def __issubclasshook__(cls, subclass):
        """
        :param subclass:
        :return:
        """
        return (hasattr(subclass, 'log_step_result') and callable(subclass.log_step_result) and
                hasattr(subclass, 'log_test_result') and callable(subclass.log_test_result) or NotImplemented)

    @abc.abstractmethod
    def log_step_result(self, testname, stepname, stepdescription, stepverify,
                        actualresult, status, comment="", snapshotlink=""):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def log_test_result(self, groupname, testcase, status):
        """Extract text from the data set"""
        raise NotImplementedError





