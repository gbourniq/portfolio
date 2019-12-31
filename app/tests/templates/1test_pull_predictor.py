from pathlib import Path
from unittest.mock import Mock

import pytest

from tests.mocks import MockQuestionClient

LEGAL_PKL_FNAME = "predictor.pkl"
PREDICTOR_CONTENT = "i am a gurken"


@pytest.fixture
def mock_timestamped_dir(mock_timestamped_dir_attr, pull_predictor_instance):
    return mock_timestamped_dir_attr(
        pull_predictor_instance, "timestamped_pull_predictor"
    )


class TestPullPredictorCmd:
    def test_handle(self, monkeypatch, pull_predictor_instance):
        mock_pull = Mock()
        monkeypatch.setattr(
            pull_predictor_instance, "pull_predictor_to_filesystem", mock_pull
        )

        args = Mock(
            output_directory="some/output/dir/",
            project_name="mock_project",
            qnums=[1],
        )
        pull_predictor_instance.handle(args)

        mock_pull.assert_called_once_with(
            Path(args.output_directory), args.project_name, [1]
        )

    @pytest.mark.parametrize(
        "qnums, legal", [([1, 2, 3], True), ([], True), ([1, 1, 3], False)]
    )
    def test_validate_args(
        self, monkeypatch, pull_predictor_instance, qnums, legal
    ):
        mock_validate_qnum = Mock(return_value="" if legal else "error")
        monkeypatch.setattr(
            pull_predictor_instance, "validate_qnum_list", mock_validate_qnum
        )
        args = Mock(qnums=qnums)
        if legal:
            pull_predictor_instance.validate_args(args)
        else:
            with pytest.raises(SystemExit):
                pull_predictor_instance.validate_args(args)
        if qnums:
            mock_validate_qnum.assert_called_once_with(args.qnums)
        else:
            mock_validate_qnum.assert_not_called()

    def test_save_predictor(self, tmp_path, pull_predictor_instance):
        pull_predictor_instance.save_predictor(
            LEGAL_PKL_FNAME, Path(tmp_path), bytes(PREDICTOR_CONTENT, "utf-8")
        )

        pkl_path = tmp_path / LEGAL_PKL_FNAME
        assert len(list(tmp_path.iterdir())) == 1
        assert next(tmp_path.iterdir()).name == LEGAL_PKL_FNAME
        assert pkl_path.read_text() == PREDICTOR_CONTENT

    def test_save_predictor_mkdir(self, tmp_path, pull_predictor_instance):
        output = tmp_path / "output"
        pull_predictor_instance.save_predictor(
            LEGAL_PKL_FNAME, Path(output), bytes(PREDICTOR_CONTENT, "utf-8")
        )

        pkl_path = output / LEGAL_PKL_FNAME
        assert next(tmp_path.iterdir()).name == "output"
        assert len(list(output.iterdir())) == 1
        assert next(output.iterdir()).name == LEGAL_PKL_FNAME
        assert pkl_path.read_text() == PREDICTOR_CONTENT

    def test_pull_predictor_to_filesystem_missing_qnums(
        self,
        tmp_path,
        monkeypatch,
        pull_predictor_instance,
        mock_project_name,
        mock_get_questions,
        mock_timestamped_dir,
    ):
        monkeypatch.setattr(
            pull_predictor_instance,
            "get_project_and_questions_or_exit",
            mock_get_questions,
        )
        with pytest.raises(SystemExit):
            pull_predictor_instance.pull_predictor_to_filesystem(
                Path(tmp_path), mock_project_name, qnums=[4]
            )

    @pytest.mark.parametrize("qnums", [[], [1, 3]])
    def test_pull_predictor(
        self,
        tmpdir,
        monkeypatch,
        pull_predictor_instance,
        mock_get_questions,
        mock_project_name,
        mock_timestamped_dir,
        qnums,
    ):
        monkeypatch.setattr(
            pull_predictor_instance,
            "get_project_and_questions_or_exit",
            mock_get_questions,
        )
        mock_save = Mock()
        monkeypatch.setattr(
            "moltres.cli.commands.pull_predictor.PullPredictorCommand.save_predictor",
            mock_save,
        )

        output = Path(tmpdir)
        pull_predictor_instance.pull_predictor_to_filesystem(
            output, mock_project_name, qnums
        )

        save_count = (
            len(qnums) if qnums else len(MockQuestionClient.default_questions())
        )

        mock_get_questions.assert_called_once_with(mock_project_name)
        assert mock_save.call_count == save_count

    def test_pull_predictor_not_found(
        self,
        tmp_path,
        monkeypatch,
        pull_predictor_instance,
        mock_get_questions,
        mock_project_name,
        mock_timestamped_dir,
    ):
        mock_save = Mock()
        monkeypatch.setattr(
            "moltres.cli.commands.pull_predictor.PullPredictorCommand.save_predictor",
            mock_save,
        )
        monkeypatch.setattr(
            pull_predictor_instance,
            "get_project_and_questions_or_exit",
            mock_get_questions,
        )
        mock_pull = Mock(return_value=(None, 400))
        monkeypatch.setattr(MockQuestionClient, "pull_predictor", mock_pull)

        mock_blueit = Mock()
        mock_blueit.return_value = lambda msg: msg

        monkeypatch.setattr(
            "moltres.cli.commands.pull_predictor.blueit", mock_blueit
        )

        output = Path(tmp_path)
        qnums = []
        pull_predictor_instance.pull_predictor_to_filesystem(
            output, mock_project_name, qnums
        )

        mock_get_questions.assert_called_once_with(mock_project_name)
        mock_save.assert_not_called()
        mock_blueit.assert_called()
