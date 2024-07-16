from pydantic import BaseModel
from ft.model import ModelMetadata
from typing import Optional 
from transformers import BitsAndBytesConfig


class FineTuningJobMetadata(BaseModel):
    job_id: str 
    """
    Unique job identifier of the job. For some job implementations (local
    fine tuning with the AMP), this job ID does not specifically have a
    CML counterpart or significance in the CDP ecosystem.
    """


class LocalFineTuningWorkerProps(BaseModel):
    num_cpu: int = 2 
    num_memory: int = 8
    num_gpu: int = 1



class LocalFineTuningJobMetadata(FineTuningJobMetadata):
    out_dir: str
    """
    Project-relative output directory of the fine-tuning job. 
    """

    start_time: int
    """
    Unix epoch start time (milliseconds) of the job run
    """

    base_model_id: str 
    """
    The model ID of the base model that should be used as a 
    base for the fine tuning job.
    """

    dataset_id: str 
    """
    The dataset that will be used to perform the training.
    This dataset ID is the App-specific ID.
    """

    prompt_id: str 
    """
    The prompt that will be used for training. This is 
    tied to the dataset for now, but that won't necessarily
    be a many-to-one relationship in the future.
    """

    num_workers: int 
    """
    Number of workers to use for this fine-tuning job. 
    """

    worker_props: Optional[LocalFineTuningWorkerProps] = LocalFineTuningWorkerProps()
    """
    Properties of each worker that will be spawned up.
    """





class StartFineTuningJobRequest(BaseModel):
    
    job_name: str
    """
    Human-friendly identifier for the job to run. There
    is no need to have a unique job name for local fine tuning
    jobs because the job id will be automatically generated 
    and will be unique.
    """

    base_model_id: str 
    """
    The model ID of the base model that should be used as a 
    base for the fine tuning job.
    """

    dataset_id: str 
    """
    The dataset that will be used to perform the training.
    This dataset ID is the App-specific ID.
    """

    prompt_id: str 
    """
    The prompt that will be used for training. This is 
    tied to the dataset for now, but that won't necessarily
    be a many-to-one relationship in the future.
    """

    num_workers: int 
    """
    Number of workers to use for this fine-tuning job. 
    """

    bits_and_bytes_config: Optional[BitsAndBytesConfig]
    """
    Bits and bytes config used to quantize the model. If this
    is present, then a model will be loaded with BnB config
    enabled.
    """



    


