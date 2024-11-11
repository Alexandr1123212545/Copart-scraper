import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('parser.log')
    ]
)
logging.getLogger('undetected_chromedriver').setLevel(logging.CRITICAL)
logging.getLogger('uc').setLevel(logging.CRITICAL)

logger = logging.getLogger('parser')