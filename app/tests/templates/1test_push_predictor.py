from unittest.mock import MagicMock, Mock

import pytest

from tests.mocks import MockQuestionClient

LEGAL_PKL_FNAME = "predictor.pkl"
ILLEGAL_PKL_FNAME = "not_valid.pkl"
PREDICTOR_CONTENT = "i am a gurken"


@pytest.fixture(
    params=[
        # source, legal?
        (LEGAL_PKL_FNAME, True),
        ("non_valid/", False),
        (ILLEGAL_PKL_FNAME, False),
        ("not_exist", False),
    ]
)
def push_predictor_arguments(request):
    return request.param


class TestPushPredictorCmd:
    def create_mock_push_args(self, args):
        mock = Mock()
        mock.source = args[0]
        mock.should_pass = args[1]
        return mock

    def test_handle(
        self, monkeypatch, push_predictor_instance, push_predictor_arguments
    ):
        mock_push = Mock()
        monkeypatch.setattr(
            push_predictor_instance,
            "push_predictor_from_file_system",
            mock_push,
        )

        args = self.create_mock_push_args(push_predictor_arguments)
        args.project_name = "mock_project"
        args.qnum = 1
        push_predictor_instance.handle(args)
        mock_push.assert_called_once_with(
            args.source, args.project_name, args.qnum
        )

    def test_validate_args(
        self,
        monkeypatch,
        tmp_path,
        push_predictor_instance,
        push_predictor_arguments,
    ):
        mock_exit = Mock()
        monkeypatch.setattr(push_predictor_instance, "exit_script", mock_exit)

        args = self.create_mock_push_args(push_predictor_arguments)

        # Setup source folder
        source = args.source
        pkl_fname = LEGAL_PKL_FNAME if args.should_pass else ILLEGAL_PKL_FNAME
        if "/" in args.source:
            # Mock source is dir
            source = tmp_path / args.source
            source.mkdir()
            pkl = source / pkl_fname
            pkl.write_text(PREDICTOR_CONTENT)
        elif args.source and "not_exist" not in args.source:
            # Mock source is file
            source = tmp_path / pkl_fname
            source.write_text(PREDICTOR_CONTENT)
        args.source = source

        push_predictor_instance.validate_args(args)
        if args.should_pass:
            mock_exit.assert_not_called()
        else:
            mock_exit.assert_called_once()

    @pytest.mark.parametrize("response", [True, False])
    def test_push_predictor_override(
        self, monkeypatch, push_predictor_instance, response
    ):
        mock_get_question = Mock(
            return_value=MockQuestionClient.default_question(trained=True)
        )
        monkeypatch.setattr(
            push_predictor_instance, "get_question_or_exit", mock_get_question
        )
        mock_yes_response = Mock(return_value=response)
        monkeypatch.setattr(
            "moltres.cli.commands.push_predictor.yes_no_input",
            mock_yes_response,
        )

        source = MagicMock(name="source")
        proj_name = "mock_proj_name"
        qnum = "1"
        if not response:
            with pytest.raises(SystemExit):
                push_predictor_instance.push_predictor_from_file_system(
                    source, proj_name, qnum
                )
        else:
            push_predictor_instance.push_predictor_from_file_system(
                source, proj_name, qnum
            )

        mock_get_question.assert_called_once_with(proj_name, qnum)
