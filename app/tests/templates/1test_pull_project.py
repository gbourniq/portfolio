from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

from tests.mocks import (
    MockDocumentClient,
    MockDocumentTypeClient,
    MockQuestionClient,
)


class TestPullProjectCommand:
    def test_handle(self, monkeypatch, pull_project_instance):
        mock_pull = Mock()
        monkeypatch.setattr(
            pull_project_instance, "pull_project_to_filesystem", mock_pull
        )

        args = Mock(
            output_directory="out/dir",
            project_name="mock_project",
            qnums=[1, 2, 3],
            tarball=False,
            all_docs=False,
            sleep=1,
        )
        pull_project_instance.handle(args)

        mock_pull.assert_called_once_with(
            Path(args.output_directory),
            args.project_name,
            [1, 2, 3],
            args.tarball,
            args.all_docs,
            1,
        )

    @pytest.mark.parametrize(
        "qnums, legal", [([1, 2, 3], True), ([], True), ([1, 1, 3], False)]
    )
    def test_validate_args(
        self, monkeypatch, pull_project_instance, qnums, legal
    ):
        mock_validate_qnum = Mock(return_value="" if legal else "error")
        monkeypatch.setattr(
            pull_project_instance, "validate_qnum_list", mock_validate_qnum
        )
        args = Mock(qnums=qnums)
        if legal:
            pull_project_instance.validate_args(args)
        else:
            with pytest.raises(SystemExit):
                pull_project_instance.validate_args(args)
        if qnums:
            mock_validate_qnum.assert_called_once_with(args.qnums)
        else:
            mock_validate_qnum.assert_not_called()

    @pytest.mark.parametrize(
        "status, sleep_time", [(200, 1), (399, 3), (400, 0), (401, 0), (500, 0)]
    )
    def test_pull_documents(
        self, monkeypatch, tmpdir, pull_project_instance, status, sleep_time
    ):
        MockDocumentClient.DEFAULT_RESPONSE_CODE = status

        mock_sleep = Mock()
        monkeypatch.setattr(
            "moltres.cli.commands.pull_project.time.sleep", mock_sleep
        )

        pull_project_instance.pull_documents(
            ["1", "2", "3"], tmpdir, sleep_time
        )
        if status < 400:
            documents = MockDocumentClient.default_documents()
        else:
            documents = []

        if sleep_time:
            assert mock_sleep.call_count == len(documents)

        assert len(tmpdir.listdir()) == len(documents)
        for document in documents:
            filename = MockDocumentClient.default_filename(document["id"])
            assert (
                tmpdir.join(filename).read()
                == MockDocumentClient.default_contents().decode()
            )

    @pytest.mark.parametrize(
        "all_docs, questions, qnums, expected",
        [
            (
                True,
                MockQuestionClient.default_questions(),
                [],
                {d["id"] for d in MockDocumentClient.default_documents()},
            ),
            (
                True,
                MockQuestionClient.default_questions(),
                [1, 2],
                {d["id"] for d in MockDocumentClient.default_documents()},
            ),
            (False, MockQuestionClient.default_questions(), [1, 2], {1, 2}),
            (
                False,
                [
                    MockQuestionClient.default_question(training_documents=[1]),
                    MockQuestionClient.default_question(
                        training_documents=[6, 99]
                    ),
                ],
                [],
                {1, 6, 99},
            ),
        ],
    )
    def test_doc_ids_to_pull(
        self, pull_project_instance, all_docs, questions, qnums, expected
    ):

        doc_ids = pull_project_instance.get_doc_ids_to_pull(
            all_docs, qnums, questions, MockDocumentTypeClient.DEFAULT_ID
        )
        assert doc_ids == expected

    @pytest.mark.parametrize(
        "qnums, expected_cheatsheets",
        [
            ([], len(MockQuestionClient.default_questions())),
            ([1], 1),
            ([1, 2], 2),
        ],
    )
    def test_pull_cheatsheets(
        self, tmpdir, pull_project_instance, qnums, expected_cheatsheets
    ):
        mock_project_name = "mock_project"
        pull_project_instance.pull_cheatsheets(
            MockQuestionClient.default_questions(),
            mock_project_name,
            tmpdir,
            qnums,
        )

        assert len(tmpdir.listdir()) == expected_cheatsheets

    def test_pull_project_to_filesystem_missing_qnums(
        self,
        monkeypatch,
        pull_project_instance,
        mock_project_name,
        mock_get_questions,
    ):
        monkeypatch.setattr(
            pull_project_instance,
            "get_project_and_questions_or_exit",
            mock_get_questions,
        )

        doc_ids = {1, 2, 3}
        mock_get_doc_ids = Mock(return_value=doc_ids)
        monkeypatch.setattr(
            pull_project_instance, "get_doc_ids_to_pull", mock_get_doc_ids
        )

        with pytest.raises(SystemExit):
            pull_project_instance.pull_project_to_filesystem(
                "path", mock_project_name, qnums=[4]
            )

    @pytest.mark.parametrize(
        "use_tarball, doc_ids", [(False, ["1", "2", "3"]), (True, [])]
    )
    def test_pull_project_to_filesystem(
        self,
        monkeypatch,
        tmp_path,
        pull_project_instance,
        mock_get_questions,
        mock_project_name,
        use_tarball,
        doc_ids,
    ):
        mock_project_name = "project_name_timestamped"
        output_directory = tmp_path

        mock_moltres_question = MockQuestionClient.default_questions()
        monkeypatch.setattr(
            pull_project_instance,
            "get_project_and_questions_or_exit",
            mock_get_questions,
        )
        mock_get_doc_ids = Mock(return_value=doc_ids)
        monkeypatch.setattr(
            pull_project_instance, "get_doc_ids_to_pull", mock_get_doc_ids
        )

        project_dir = output_directory / "timestamped_pull_project"
        docs_dir = project_dir / "Documents"
        cheatsheets_dir = project_dir / "Cheatsheets"
        for cur_dir in (project_dir, docs_dir, cheatsheets_dir):
            cur_dir.mkdir(exist_ok=True)

        tarfile_path = (
            output_directory / project_dir.with_suffix(".tar.gz").name
        )
        monkeypatch.setattr(
            pull_project_instance, "tarfile_path", tarfile_path, raising=False
        )

        mock_pull_cheatsheets = Mock()
        monkeypatch.setattr(
            pull_project_instance, "pull_cheatsheets", mock_pull_cheatsheets
        )

        mock_pull_documents = Mock()
        monkeypatch.setattr(
            pull_project_instance, "pull_documents", mock_pull_documents
        )

        mock_tar = MagicMock()
        monkeypatch.setattr(
            "moltres.cli.commands.pull_project.TarFile.open", mock_tar
        )

        all_docs = True
        sleep_time = 1
        pull_project_instance.pull_project_to_filesystem(
            output_directory,
            mock_project_name,
            qnums=None,
            use_tarball=use_tarball,
            all_docs=all_docs,
            sleep_time=sleep_time,
            timestamped_dir=project_dir,
        )

        mock_get_doc_ids.assert_called_once_with(
            all_docs,
            None,
            mock_moltres_question,
            MockDocumentTypeClient.DEFAULT_ID,
        )

        mock_pull_cheatsheets.assert_called_once()
        mock_pull_documents.assert_called_once_with(
            doc_ids, docs_dir, sleep_time
        )

        if use_tarball:
            mock_tar.assert_called_once_with(tarfile_path, "w:gz")
        else:
            mock_tar.assert_not_called()
