from s3file.storages_optimized import S3OptimizedUploadStorage


class PrivateMediaStorage(S3OptimizedUploadStorage):
    location = "private"
    # default_acl = "private"
    file_overwrite = False
    # custom_domain = False
