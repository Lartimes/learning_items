import os

import dearpygui.dearpygui as dpg

from oss.oss import OSS as aliyun_oss


# TODO 云存储文件渲染
def render_files():
    files = aliyun_oss.get_files()
    dpg.delete_item("files_list_window")
    dpg.delete_item("file_info")
    with dpg.window(label="files_list_window ", tag="files_list_window", pos=(950, 200), width=300, height=600,
                    no_resize=True, no_title_bar=True, no_move=True, no_scrollbar=True, no_scroll_with_mouse=True):
        dpg.add_text(default_value="oss cloud files", indent=50)
        with dpg.table(tag="file_info", header_row=False, row_background=True, borders_innerH=True, borders_outerH=True,
                       borders_innerV=True, borders_outerV=True, width=200, height=80, ):
            dpg.add_table_column(label="files")
            dpg.add_table_column(label="btn1")
            dpg.add_table_column(label="btn2")
            for (file_name, obj_name) in files.items():
                with dpg.table_row():
                    dpg.add_text(default_value=file_name)
                    dpg.add_button(label="download", callback=download, user_data=file_name + ":" + obj_name)
                    if str(file_name).lower().endswith(".txt"):
                        dpg.add_button(label="check contents", callback=check_info, user_data=obj_name)





def check_info(sender, app_data, user_data):
    print(user_data)
    #     TODO ,模态窗口
    (content, local_path) = aliyun_oss.pull_file_to_local(file_name=user_data)
    print(content)
    dpg.delete_item("file_tag")
    with dpg.window(label="file content", tag="file_tag", width=800, height=400, modal=True, pos=(200, 200),
                    no_move=True):
        dpg.add_text(content)





#     TODO 渲染用户上传文件,

def download(sender, app_data, user_data: str):
    names = user_data.split(":")
    ab_len = len(names)
    (content, local_path) = aliyun_oss.pull_file_to_local(file_name=names[1], is_download=True)
    length = len(local_path.split("/")[-1])
    new_path = local_path[0:ab_len - length - 2:] + names[0]
    print(new_path)
    try:
        with open(new_path, "w", encoding="utf8") as fl:
            fl.write(content)
            fl.flush()
    except:
        print("不支持覆盖写入")
        os.rename(local_path, new_path)
        print("重命名")
    finally:
        os.remove(local_path)
    print(length)
    #     弹窗
    dpg.delete_item("content_show_win")
    with dpg.window(label="file content", tag="content_show_win", width=800, height=400, modal=True, pos=(200, 200),
                    no_move=True):
        dpg.add_text(f"the download file 's path is {new_path}")
