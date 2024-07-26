from pydantic import BaseModel
from enum import Enum
from typing import Optional


class AdapterType(Enum):
    """
    Type of PEFT adapter.
    """

    LOCAL = "local"
    """
    Local PEFT adapter imported from project
    files, probably created after a fine-tuning
    job was ran in our app.
    """

    HUGGINGFACE = "huggingface"
    """
    Huggingface-stored adapter that can be pulled
    down from HF hub.
    """


class AdapterMetadata(BaseModel):

    id: str
    """
    Unique ID of the PEFT adapter.
    """

    name: str
    """
    Human friendly name of the adapter for tracking.
    """

    type: AdapterType
    """
    Type of model adapter.
    """

    model_id: str
    """
    Corresponding model ID that this adapter is designed for. This is the
    model ID in the FT app.
    """

    location: Optional[str] = None
    """
    Project-relative directory where the PEFT adapter data is stored.

    When training with HF/TRL libraries, a typical output directory
    for PEFT adapters will contain files like:
    * adapter_config.json
    * adapter_model.bin

    This dataclass currently just stores the location of the PEFT adapter
    in the local directory which can then be used to load an adapter.
    """

    huggingface_name: Optional[str] = None
    """
    Huggingface PEFT adapter name (identifier used to find
    the adapter on HF hub).
    """

    job_id: Optional[str] = None
    """
    Job ID of the job that was used to train/create this adapter. This is
    used to determine if an adapter is completely trained or not.
    """
