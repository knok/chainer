from chainer import configuration
from chainer.training import extension
from chainer import variable
import six


class unchain_variables(extension.Extension):
    """Trainer extension to unchain all comptational graphs.

    This extenstion unchains all comptational graphs after all extensions are
    run to avoid any memory problem.
    It observes the previous ``chainer.config.keep_graph_on_report`` flag.
    The extension is enable while the flag is turned on.

    """
    priority = 0

    def __init__(self):
        self._prev_flag = None

    def initialize(self, _):
        self._prev_flag = configuration.config.keep_graph_on_report

    def trigger(self, _):
        flag = self._prev_flag
        self._prev_flag = configuration.config.keep_graph_on_report
        return flag

    def __call__(self, trainer):
        for var in six.itervalues(trainer.observation):
            if isinstance(var, variable.Variable):
                var.unchain_backward()
