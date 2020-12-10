# -*- coding: utf-8 -*-
"""
@author:liangr
@file:util.py
@time:2020/12/9 15:39
@file_dese:
    抽出公共的方法
"""
import re


def sub_key_rule1(line, patten):
    """
    第一章  绪  论 =>  绪  论
    第五章  诊断与病案 ==> 诊断与病案
        第一节、望  诊 =》望诊

    :param line:
    :return:
    """
    replacedStr = re.sub(patten, '', line)
    if replacedStr:
        replacedStr = replacedStr.replace(" ", "")
    return replacedStr


def sub_key_rule2(line, patten):
    rsstr = "None"
    objs = re.match('^\[(.*)\]', line)
    if objs:
        rsstr = objs.groups()[0]
    return rsstr


def content_rule1(line):
    replacedStr = re.sub('\[.*\]', '', line)
    return replacedStr


def sub_key_rule3(line, patten):
    replacedStr = line.replace(" ", "")
    return replacedStr


def get_content(line, cur_key):
    rs = []
    if '示意图' in line:
        tmp_items = line.split(' ')
        rs.append(tmp_items[0])
        rs.append(tmp_items[1].replace('示意图', ''))
    else:
        tmp_items = line.split(' ')
        rs.append(tmp_items[0])
        rs.append(line)
    return rs


def pop_items_stack(pre_key, cur_leve_no):
    # 弹出低层次的父类
    while not pre_key.is_empty():
        p_no, p_key = pre_key.gettop()
        if p_no >= cur_leve_no:
            pre_key.pop()
        else:
            break


class Stack(object):

    def __init__(self):
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def clear(self):
        self.stack.clear()

    def push(self, data):
        """
        进栈函数
        """
        self.stack.append(data)

    def pop(self):
        """
        出栈函数，
        """
        return self.stack.pop()

    def gettop(self):
        """
        取栈顶
        """
        return self.stack[-1]
