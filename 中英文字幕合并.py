# -*- coding:utf-8 -*-
# name: myb
# 读取同级文件夹 chinese_subtitles 和 english_subtitles 下同一顺序的文件的内容，将里面的中文与英文进行合并

import os
import re
import pandas as pd


# 读取文件夹下所有文件名
def get_file_name(path):
    file_names = os.listdir(path)
    # 排序
    file_names.sort()
    return file_names


# 读取文件内容
def read_srt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    subtitles = []
    sub = ''
    for line in lines:
        if line.strip().isdigit():  # 如果是数字，说明是序号，跳过
            if sub:  # 如果sub不为空，说明是上一个字幕的结束，将其加入subtitles
                subtitles.append(sub.strip())
                sub = ''
        else:
            sub += line.strip() + ' '

    # 将时间去掉
    subtitles = [re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', content) for content in subtitles]
    # 转成df
    df = pd.DataFrame(subtitles, columns=['content'])
    return df


# 将两个df按行合并
def merge_df(df1, df2):
    df = pd.concat([df1, df2], axis=1)
    return df


# 将上面的逻辑进行封装
def merge_srt_files(file1, file2, serial_num):
    contents = merge_df(read_srt_file(file1), read_srt_file(file2))
    # 写入文件，要求不覆盖之前的记录
    with open('prompt_eng_intro.txt', 'a') as file:
        # 将文件名写入，文件名为： 按'_'分割，除去最后一个单词的其他字符串
        file.write(f'# {serial_num}、 ' + '_'.join(file1.split('/')[-1].split('_')[:-1]) + '\n')
        for i in range(len(contents)):
            file.write(contents.iloc[i, 0] + '\n')
            file.write(contents.iloc[i, 1] + '\n')
            file.write('\n')


def merge_srt_files_from_folder(folder1, folder2):
    file_names1 = get_file_name(folder1)
    file_names2 = get_file_name(folder2)
    for i in range(len(file_names1)):
        file1 = folder1 + '/' + file_names1[i]
        file2 = folder2 + '/' + file_names2[i]
        merge_srt_files(file1, file2, i + 1)


folder1 = "english_subtitles"
folder2 = "chinese_subtitles"
merge_srt_files_from_folder(folder1, folder2)
# merge_srt_files_from_folder(folder1, folder2)
