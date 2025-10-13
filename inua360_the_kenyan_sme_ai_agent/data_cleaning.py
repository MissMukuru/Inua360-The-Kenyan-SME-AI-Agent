from pathlib import Path
from loguru import logger
from tqdm import tqdm
import typer

from inua360_the_kenyan_sme_ai_agent.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

def clean_data(
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
) -> None:
    '''
    Reads the excel files Excel data, en'''