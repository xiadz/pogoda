from datetime import datetime, timezone
import threading
import time

import config
import instance_config

class LoggerStatistics(object):
    """A class that collects various logger statistics.

    Thread safe.

    Periodically writes statistics to the DB queue."""

    def __init__(self):
        self._lock = threading.Lock()
        self._total_comm_lines_read = 0
        self._total_comm_parsed_lines_read = 0
        self._total_comm_bytes_read = 0
        self._arduino_bps_last_time = None
        self._arduino_bps_last_bytes = None
        self._arduino_lps_last_time = None
        self._arduino_lps_last_lines = None
        self._cloud_db_successes = []
        self._cloud_db_latencies = []
        self._cloud_db_elements_written = 0
        self._last_cloud_db_success_time = None
        self._last_cloud_db_failure_time = None
        self._number_of_new_readings = 0
        self._timestamp_start = datetime.now(timezone.utc)

    def add_comm_lines_read(self, to_add=1):
        """Increments the amount of lines read from the comm port."""
        with self._lock:
            self._total_comm_lines_read += to_add

    def add_comm_parsed_lines_read(self, to_add=1):
        """Increments the amount of parsed lines read from the comm port."""
        with self._lock:
            self._total_comm_parsed_lines_read += to_add

    def add_comm_bytes_read(self, to_add=1):
        """Increments the amount of bytes read from the comm port."""
        with self._lock:
            self._total_comm_bytes_read += to_add

    def total_comm_lines_read(self):
        """Returns the amount of lines read from the comm port."""
        with self._lock:
            return self._total_comm_lines_read

    def total_comm_parsed_lines_read(self):
        """Returns the amount of parsed lines read from the comm port."""
        with self._lock:
            return self._total_comm_parsed_lines_read

    def total_comm_bytes_read(self):
        """Returns the amount of bytes read from the comm port."""
        with self._lock:
            return self._total_comm_bytes_read

    def cloud_db_write_result(self, success, latency=None, elements=0):
        """Saves a single cloud DB write result.

        If success is True latency must be passed (in s) and the
        number of elements written."""
        with self._lock:
            if success:
                self._cloud_db_successes.append(True)
                self._cloud_db_latencies.append(float(latency))
                self._cloud_db_elements_written += elements
                self._last_cloud_db_success_time = datetime.now(timezone.utc)
            else:
                self._cloud_db_successes.append(False)
                self._last_cloud_db_failure_time = datetime.now(timezone.utc)

    def register_new_reading(self):
        """Registers a new reading."""
        with self._lock:
            self._number_of_new_readings += 1

    def number_of_new_readings(self):
        """Returns the total amount of new readings."""
        with self._lock:
            return self._number_of_new_readings

    def cloud_db_elements_written(self):
        """Returns the total amount of elements written to the cloud DB."""
        with self._lock:
            return self._cloud_db_elements_written

    def cloud_db_time_since_success(self):
        """Returns the time since last cloud DB write success, or None."""
        with self._lock:
            if self._last_cloud_db_success_time is None:
                return None
            return datetime.now(timezone.utc) - self._last_cloud_db_success_time

    def cloud_db_time_since_failure(self):
        """Returns the time since last cloud DB write failure, or None."""
        with self._lock:
            if self._last_cloud_db_failure_time is None:
                return None
            return datetime.now(timezone.utc) - self._last_cloud_db_failure_time

    def time_running(self):
        """Returns the total time running."""
        return datetime.now(timezone.utc) - self._timestamp_start

    def _get_and_clear_db_success_rate(self):
        with self._lock:
            if len(self._cloud_db_successes) < 5:
                # Not enough data collected.
                return None
            success_rate = (
                float(self._cloud_db_successes.count(True)) /
                float(len(self._cloud_db_successes))
            )
            self._cloud_db_successes = []
            return success_rate

    def _get_and_clear_avg_db_latency(self):
        with self._lock:
            if len(self._cloud_db_latencies) < 5:
                # Not enough data collected.
                return None
            avg_latency = (
                float(sum(self._cloud_db_latencies)) /
                float(len(self._cloud_db_latencies))
            )
            self._cloud_db_latencies = []
            return avg_latency

    def _get_and_update_arduino_bps(self):
        with self._lock:
            bps = None
            if self._arduino_bps_last_time is not None:
                bytes_change = self._total_comm_bytes_read - self._arduino_bps_last_bytes
                time_change = datetime.now(timezone.utc) - self._arduino_bps_last_time
                bps = float(bytes_change) / time_change.total_seconds()
            self._arduino_bps_last_time = datetime.now(timezone.utc)
            self._arduino_bps_last_bytes = self._total_comm_bytes_read
        return bps

    def _get_and_update_arduino_lps(self):
        with self._lock:
            lps = None
            if self._arduino_lps_last_time is not None:
                bytes_change = self._total_comm_bytes_read - self._arduino_lps_last_bytes
                time_change = datetime.now(timezone.utc) - self._arduino_lps_last_time
                lps = float(bytes_change) / time_change.total_seconds()
            self._arduino_lps_last_time = datetime.now(timezone.utc)
            self._arduino_lps_last_bytes = self._total_comm_bytes_read
        return lps

    def _put_stat(self, data_queue, name, value):
        if value is None:
            return
        timestamp = datetime.now(timezone.utc)
        kind = (instance_config.GCP_INSTANCE_NAME_PREFIX +
                config.GCP_CONN_QUALITY_PREFIX +
                name)
        data_queue.put(
            timestamp=timestamp,
            kind=kind,
            value=value)

    def _put_stats_once(self, data_queue):
        success_rate = self._get_and_clear_db_success_rate()
        self._put_stat(data_queue, "cloud_db_write_success_rate", success_rate)
        avg_latency = self._get_and_clear_avg_db_latency()
        self._put_stat(data_queue, "cloud_db_write_latency", avg_latency)
        bps = self._get_and_update_arduino_bps()
        self._put_stat(data_queue, "arduino_comm_bps", bps)
        lps = self._get_and_update_arduino_lps()
        self._put_stat(data_queue, "arduino_comm_lps", lps)

    def statistics_writer_thread(self, data_queue, logger_statistics):
        while True:
            try:
                time.sleep(config.LOGGER_STATS_INTERVAL_SEC)
                if data_queue.qsize() >= config.MAX_QUEUE_SIZE:
                    # Dropping data, queue too long.
                    pass
                else:
                    self._put_stats_once(data_queue)
            except Exception as e:
                print("Problem in the statistics writer thread.")
                print(e)
                time.sleep(120.0)

