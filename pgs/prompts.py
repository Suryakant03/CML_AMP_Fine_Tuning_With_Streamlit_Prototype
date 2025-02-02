import streamlit as st
from ft.dataset import DatasetMetadata
from ft.app import get_app
from ft.dataset import *
from ft.consts import HF_LOGO
from ft.state import get_state
from datasets import load_dataset
import random
from uuid import uuid4
from ft.prompt import PromptMetadata
from typing import List


def display_header():
    with st.container(border=True):
        col1, col2 = st.columns([1, 17])
        with col1:
            col1.image("./resources/images/chat_24dp_EA3323_FILL0_wght400_GRAD0_opsz48.png")
        with col2:
            col2.subheader('Prompts')
            col2.caption(
                'Generate tailored prompts for your fine-tuning tasks on the specified datasets and models to enhance performance.')


def display_create_prompt():
    loaded_dataset = None

    col1, col2 = st.columns([3, 2])
    with col1:
        with st.container(border=True):
            new_prompt_name = st.text_input("Prompt Name", placeholder="Enter a human-friendly prompt name")

            datasets = get_state().datasets
            dataset_idx = st.selectbox(
                "Dataset",
                range(
                    len(datasets)),
                format_func=lambda x: datasets[x].name,
                index=0)  # Set the default index as needed

            if dataset_idx is not None:
                dataset = datasets[dataset_idx]
                st.code("Dataset Columns: \n * " + '\n * '.join(dataset.features))

                generate_example_button = st.button(
                    "Generate Prompt Example", type="secondary", use_container_width=True)

                cc1, cc2 = st.columns([1, 1])
                prompt_template = cc1.text_area("Prompt Template", height=200)

                prompt_output = None
                if generate_example_button:
                    with st.spinner("Generating Prompt..."):
                        loaded_dataset = load_dataset(dataset.huggingface_name)

                    dataset_size = len(loaded_dataset["train"])
                    idx_random = random.randint(0, dataset_size - 1)
                    dataset_idx = loaded_dataset["train"][idx_random]
                    prompt_output = prompt_template.format(**dataset_idx)

                cc2.text_area(
                    "Example Prompt",
                    value=prompt_output,
                    height=200,
                    disabled=True)

                if st.button("Create Prompt", type="primary", use_container_width=True):
                    if not new_prompt_name:
                        st.error("Prompt Name cannot be empty!", icon=":material/error:")
                    else:
                        try:
                            add_prompt(new_prompt_name, dataset.id, prompt_template)
                            st.success("Prompt Created. Please go to **View Prompts** tab!", icon=":material/check:")
                            st.toast("Prompt has been created successfully!", icon=":material/check:")
                        except Exception as e:
                            st.error(f"Failed to create prompt: **{str(e)}**", icon=":material/error:")
                            st.toast(f"Failed to create prompt: **{str(e)}**", icon=":material/error:")

    with col2:
        st.info("""
            ### How the Prompt Template Helps in Fine-Tuning

            ### 1. Task-Specific Formatting
            - **Explanation**: Tailors the data format to the specific task.
            - **Impact**: Enhances the model's performance on the specific task.

            ### 2. Enhanced Context Understanding
            - **Explanation**: Provides additional context to each data entry.
            - **Impact**: Improves the model's understanding and response generation.

            ### 3. LoRA-Specific Benefits
            - **Explanation**: Maximizes the information content of each input.
            - **Impact**: Improves the model's adaptation to new tasks with a small number of parameters.

            ### Summary
            The prompt template structures the input data consistently and informatively, aiding the model in understanding and learning more effectively during the LoRA fine-tuning process. This leads to better performance and more efficient adaptation to new tasks.
            """)


def add_prompt(name, dataset_id, template):
    get_app().add_prompt(PromptMetadata(
        id=str(uuid4()),
        name=name,
        dataset_id=dataset_id,
        slots=None,
        prompt_template=template
    ))


def display_available_prompts():
    prompts: List[PromptMetadata] = get_state().prompts

    if not prompts:
        st.info("No prompts available.")
        return

    col1, col2 = st.columns(2)

    for i, prompt in enumerate(prompts):
        container = col1 if i % 2 == 0 else col2
        display_prompt(prompt, container)


def display_prompt(prompt: PromptMetadata, container):
    with container.container(height=200):
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{prompt.name}**")
        c1.caption(prompt.id)
        remove = c2.button("Remove", type="primary", key=f"{prompt.id}_remove_button", use_container_width=True)

        c1, c2 = st.columns([3, 1])
        c1.code(prompt.prompt_template)

        c2.text("Dataset:")
        c2.caption(get_app().datasets.get_dataset(prompt.dataset_id).name)

        if remove:
            get_app().remove_prompt(prompt.id)
            st.rerun()


display_header()
create_prompt_tab, available_prompts_tab = st.tabs(["**Create Prompt**", "**Available Prompts**"])

with create_prompt_tab:
    display_create_prompt()

with available_prompts_tab:
    display_available_prompts()
