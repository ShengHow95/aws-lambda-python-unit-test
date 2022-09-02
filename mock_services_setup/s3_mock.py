from contextlib import contextmanager

# Use a context manager to help handle setup/teardown automatically before/after tests are run
@contextmanager
def s3_setup(s3_resource, bucketName):
    s3_resource.create_bucket(Bucket=bucketName)
    yield

def list_buckets(s3_resource):
    response = s3_resource.bucket.all()
    return response

def list_objects(s3_resource, bucketName):
    response = s3_resource.Bucket(bucketName).objects.all()
    return response

def upload_file(s3_resource, bucketName, fileName, s3Path, metadata):
    if fileName and s3Path:
        response = s3_resource.Bucket(bucketName).upload_file(fileName, s3Path, ExtraArgs={"Metadata": metadata})
    return response

def put_object(s3_resource, bucketName, objectBody, s3Path):
    if objectBody and s3Path:
        response = s3_resource.Bucket(bucketName).put_object(objectBody, s3Path)
    return response

def generate_presigned_url(s3_client, bucketName, s3Path, clientMethod='get_object', expiredIn=3600):
    response = s3_client.generate_presigned_url(
        ClientMethod=clientMethod,
        Params={'Bucket': bucketName, 'Key': s3Path},
        ExpiresIn=expiredIn
    )
    return response

def S3_Bucket_Mock(s3_resource, bucketName, initialFiles=[]):
    with s3_setup(s3_resource, bucketName):
        for initialFile in initialFiles:
            upload_file(s3_resource, bucketName, initialFile.get('filename'), initialFile.get('s3Path'), initialFile.get('metadata') or {})
        return s3_resource.Bucket(bucketName)
