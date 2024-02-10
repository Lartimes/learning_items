class ResourceBundle:
    properties = {}
    property_list = []

    def __init__(self):
        print("can not be created to an instance")
        return
    @staticmethod
    def __read_pro(cls , file_path:str):
        with open(file_path) as fl:
            for line in fl:
                items = line.replace("\n", "").split("=")
                key = str(items[0]).split(".")
                # "{'key' : {"key2" :{ "key3" : }}}"
                cls.properties[key[0]] = {}
                length = len(key)
                tmp = ""
                for elem in key:
                    tmp += "{ '"
                    tmp += elem
                    tmp += "' :"
                value = str(items[1])
                tmp += "\'" + value + "\'"
                for i in range(length):
                    tmp += "}"
                cls.property_list.append(eval(tmp))
    @classmethod
    def __merge_dict(cls):
        for prop in cls.property_list:
            for key , value in dict(prop).items():
                if cls.properties[key]:
                    tmp = cls.properties[key]
                    for t1 , t2 in dict(value).items():
                        tmp[t1] = t2
                    cls.properties[key] = tmp
                else:
                    cls.properties[key] = dict(value)
    @classmethod
    def get_bundle(cls ,path:str="datasource.properties"):
        cls.__read_pro(cls=cls ,file_path=path)
        cls.__merge_dict()
        return cls.properties


if __name__ == '__main__':
    properties = ResourceBundle.get_bundle()
    print(properties)