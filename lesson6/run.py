import time
import logging

class TimerContext:
    def __enter__(self):
        self.start_time = time.time()
        logging.info("Timer started.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        logging.info(f"Timer stopped. Execution time: {elapsed_time:.4f} seconds.")

class Configuration:
    def __init__(self, updates, validator=None):
        """Context manager for temporarily modifying the global configuration."""
        self.updates = updates
        self.validator = validator
        self.original_config = None

    def __enter__(self):
        """Enter the context: Apply the configuration updates."""
        global GLOBAL_CONFIG
        self.original_config = GLOBAL_CONFIG.copy()
        GLOBAL_CONFIG.update(self.updates)
        logging.info("Configuration updated: %s", self.updates)

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context: Restore the original configuration."""
        global GLOBAL_CONFIG
        if self.validator and not self.validator(GLOBAL_CONFIG):
            logging.error("Validation failed. Restoring original configuration.")
            GLOBAL_CONFIG = self.original_config
        elif exc_type:
            logging.error("Exception occurred: %s. Restoring original configuration.", exc_value)
            GLOBAL_CONFIG = self.original_config
        else:
            logging.info("Configuration changes applied successfully.")
        logging.info("Configuration restored to: %s", GLOBAL_CONFIG)

def validate_config(config: dict) -> bool:
    """Example validator function to check the validity of the configuration."""
    if not isinstance(config.get("feature_a"), bool):
        logging.error("Invalid value for feature_a.")
        return False
    if config.get("max_retries", 0) < 0:
        logging.error("Invalid value for max_retries: Must be non-negative.")
        return False
    return True

GLOBAL_CONFIG = {
    "feature_a": True,
    "feature_b": False,
    "max_retries": 3
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

with TimerContext():
    time.sleep(2)

if __name__ == "__main__":
    logging.info("Initial GLOBAL_CONFIG: %s", GLOBAL_CONFIG)

    try:
        with Configuration({"feature_a": False, "max_retries": 5}):
            logging.info("Inside context: %s", GLOBAL_CONFIG)
    except Exception as e:
        logging.error("Error: %s", e)

    logging.info("After context: %s", GLOBAL_CONFIG)

    try:
        with Configuration({"feature_a": "invalid_value", "max_retries": -1}, validator=validate_config):
            logging.info("This should not be printed if validation fails.")
    except Exception as e:
        logging.error("Caught exception: %s", e)

    logging.info("After failed context: %s", GLOBAL_CONFIG)
