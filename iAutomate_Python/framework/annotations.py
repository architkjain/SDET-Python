import logging


def groupInit(f):
    def decorated():
        print("i am in decorated" + f.__name__)
        logging.info("i am in decorated" + f.__name__)
        # decorated.func_name__=f.__name__

    return f


def groupCleanup(f):
    def decorated():
        print("i am in decorated" + f.__name__)
        logging.info("i am in decorated" + f.__name__)
        # decorated.func_name__=f.__name__

    return f


def makeRegisteringDecorator(foreignDecorator):
    """
        Returns a copy of foreignDecorator, which is identical in every
        way(*), except also appends a .decorator property to the callable it
        spits out.
    """

    def newDecorator(func):
        # Call to newDecorator(method)
        # Exactly like old decorator, but output keeps track of what decorated it
        R = foreignDecorator(func)  # apply foreignDecorator, like call to foreignDecorator(method) would have done
        R.decorator = newDecorator  # keep track of decorator
        # R.original = func         # might as well keep track of everything!
        return R

    newDecorator.__name__ = foreignDecorator.__name__
    newDecorator.__doc__ = foreignDecorator.__doc__

    return newDecorator


groupInit = makeRegisteringDecorator(groupInit)
groupCleanup = makeRegisteringDecorator(groupCleanup)


def platforms(**parameters):
    """ registers platforms for tests
    :param parameters: small case android and ios with boolean values True or False
    :return: wrapper
    """
    def wrapper(test):
        """ sets platforms and other information from args
        :param test: class which is python object
        :return: newly constructed class
        """
        test.platforms = dict()

        # for parameter, value in parameters.iteritems():
        for parameter, value in parameters.items():
            test.platforms[parameter.lower()] = value
        return test
    return wrapper

