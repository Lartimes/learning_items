import os
import time

import dearpygui.dearpygui as dpg
import thread

import system.student_info as stu_info
from excel.ImEXportUtils import DataUtils as data_utils
from notepad.note_pad import start_notepad
from oss.oss import OSS as aliyun_oss
from sqlUtils.SqlSession import SqlSession as sql_session
from userInfo.UserOssFiles import render_files


def open_rust():
    workdir = os.getcwd()
    workdir = workdir.replace("\\", "/")
    workdir += "/rust_file/FileSystem.exe"
    print(workdir)
    os.system(f"{workdir}")


def delete_stu():
    stu_id = dpg.get_value("del_stu:del_stu_id")  # 数据库已经设置为cascade atomic原子操作 级联删除
    sql_session.del_by_stu_id(int(stu_id))
    dpg.delete_item("tmp2")
    stu_info.stu_render(None)


def update_stu():
    list_stu = ["modify_stu:stu_id", "modify_stu:name", "modify_stu:class_name", "modify_stu:college", ]
    stu_id = int(dpg.get_value(list_stu[0]))
    name = str(dpg.get_value(list_stu[1]))
    class_name = str(dpg.get_value(list_stu[2]))
    college = str(dpg.get_value(list_stu[3]))
    sql_session.update_stu(stu_id, name, class_name, college)
    dpg.delete_item("tmp4")
    stu_info.stu_render(None)


def modify_stu():
    if not dpg.get_value("tmp4"):
        dpg.delete_item("tmp4")
    print("=======================")
    with dpg.window(label="update student", tag="tmp4", width=800, height=400, modal=True, pos=(200, 200),
                    no_move=True):
        list_stu = ["stu_id", "name", "class_name", "college", ]
        for tag in list_stu:
            dpg.delete_item(tag)
        theme = "modify_stu"
        with dpg.table(header_row=False):
            dpg.add_table_column()
            dpg.add_table_column()
            len = list_stu.__len__() + 1
            for i in range(len):
                with dpg.table_row():
                    if i != len - 1:
                        for j in range(0, 2):
                            if j:
                                dpg.add_input_text(tag=theme + ":" + list_stu[i], width=300, height=100)
                            else:
                                dpg.add_text(list_stu[i])
                    else:
                        for j in range(0, 2):
                            if j:
                                dpg.add_button(width=100, height=30, label="cancel",
                                               callback=lambda: dpg.configure_item("tmp4", show=False))
                            else:
                                dpg.add_button(label="submit", width=100, height=30, callback=update_stu)


def del_stu():
    if not dpg.get_value("tmp2"):
        dpg.delete_item("tmp2")
    with dpg.window(label="delete student", tag="tmp2", width=800, height=400, modal=True, pos=(200, 200),
                    no_move=True):
        theme = "del_stu"
        list_tags = [theme + ":del_stu_id"]
        for list_tag in list_tags:
            dpg.delete_item(list_tag)
        with dpg.table(header_row=False):
            dpg.add_table_column()
            for i in range(3):
                with dpg.table_row():
                    if i:
                        if i == 2:
                            dpg.add_button(label="confirm delete", callback=delete_stu)
                            return
                        dpg.add_input_text(tag=list_tags[0], width=300, height=100, indent=100)
                    else:
                        dpg.add_text("id of the student that you want to delete..")
    stu_info.stu_render(None)


def add_student():
    list_tags = ["add_stu:name", "add_stu:class_name", "add_stu:college"]
    args = []
    for list_tag in list_tags:
        args.append(str(dpg.get_value(list_tag)))
    print(args)
    sql_session.add_stu(name=args[0], class_name=args[1], college=args[2])
    for list_tag in list_tags:
        dpg.delete_item(list_tag)
    # 删除tmp1 tag
    dpg.delete_item("tmp1")
    stu_info.stu_render(None)


def add_stu():
    if not dpg.get_value("tmp1"):
        dpg.delete_item("tmp1")
    with dpg.window(label="add student", tag="tmp1", width=800, height=400, modal=True, pos=(200, 200), no_move=True):
        #          stu : name , class_name college  , head_teacher
        list_stu = ["name", "class_name", "college"]
        for e in list_stu:
            dpg.delete_item(e)
        theme = "add_stu"
        with dpg.table(header_row=False):
            dpg.add_table_column()
            dpg.add_table_column()
            len = list_stu.__len__() + 1
            for i in range(len):
                with dpg.table_row():
                    if i != len - 1:
                        for j in range(0, 2):
                            if j:
                                dpg.add_input_text(tag=theme + ":" + list_stu[i], width=300, height=100)
                            else:
                                dpg.add_text(list_stu[i], )
                    else:
                        for j in range(0, 2):
                            if j:
                                dpg.add_button(label="cancel", width=100, height=30,
                                               callback=lambda: dpg.configure_item("tmp1", show=False))
                            else:
                                dpg.add_button(tag=theme + "submit", label="submit", width=100, height=30,
                                               callback=add_student)


user_bucket = "lartimes"


def upload(sender, app_data):
    file_dict = dict(app_data['selections'])
    print(file_dict.values())
    file_path = list(file_dict.values())[0].replace("\\", "/")
    print(file_path)
    aliyun_oss.put_file_oss(file_path, user_bucket)
    render_files()


def imp_xlsx(sender, app_data):
    file_dict = dict(app_data['selections'])
    print(file_dict.values())
    file_path = list(file_dict.values())[0].replace("\\", "/")
    print(file_path + "========excel===========")
    data_utils.import_xls(path=file_path)
    stu_info.stu_render()


def import_excel():
    #     TODO 主要逻辑进行
    dpg.delete_item("import_excel")
    with dpg.file_dialog(directory_selector=False, show=False, callback=imp_xlsx, file_count=3, tag="import_excel",
                         width=700, height=400):
        dpg.add_file_extension(".xlsx", color=(0, 255, 0, 255))
    dpg.show_item("import_excel")


def open_selector():
    #     TODO 主要逻辑进行
    dpg.delete_item("file_dialog_tag")
    with dpg.file_dialog(directory_selector=False, show=False, callback=upload, file_count=3, tag="file_dialog_tag",
                         width=700, height=400):
        dpg.add_file_extension("", color=(255, 150, 150, 255))
        dpg.add_file_extension(".*")
        dpg.add_file_extension(".cpp", color=(255, 255, 0, 255))
        dpg.add_file_extension(".h", color=(255, 0, 255, 255))
        dpg.add_file_extension(".java", color=(200, 0, 255, 255))
        dpg.add_file_extension(".rs", color=(150, 0, 200, 255))
        dpg.add_file_extension(".py", color=(0, 255, 0, 255))
    dpg.show_item("file_dialog_tag")


list_tags = ["user_auth_privilege", "upload files", "file_system_pack_up", "make_note", "import excel", "export excel"]


def callback(sender, app_data, user_data, ):
    print("Called on the main thread!")
    print(user_data)
    if user_data == list_tags[1]:
        # TODO
        open_selector()  # //日志 云存储
    elif user_data == list_tags[3]:
        #     文本编辑器， 同样保存即上传。
        start_notepad()
    elif user_data == list_tags[2]:
        t1 = thread.Thread(open_rust)
        t1.start()
        time.sleep(3)
        t1.kill()  # 调用CMD的话，好像程序就被杀死,此处只进行演示吧。
    #      这个文件整理当然可以做好，包所有整理文件搞好，列一个清单
    #      后面没有实现
    elif user_data == list_tags[4]:
        # "import excel" ,"export excel"
        import_excel()
    elif user_data == list_tags[5]:
        output_file = data_utils.export_xls()
        dpg.delete_item("excel_output")
        with dpg.window(label="file content", tag="excel_output", width=800, height=400, modal=True, pos=(200, 200),
                        no_move=True):
            dpg.add_text(output_file)

    elif user_data == "add student":
        add_stu()
    elif user_data == "delete student":
        del_stu()
    elif user_data == "modify student info":
        modify_stu()


def user_auth(role_id=1):
    for list_tag in list_tags:
        dpg.delete_item(list_tag)
    with dpg.window(label="user_auth_privilege", pos=(0, 180), no_resize=True, no_title_bar=True, no_move=True,
                    width=200, height=520, tag="user_auth_privilege"):
        if role_id:
            auth_tree = sql_session.get_auth(role_id=role_id)
            if auth_tree is not None:
                for auth in auth_tree:
                    length = len(str(auth))
                    temp = str(auth)[2:length - 3]
                    print(temp)
                    list_tags.append(temp)
                    dpg.add_button(label=str(temp), width=170, height=50, tag=str(temp), callback=callback,
                                   user_data=str(temp))

        # 加载权限
        #         sql_session.
        # //TODO 文件导出， 还有 数据可视化
        for i in range(1, 6):
            # lable , tag ,  user_data , callback
            dpg.add_button(label=list_tags[i],  # PY 实现整理， Rust进行整理，
                           width=170, height=50, tag=list_tags[i], callback=callback, user_data=list_tags[i])
