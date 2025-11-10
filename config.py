import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://igracias.telkomuniversity.ac.id")
SURVEY_URL = os.getenv("SURVEY_URL", f"{BASE_URL}/survey/?pageid=1661")
NEXT_SURVEY_URL = os.getenv("NEXT_SURVEY_URL", f"{BASE_URL}/survey/index.php?pageid=2001")

DEFAULT_COMMENT = os.getenv("DEFAULT_COMMENT", "Terima kasih atas ilmu dan bimbingannya selama perkuliahan.")

try:
    RADIO_OPTION_INDEX = int(os.getenv("RADIO_OPTION_INDEX", -1))
except (ValueError, TypeError):
    RADIO_OPTION_INDEX = -1