import random
import time


def random_delay(min_seconds=1, max_seconds=3):
    """Sleep for a random delay between min and max seconds."""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)