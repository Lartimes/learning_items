import dearpygui.dearpygui as dpg
from  oss.oss import OSS as aliyun_oss
import system.search_bar as search
import system.student_info as stu_info
import system.welcome as welcome
import userInfo.UserWindow as userwin
import userInfo.userAuthWindow as userauth

if __name__ == '__main__':
    dpg.create_context()
    dpg.configure_app(manual_callback_management=True)
    # 加载字体
    with dpg.font_registry():
        default_font = dpg.add_font("./resource/ChillDuanSans_Bold.otf", 15)
        title_font = dpg.add_font("./resource/XuandongKaishu.otf", 30, )
    dpg.bind_font(default_font)
    # 装载容器
    with dpg.window(label="user_window", pos=(0, 0), width=200, height=700, no_resize=True, no_title_bar=True,
                    no_move=True, no_bring_to_front_on_focus=True):
        # user Info windows
        userwin.render_window()
        # user auth tree window
        userauth.user_auth()

    # // 首页
    with dpg.window(label="stu_info", pos=(200, 0), no_resize=True, no_title_bar=True, no_move=True, width=1200,
                    height=700, no_bring_to_front_on_focus=True):
        title = welcome.welcome_window()
        dpg.bind_item_font(title, title_font)
        # search bar
        search.search_render()
        # stu info table 这个应该是一个gloabl table
        stu_info.stu_render()
        # other data import operations
    #     TODO : oss -files
        userauth.render_files()





    dpg.create_viewport(title='Student Management System', width=1200, height=700,
                        large_icon="./resource/winter flower.ico",
                        resizable=False)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        jobs = dpg.get_callback_queue()  # retrieves and clears queue
        dpg.run_callbacks(jobs)
        dpg.render_dearpygui_frame()
    dpg.start_dearpygui()
    dpg.destroy_context()
