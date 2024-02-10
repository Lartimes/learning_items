import dearpygui.dearpygui as dpg

import system.student_info as stu_inf


def page_flush(sender, app_data, user_data):
    stu_inf.stu_render(None, user_data)


def pages_render(page_num: int, total_pages: int):
    #   page_num <= total_pages
    print("pages_render", page_num)
    print(total_pages)
    page_up = 1
    page_down = 1
    pages = []
    if page_num != 1:
        pages.append(page_num - 1)
        page_up = page_num - 1
    pages.append(page_num)
    if total_pages - page_num >= 1:
        pages.append(page_num + 1)
        page_down = page_num + 1

    with dpg.window(label="pages_info_window", pos=(200, 600), width=750, height=100, indent=100, no_resize=True,
                    no_title_bar=True, no_move=True):
        with dpg.table(label="pages", header_row=False, row_background=True, borders_innerH=True, borders_outerH=True,
                       borders_innerV=True, borders_outerV=True, width=750, height=80):
            for e in range(5):
                dpg.add_table_column(width=100)

            with dpg.table_row(height=40):
                dpg.add_button(label="page up", width=100, height=40, callback=page_flush, user_data=page_up)
                for page in pages:
                    dpg.add_button(label=f"{page}", width=100, height=40, callback=page_flush, user_data=page)
                dpg.add_button(label="page down", width=100, height=40, callback=page_flush, user_data=page_down)
