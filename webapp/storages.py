from s3file.storages_optimized import S3OptimizedUploadStorage
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStore(S3Boto3Storage):
    location = "media"
    file_overwrite = False


class PrivateMediaStorage(S3OptimizedUploadStorage):
    location = "private"
    default_acl = "private"
    file_overwrite = False
    custom_domain = False
