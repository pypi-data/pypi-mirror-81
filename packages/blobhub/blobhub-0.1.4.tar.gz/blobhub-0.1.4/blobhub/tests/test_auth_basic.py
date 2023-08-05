from blobhub.blob import Blob


class TestCollection:

    ORG_ID = "blobhub-unit-tests"
    BLOB_ID = "unit-test-auth"
    API_KEY = "NU5WbNSZKiQ70WCkOIc1TebUm_IRVyTBrAHf6N9555l_j20tlM9rn1HVBpaLByiZl9LN2MsVBhLrx9qRzUW1gsXZXoaSYdNvPjVVt5ZM0PtRhPkWBWYs0CczPBfvodPxVgHq3vGy1ybXNDwuhDD8J-zYPKF1_II_laVqyAfOugA0nubhhU2c6-1bvPiXQ4ZXfXBiKS2ywn1dGBlWObH9jZMvoU8_ehcKaxP8dtrJLyurkq2aQIflHnMOCIxWxYNl61aoigQh7NvNHFHvI4Ly5nhVfmkiJL4VL6_MWLOChJuULV97-Xfb8kcTe_YcfV7MnbfyRcPzNF2F-o32BtTlSQ"

    def test_fetch_blob_revision(self):
        blob = Blob(org_id=self.ORG_ID, blob_id=self.BLOB_ID, api_key=self.API_KEY)
        assert blob[Blob.FIELD_STATUS] == Blob.STATUS_READY

    # TODO: Anonymous read of public - success
    # TODO: Anonymous write of public - failure
    # TODO: Anonymous read of private - failure
    # TODO: Api key fetch of another blob - failure
    # TODO: Api key write operation for write role - success
    # TODO: Api key write operation for read role - failure

