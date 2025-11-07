"""
此模块负责挂载或解开wim映像文件。
"""
import subprocess


_callback = lambda x: None
exitcode = 0

def set_callback_function(callback):
    """
    设置用于输出日志的回调函数。
    :param callback:要传入的回调函数名
    :return:无
    """
    global _callback
    _callback = callback


def extract_dism(wim_file, wim_index, dest_dir):
    """
    解开映像到指定文件夹。
    :param wim_file: wim文件路径
    :param wim_index: wim映像分卷号
    :param dest_dir: 目标文件夹
    :return:
    """

    extract_log = subprocess.Popen(
        ["dism", "/Apply-Image", f"/ImageFile:{wim_file}", f"/ApplyDir:{dest_dir}", f"/Index:{wim_index}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True)

    # 处理输出日志
    while True:
        output_log = extract_log.stdout.readline()
        if output_log:
            _callback((None, output_log))
            print(output_log)
            # WimWorkshop_GUI.log_output(output_log)
        else:
            _callback((None, "\n\n\n"))
            break

def mount_dism(wim_file, wim_index, dest_dir, mode):
    """
    挂载映像到指定文件夹。
    :param wim_file: wim文件路径
    :param wim_index: wim映像分卷号
    :param dest_dir: 目标文件夹
    :param mode: 挂载模式（"/ReadOnly"为只读，None为可读写）
    :return:
    """
    global exitcode

    mount_command = [f"dism", "/Mount-Image", f"/ImageFile:{wim_file}", f"/MountDir:{dest_dir}", f"/Index:{wim_index}"]
    if mode == "ReadOnly":
        mount_command.append("/ReadOnly")

    mount_log = subprocess.Popen(mount_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    mount_log.wait()                # 等待程序执行完毕（必须要有）

    # 处理日志输出
    while True:
        output_log = mount_log.stdout.readline()        # 一行一行读取日志
        if output_log:
            _callback((None, output_log))                       # 通过回调函数将日志发送到主界面
            print(output_log)
        else:
            print("\n\n\n")
            break

    exitcode = mount_log.returncode         # 获取dism程序返回值（0为挂载操作成功完成）
    if exitcode == 0:
        _callback((None, "finish"))                 # 返回finish表示挂载操作已经完成
    else:
        _callback((None, "error"))                  # 返回error表示挂载出现错误

def unmount_dism(mounted_dir, save, choose_number):
    """
    卸载已经挂载的映像
    :param mounted_dir: 已经挂载的文件夹路径
    :param save:是否保存更改到镜像（True或False）
    :param choose_number: 用户选择的列表序号（卸载映像时不会用到，用于删除已卸载的列表项目）
    :return:
    """
    global exitcode

    unmount_command = ["dism", "/Unmount-Image", f"/MountDir:{mounted_dir}"]
    if save:
        unmount_command.append("/Commit")          # 保存更改
    else:
        unmount_command.append("/Discard")
    unmount_log = subprocess.Popen(unmount_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    unmount_log.wait()

    while True:
        output_log = unmount_log.stdout.readline()
        if output_log:
            _callback((None, output_log))
            print(output_log)
        else:
            print("\n\n\n")
            break

    exitcode = unmount_log.returncode
    if exitcode == 0:
        _callback((choose_number, "unmount finished"))
    else:
        _callback((None, "error"))


if __name__ == '__main__':
    pass
