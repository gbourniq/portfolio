from http import HTTPStatus
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

import pytest

from moltres.client.entities.question import Question
from tests.mocks import MockProjectClient


def fetch_question_data(
    qnum=1, text="my question name", qtype=0, trained=False
):
    mock_question_data = {
        "id": 1,
        "question_type": qtype,
        "document_type": 14,
        "text": text,
        "qnum": qnum,
        "latest_seedling": 27,
        "trained": trained,
        "training_documents": [],
        "logic": {},
    }
    return Question(mock_question_data)


@pytest.fixture(
    params=[
        # qnums, qnums_from, qnums_to, legal arguments?
        ([], [], [], True),
        ([1], [], [], True),
        ([1, 2, 3], [], [], True),
        ([], [1], [2], True),
        ([], [1, 2, 3], [4, 5, 6], True),
        ([1], [1], [1], False),
        ([], [1], [], False),
        ([], [], [1], False),
        ([], [1], [1, 2], False),
        ([], [1, 2], [1], False),
        ([], [2, 2], [1, 2], False),
        ([], [1, 2], [2, 2], False),
    ]
)
def push_arguments(request):
    return request.param


def mock_arguments(args):
    mock = Mock()
    mock.qnums = args[0]
    mock.qnums_from = args[1]
    mock.qnums_to = args[2]
    mock.should_pass = args[3]
    return mock


class TestPushProjectCreateCommand:
    def test_handle(self, monkeypatch, push_project_instance):
        qnums_from = ["1"]
        qnums_to = ["2"]
        mock_handle_qnums = Mock(return_value=(qnums_from, qnums_to))
        mock_push = Mock()

        monkeypatch.setattr(
            push_project_instance, "handle_qnums", mock_handle_qnums
        )
        monkeypatch.setattr(
            push_project_instance, "push_project_from_filesystem", mock_push
        )

        args = Mock(
            source="mock_source",
            project_nam="mock_name",
            mode="create",
            qnums=[],
            qnums_from=[1, 2],
            qnums_to=[3, 4],
            force=False,
        )
        push_project_instance.handle(args)

        mock_handle_qnums.assert_called_once_with(
            args.qnums, args.qnums_from, args.qnums_to
        )
        mock_push.assert_called_once_with(
            args.source,
            args.project_name,
            args.mode,
            qnums_from,
            qnums_to,
            force=args.force,
        )

    @pytest.mark.parametrize("error_msg", ["some error", ""])
    def test_validate_args(self, monkeypatch, push_project_instance, error_msg):
        mock_validate_source = Mock(
            return_value=({"source": Path(), "tmp_dir": None}, "")
        )
        mock_validate_qnum = Mock(return_value=error_msg)
        monkeypatch.setattr(
            push_project_instance,
            "validate_project_source",
            mock_validate_source,
        )

        monkeypatch.setattr(
            push_project_instance,
            "validate_qnum_and_qnum_mapping_args",
            mock_validate_qnum,
        )

        args = Mock(
            source="mock_source",
            tarball=False,
            qnums=[],
            qnums_from=[1, 2],
            qnums_to=[3, 4],
        )
        if error_msg:
            with pytest.raises(SystemExit):
                push_project_instance.validate_args(args)
        else:
            push_project_instance.validate_args(args)

        mock_validate_qnum.assert_called_once_with(
            args.qnums, args.qnums_from, args.qnums_to
        )
        mock_validate_source.assert_called_once_with(
            "mock_source", args.tarball
        )

    @pytest.mark.parametrize(
        "mode, sources",
        [
            ("create", {"tmp_dir": None}),
            ("create", {"tmp_dir": TemporaryDirectory()}),
            ("update", {"tmp_dir": None}),
            ("update", {"tmp_dir": TemporaryDirectory()}),
        ],
    )
    def test_push_from_filesystem(
        self,
        monkeypatch,
        push_project_instance,
        mode,
        sources,
        project_structure,
    ):
        sources["source"] = Path(project_structure["source_dir"])
        mock_create_or_update_project = Mock()
        monkeypatch.setattr(
            push_project_instance,
            f"create_project",
            mock_create_or_update_project,
        )
        monkeypatch.setattr(
            push_project_instance,
            f"update_project",
            mock_create_or_update_project,
        )

        mock_project_name = "mock_name"
        mock_project_data = MockProjectClient.default_project(mock_project_name)
        mock_get = Mock(return_value=(mock_project_data, HTTPStatus.OK))
        monkeypatch.setattr(
            "moltres.cli.commands.push_project.PushProjectCommand.client.project.get_by_name",
            mock_get,
        )

        push_project_instance.push_project_from_filesystem(
            sources, mock_project_name, mode
        )

        args = [
            sources["source"] / "Documents",
            project_structure["cheatsheet_path"],
            "mock_name",
            mock_project_data,
            None,
            None,
        ]
        if mode == "update":
            args.append(False)

        mock_create_or_update_project.assert_called_once_with(*args)
        if sources["tmp_dir"]:
            assert not Path(sources["tmp_dir"].name).exists()
