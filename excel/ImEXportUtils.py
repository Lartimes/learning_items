import os
import uuid
import pandas as pd
from sqlUtils.SqlSession import SqlSession as sql_session


class DataUtils:
    dict_column = {"stu_name": 0, "college": 1, "class_name": 2, "Java Course": 3,
                   "Python Course": 4, "Rust Course": 5}
    course_list = ["Java Course", "Python Course", "Rust Course"]

    def __init__(self):
        print("this class can not be created as an instance")
        return

    @classmethod
    def import_xls(cls, path="C:/Users/33769/Desktop/stu.xlsx"):  # [{}  , {} , {}]
        # path = "C:/Users/33769/Desktop/student.xlsx"
        # //TODO sheet name 多个sheet name
        xls = pd.read_excel(path)
        data = []
        for (row_id, row_info) in xls.iterrows():
            temp = {}
            for (column_name, index) in DataUtils.dict_column.items():
                temp[column_name] = row_info[index]
            data.append(temp)
        # list(dict)
        # sql insert
        cols = list(DataUtils.dict_column.keys())
        course_ids = sql_session.get_course_id(cols[3:])
        course_id_dict = {}
        for index in range(len(course_ids)):
            course_id_dict[str(course_ids[index][1])] = course_ids[index][0]
        # stu_id   stu_name course_name   score , tuple()
        #  0-=stu_id   stu_name ava  cpp rust_file python
        print(course_id_dict)
        # list(dict())
        # course = sql_session
        # stu_name': 'ALAN1', 'college': '电子信息工程学院', 'class_name': '大数据222',
        # 'Java Course': 10, 'Python Course': 70, 'Rust Course': 90}
        for datum in data:
            stu_id = sql_session.add_stu(datum[cols[0]], datum[cols[2]], datum[cols[1]])
            print("stu_id", stu_id)
            # stu_id , course_id , score
            for key, value in course_id_dict.items():
                print(stu_id)
                print(value)
                print(datum[key])
                sql_session.insert_score_by_id(int(stu_id), int(value), datum[key])
        print(data)
        return data

    @staticmethod
    def export_xls():
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取当前工作顶级目录
        print(project_path)
        output_file = os.path.join(project_path, uuid.uuid4().hex + 'stu.xlsx')  # uuid + stu.xlsx
        print(output_file)
        ret = sql_session.export_all()
        length = len(ret)
        course_len = len(DataUtils.course_list)
        java_list = []
        py_list = []
        rs_list = []
        for i in range(length):
            course_name = str(ret[i][4])
            if course_name == DataUtils.course_list[0]:
                java_list.append(ret[i][3])
            elif course_name == DataUtils.course_list[1]:
                py_list.append(ret[i][3])
            elif course_name == DataUtils.course_list[2]:
                rs_list.append(ret[i][3])
        rows = length / course_len  # row , result , 读取course ，
        data = {}  # export -- 》 {column , []}
        for column_name, index in DataUtils.dict_column.items():
            #             每一列进行填充 0 1 2  length
            tmp = []
            for i in range(int(rows)):  # 0 1 2 row
                if index < 3:
                    print(ret[(i - 1) * course_len][index])
                    tmp.append(ret[i][index])
                    continue
                # 读取课程score
                break
            if tmp:
                data[column_name] = tmp

        data[DataUtils.course_list[0]] = java_list
        data[DataUtils.course_list[1]] = py_list
        data[DataUtils.course_list[2]] = rs_list
        print(output_file)
        for datum in data.values():
            print(datum)
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
        return  output_file



if __name__ == '__main__':
    print(list(DataUtils.dict_column.keys())[3:])
    DataUtils.import_xls("C:/Users/33769/Desktop/stu.xlsx")
    DataUtils.export_xls()
