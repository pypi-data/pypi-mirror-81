import time

from blobhub.blob import Blob, Revision
from blobhub.presets.onnx import Onnx, Model, Config


class TestCollection:

    ORG_ID = "blobhub-unit-tests"
    BLOB_ID = "unit-test-onnx-end-2-end"
    API_KEY = "fxJHyg5wDvfiDe8ElFgJO7sA77EEAI4G5CMN0DH-AeQrHe5w146Il00pjvBHQZWUnSHSkt9Yqy9m6HvvA-diB6apm60OysNHSnO6xeRTRicSk1ySF7H-hYJqt1j8YmnK5lbWqoRy-H7Kmkt9nMoSyrC3D0_c1EYilsJJYehrabGubk9hD6xP7-_Rk9oUpGlH7YjcGiocGzk7EoIClWi64maQR2EJFKvBkFjrnD22-Af0hOA3BBvHog3QDjaFFlFOqQ7r4MCcjWJwyj_Y7mXlm2jaPjZ0nVqMnFEdZMlHhWULcYmHTl8c80U4Z3x4c-Mycz5Q6lc9IpOJwv3VDzQZXQ"

    def test_model_end_to_end(self):
        # Find blob
        blob = Blob(org_id=self.ORG_ID, blob_id=self.BLOB_ID, api_key=self.API_KEY)
        revision = blob.revisions.latest()

        # Revision must be "draft" and "ready"
        assert revision[Revision.FIELD_PHASE] == Revision.PHASE_DRAFT
        assert revision[Revision.FIELD_STATUS] == Revision.STATUS_READY

        # Force multi-part operations
        config = Config(
            force_multipart_download=True,
            force_multipart_upload=True
        )

        # Initialize preset
        onnx = Onnx(revision=revision, config=config)

        # Upload the model to the revision
        initial_model = Model.from_local_file(onnx=onnx, path="./data/onnx/mnist.onnx")
        success = onnx.upload(model=initial_model)
        assert True == success

        # Wait for the model to be processed
        time.sleep(5)

        # Download and save the model
        downloaded_model = onnx.download()
        assert None != downloaded_model

        # Confirm that downloaded model is identical to the initially downloaded one
        assert downloaded_model.is_identical(model=initial_model)
