import csv
import hashlib
import json
import mimetypes
import os

from minio import Minio


class MinioService:

    host = 'minio1:9000'
    a_key = 'minio'
    s_key = 'minio123'
    secure_connection = False

    def __init__(self):

        self.service = Minio(
            self.host,
            access_key=self.a_key,
            secret_key=self.s_key,
            secure=self.secure_connection

        )

    def get_buckets(self):
        buckets = self.service.list_buckets()
        buckets_list = []

        for b in buckets:
            buckets_list.append(b.__dict__)

        return buckets_list

    def get_bucket_by_name(self, bucket_name):
        buckets = self.service.list_buckets()
        for b in buckets:
            if b.__dict__["_name"] == bucket_name:
                return b.__dict__
        return "{}"

    def get(self, config_key):
        return json.loads('{"Value": "value", "Key": "key"}')

    def create_object(self, data):

        self.validate_object_type(data)

        full_file_name = data["file"].filename

        data["file"].save('/tmp/' + full_file_name)
        file_stat = os.stat('/tmp/' + full_file_name)

        file_hash = hashlib.md5(open('/tmp/' + full_file_name, 'rb').read()).hexdigest()

        if file_stat.st_size == 0:
            raise Exception("File is empty.")

        self.validate_object_content(data)

        with open('/tmp/' + full_file_name, 'rb') as file_data:
            self.service.put_object(data["bucket_name"], full_file_name, file_data, file_stat.st_size)
            os.remove('/tmp/' + full_file_name)

        return full_file_name, file_hash

    # def upload_file(self, data):
    #
    #     full_file_name = data["full_file_name"]
    #     file_stat = os.stat('/tmp/' + full_file_name)
    #
    #     with open('/tmp/' + full_file_name, 'rb') as file_data:
    #         self.service.put_object(data["bucket_name"], full_file_name, file_data, file_stat.st_size)
    #         os.remove('/tmp/' + full_file_name)

    def get_all_from_all_buckets(self):
        buckets = self.get_buckets()
        objects_list=[]
        for bucket in buckets:

            objects_in_bucket = self.service.list_objects(bucket["_name"])

            for obj in objects_in_bucket:
                objects_list.append(obj.__dict__)

        return objects_list

    def get_number_of_objects_in_bucket(self, bucket_name):
        objects_list = []

        objects_in_bucket = self.service.list_objects(bucket_name)
        for obj in objects_in_bucket:
            objects_list.append(obj.__dict__)

        return len(objects_list)

    def delete_bucket(self, bucket_name):
        self.service.remove_bucket(bucket_name)
        return True

    def create_bucket(self, bucket_name):
        self.service.make_bucket(bucket_name)
        return True

    def download_file(self, filename, bucket):
        self.service.fget_object(bucket, filename, '/tmp/' + filename)

    def delete_object(self, bucket_name, object_name):
        self.service.remove_object(bucket_name, object_name)


