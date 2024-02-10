# -*- coding: utf-8 -*-
import os
import uuid

import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

from sqlUtils.SqlSession import SqlSession as sql_session


class OSS:
    cwd = os.getcwd().replace("\\", "/")
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
    endpoint = 'https://oss-cn-hangzhou.aliyuncs.com'
    username = "lartimes"  # bucket_name
    list_tags = ["file_oss_list", "files_oss_info"]

    def __init__(self):
        print("OSS class can not be new to an instance")
        return

    @classmethod
    def does_bucket_exist(cls, bucket: oss2.Bucket):
        try:
            bucket.get_bucket_info()
        except oss2.exceptions.NoSuchBucket:
            return False
        except:
            raise
        return True

    @classmethod
    def put_file_oss(cls, path: str, user: str = "lartimes"):
        bucket = oss2.Bucket(OSS.auth, OSS.endpoint, OSS.username)
        if not OSS.does_bucket_exist(bucket):  # 不存在
            bucketConfig = oss2.models.BucketCreateConfig(oss2.BUCKET_STORAGE_CLASS_STANDARD,
                                                          oss2.BUCKET_DATA_REDUNDANCY_TYPE_ZRS)
            bucket.create_bucket(oss2.BUCKET_ACL_PRIVATE, bucketConfig)
        # 生成 UUID / sha256 ， put file ， filePath ，
        list_path = path.split(".")
        file_name = path.split("/")[-1]
        obj_name = user + "/journal/" + uuid.uuid4().hex + "." + list_path[1]
        bucket.put_object_from_file(obj_name, path)
        sql_session.insert_file_obj(user=user, file_name=file_name, obj_name=obj_name)
        os.remove(path)

    #     TODO 渲染文件

    #     进行sql 持久化
    @classmethod
    def pull_file_to_local(cls, file_name: str, username: str = "lartimes", is_download: bool = False, ):
        bucket = oss2.Bucket(OSS.auth, OSS.endpoint, OSS.username)
        # file_name TODO 根据file——name 获取OSS filePath （obj_name）
        local_path = OSS.cwd + "/" + uuid.uuid4().hex + "." + file_name.split(".")[1]
        bucket.get_object_to_file(file_name, local_path)
        content = ""
        try:
            with open(local_path, "r", encoding="utf8") as fl:
                result = fl.readlines()
                for line in result:
                    content += line
        except:
            print("不持支该格式直接读入")
        print(content)
        if not is_download:
            os.remove(local_path)
        return (content, local_path)

    @staticmethod
    def get_files():
        files = sql_session.get_oss_files()
        oss_file = {}
        length = len(files)
        print(length)
        for index in range(length):
            oss_file[str(files[index][0])] = str(files[index][1])
        return oss_file


print(OSS.cwd)  # D:\Dev\PyDev\GUIWork\pythonProject\oss  # OSS.put_file_oss("D:/Dev/PyDev/GUIWork/pythonProject/oss/qweqweqqw.txt", "lartimes")  # OSS.pull_file_to_local("lartimes","qweqweqqw.txt")  # render_files()
