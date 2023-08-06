object-clerk
============

|codecov|

A wrapper for the following boto3 s3 client operations with connection retry and checksum verification:

- get_object

- head_object

- upload_fileobj

- copy_object

- delete_object

- list_objects_v2

Features
--------

- Retry connection failures

- Confirm checksum of uploaded and retrieved objects

- Move object

- Constrained interface to support simple CRUD operations for objects in existing buckets

Configuration
-------------
The following environment variables configure the object clerk.

+---------------------+---------------------------------------------------------------------------------------------------------------------------------+--------+-----------------------------------------------------------------------------------------+
| *Variable*          | *Description*                                                                                                                   | *Type* | *Default*                                                                               |
+=====================+=================================================================================================================================+========+=========================================================================================+
| MULTIPART_THRESHOLD | Threshold in bytes at which uploads are broken into multiple parts for upload.  Impacts the checksum stored in the eTag         | STR    | 524288000                                                                               |
+---------------------+---------------------------------------------------------------------------------------------------------------------------------+--------+-----------------------------------------------------------------------------------------+
| S3_CLIENT_CONFIG    | Boto Core Client Configuration                                                                                                  | JSON   | ```json {"connect_timeout": 60, "read_timeout": 60, "retries": {"max_attempts": 0}} ``` |
|                     | https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html                                                |        |                                                                                         |
|                     | Defaults reflect capturing the retry of failed operations at a higher level.                                                    |        |                                                                                         |
+---------------------+---------------------------------------------------------------------------------------------------------------------------------+--------+-----------------------------------------------------------------------------------------+
| S3_UPLOAD_CONFIG    | Transfer Configuration applied to uploads                                                                                       | JSON   | ```json {} ```                                                                          |
|                     | https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig       |        |                                                                                         |
|                     | multipart_threshold and multipart_chunksize are set by the MULTIPART_THRESHOLD environment variable.  Values for these keys in  |        |                                                                                         |
|                     | the S3_UPLOAD_CONFIG will be discarded.                                                                                         |        |                                                                                         |
+---------------------+---------------------------------------------------------------------------------------------------------------------------------+--------+-----------------------------------------------------------------------------------------+
| S3_DOWNLOAD_CONFIG  | Transfer Configuration applied to downloads                                                                                     | JSON   | ```json {} ```                                                                          |
|                     | https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig       |        |                                                                                         |
+---------------------+---------------------------------------------------------------------------------------------------------------------------------+--------+-----------------------------------------------------------------------------------------+

Installation
------------

.. code:: bash

    pip install object-clerk

Examples
--------

**Initialize**

.. code:: python

    clerk = ObjectClerk(host=127.0.0.1, port=8080, access_key=12342, secret_key=12342, retry_delay=1, retry_backoff=1, retry_jitter=(1, 3), retry_max_delay=5, retry_tries=3, use_ssl=False)'

**Get Object**

.. code:: python

    # with checksum verified

    bytes_response = clerk.get_object("bucket", "object_key")

    # without checksum verified

    bytes_response = clerk.get_object("bucket", "object_key", verify_checksum=False)

**Delete Object**

.. code:: python

    clerk.delete_object("bucket", "object_key")

**Get Object Info**

.. code:: python

    dict_response = clerk.get_object_info("bucket", "object_key")

**Copy Object**

.. code:: python

    # with checksum verified

    clerk.copy_object(
        "source_bucket",
        "source_object_key",
        "destination_bucket",
        "destination_object_key",
    )

    # without checksum verified

    clerk.copy_object(
        "source_bucket",
        "source_object_key",
        "destination_bucket",
        "destination_object_key",
        verify_checksum=False
    )

**Upload Object**

.. code:: python

    # with checksum verified

    with open("file", mode='rb') as f:

        clerk.upload_object(f, "bucket", "object_key")

    # without checksum verified

    with open("file", mode='rb') as f:

        clerk.upload_object(f, "bucket", "object_key", verify_checksum=False)

**Move Object**

.. code:: python

    # with checksum verified

    clerk.move_object(
        "source_bucket",
        "source_object_key",
        "destination_bucket",
        "destination_object_key",
    )

    # without checksum verified

    clerk.move_object(
        "source_bucket",
        "source_object_key",
        "destination_bucket",
        "destination_object_key",
        verify_checksum=False
    )

**List Object**

.. code:: python

    clerk.list_objects(
        "bucket_name",
        1000
    )


Test
----

.. code:: bash

    git clone git@bitbucket.org:swiant/object_store_wrapper.git

    pip install -e .

    export HOST=<host>

    export PORT=<port>

    export ACCESS_KEY=<access_key>

    export SECRET_KEY=<secret_key>

    pytest -v object_clerk



.. |codecov| image:: https://codecov.io/bb/dkistdc/object_store_wrapper/branch/master/graph/badge.svg
   :target: https://codecov.io/bb/dkistdc/object_store_wrapper
