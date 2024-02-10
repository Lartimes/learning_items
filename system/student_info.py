import math

import dearpygui.dearpygui as dpg

import system.pages_window as pages
from sqlUtils.SqlSession import SqlSession as sql_session


def check_info(sender, app_data, user_data):
    if not dpg.get_value("check_info"):
        dpg.delete_item("check_info")
    # 模态窗口
    scores = sql_session.check_score(int(user_data))
    length = len(scores)
    print(scores)
    if length:
        with dpg.window(label="student info", tag="check_info", width=800, height=400, modal=True, pos=(200, 200),
                        no_move=True):
            dpg.add_text(str(scores[0][0]) + "'s personal scores")
            dpg.add_text("stu_id : " +str(scores[0][1]) )
            for i in range(length):
                dpg.add_text(str(scores[i][2]))
                dpg.add_text(str(scores[i][3]), indent=100)



list_tags = ["check_info", "stu_info_tag"]


def stu_render(data=None, page_num=1):
    for list_tag in list_tags:
        dpg.delete_item(list_tag)
    with dpg.window(label="stu_info ", pos=(200, 200), width=750, height=400, indent=100, no_resize=True,
                    no_title_bar=True, no_move=True, no_scrollbar=True, no_scroll_with_mouse=True):
        # 根据数据查询 设置column counts
        # 有什么字段？
        with dpg.table(header_row=False, row_background=True, borders_innerH=True, borders_outerH=True,
                       borders_innerV=True, borders_outerV=True, width=750, height=80, tag="stu_info_tag"):
            list_column = ["stu_name", "class_name", "college_name", "sum_score", "rank", "auth_btn"]
            for col in list_column:
                dpg.add_table_column(label=col, width=100)
            # [list(map)]
            if data is None:
                data = sql_session.get_score(page=page_num)
                print(data)
            result = []
            length = len(data)  # 页数
            count = sql_session.get_stu_count()
            total_pages = math.ceil(count / 8)
            print("total pages ", total_pages)
            print(count)
            for i in range(length):
                tmp = {}
                for j in range(5):
                    if data[i] is not None:
                        if list_column[j] == "rank":
                            tmp[list_column[-1]] = data[i][j]
                            break
                        tmp[list_column[j]] = data[i][j]
                result.append(tmp)
            print(result)
            if length:
                for i in range(length + 1):  # size : list_len
                    with dpg.table_row(height=40):
                        print(i)
                        if i:  # 真的i ==> rank
                            for col in list_column:
                                if col == "rank":
                                    dpg.add_text(str(i))
                                else:
                                    if col == "auth_btn":
                                        dpg.add_button(user_data=str(result[i - 1][col]), label="check stu info",
                                                       callback=check_info)
                                        continue
                                    dpg.add_text(str(result[i - 1][col]))

                        else:
                            for j in list_column:
                                dpg.add_text(j)

            # pagess
            pages.pages_render(page_num, total_pages)  # 渲染page window
