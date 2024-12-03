import logging
import multiprocessing

from agent.utils import run_logged

GB_PER_THREAD = 2


class GBOM:
    """
    runs AI Code monitor on given directories
    """

    def freemem(self):
        """
        Returns the free memory in GB.
        Note that this is Linux-specific, which is fine because we are always
        running in a Docker container.
        """
        with open("/proc/meminfo") as file:
            for line in file:
                if "MemAvailable" in line:
                    kbfree = line.split()[1]
                    return float(kbfree) / (1024 * 1024)

    def run(self, directories):
        # We can use as many threads as available CPUs, but we need to cap the
        # number so that each thread has GB_PER_THREAD of memory available.
        gbfree = self.freemem() or GB_PER_THREAD
        threads = min(multiprocessing.cpu_count(), max(1, int(gbfree / GB_PER_THREAD)))

        logger = logging.getLogger(__name__)
        logger.info(f"Running GBOM with {threads} threads (free memory: {gbfree:.2f} GB)")

        run_logged(
            [
                "ai_engine",
                directories.repository,
                "--output-dir",
                directories.mkdir("GBOM"),
                "--cpu_count",
                str(threads),
            ],
            log_dir=directories.log_dir,
        )
