import logging

from pathlib import Path
from datetime import datetime, timedelta, date

log_folder = '/sample/log/path'

if not Path(log_folder).exists():
    print(f"log_folder not found, creating => {log_folder}")
    Path(log_folder).mkdir()

logFileName = Path(__file__).stem + "-" + date.today().isoformat() + ".log"
logFilePath = Path(log_folder, logFileName)

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(lineno)d >%(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
    level=logging.INFO,
    handlers=[logging.FileHandler(str(logFilePath)), logging.StreamHandler()]
)

logger = logger.getLogger(__name__)
logger.info("\n************************************")