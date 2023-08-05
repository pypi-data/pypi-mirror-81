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

## import package

```python
from importlib import reload
from s3bz.s3bz import S3
```

### set up dummy data

```python
bucket = 'pybz-test'
key = 'test.dict'
sampleDict = {'test': 'bool'}
```

## save object

```python
result = S3.save(key = key, 
       objectToSave = sampleDict,
       bucket = bucket,
       user=USER,
       pw = PW,
       accelerate = True)
print(('failed', 'success')[result])
```

    success


## check if an object exist

```python
result = S3.exist('', bucket, user=USER, pw=PW, accelerate = False)
print(('doesnt exist', 'exist')[result])
```

    exist


## load object

```python
result = S3.load(key = key,
       bucket = bucket,
       user = USER,
       pw = PW,
       accelerate = True)
print(result)
```

    {'test': 'bool'}


## presign download object

```python
url = S3.presign(key=key,
              bucket=bucket,
              expiry = 1000,
              user=USER,
              pw=PW)
print(url)
```

    https://pybz-test.s3-accelerate.amazonaws.com/test.dict?AWSAccessKeyId=AKIAVX4Z5TKDVBQJXL2G&Signature=6rqC1shPQYrTz4qNeU0viiFEzS4%3D&Expires=1601444414


### testing signed link

```python
import bz2, json
r = requests.get(url)
result = json.loads(bz2.decompress(r.content).decode())
print(f'result is {result}')
```

    result is {'test': 'bool'}

