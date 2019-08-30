import mock

import neo.libs.image
from neo.libs import image


class TestImage:
    def fake_client_list_images(self, session):
        fake_image = mock.Mock()
        fake_image.images.list.return_value = ["fake_img1", "fake_img2"]
        return fake_image

    def test_get_list(self, monkeypatch):
        monkeypatch.setattr(
            neo.libs.image, "get_image_client", self.fake_client_list_images
        )
        assert image.get_list("fake_session") == ["fake_img1", "fake_img2"]

    def fake_client_get_images(self, session):
        fake_image = mock.Mock()
        fake_image.images.get.return_value = "a detail"
        return fake_image

    def test_detail(self, monkeypatch):
        monkeypatch.setattr(
            neo.libs.image, "get_image_client", self.fake_client_get_images
        )
        assert image.detail("123") == "a detail"
