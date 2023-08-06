from .base import FormatterBase


class LogstashFormatter(FormatterBase):

    def format(self, record):
        message = super().format(record)
        return self.serialize(message)
