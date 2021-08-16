import json
import datetime
import os

from minio import Minio
from .config import ApplicationConfigurator, DEFAULT_CONFIG


class MinioService(object):

    host = None
    a_key = None
    s_key = None
    secure_connection = False
    entity = None

    def __init__(self, config=None):

        if config:
            self.host = config["MINIO_HOST"]
            self.a_key = config["MINIO_ACCESS_KEY"]
            self.s_key = config["MINIO_SECRET_KEY"]
            self.secure_connection = config["MINIO_SECURE_CONNECTION"]
        else:
            self.host = ApplicationConfigurator.get(DEFAULT_CONFIG).get('MINIO_HOST')
            self.a_key = ApplicationConfigurator.get(DEFAULT_CONFIG).get("MINIO_ACCESS_KEY")
            self.s_key = ApplicationConfigurator.get(DEFAULT_CONFIG).get('MINIO_SECRET_KEY')
            self.secure_connection = ApplicationConfigurator.get(DEFAULT_CONFIG).get('MINIO_SECURE_CONNECTION')

        self.service = Minio(
            self.host,
            access_key=self.a_key,
            secret_key=self.s_key,
            secure=False

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

    def create_object(self, file, bucket_name, supported_extensions=None, subfolder=None, file_name=None):

        self.validate_file_extension(file, supported_extensions)
        file_path = self.save_file_to_system(file)

        file_name = file_name if file_name else self.generate_file_name(file_path)
        if subfolder:
            file_name = f"{subfolder}/{file_name}"

        with open(file_path, 'rb') as file_data:
            self.service.put_object(bucket_name, file_name, file_data, os.stat(file_path).st_size)
            os.remove(file_path)
        return True

    def generate_file_name(self, original_file_name):

        ts = datetime.datetime.utcnow().strftime('%d-%m-%Y_%H:%M:%S')

        return self.entity + "_" + ts + "." + self.get_file_extension(original_file_name)

    @staticmethod
    def get_file_extension(original_file_name):
        return original_file_name.split(".")[-1]

    @staticmethod
    def validate_file_extension(file, supported_extensions=None):

        if supported_extensions and file.filename.rsplit(".")[1] in supported_extensions:
            return True

        return True if supported_extensions is None else False

    @staticmethod
    def save_file_to_system(file_object, folder_path='/tmp/'):

        file_object.save(folder_path + file_object.filename)

        return folder_path + file_object.filename

    def get_all_from_all_buckets(self):
        buckets = self.get_buckets()
        objects_list=[]
        for bucket in buckets:

            objects_in_bucket = self.service.list_objects(bucket["_name"])

            for obj in objects_in_bucket:
                objects_list.append(obj.__dict__)

        return objects_list

    def get_all_from_bucket(self, bucket_name):
        objects_list = []
        objects_in_bucket = self.service.list_objects(bucket_name)
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

    def validate_object_type(self, data):

        pass

    def validate_object_content(self, data):

        pass
