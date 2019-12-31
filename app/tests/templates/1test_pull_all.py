from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest


@pytest.fixture
def mock_timestamped_dir(mock_timestamped_dir_attr, pull_all_instance):
    return mock_timestamped_dir_attr(
        pull_all_instance, "timestamped_projectname_folder"
    )


def get_cli_args(**kwargs):

    params = dict(
        qnums=[1, 2, 3],
        output_directory="out/dir",
        project_name="mock_project",
        all_docs=False,
        tarball=False,
        sleep=2,
        log_dir=None,
    )
    params.update(**kwargs)
    return Mock(**params)


class TestPullAllCommand:
    def test_handle(self, monkeypatch, pull_all_instance):
        mock_pull = Mock()
        monkeypatch.setattr(
            pull_all_instance, "pull_all_to_filesystem", mock_pull
        )

        args = get_cli_args()

        pull_all_instance.handle(args)

        mock_pull.assert_called_once_with(
            [1, 2, 3],
            Path(args.output_directory),
            args.project_name,
            args.tarball,
            args.all_docs,
            2,
        )

    def test_run_pull_commands(
        self, monkeypatch, tmp_path, pull_all_instance, mock_timestamped_dir
    ):
        mock_pull_project = Mock()
        monkeypatch.setattr(
            pull_all_instance, "pull_project_to_filesystem", mock_pull_project
        )
        mock_pull_predictor = Mock()
        monkeypatch.setattr(
            pull_all_instance,
            "pull_predictor_to_filesystem",
            mock_pull_predictor,
        )
        mock_pull_logic = Mock()
        monkeypatch.setattr(
            pull_all_instance, "pull_logic_to_filesystem", mock_pull_logic
        )
        output_directory = tmp_path
        timestamped_dir = mock_timestamped_dir

        mock_project_name = "mock_project"
        qnums = [1, 2, 3]
        all_docs = False
        sleep_time = 0

        pull_all_instance.run_pull_commands(
            qnums, output_directory, mock_project_name, all_docs, sleep_time=0
        )

        mock_pull_project.assert_called_once_with(
            output_directory,
            mock_project_name,
            qnums,
            all_docs=all_docs,
            sleep_time=sleep_time,
            timestamped_dir=timestamped_dir,
        )
        mock_pull_logic.assert_called_once_with(
            output_directory, mock_project_name, qnums, timestamped_dir
        )
        mock_pull_predictor.asset_called_once_with(
            output_directory, mock_project_name, qnums, timestamped_dir
        )

    @pytest.mark.parametrize("tarball", [True, False])
    def test_pull_all_to_filesystem(
        self,
        monkeypatch,
        tmpdir,
        pull_all_instance,
        mock_timestamped_dir,
        tarball,
    ):

        mock_pull_commands = Mock()
        monkeypatch.setattr(
            pull_all_instance, "run_pull_commands", mock_pull_commands
        )
        output_directory = Path(tmpdir)
        mock_project_name = "projectname_folder"
        timestamped_dir = mock_timestamped_dir
        mock_tar_open = MagicMock()
        monkeypatch.setattr(
            "moltres.cli.commands.pull_all.TarFile.open", mock_tar_open
        )
        mock_glob = Mock(return_value=["path/to/project", "path/to/etc"])
        monkeypatch.setattr(
            "moltres.cli.commands.pull_all.Path.glob", mock_glob
        )

        qnums = ["1", "2", "3"]
        sleep_time = 0
        all_docs = False

        pull_all_instance.pull_all_to_filesystem(
            qnums, output_directory, mock_project_name, tarball, all_docs
        )

        if tarball:
            mock_tar_open.assert_called_once_with(
                timestamped_dir.with_suffix(".tar.gz"), "w:gz"
            )
            mock_pull_commands.assert_called_once()
        else:
            mock_tar_open.assert_not_called()
            mock_pull_commands.assert_called_once_with(
                qnums, output_directory, mock_project_name, all_docs, sleep_time
            )

    @pytest.mark.slow
    @pytest.mark.parametrize("tarball", [True, False])
    def test_timestamped_dir_attribute(
        self, monkeypatch, tmpdir, pull_all_instance, tarball
    ):
        """Check if timestamped_dir is created succesfully"""

        args = get_cli_args(output_directory=tmpdir, tarball=tarball)

        with pull_all_instance as instance:

            assert instance.timestamped_dir is None
            instance.run(args)

        timestamped_dir_exists = getattr(instance, "timestamped_dir").exists()
        if tarball:
            assert getattr(instance, "tarfile_path").exists()
            assert timestamped_dir_exists is False
        else:
            assert timestamped_dir_exists

    @pytest.mark.parametrize("tarball", [True, False])
    def test_timestamped_dir_error_clean_up(
        self, monkeypatch, tmpdir, pull_all_instance, tarball
    ):
        """Check if timestamped_dir is deleted upon an error"""

        args = get_cli_args(output_directory=tmpdir, tarball=tarball)

        monkeypatch.setattr(
            pull_all_instance, "run_pull_commands", Mock(side_effect=Exception)
        )

        with pytest.raises(Exception):
            with pull_all_instance as instance:
                instance.run(args)

        tarfile_path = getattr(instance, "tarfile_path")
        if tarball:
            assert tarfile_path.exists() is False
        else:
            assert tarfile_path is None

        assert getattr(instance, "timestamped_dir").exists() is False
