"""
此模块用于制作wim映像文件。
"""
from subprocess import Popen, PIPE

_callback = lambda x: None

def set_callback_function(callback):
    """
    设置用于输出日志的回调函数。
    :param callback: 函数名
    :return:
    """
    global _callback
    _callback = callback

def make_dism(wim_path, folder_path, wim_name, wim_description, bootable):
    """
    从目标文件夹捕获wim映像。
    :param wim_path:wim映像保存路径
    :param folder_path:目标文件夹
    :param wim_name:wim映像卷名称（可选，留空请设为None）
    :param wim_description:wim映像卷描述（可选，留空请设为None）
    :param bootable:是否支持引导（True或False）
    :return:
    """
    # if bootable is True:
    #     _bootable = "/bootable"
    # else:
    #     _bootable = ""
    # if wim_name:
    #     _wim_name = f"/Name:{wim_name}"
    # else:
    #     _wim_name = ""
    # if wim_description:
    #     _wim_description = f"/Description:{wim_description}"
    # else:
    #     _wim_description = ""

    make_wim_command = ["dism", "/Capture-Image", f"/ImageFile:{wim_path}", f"/CaptureDir:{folder_path}"]

    if bootable is True:
        make_wim_command.append("/bootable")
    if wim_name:
        make_wim_command.append(f"/Name:{wim_name}")
    if wim_description:
        make_wim_command.append(f"/Description:{wim_description}")

    mount_log = Popen(make_wim_command, shell=True, text=True, stdout=PIPE, stderr=PIPE)

    # 处理日志输出
    while True:
        output_log = mount_log.stdout.readline()
        if output_log:
            print(output_log)
            _callback(output_log)
        else:
            break

if __name__ == '__main__':
    pass