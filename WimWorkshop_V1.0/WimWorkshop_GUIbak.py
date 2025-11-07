"""
WimWorkshop软件主程序，负责显示图形界面、捕获并显示异常、调用其他模块。
"""
import os
import tkinter as tk
import tkinter.ttk as ttk
# import multiprocessing
from threading import Thread
from tkinter import filedialog, messagebox
from tkinter.constants import ANCHOR

import Checker
import wim_init
import wim_maker
import wim_mounter

wim_info = ""

class ui_wim_index:
    def __init__(self, page, place_x, place_y, disable):
        """
        此类用于创建一个选择映像分卷号的控件。
        :param page: 标签页
        :param place_x: x坐标
        :param place_y: y坐标
        :param disable:是否禁止用户在映像名称、描述框内输入内容（True或False）此参数暂时未完成开发，没有作用
        """
        self.page = page
        self.place_x = place_x
        self.place_y = place_y
        self.wim_info = None
        self.wim_index = None       # 此属性为用户选择的映像分卷号，可以随时从类外部获取
        # 以下为UI控件
        self.spinbox_text = None
        self.Description_input_text = None
        self.name_input_text = None
        self.spinbox = None
        self.Description_input_box = None
        self.name_input_box = None
        self.disable = disable


        self.var = tk.StringVar()

        self.show_wim_index()


    def update_wim_index(self, info):
        """
        更新GUI界面wim文件的信息。
        :param info: 一个包含wim映像信息的字典，格式为 {1: ["映像名", "映像描述"], 2: ["映像名", "映像描述"], ……}
        :return:
        """
        self.wim_info = info
        print(self.wim_info)

        wim_sum = len(info)                         # 获取wim文件中的卷数量（即字典的长度）
        self.spinbox.configure(from_=1, to=wim_sum)     # 根据获取到的数量，设置映像选择的最大值
        # 更新分卷号选择框的序号为默认（第1卷）
        self.spinbox.delete(0, tk.END)
        self.spinbox.insert(0, 1)

    def update_wim_name(self, *args):
        """
        当wim映像分卷号选择控件的值被改变时，调用此函数以更新映像卷名称、映像卷描述框的内容。
        :return:
        """
        # 当分卷号选择框中有内容时才执行此函数，防止报错
        if self.spinbox.get() != "":
            current_sum = int(self.spinbox.get())       # 获取当前用户选择的映像分卷号
        else:
            return
        self.wim_index = current_sum

        if self.wim_info is None:
            return
        current_info  = self.wim_info [current_sum]
        wim_name = current_info [0]                  # 获取wim映像卷名称
        wim_description = current_info [1]           # 获取wim映像卷描述

        # 更新映像卷名称、映像卷描述框的内容
        self.name_input_box.delete(0, tk.END)
        self.name_input_box.insert(0, wim_name)
        self.Description_input_box.delete(0, tk.END)
        self.Description_input_box.insert(0, wim_description)

    def disable_input(self, work):
        """
        启用或禁用控件。
        :return:
        """
        #
        # mode = None
        # mode_text = None
        # a = self.name_input_box["state"]
        # if work == "enabled":
        #     if a == "disabled":
        #         mode = "enabled"
        #         mode_text = "normal"
        #     elif a == "enabled" or a == "normal":
        #         return
        # elif work == "disabled":
        #     if a == "normal" or a == "enabled":
        #         mode = mode_text = "disabled"
        #     elif self.name_input_box["state"] == "disabled":
        #         return
        #     else:
        #         print(self.name_input_box["state"])
        # else:
        #     return
        # self.spinbox.configure(state=mode)
        # self.Description_input_box.configure(state=mode)
        # self.name_input_box.configure(state=mode)
        # self.name_input_text.configure(state=mode_text)
        # self.spinbox_text.configure(state=mode_text)
        # self.Description_input_text.configure(state=mode_text)


    def show_wim_index(self):
        # 映像序号选择
        self.spinbox = ttk.Spinbox(self.page, width=4, from_=0, to=0, textvariable=self.var)
        self.var.trace('w', self.update_wim_name)
        self.spinbox.place(x=self.place_x, y=self.place_y)
        self.spinbox_text = tk.Label(self.page, text="分卷号：")
        self.spinbox_text.place(x=self.place_x - 70, y=self.place_y)
        # 映像名称输入框
        self.name_input_box = ttk.Entry(self.page, width=15)
        self.name_input_box.place(x=self.place_x, y=self.place_y + 25)
        self.name_input_text = tk.Label(self.page, text="映像名称：")
        self.name_input_text.place(x=self.place_x - 70, y=self.place_y + 25)
        # 映像描述输入框
        self.Description_input_box = ttk.Entry(self.page, width=15)
        self.Description_input_box.place(x=self.place_x, y=self.place_y + 50)
        self.Description_input_text = tk.Label(self.page, text="映像描述：")
        self.Description_input_text.place(x=self.place_x - 70, y=self.place_y + 50)


class ui_choose:
    def __init__(self, page, place_x, place_y, text, open_type):
        """
        ui_choose类用于创建选择文件或文件夹的窗口控件。包含：文字提示、路径输入框、浏览文件按钮。
        :param page: 创建控件的标签页
        :param place_x: 控件左上角的x坐标
        :param place_y: 控件左上角的y坐标
        :param text: 文字提示内容
        :param open_type: 选择类型。若为"file"则为选择文件；若为"folder"则选择文件夹
        """
        self.page = page
        self.text = text
        self.place_x = place_x
        self.place_y = place_y
        self.open_type = open_type
        self.var = tk.StringVar()                   # 创建StringVar对象，后面将用于输入框内容存入变量
        self.path = None                            # path属性为用户选择的文件（或文件夹）路径

        self.input = None
        self.button = None
        # 根据open_type选择打开文件或文件夹
        if self.open_type == "file":
            self.dialog = self.openfile_dialog
        elif self.open_type == "folder":
            self.dialog = self.openfolder_dialog

    def openfile_dialog(self):
        """
        调用此函数，创建一个选择文件的对话框。
        选择的文件路径将被赋值给全局变量file_path。文件路径输入框的内容改变时也会被赋值给这个变量。
        :return:无
        """

        self.path = filedialog.askopenfilename(title="浏览文件", filetypes=[("wim映像文件", "*.wim")])
        self.update_input(self.path)        # 调用update_input函数，更新输入框的内容
        # main_window.log_output(f"已选择文件：{self.path}")

    def openfolder_dialog(self):
        """
        调用此函数，创建一个选择文件夹的对话框。
        选择的文件夹路径将会被赋值给全局变量folder_path，文件夹路径输入框的内容在改变时也会被赋值给这个变量。
        :return:无
        """

        self.path = filedialog.askdirectory(title="浏览文件夹", initialdir=os.getcwd())
        self.update_input(self.path)        # 调用update_input函数，更新输入框的内容
        # main_window.log_output(f"已选择文件夹：{self.path}")

    def update_input(self, new_path):
        """
        用户选择文件或文件夹后调用此函数，更新输入框中的内容
        :param new_path: 更新后的输入框内容
        :return:无
        """
        # 如果用户没有选择（直接关闭了文件选择对话框）或选择路径不合法，则不更新输入框的内容！
        if not os.path.exists(new_path):
            return
        self.input.delete(0, tk.END)        # 清空输入框内容
        self.input.insert(0, new_path)      # 插入新的内容

    def show_choose(self):
        """
        创建控件的核心函数。
        :return: 无。
        """
        # 文字提示
        self.text = tk.Label(self.page, text=self.text)
        self.text.place(x=self.place_x, y=self.place_y)
        # 输入框
        self.input = ttk.Entry(self.page, width=30, textvariable=self.var)
        self.var.trace("w",self.update)                                 # StringVar对象与输入框绑定，用于在输入框内容改变时调用update函数
        self.input.place(x=self.place_x + 95, y=self.place_y)
        # 按钮
        self.button = ttk.Button(self.page, text="浏览", width=6, command=self.dialog)
        self.button.place(x=self.place_x + 320, y=self.place_y)

    def update(self, *args):
        """
        当输入框的内容被改变时，会调用此函数，将文件或文件夹输入框的值存入全局变量file_path和folder_path中
        注：选择文件、文件夹对话框的选择结果也会存入全局变量，同时更新输入框的值。
        :param args: 没什么用，但一定要有args，因为Var对象会传参过来
        :return: 无。
        """
        global wim_info
        # 获取输入框的内容，并存入path属性
        self.path = self.input.get()

        # 调用wim_init模块，获取wim文件的信息，存入wim_info变量
        wim_path = self.input.get()
        if os.path.isfile(wim_path):
            wim_info = wim_init.wim_get_info(wim_path)

    def get_result(self):
        """
        调用此函数，获取用户选择的文件或文件夹路径。
        :return: 用户选择的文件或文件夹路径（字符串）
        """
        return self.path


class ui_mounted_list:
    def __init__(self, root, place, size):
        """
        显示一个显示挂载列表的控件
        :param root:父窗口
        :param place:一个元组，指定控件的位置，格式为(x, y)
        :param size:一个元组，指定控件大小，格式为(宽, 高)
        """
        self.root = root
        self.place = place
        self.size = size
        self.mounted_list = []                  # 这个列表用于存储用户挂载的每一个映像的信息，格式为[(映像路径1, 挂载文件夹1), (映像路径2, 挂载文件夹2), ……]

        self.list = None
        self.text = None
        self.menu = None

        self.show_mounted_list()        # 初始化并显示挂载列表
        self.context_menu()             # 初始化列表右键菜单
        # self.add("什么也没有~~~")

    def add(self, wim_path, folder_path):
        """
        向列表中添加一个项目。
        :param wim_path: 项目名称
        :param folder_path: 挂载文件夹路径
        :return:
        """
        mount_info = (wim_path, folder_path)
        self.mounted_list.append(mount_info)            # 向列表中添加新加的挂载信息
        self.list.insert("end", wim_path)

    def remove(self, index):
        """
        从列表中删除一个项目。
        :param index: 要删除的项目序号
        :return:
        """
        self.list.delete(index)

    def context_menu(self):
        """
        初始化列表中的右键菜单项目
        :return:
        """
        self.menu = tk.Menu(self.list, tearoff=0)
        self.menu.add_command(label="打开挂载目录", command=self.open_mount_folder)
        self.menu.add_command(label="卸载映像", command=self.unmount_image)
        # 将list控件与show_context_menu函数绑定，使右键list时执行函数以显示右键菜单（<Button-3>表示鼠标右键点击）
        self.list.bind("<Button-3>", self.show_context_menu)

    def open_mount_folder(self):
        """
        点击“打开挂载目录”右键菜单时会调用此函数，打开挂载文件夹。
        :return:
        """
        select = self.list.curselection()                       # 获取当前用户选择的列表项
        select_folder = self.mounted_list [select [0]] [1]       # 根据列表项，获取挂载文件夹路径
        os.startfile(select_folder)                             # 打开文件夹

    def unmount_image(self):
        """
        点击“卸载映像”右键菜单时调用此函数。
        :return:
        """
        select = self.list.curselection()                           # 获取当前用户选择的列表项
        mount_folder = self.mounted_list [select [0]] [1]         # 根据列表项，获取挂载文件夹路径
        choice = ask_dialog("即将卸载映像。\n是否保存更改到映像文件？")
        if choice:
            wim_mounter.unmount_dism(mount_folder, True, select [0])
        else:
            wim_mounter.unmount_dism(mount_folder, False, select [0])


    def show_context_menu(self, event):
        """
        调用此函数，显示列表中的右键菜单
        :param event:
        :return:
        """
        # 若选中了一个项目，才会显示右键菜单（没有选中则为空字符串）
        if not self.list.get(ANCHOR) == "":
            self.menu.post(event.x_root, event.y_root)

    def show_mounted_list(self):
        """
        显示已挂载映像的列表
        :return:
        """
        self.text = tk.Label(self.root, text="已挂载的映像")
        self.list = tk.Listbox(self.root)
        self.list.place(x=self.place [0], y=self.place [1], width=self.size [0], height=self.size [1])
        self.text.place(x=self.place [0], y=self.place [1] - 25)


def error_dialog(err_info):
    """
    显示一个错误弹出窗口，文字内容自定义。
    :param err_info: 文字内容
    :return: 无
    """
    tk.messagebox.showerror(title="错误", message=err_info)

def ask_dialog(info):
    """
    显示一个询问弹窗
    :param info: 询问信息
    :return: True（是）或者False（否）或者None（点击 "x" 取消）
    """
    result = tk.messagebox.askyesno("请确认操作", info)
    return result


class WimWorkshop:
    def __init__(self):
        """
        WimWorkshop软件核心模块，负责配置和创建图形界面窗口
        """
        wim_mounter.set_callback_function(self.log_output)

        self.root = tk.Tk()
        self.root.geometry("640x460")                       # 默认窗口大小
        self.root.title("WimWorkshop - 内部开发版本")         # 窗口标题

        # 创建3个标签页
        self.tab_frame = ttk.Notebook(self.root)
        self.tab_frame.pack(expand=1, fill="both")
        self.tab1 = ttk.Frame(self.tab_frame)
        self.tab_frame.add(self.tab1, text="Tab1")
        self.tab2 = ttk.Frame(self.tab_frame)
        self.tab_frame.add(self.tab2, text="Tab2")
        self.tab3 = ttk.Frame(self.tab_frame)
        self.tab_frame.add(self.tab3, text="Tab3")

        # 初始化控件
        self.ui1 = ui_choose(self.tab1, 5, 10, "wim映像文件", "file")
        self.ui1.show_choose()
        self.ui2 = ui_choose(self.tab1, 5, 40, "目标文件夹", "folder")
        self.ui2.show_choose()
        self.ui3 = ui_choose(self.tab2, 5, 10, "目标文件夹", "folder")
        self.ui3.show_choose()
        self.ui4 = ui_choose(self.tab2, 5, 40, "wim文件保存", "file")
        self.ui4.show_choose()

        self.list = ui_mounted_list(self.tab1, (10, 180), (610, 100))

        # ==========标签1：操作按钮==========
        self.mount_button = (
            ttk.Button(
                self.tab1,
                text="挂载映像",
                style="TButton",
                width=15,
                state="disabled",
                command=lambda: self.start_work("tab1", "mount", str(self.ui5.wim_index))))
        self.extract_button = (
            ttk.Button(
                self.tab1,
                text="解开映像",
                style="TButton",
                width=15,state="disabled",
                command=lambda: self.start_work("tab1", "extract", str(self.ui5.wim_index))))
        # self.unmount_button = (
        #     ttk.Button(
        #         self.tab1,
        #         text="卸载映像",
        #         style="TButton",
        #         width=15,
        #         state="disabled",
        #         command=lambda: self.start_work("tab1", "unmount", str(self.ui5.wim_index))))
        self.new_button = (
            ttk.Button(
                self.tab2,
                text="新建映像",
                style="TButton",
                width=15,
                state="disabled",
                command=lambda: self.start_work("tab2", "new", str(self.ui5.wim_index))))

        self.mount_button.place(x=10, y=90)
        self.extract_button.place(x=135, y=90)
        # self.unmount_button.place(x=260, y=90)
        self.new_button.place(x=10, y=90)

        # 日志窗口
        self.log_text = tk.Label(self.root, text="日志窗口")
        self.log_text.place(x=10, y=320)
        self.log_window = tk.Text(self.root)
        # self.log_window.pack(fill="both", expand=1, pady=10, padx=5)
        self.log_window.place(x=10, y=350, width=620, height=90)

        # 映像信息显示控件
        self.ui5 = ui_wim_index(self.tab1, 500, 40, True)       # 标签页1
        self.ui6 = ui_wim_index(self.tab2, 500, 10, True)       # 标签页2

        self.load_wim_button = ttk.Button(self.tab1, width=25, text="加载选定的映像", command=self.load_wim_button)
        self.load_wim_button.place(x=430, y=10)

        self.log_output((None, "WimWorkshop_v1.0 内部版本 - 程序初始化完成。"))


        # self.root.mainloop()
        # print(f"tab1参数:{self.ui1.get_result()}   {self.ui2.get_result()}   \ntab2参数:{self.ui3.get_result()}   {self.ui4.get_result()}")

    def load_wim_button(self):
        """
        点击“加载映像”按钮时调用此函数。
        :return:
        """
        try:
            Checker.file_check(self.ui1.get_result(), b"MSWIM", 5)
        except Exception as err:
            error_dialog(err)
        else:
            # 更新显示文件信息
            self.ui5.update_wim_index(wim_info)
            # 将按钮设置为可点击状态
            self.mount_button.config(state="enabled")
            self.extract_button.config(state="enabled")
            # self.unmount_button.config(state="disabled")


    def log_output(self, log_text):
        """
        记录日志。
        :param log_text:一个元组，元组第一项是已挂载映像列表组件序号，一般不用，设为None即可；
        第二项是日志内容，str格式，注意以下特殊的通信内容，若非为了实现对应功能，请不要将日志内容设置为这些：
            1、finish：表示挂载操作完成，此时将已挂载项目添加到list列表框中。不会打印在日志窗口；
            2、unmount finished：表示卸载操作完成，此时会读取元组第一项的组件序号，删除list列表中的指定组件，不会打印在日志窗口。
        :return:
        """
        text = log_text [1]
        # 若返回内容为finish，则表明挂载操作已经完成。此时可以将已挂载项目添加到list列表框中。
        if text == "finish":
            self.list.add(self.wim_path, self.folder_path)
            return          # return不打印在日志窗口上
        elif text == "unmount finished":
            self.list.remove(log_text [0])
            return

        # self.log_window.delete(0, tk.END)
        self.log_window.insert(tk.END, text + "\n")
        self.log_window.see(tk.END)


    def start_work(self, tab, work, wim_index):
        """
        点击“挂载映像”等操作按钮时，调用此函数。
        :param tab:
        :param work:点击按钮所执行的工作。\n可用的工作有：\n"mount"挂载映像、\n"unmount"卸载映像、\n"extract"解开映像、\n"new"新建映像。\n
        :param wim_index:wim映像分卷号
        :return:无
        """
        # 获取用户选择的目标wim文件和文件夹的路径
        # wim_path = self.ui1.get_result()
        # folder_path = self.ui2.get_result()
        if tab == "tab1":
            wim_path = self.ui1.get_result()
            folder_path = self.ui2.get_result()
        elif tab == "tab2":
            folder_path = self.ui3.get_result()
            wim_path = self.ui4.get_result()
        else:
            return

        # 先调用Checker模块检查文件和文件夹路径是否正确
        try:
            Checker.file_check(wim_path, b"MSWIM", 5)
            Checker.folder_check(folder_path)
        except Exception as err:
            # 若文件（夹）路径不存在，则弹出错误窗口
            error_dialog(err)
            return

        # 检查、修改路径分隔符，避免dism报错：参数错误
        self.wim_path = Checker.path_check(wim_path)
        self.folder_path = Checker.path_check(folder_path)

        if work == "extract":
            # 解开映像
            # wim_mounter.extract_dism(wim_path, wim_index, folder_path)
            # multiprocessing.Process(target=wim_mounter.extract_dism, args=(wim_path, wim_index, folder_path), name="WIM_EXTRACT_PROCESS").start()               # 多线程（避免操作进行时界面未响应）
            # 用单独的线程执行，以便实时输出日志到GUI界面
            s1 = Thread(target=wim_mounter.extract_dism, args=(self.wim_path, wim_index, self.folder_path), name="WIM_EXTRACT_PROCESS")
            s1.start()
        elif work == "mount":
            # 挂载映像
            mount_choice = ask_dialog("是否使用只读模式挂载？\n如果你想稍后修改挂载文件夹中的文件，请不要使用只读模式。")
            if mount_choice:
                mount_mode = "ReadOnly"
            else:
                mount_mode = ""
            # wim_mounter.mount_dism(wim_path, wim_index, folder_path, mount_mode)
            # multiprocessing.Process(target=wim_mounter.mount_dism, args=(wim_path, wim_index, folder_path, mount_mode), name="WIM_MOUNT_PROCESS").start()       # 多线程
            # 用单独的线程执行，以便实时输出日志到GUI界面
            s2 = Thread(target=wim_mounter.mount_dism, args=(self.wim_path, wim_index, self.folder_path, mount_mode), name="WIM_MOUNT_PROCESS")
            s2.start()
        elif work == "unmount":
            pass
        elif work == "new":
            wim_maker.make_dism(self.wim_path, self.folder_path, None, None, False)
        else:
            return

if __name__ == '__main__':
    main_window = WimWorkshop()
    main_window.root.mainloop()
    print(f"tab1参数：{main_window.ui1.get_result(), main_window.ui2.get_result()}\ntab2参数：{main_window.ui3.get_result(), main_window.ui4.get_result()}")

# print("tab1参数：", file_path, folder_path, "\ntab2参数：", tab2_file_path, tab2_folder_path)
