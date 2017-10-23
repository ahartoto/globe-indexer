# Filename: error.py

"""
Globe Indexer Error Module

Interface classes:
    GlobeIndexerError
"""

NEW_LINE = '\n'


class _GlobeIndexerBaseError(Exception):
    """

    """
    def __init__(self, message, details=None, hint=None):
        Exception.__init__(self, message)
        self.message = message
        self.details = details
        self.hint = hint

    def __repr__(self):
        return "<{} '{}'>".format(self.__class__.__name__, self.message)

    def __str__(self):
        messages = [self.message]
        if self.hint:
            messages.append('[=== Hint ===]')
            messages.append(self.hint)
        if self.details:
            messages.append('[=== Details ===]')
            messages.append(self.details)

        return NEW_LINE.join(messages)


class GlobeIndexerError(_GlobeIndexerBaseError):
    pass
