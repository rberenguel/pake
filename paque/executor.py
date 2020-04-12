import logging
import subprocess
import time
from typing import Any, List

logger = logging.getLogger("paque.executor")


class Executor:
    def __init__(self, plan: List[Any]) -> None:
        self._plan = plan

    def dry_run(self) -> None:
        logger.debug("The plan: %s", self._plan)
        for task in self._plan:
            logger.info(">>> Running task %s", task.name)
            msgs = zip(
                ["message", "run", "sleep"], [task.message, task.run, task.get_sleep()]
            )
            for msg, log in msgs:
                logger.info("%s: %s", msg, log)

    def run(self) -> None:
        logger.info("Running plan")
        for task in self._plan:
            message = task.message
            if message is not None:
                logger.info(message)
            run = task.run
            if run is not None:
                logger.debug("Running %s", run)
                subprocess.run(run, shell=True, check=True)
            duration = task.get_sleep()
            if duration is not None:
                logger.debug("Sleeping for %s", duration)
                time.sleep(duration)
