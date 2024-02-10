import os
import time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from  oss.oss import  OSS as aliyun_oss
from  userInfo.UserOssFiles import  render_files
class NotePad:
    @staticmethod
    def nodefined():
        pass

    def openfile(self):
        filename = filedialog.askopenfilename()
        f = open(filename, 'r')
        f2 = f.read()
        f.close()
        self.text.insert(INSERT, f2)

    def savefileas(self):
        filename = filedialog.asksaveasfilename(filetypes=[("TXT", ".txt")]) + ".txt"
        print(filename)
        content = self.text.get('0.0', 'end')
        print(content)
        with open(filename, 'w' ,encoding="utf8") as f:
            f.write(content)
            f.flush()
    # TODO filename ---> 云存储， 渲染
        print(filename)
        aliyun_oss.put_file_oss(filename)
        render_files()



    def quit(self):
        self.root.destroy()

    # 复制功能函数
    def copy(self):
        global content
        content = self.text.get(SEL_FIRST, SEL_LAST)
        return content

    def cut(self):
        global content
        content = self.text.get(SEL_FIRST, SEL_LAST)
        self.text.delete(SEL_FIRST, SEL_LAST)
        return content

    # 粘贴功能函数

    def paste(self):
        self.text.insert(INSERT, content)

    @staticmethod
    def about():
        messagebox.showinfo("关于", "开发者：Lartimes")

    def popup(self, event):
        self.popupmenu.post(event.x_root, event.y_root)

    def __init__(self):
        # 顶级菜单窗口
        self.root = Tk()
        self.topmenu = Menu(self.root)
        self.root.title("Text Editor")
        # 文字编辑区text
        self.text = Text(self.root, width=90, height=40, selectforeground="black", undo=True, font=50)
        self.text.pack()
        self.menu_render()


    def menu_render(self):
        # 创建文件下拉菜单，添加到顶层菜单窗口
        filemenu = Menu(self.topmenu, tearoff=False)
        # 添加下拉内容：
        filemenu.add("command", label="打开", command=self.openfile)
        filemenu.add_command(label="保存/上传", command=self.savefileas)
        filemenu.add_command(label="另存为", command=self.savefileas)
        filemenu.add_separator()
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=quit)
        self.topmenu.add_cascade(label="文件", menu=filemenu)
        editmenu = Menu(self.topmenu, tearoff=False)
        editmenu.add_separator()
        editmenu.add_command(label="撤销", command=self.callback)
        editmenu.add("command", label="剪切", command=self.cut)
        editmenu.add_command(label="复制", command=self.copy)
        editmenu.add_command(label="粘贴", command=self.paste)
        editmenu.add_separator()
        editmenu.add_command(label="查找", command=NotePad.nodefined)
        editmenu.add_command(label="替换", command=NotePad.nodefined)
        editmenu.add_command(label="转到", command=NotePad.nodefined)
        editmenu.add_separator()
        self.topmenu.add_cascade(label="编辑", menu=editmenu)
        formatmenu = Menu(self.topmenu, tearoff=False)
        self.topmenu.add_cascade(label="格式", menu=formatmenu)
        viewmenu = Menu(self.topmenu, tearoff=False)
        viewmenu.add_command(label="查看状态栏", command=self.callback)
        self.topmenu.add_cascade(label="查看", menu=viewmenu)
        helpmenu = Menu(self.topmenu, tearoff=False)
        helpmenu.add_command(label="查看帮助", command=self.callback)
        helpmenu.add_separator()
        helpmenu.add_command(label="关于笔记本", command=NotePad.about)
        self.topmenu.add_cascade(label="帮助", menu=helpmenu)
        self.popupmenu = Menu(self.root, tearoff=False)
        self.popupmenu.add_command(label="保存", command=self.savefileas)
        self.popupmenu.add_command(label="另存为", command=self.savefileas)
        self.popupmenu.add_separator()
        self.popupmenu.add_command(label="撤回", command=self.callback)
        self.popupmenu.add_separator()
        self.popupmenu.add("command", label="剪切", command=self.cut)
        self.popupmenu.add_command(label="复制", command=self.copy)
        self.popupmenu.add_command(label="粘贴", command=self.paste)
        self.popupmenu.add("command", label="删除", command=self.textdelete)


    # 删除函数
    def textdelete(self, text: Text):
        text.delete(SEL_FIRST, SEL_LAST)


    def callback(self):
        self.text.edit_undo()


def start_notepad():
    notepad = NotePad()
    notepad.text.bind("<Button-3>", notepad.popup)
    notepad.root.config(menu=notepad.topmenu)
    mainloop()


if __name__ == '__main__':
    start_notepad()
