# this is a different way of integration with the MLFlow transformers
# or custom connectors to API calls/ AI inference.
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig


'''
class MLFlowTransformers():
    def __init__(self):
        pass


    def get_quantization_config():
        quantization_config = BitsAndBytesConfig(
        # Load the model with 4-bit quantization
        load_in_4bit=True,
        # Use double quantization
        bnb_4bit_use_double_quant=True,
        # Use 4-bit Normal Float for storing the base model weights in GPU memory
        bnb_4bit_quant_type="nf4",
        # De-quantize the weights to 16-bit (Brain) float before the forward/backward pass
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    def get_peft_model_and_tokenizer(self, base_model_id):
        quantization_config = self.get_quantization_config()
        model = AutoModelForCausalLM.from_pretrained(base_model_id, quantization_config=quantization_config)

'''
