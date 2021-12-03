SOURCE_BUCKET = "source-test"
DESTINATION_BUCKET = "dest-test"
KEY = "test/test.py"

# mock s3 client
@pytest.fixture
def s3():
    """Pytest fixture that creates two buckets and key
    Yields a fake boto3 s3 client
    """
    with mock_s3():
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket=DESTINATION_BUCKET)
        s3.create_bucket(Bucket=SOURCE_BUCKET)
        s3.put_object(Bucket=SOURCE_BUCKET, Key=KEY)
        yield s3
        
def test_copy_object(s3):

      assert function.copy_object(
        s3, dest_bucket) == SUCCESS_MESSAGE
