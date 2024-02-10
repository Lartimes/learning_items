import dearpygui.dearpygui as dpg

import system.student_info as stu_info
from sqlUtils.SqlSession import SqlSession as sql_session

list_cases = ["search_name", "search_class", "search_college"]


def search_stu_info():
    name = str(dpg.get_value(list_cases[0]))
    class_name = str(dpg.get_value(list_cases[1]))
    college = str(dpg.get_value(list_cases[2]))
    if len(name) or len(class_name) or len(college):
        data = sql_session.select_like(name, class_name, college)
        stu_info.stu_render(data)  # 默认第一页数
    else:
        stu_info.stu_render(None)


def search_render():
    with   dpg.window(label="welcome_window", pos=(200, 100), width=1000, height=100, no_move=True, no_resize=True,
                      no_title_bar=True, ):
        with dpg.table(header_row=False, row_background=True, borders_innerH=True, borders_outerH=True,
                       borders_innerV=True, borders_outerV=True, width=750, height=80):
            dpg.add_table_column(width=250, )
            dpg.add_table_column(width=250, )
            dpg.add_table_column(width=250, )
            for i in range(2):
                with dpg.table_row(height=40):
                    if i:
                        for list_case in list_cases:
                            dpg.add_input_text(width=180, indent=30, tag=list_case)
                    else:  # // 0
                        for list_case in list_cases:
                            dpg.add_text(list_case)
        dpg.add_button(label="search button", pos=(760, 10), width=200, height=75, callback=search_stu_info)
