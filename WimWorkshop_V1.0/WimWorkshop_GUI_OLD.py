"""
WimWorkshop软件主程序，负责显示图形界面、捕获并显示异常、调用其他模块。
"""
import tkinter as tk
import tkinter.ttk as ttk
import os
from tkinter import filedialog, messagebox
import Checker
import wim_mounter

path = ""

class ui_choose:
    def __init__(self, page, place_x, place_y, text, open_type):
        """
        ui_choose类用于创建选择文件或文件夹的窗口控件。包含：文字提示、路径输入框、浏览文件按钮。
        :param window_root: 根窗口
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
        # if self.page == tab1:                     # 不同的标签页，使用不同的变量！否则不同标签页选择的文件会混淆
        #     self.file_path = file_path
        #     self.folder_path = folder_path
        # elif self.page == tab2:
        #     self.file_path = tab2_file_path
        #     self.folder_path = tab2_folder_path
        self.path = None                            # path属性为用户选择的文件（或文件夹）路径

        self.input = None
        self.button = None
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
        # global file_path

        # log_print("打开文件！")
        self.path = filedialog.askopenfilename(title="浏览文件", filetypes=[("wim映像文件", "*.wim")])
        # log_print(f"函数openfile_dialog：当前文件路径{self.file_path}")
        self.update_input(self.path)        # 调用update_input函数，更新输入框的内容

    def openfolder_dialog(self):
        """
        调用此函数，创建一个选择文件夹的对话框。
        选择的文件夹路径将会被赋值给全局变量folder_path，文件夹路径输入框的内容在改变时也会被赋值给这个变量。
        :return:无
        """
        # global folder_path

        # log_print("打开文件夹！")
        self.path = filedialog.askdirectory(title="浏览文件夹", initialdir=os.getcwd())
        # log_Viewer.log_print(f"函数openfolder_dialog：当前文件夹路径{self.folder_path}")
        self.update_input(self.path)        # 调用update_input函数，更新输入框的内容

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
        当输入框的内容被改变时，会调用此函数，将文件和文件夹输入框的值存入全局变量file_path和folder_path中
        注：选择文件、文件夹对话框的选择结果也会存入全局变量，同时更新输入框的值。
        :param args: 没什么用，但一定要有args，因为Var对象会传参过来
        :return: 无。
        """
        #global file_path, folder_path, tab2_file_path, tab2_folder_path
        global path
        # if self.open_type == "folder":
        #     # if self.page == tab1:
        #     #     folder_path = self.input.get()
        #     # elif self.page == tab2:
        #     #     tab2_folder_path = self.input.get()
        #
        # elif self.open_type == "file":
        #     if self.page == tab1:
        #         file_path = self.input.get()
        #     elif self.page == tab2:
        #         tab2_file_path = self.input.get()
        path = self.input.get()

    def get_result(self):
        """
        调用此函数，获取用户选择的文件或文件夹路径。
        :return: 用户选择的文件或文件夹路径（字符串）
        """
        return self.path


# class work_buttons:
#     def __init__(self, page, place_x, place_y, work):
#         """
#         在各个标签页创建不同的操作按钮。
#         :param page: 目标标签页变量名
#         :param place_x: x坐标
#         :param place_y: y坐标
#         :param work:
#         """
#         self.page = page
#         self.place_x = place_x
#         self.place_y = place_y
#         self.work = work
#         if page == tab1:
#             self.work_button_tab1()
#         elif page == tab2:
#             self.work_button_tab2()
#
#     def work_button_tab1(self):
#         """
#         在标签1创建按钮。
#         :return:
#         """
#         mount_button1 = ttk.Button(self.page, text="挂载映像", style="TButton", width=15)
#         mount_button1.place(x=self.place_x, y=self.place_y)
#         extract_button1 = ttk.Button(self.page, text="解开映像", style="TButton", width=15)
#         extract_button1.place(x=self.place_x + 95, y=self.place_y)
#         unmount_button1 = ttk.Button(self.page, text="卸载映像", style="TButton", width=15)
#         unmount_button1.place(x=self.place_x + 320, y=self.place_y)
#
#     def work_button_tab2(self):
#         """
#         在标签2新建按钮。
#         :return:
#         """
#         new_button2 = ttk.Button(self.page, text="新建映像", style="TButton", width=15)
#         new_button2.place(x=self.place_x, y=self.place_y)


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


# file_path = None
# folder_path = None
# tab2_file_path = None
# tab2_folder_path = None


class WimWorkshop:
    def __init__(self):
        """
        WimWorkshop软件核心模块，负责配置和创建图形界面窗口
        """
        self.root = tk.Tk()
        self.root.geometry("850x350")                       # 默认窗口大小
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

        # ==========标签1：操作按钮==========
        # mount_button = ttk.Button(tab1, text="挂载映像", style="TButton", width=15, command=lambda: Checker.file_check(ui1.file_path, b"MSWIM", 5))
        self.mount_button = ttk.Button(self.tab1, text="挂载映像", style="TButton", width=15, command=lambda: self.start_work("mount"))
        self.extract_button = ttk.Button(self.tab1, text="解开映像", style="TButton", width=15, command=lambda: self.start_work("extract"))
        self.unmount_button = ttk.Button(self.tab1, text="卸载映像", style="TButton", width=15, command=lambda: self.start_work("unmount"))
        self.new_button = ttk.Button(self.tab2, text="新建映像", style="TButton", width=15, command=lambda: self.start_work("new"))
        self.mount_button.place(x=10, y=90)
        self.extract_button.place(x=135, y=90)
        self.unmount_button.place(x=260, y=90)
        self.new_button.place(x=10, y=90)

        self.root.mainloop()
        print(f"tab1:{self.ui1.get_result()}   {self.ui2.get_result()}   \ntab2:{self.ui3.get_result()}   {self.ui4.get_result()}")

    def start_work(self, work):
        """
        点击“挂载映像”等操作按钮时，调用此函数。
        :param work:点击按钮所执行的工作。\n可用的工作有：\n"mount"挂载映像、\n"unmount"卸载映像、\n"extract"解开映像、\n"new"新建映像。\n
        :return:无
        """
        # global file_path, folder_path
        # 获取用户选择的目标wim文件和文件夹的路径
        wim_path = self.ui1.get_result()
        folder_path = self.ui2.get_result()

        # 先调用Checker模块检查文件和文件夹路径是否正确
        try:
            Checker.file_check(wim_path, b"MSWIM", 5)
            Checker.folder_check(folder_path)
        except Exception as err:
            error_dialog(err)
            return

        if work == "extract":
            wim_mounter.extract_dism(wim_path, "1", folder_path)
        #     while True:
        #         # log_print(wim_mounter.log)
        #         if not wim_mounter.log:
        #             break
        elif work == "mount":
            mount_mode = ask_dialog("是否使用只读模式挂载？\n如果你想稍后修改挂载文件夹中的文件，请不要使用只读模式。")
            if mount_mode == "True":
                mount_mode = "/ReadOnly"
            else:
                mount_mode = ""
            wim_mounter.mount_dism(wim_path, "1", folder_path, mount_mode)


"""
# 创建根窗口
root = tk.Tk()
# 窗口大小
root.geometry("850x350")
# 窗口标题
root.title("WimWorkshop - 内部开发版本")

# 创建3个标签页
tab_frame = ttk.Notebook(root)
tab_frame.pack(expand=1, fill="both")
tab1 = ttk.Frame(tab_frame)
tab_frame.add(tab1, text="Tab1")
tab2 = ttk.Frame(tab_frame)
tab_frame.add(tab2, text="Tab2")
tab3 = ttk.Frame(tab_frame)
tab_frame.add(tab3, text="Tab3")

# 初始化控件
ui1 = ui_choose(root, tab1, 5, 10, "wim映像文件", "file")
ui1.show_choose()
ui2 = ui_choose(root, tab1, 5, 40, "目标文件夹", "folder")
ui2.show_choose()
ui3 = ui_choose(root, tab2, 5, 10, "目标文件夹", "folder")
ui3.show_choose()
ui4 = ui_choose(root, tab2, 5, 40, "wim文件保存", "file")
ui4.show_choose()


# ==========标签1：操作按钮==========
# mount_button = ttk.Button(tab1, text="挂载映像", style="TButton", width=15, command=lambda: Checker.file_check(ui1.file_path, b"MSWIM", 5))
mount_button = ttk.Button(tab1, text="挂载映像", style="TButton", width=15, command=lambda: start_work(tab1, "mount"))
extract_button = ttk.Button(tab1, text="解开映像", style="TButton", width=15, command=lambda: start_work(tab1, "extract"))
unmount_button = ttk.Button(tab1, text="卸载映像", style="TButton", width=15, command=lambda: start_work(tab1, "unmount"))
new_button = ttk.Button(tab2, text="新建映像", style="TButton", width=15, command=lambda: start_work(tab2, "new"))
mount_button.place(x=10, y=90)
extract_button.place(x=135, y=90)
unmount_button.place(x=260, y=90)
new_button.place(x=10, y=90)

# log_print("========== WimWorkshop 内部版本 v1.0 ==========\n程序初始化完成！")
root.mainloop()
"""
if __name__ == '__main__':
    WimWorkshop()

# print("tab1参数：", file_path, folder_path, "\ntab2参数：", tab2_file_path, tab2_folder_path)


