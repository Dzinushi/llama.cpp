from LogicLLaMA.metrics import UniversalMetrics
import signal
import functools


def timeout(seconds=5, default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def handle_timeout(signum, frame):
                raise TimeoutError()

            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(seconds)
            result = func(*args, **kwargs)
            signal.alarm(0)
            return result

        return wrapper

    return decorator


class MetricLE:
    def __init__(self):
        self.metric = UniversalMetrics()

    @timeout(seconds=5)
    def __call__(self, pred_text_FOL: str, true_text_FOL: str):
        try:
            score, _, _ = self.metric.compute_LE(pred_text_FOL=pred_text_FOL, true_text_FOL=true_text_FOL)
            return score
        except TimeoutError:
            return 0.0


class MetricBLEU:
    def __init__(self):
        self.metric = UniversalMetrics()

    @timeout(seconds=5)
    def __call__(self, pred_seq: str, true_seq: str):
        try:
            score = self.metric.compute_FOL_bleu(pred_seq=pred_seq, true_seq=true_seq)
            return score
        except TimeoutError:
            return 0.0
