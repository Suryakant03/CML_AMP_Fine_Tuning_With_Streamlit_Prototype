from typing import List
from unittest.mock import patch
from uuid import uuid4
import pytest


from ft.dataset import DatasetMetadata, ImportDatasetRequest, ImportDatasetResponse, DatasetType
from ft.job import FineTuningJobMetadata, StartFineTuningJobRequest
from ft.managers.models import ModelsManagerBase, ModelsManagerSimple
from ft.managers.datasets import DatasetsManagerBase, DatasetsManagerSimple
from ft.managers.jobs import FineTuningJobsManagerBase, FineTuningJobsManagerSimple
from ft.managers.evaluation import MLflowEvaluationJobsManagerSimple

from ft.app import (
    FineTuningApp,
    FineTuningAppProps
)

from ft.model import (
    ExportModelRequest,
    ExportModelResponse,
    ExportType,
    ImportModelRequest,
    ImportModelResponse,
    ModelMetadata,
    ModelType
)

from ft.prompt import PromptMetadata

from ft.state import AppState

from tests.mock import *


class TestAppDatasets():

    @patch("ft.app.update_state")
    @patch("ft.app.get_state")
    def test_remove_dataset_no_prompts(self, get_state, update_state):
        datasets: List[DatasetMetadata] = [
            DatasetMetadata(
                id=str(uuid4()),
                type=DatasetType.HUGGINGFACE
            )
        ]

        class MockDatasetsManagerConstant(MockDatasetsManager):
            def list_datasets(self) -> List[DatasetMetadata]:
                return datasets

        app = FineTuningApp(FineTuningAppProps(
            MockDatasetsManagerConstant(),
            MockModelsManager(),
            MockFineTuningJobsManager(),
            MockEvaluatorManager(),
        ))

        app.remove_dataset(datasets[0].id)
        update_state.assert_any_call({"datasets": []})
        update_state.assert_any_call({"prompts": []})

    @patch("ft.app.update_state")
    @patch("ft.app.get_state")
    def test_remove_dataset_associated_prompt(self, get_state, update_state):
        datasets: List[DatasetMetadata] = [
            DatasetMetadata(
                id=str(uuid4()),
                type=DatasetType.HUGGINGFACE
            ),
            DatasetMetadata(
                id=str(uuid4()),
                type=DatasetType.HUGGINGFACE
            )
        ]

        prompts: List[PromptMetadata] = [
            PromptMetadata(
                id=str(uuid4()),
                name="",
                dataset_id=datasets[0].id,
                prompt_template=""
            ),
            PromptMetadata(
                id=str(uuid4()),
                name="",
                dataset_id=datasets[1].id,
                prompt_template=""
            )
        ]

        class MockDatasetManagerConstant(MockDatasetsManager):
            def list_datasets(self) -> List[DatasetMetadata]:
                return datasets

        app = FineTuningApp(FineTuningAppProps(
            MockDatasetManagerConstant(),
            MockModelsManager(),
            MockFineTuningJobsManager(),
            MockEvaluatorManager(),
        ))

        get_state.return_value = AppState(prompts=prompts)

        app.remove_dataset(datasets[0].id)
        update_state.assert_any_call({"datasets": [datasets[1]]})
        update_state.assert_any_call({"prompts": [prompts[1]]})


class TestAppModels():

    @patch("ft.app.update_state")
    @patch("ft.app.get_state")
    def test_export_model_no_response(self, get_state, update_state):

        # Make a mock model manager
        class MockModelManagerNone(MockModelsManager):
            def export_model(self, request: ExportModelRequest) -> ExportModelResponse:
                return ExportModelResponse()

        app = FineTuningApp(FineTuningAppProps(
            MockDatasetsManager(),
            MockModelManagerNone(),
            MockFineTuningJobsManager(),
            MockEvaluatorManager()
        ))

        response: ExportModelResponse = app.export_model(ExportModelRequest(
            type=ExportType.MODEL_REGISTRY,
            model_id=str(uuid4())
        ))

        assert response.model is None
        get_state.assert_not_called()
        update_state.assert_not_called()

    @patch("ft.app.update_state")
    @patch("ft.app.get_state")
    def test_export_model_model_registry(self, get_state, update_state):

        model_uuid = str(uuid4())
        cml_model_uuid = str(uuid4())

        # Make a mock model manager
        class MockModelManagerExportWithId(MockModelsManager):
            def export_model(self, request: ExportModelRequest) -> ExportModelResponse:
                return ExportModelResponse(
                    model=ModelMetadata(
                        type=ModelType.MODEL_REGISTRY,
                        id=model_uuid,
                        cml_registered_model_id=cml_model_uuid
                    )
                )

        get_state.return_value = AppState()

        app = FineTuningApp(FineTuningAppProps(
            MockDatasetsManager(),
            MockModelManagerExportWithId(),
            MockFineTuningJobsManager(),
            MockEvaluatorManager()
        ))

        response: ExportModelResponse = app.export_model(ExportModelRequest(
            type=ExportType.MODEL_REGISTRY,
            model_id=model_uuid
        ))

        assert response.model is not None
        get_state.assert_called_once()
        update_state.assert_called_once()
        update_state.assert_called_with({
            "models": [
                ModelMetadata(
                    type=ModelType.MODEL_REGISTRY,
                    id=model_uuid,
                    cml_registered_model_id=cml_model_uuid
                )
            ]
        })
