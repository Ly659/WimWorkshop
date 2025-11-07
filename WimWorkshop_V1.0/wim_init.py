"""
此模块用于初始化wim文件，包括读取wim文件信息等功能。
"""
import os.path
import subprocess
__all__ = ["wim_get_info"]

def list_split(lst, sum1):
    data = []
    for item in range(0, len(lst), sum1):
        data.append(lst[item : item + sum1])
    return data


def wim_get_info(wim_file):
    """
    读取wim文件信息
    :param wim_file:目标wim映像文件路径
    :return: wim文件信息（一个字典）
    """
    if not os.path.isfile(wim_file):
        return None
    dism_get_wim_info = subprocess.Popen(["dism.exe", "/Get-WimInfo", "/English", f"/WimFile:{wim_file}"], shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # while True:
    #     a = info.stdout.readline()
    #     if a:
    #         print(a)
    #     else:
    #         break
    # 将dism返回的所有控制台信息保存为一个列表（每一行保存为一个列表项）
    info = dism_get_wim_info.stdout.readlines()

    # 替换所有\n为空
    # len(info)返回列表的长度
    for x in range(len(info)):
        info[x] = info[x].replace("\n", "")

    # 删除列表的所有空元素（即控制台输出的空行）
    while "" in info:
        info.remove("")

    print(info)

    # 筛选有用行（映像索引）
    list1 = []
    key = []
    for x in info:
        if "Index" in x:
            index = x[8:]               # 将分卷号的数字分割出来
            # print(x)
            # print(index)
            key.append(int(index))      # 将映像分卷号保存进列表key中

        if "Name" in x:
            name = x[7:]                # 将映像卷名称分割出来
            # print(x)
            # print(name)
            list1.append(name)          # 将映像卷名称保存进列表list1中

        if "Description" in x:
            description = x[14:]        # 将映像描述分割出来
            # print(x)
            # print(description)
            list1.append(description)   # 将映像描述保存进列表list1中

    # 分割列表list1，每2个列表项（卷名称和卷描述）分割为一个新列表
    # 新列表value：[[映像卷名称, 映像卷描述], [映像卷名称, 映像卷描述], ……]
    value = list_split(list1, 2)

    # 将列表key和value合并为一个字典（key作为键，value作为值），包含每个分卷的卷名和描述
    wim_info = dict(zip(key, value))
    # print(wim_info)
    return wim_info


if __name__ == '__main__':
    print("正在测试模块wim_init……\n=============================")
    test_wim_file = input("请输入一个wim文件的路径：")
    test_result = wim_get_info(test_wim_file)
    print(f"返回的内容为：{test_result}")
