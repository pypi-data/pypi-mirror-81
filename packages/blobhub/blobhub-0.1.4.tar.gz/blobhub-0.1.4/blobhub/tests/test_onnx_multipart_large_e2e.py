import time

from blobhub.blob import Blob, Revision
from blobhub.presets.onnx import Onnx, Model


class TestCollection:

    ORG_ID = "blobhub-unit-tests"
    BLOB_ID = "unit-test-onnx-large-end-2-end"
    API_KEY = "u2IpwaUzc5beotpkzD_ua6V8PNVbf9zTfLo3OIM2UJy9A7f0CKgxfqihBBcwyPIoCVDTA51PPJoibQZanad6wDhaiWDAk-HlLOV0IxbGix9TjKfsuwxCIi0RBUzaTzlH9R--trXGUEtVSL9ye-sG2WXYuJnSPNcoPHZq-sirPy075MDhZ51odfdtRKDgOdE_J5Stbh6l8pZnU9kJRwJRuRiJr43xSb0KcOgHdaJm-6XvsUjoQtxsjzHgRkCl-l8T4_L_AvHE7hhUbjVsHDZ9vkedjbYt47LJXlDq1KP1bGYPEwlI_Ql4HLVNtaddVKhwh6u5PbbCos7clxeUQwxelA"

    def test_model_end_to_end(self):
        # Find blob
        blob = Blob(org_id=self.ORG_ID, blob_id=self.BLOB_ID, api_key=self.API_KEY)
        revision = blob.revisions.latest()

        # Revision must be "draft" and "ready"
        assert revision[Revision.FIELD_PHASE] == Revision.PHASE_DRAFT
        assert revision[Revision.FIELD_STATUS] == Revision.STATUS_READY

        # Initialize preset
        onnx = Onnx(revision=revision)

        # Upload the model to the revision
        initial_model = Model.from_local_file(onnx=onnx, path="./data/onnx/bertsquad10.onnx")
        success = onnx.upload(model=initial_model)
        assert True == success

        # Wait for the model to be processed
        time.sleep(60)

        # Download and save the model
        downloaded_model = onnx.download()
        assert None != downloaded_model

        # Confirm that downloaded model is identical to the initially downloaded one
        assert downloaded_model.is_identical(model=initial_model)
