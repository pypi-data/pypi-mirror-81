# S3Bz
> save and load dictionary to s3 using bz compression


## Install

`pip install s3bz`

## How to use

### Create a bucket and make sure that it has transfer acceleration enabled
#### create a buket
`aws s3 mb s3://<bucketname>`
#### put transfer acceleration
`aws s3api put-bucket-accelerate-configuration --bucket <bucketname> --accelerate-configuration Status=Enabled`

First, import the s3 module

## dummy data

```python
from importlib import reload
from s3bz.s3bz import S3

bucket = 'pybz-test'
key = 'test.dict'
sampleDict = {'test': 'bool'}
```

## save object

```python
assert S3.save(key = key, 
       objectToSave = sampleDict,
       bucket = bucket,
       user=USER,
       pw = PW,
       accelerate = True), 'saving failed'
```

    INFO:root:using accelerate endpoint
    INFO:root:data was saved to s3


## check if an object exist

```python
assert S3.exist('', bucket, user=USER, pw=PW, accelerate = False), 'bucket doesnt exist'
```

    INFO:root:using standard endpoint


## load object

```python
result = S3.load(key = key,
       bucket = bucket,
       user = USER,
       pw = PW,
       accelerate = True)
assert result == sampleDict, f'wrong result {result}, should be {sampleDict}'
```

    INFO:root:using accelerate endpoint
    INFO:root:object exists, loading
    INFO:root:using accelerate endpoint


## presign download object

```python
url = S3.presign(key=key,
              bucket=bucket,
              expiry = 1000,
              user=USER,
              pw=PW)
r = requests.get(url)
r.json()
```

    INFO:root:using accelerate endpoint
    INFO:botocore.credentials:Found credentials in shared credentials file: ~/.aws/credentials



    ---------------------------------------------------------------------------

    ClientError                               Traceback (most recent call last)

    <ipython-input-8-09797d055370> in <module>
    ----> 1 url = S3.presign(key=key,
          2               bucket=bucket,
          3               expiry = 1000,
          4               user=USER,
          5               pw=PW)


    ~/pip/s3bz/s3bz/s3bz.py in presign(cls, key, expiry, bucket, **kwargs)
         59   @classmethod
         60   def presign(cls, key, expiry = 1000, bucket = '',**kwargs):
    ---> 61     if not cls.checkIfExist(key,bucket=bucket): return 'object doesnt exist'
         62     s3 = cls.s3(**kwargs)
         63     result = s3.generate_presigned_url(


    ~/pip/s3bz/s3bz/s3bz.py in checkIfExist(cls, key, bucket)
         70   @classmethod
         71   def checkIfExist(cls, key, bucket = ''):
    ---> 72     results = cls.s3().list_objects(Bucket=bucket , Prefix= key)
         73     return 'Contents' in results


    /usr/local/Caskroom/miniconda/base/envs/python38/lib/python3.8/site-packages/botocore/client.py in _api_call(self, *args, **kwargs)
        314                     "%s() only accepts keyword arguments." % py_operation_name)
        315             # The "self" in this scope is referring to the BaseClient.
    --> 316             return self._make_api_call(operation_name, kwargs)
        317 
        318         _api_call.__name__ = str(py_operation_name)


    /usr/local/Caskroom/miniconda/base/envs/python38/lib/python3.8/site-packages/botocore/client.py in _make_api_call(self, operation_name, api_params)
        624             error_code = parsed_response.get("Error", {}).get("Code")
        625             error_class = self.exceptions.from_code(error_code)
    --> 626             raise error_class(parsed_response, operation_name)
        627         else:
        628             return parsed_response


    ClientError: An error occurred (AccessDenied) when calling the ListObjects operation: Access Denied

