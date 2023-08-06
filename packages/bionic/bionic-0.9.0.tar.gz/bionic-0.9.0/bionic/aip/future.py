import logging
import time
from concurrent.futures import Future as _Future, TimeoutError, CancelledError
from enum import Enum, auto

from bionic.deps.optdep import import_optional_dependency


class AipError(Exception):
    pass


class State(Enum):
    STATE_UNSPECIFIED = auto()
    QUEUED = auto()
    PREPARING = auto()
    RUNNING = auto()
    SUCCEEDED = auto()
    FAILED = auto()
    CANCELLING = auto()
    CANCELLED = auto()

    def is_executing(self):
        return self in {
            State.STATE_UNSPECIFIED,
            State.QUEUED,
            State.PREPARING,
            State.RUNNING,
        }

    def is_cancelled(self):
        return self in {State.CANCELLING, State.CANCELLED}

    def is_finished(self):
        return self in {
            State.SUCCEEDED,
            State.FAILED,
            State.CANCELLING,
            State.CANCELLED,
        }


class Future(_Future):
    """This future represents a job running on AI platform

    The result of the running job will be pickled, and this future can load that pickle.
    You can find more information about the job details and states at
    https://cloud.google.com/ai-platform/training/docs/reference/rest/v1/projects.jobs

    """

    def __init__(self, project_name: str, job_id: str, output: str):
        # Scope the import to the class to avoid raising for anyone not using it.
        discovery = import_optional_dependency("googleapiclient.discovery")
        self.project_name = project_name
        self.job_id = job_id
        self.output = output
        self.aip = discovery.build("ml", "v1", cache_discovery=False)

    @property
    def name(self):
        return f"projects/{self.project_name}/jobs/{self.job_id}"

    def cancel(self):
        request = self.aip.projects().jobs().cancel(name=self.name)
        request.execute()
        return True

    def _get_state_and_error(self):
        request = self.aip.projects().jobs().get(name=self.name)
        response = request.execute()
        return State[response["state"]], response.get("errorMessage", "")

    def cancelled(self):
        # We may want to distinguish between canceling and cancelled on GCP.
        # At the moment we trust that GCP will always succesfully cancel once requested.
        state, _ = self._get_state_and_error()
        return state.is_cancelled()

    def running(self):
        state, _ = self._get_state_and_error()
        return state.is_executing()

    def done(self):
        state, _ = self._get_state_and_error()
        return state.is_finished()

    def result(self, timeout: int = None):
        # Scope the import to this function to avoid raising for anyone not using it.
        blocks = import_optional_dependency("blocks")

        # This will need an update to support other serializers.
        exc = self.exception(timeout)
        if exc is not None:
            raise exc

        try:
            return blocks.unpickle(self.output)
        except:  # NOQA
            logging.warning(f"Failed to load output from succesful job at {self.path}")
            raise

    def exception(self, timeout: int = None):
        start = time.time()
        state, error = self._get_state_and_error()
        while state.is_executing():
            if timeout is not None and (time.time() - start) > timeout:
                raise TimeoutError(
                    f"{self.job_id} did not finish running before timeout of {timeout}s"
                )

            time.sleep(10)
            state, error = self._get_state_and_error()
            logging.info(f"Future for {self.job_id} has state {state}")

        if state.is_cancelled():
            raise CancelledError(f"{self.job_id}: " + error)
        if state is State.FAILED:
            return AipError(f"{self.job_id}: " + error)
