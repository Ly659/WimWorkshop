"""
文件或文件夹检测模块。

如果目标文件夹不存在，尝试创建一个文件夹；
如果目标文件夹是一个文件，抛出FolderTypeError；
如果目标文件不存在，抛出WimFileNotExistError；
如果目标文件类型有误，抛出WimFileTypeError；
"""
import os.path

# 以下两个函数可以从外部调用
# __all__ = ["file_check", "folder_check"]

# 定义几个异常，出错时抛出异常
class WimFileNotExistError(Exception):
    def __init__(self, file_path):
        self.file_path = file_path
    def __str__(self):
        return f"未找到文件“{self.file_path}”！"

class WimFileTypeError(Exception):
    def __init__(self, file_path):
        self.file_path = file_path
    def __str__(self):
        return f"所选文件“{self.file_path}”类型似乎不正确！"

class FolderTypeError(Exception):
    def __init__(self, folder_path):
        self.folder_path = folder_path
    def __str__(self):
        return f"所选文件夹“{self.folder_path}”不存在，或者不是文件夹！"

class CannotCreateFolderError(Exception):
    def __init__(self, folder_path):
        self.folder_path = folder_path
    def __str__(self):
        return f"无法创建指定的文件夹“{self.folder_path}。”"


def path_check(path):
    """
    检查文件或文件夹路径，确保路径分隔符正确。
    例如：传入的路径是C:/Windows/System32，返回的路径是C:\\Windows\\System32。
    :param path: 要检查的路径（字符串）
    :return: 修改后的路径
    """
    new_path = path
    if not path:
        raise FolderTypeError(path)

    if "/" in path:
        new_path = path.replace("/", "\\")
    return new_path

def file_check(file_path, file_head, file_head_byte):
    """
    此函数用于检查文件（文件路径、类型）是否正确，有误时抛出异常。
    抛出错误解释：
    WimFileTypeError：文件类型不正确
    WimFileNotExistError：文件不存在

    :param file_path: 目标文件的路径。
    :param file_head: 文件头数据，需要使用字节字符串（b-string）形式传入。例如：.wim映像文件的文件头是b"MSWIM"
    :param file_head_byte: 文件头的字节数。
    :return: 没有问题则返回True
    """
    file_path = path_check(file_path)

    # 判断文件是否存在，不存在则抛出异常
    if not os.path.exists(file_path):
        raise WimFileNotExistError(file_path)
    # 判断文件是否是一个文件夹，如果是则抛出异常
    if os.path.isdir(file_path):
        raise WimFileTypeError(file_path)
    # 查看文件后缀名，如果不是指定后缀则抛出异常
    ext = os.path.splitext(file_path)[1]
    if ext != ".wim":
        raise WimFileTypeError(file_path)
    # 读取文件头，判断文件类型，不正确则抛出异常
    wim_file = open(file_path, "rb")
    wim_data = wim_file.read(file_head_byte)
    wim_file.close()
    if not wim_data == file_head:
        raise WimFileTypeError(file_path)
    return True


def folder_check(folder_path):
    """
    此函数用于检查指定文件夹是否存在，或者类型是否正确。
    :param folder_path:目标文件夹路径。
    :return: 没有问题则返回True
    """
    folder_path = path_check(folder_path)

    # 判断目标文件夹是否存在，不存在则创建一个
    if os.path.exists(folder_path):
        # 如果目标根本不是文件夹，则抛出异常
        if not os.path.isdir(folder_path):
            raise FolderTypeError(folder_path)
    else:
        try:
            os.makedirs(folder_path)
        except Exception as err:
            raise CannotCreateFolderError(err)
    return True


if __name__ == '__main__':
    print("正在测试模块Checker……")
    file_path_test = input("请输入一个文件的路径：")
    head = input("请输入它的文件头字符串（如：MSWIM）：")
    file_head_test = head.encode("utf-8")               # 把输入的普通字符串转换为字节字符串（b-string）形式
    file_head_byte_test = int(input("请输入文件头长度（字节）："))
    print(file_check(file_path_test, file_head_test, file_head_byte_test))
    folder_path_test = input("请输入一个文件夹的路径：")
    print(folder_check(folder_path_test))
