import logging
import sys

from minionize import minionizer, ProcessCallback


logging.basicConfig(level=logging.DEBUG)


def run():
    class _Callback(ProcessCallback):
        """Simplest callback

        Takes param as a string and append them to the original command.
        """

        def to_cmd(self, param):
            return " ".join(sys.argv[1:]) + " " + str(param)

    callback = _Callback()
    m = minionizer(callback)
    m.run()
