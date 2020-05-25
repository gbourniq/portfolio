from app.main.storage_backends import PublicMediaStorage, StaticStorage


class TestStorageBackend:
    def test_static_storage_instance(self):
        static_storage = StaticStorage()
        assert static_storage.location == "django_files/static"
        assert static_storage.default_acl == "public-read"

    def test_public_media_storage_instance(self):
        public_media_storage = PublicMediaStorage()
        assert public_media_storage.location == "django_files/media"
        assert public_media_storage.default_acl == "public-read"
        assert public_media_storage.file_overwrite == False
