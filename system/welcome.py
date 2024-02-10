import dearpygui.dearpygui as dpg
def welcome_window():
    with dpg.window(label="welcome_window", pos=(200, 0), width=1000, height=100, no_move=True, no_resize=True,
                    no_title_bar=True, ):
        title = dpg.add_text("welcome to the student management system", indent=20, )
        dpg.set_item_indent(title, 250)
        return title