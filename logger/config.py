import os.path


#
# ARDUINO
#

# The port with Arduino data stream.
COMM_PORT="/dev/ttyUSB0"

# Interval for scraping the Arduino readings data.
LOGGER_INTERVAL_SEC=120


#
# IN-MEMORY QUEUE
#

# Limits RAM usage in case of DB unreachability.
# Approximate limit.
MAX_QUEUE_SIZE=256*1024


#
# LOCAL DISK DATABASE BUFFER
#

# Local SQLite database settings.
# Used to buffer data.
SQLITE_DB_FILENAME="db_buffer.sqlite3"

# Full file path for the SQLite DB.
SQLITE_DB_FILE=os.path.join((os.path.dirname(os.path.realpath(__file__))), SQLITE_DB_FILENAME)

# Start moving items from the queue to the sqlite DB
# when queue gets this long, or longer.
SQLITE_DUMP_QUEUE_LENGTH=300

# Dump this many items at once.
SQLITE_DUMP_AMOUNT=100

# Start fetching items from SQLite into the
# queue when it gets this short, or shorter.
SQLITE_FETCH_QUEUE_LENGTH=50

# Fetch this many items at once.
SQLITE_FETCH_AMOUNT=75


#
# CLOUD DATABASE
#

# Credentials to authenticate.
GCP_CREDENTIALS="./gcp-credentials.json"

# GCP project.
GCP_PROJECT="pogoda-240600"

# Cloud database schema settings.

# The entity kind for a sensor reading is fully specified as:
#    instance_config.GCP_INSTANCE_NAME_PREFIX +
#    GCP_READING_PREFIX +
#    GCP_READING_NAME_TRANSLATION.value
GCP_READING_PREFIX="reading:"
GCP_READING_NAME_TRANSLATION={
    "Humidity": "humidity",
    "Temperature": "temperature",
    "Water level": "water_level",
    "Pressure": "pressure",

    "PM 1.0 standard": "pm_10_std",
    "PM 2.5 standard": "pm_25_std",
    "PM 10.0 standard": "pm_100_std",
    "PM 1.0 environmental": "pm_10_env",
    "PM 2.5 environmental": "pm_25_env",
    "PM 10.0 environmental": "pm_100_env",

    "Particles > 0.3um / 0.1L air": "particles_03",
    "Particles > 0.5um / 0.1L air": "particles_05",
    "Particles > 1.0um / 0.1L air": "particles_10",
    "Particles > 2.5um / 0.1L air": "particles_25",
    "Particles > 5.0um / 0.1L air": "particles_50",
    "Particles > 10.0 um / 0.1L air": "particles_100",
}

# The entity kind for connection quality data is fully specified as:
#    instance_config.GCP_INSTANCE_NAME_PREFIX +
#    GCP_CONN_QUALITY_PREFIX +
#    "internet_latency"
GCP_CONN_QUALITY_PREFIX="connection:"
