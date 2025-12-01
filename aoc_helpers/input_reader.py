import logging

logger = logging.getLogger(__name__)


class AocInputReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_input_to_str(self):
        """Reads and returns the input file as a stripped UTF-8 string"""
        logger.info("Reading input: %s", self.file_path)
        with open(self.file_path, "rb") as file:
            raw = file.read()
        logger.info("Read %d bytes from %s", len(raw), self.file_path)
        data = raw.decode("utf-8").strip()
        return data
