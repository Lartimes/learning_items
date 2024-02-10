import socket
import dearpygui.dearpygui as dpg
import redis
import userInfo.userAuthWindow as user_auth
from sqlUtils.SqlSession import SqlSession as sql_session
from  PropertiesUtils.ResourceBundle import ResourceBundle as resource_bundle

properties = resource_bundle.get_bundle()
host = properties['redis']['host']
database = int(properties['redis']['database'])
def login():
    name = str(dpg.get_value("name"))
    pwd = str(dpg.get_value("pwd"))
    print(name)
    print(pwd)
    is_checked = bool(dpg.get_value("thirty_days_not_log"))
    data = sql_session.login(username=name, password=pwd)
    if data is None:
        print("密码或者账户错误")
        return
    if is_checked:
        value = ""
        for col in data:
            len = str(col).__len__()
            value += str(col)[0: len]
            value += ","
        host_ip = socket.gethostbyname(socket.gethostname())

        r = redis.Redis(host=host, port=6379, db=database)
        r.set(host_ip, value)
    list_tags = ["exit_modal", "out_btn", "texture_tag", "logout_modal", "user_info_window", "login_btn", "login_modal"]
    for list_tag in list_tags:
        dpg.delete_item(list_tag)
    render_window(username=data[0], auth=data[1])
    user_auth.user_auth(role_id=int(data[2]))
    dpg.configure_item("login_modal", show=False)


def logout():
    dpg.destroy_context()


def render_window(username="0", auth="0"):
    logged = None
    try:
        logged = int(username) != 0
    except:
        logged = True

    # 采用redis 进行数据
    # 是否30天免登录
    if logged is not None:
        host_ip = socket.gethostbyname(socket.gethostname())
        print(host_ip)
        # 保存信息
        r = redis.Redis(host='docker', port=6379, db=0)
        info = r.get(host_ip)
        username = "passenger"
        auth = "passenger"  # 最大权限
        id = "0"
        if info is not None:
            print(info)
            info = str(info).split(sep=',')  # name
            # 0 1
            for i in range(3):
                print(info[i])
            username = info[0][2:]
            auth = info[1]
            print(auth)
            id = int(str(info[2]))  # role_id
    # 加入用户信息window
    with dpg.window(label="user_info_window", pos=(0, 0), no_resize=True, no_title_bar=True, no_move=True,
                    width=200, height=180, tag="user_info_window"):
        # image
        width, height, channels, data = dpg.load_image("./snowFlower.png")
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")
        max_size = 50
        scale_factor = min(max_size / width, max_size / height)  # 计算缩放因子以保持宽高比
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        dpg.add_image("texture_tag", width=new_width, height=new_height, indent=50)
        # info
        with dpg.table(header_row=False, pos=(0, 0), tag="user_info_tag"):
            dpg.add_table_column()
            for i in range(2):
                with dpg.table_row():
                    if i:
                        dpg.add_text(f"user auth : {auth}")
                    else:
                        dpg.add_text(f"username : {username}")
        with dpg.window(label="Delete Files", modal=True, show=False, tag="exit_modal", no_title_bar=True):
            dpg.add_text("This application will be shutdown.\nThis operation cannot be undone!")
            dpg.add_separator()
            dpg.add_checkbox(label="Don't ask me next time")
            with dpg.group(horizontal=True):
                dpg.add_button(label="OK", width=75, callback=logout)
                dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item("exit_modal", show=False))

        dpg.add_button(label="logout", tag="out_btn", callback=lambda: dpg.configure_item("exit_modal", show=True))
        dpg.add_button(label="login", tag="login_btn")
        with dpg.popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True, tag="login_modal"):
            dpg.add_text("username :")
            dpg.add_input_text(tag="name")
            dpg.add_text("password :")
            dpg.add_input_text(tag="pwd", password=True)
            dpg.add_checkbox(tag="thirty_days_not_log")
            dpg.add_button(label="Login In", callback=login)
