# -*- coding: utf-8 -*-
"""
@author:liangrui
@file:tools.py
@time:2020/9/3 11:05
@file_dese:
    教材树型化框架
    # 如何解决L6与L7混乱的情况，这个应该怎样处理？加入唯一的id
"""
import pickle
import re

from treelib import Node, Tree

from utilty import sub_key_rule1, Stack, sub_key_rule3, sub_key_rule2, content_rule1, pop_items_stack

level_trigger_dict = {
    "L1": '第.{1,2}章',
    "L2": '第.{1,2}节、',
    "L3": '^[一二三四五六七八九十]、',
    "L4": '^\([一二三四五六七八九十]\)',
    "L4-1": "[目|主|复]+.*[的|要|习]+.*[要|内|思]+.*[的|容|考]+[题]?",
    "L4-3": "复.*习.*思.*考.*题",
    "L5": '^[0123456789]{1,2}、',
    # "L6": '^\(\d\){1,2}',
    "L7": '^\[.*\]',
    "L8": '^\(\d\){1,2}',
    "txt": ""
}

level_sub_key = {
    "L1": (sub_key_rule1, None),
    "L2": (sub_key_rule1, None),
    "L3": (sub_key_rule1, None),
    "L4": (sub_key_rule1, None),
    "L4-1": (sub_key_rule3, None),
    "L4-2": (sub_key_rule3, None),
    "L4-3": (sub_key_rule3, None),
    "L5": (sub_key_rule1, None),
    # "L6": (sub_key_rule1, None),
    "L7": (sub_key_rule2, content_rule1),
    "L8": (sub_key_rule1, None),
    "txt": ""
}

global_no = 0


def generate_only_key():
    global global_no
    global_no += 1
    return global_no


def built_tcm_tree(tag, in_file, out_file):
    tree = Tree()
    id_key = generate_only_key()
    tree.create_node(tag=tag, identifier=id_key)
    with open(in_file, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()
    pre_key = Stack()
    pre_key.push((0, id_key))
    cur_line_no = 0
    for line in lines:
        try:
            line = line.replace('\n', '')
            if len(line) == 0:
                continue
            line = str.strip(line)
            cur_line_no += 1
            for i, key in enumerate(level_trigger_dict.keys()):
                if key != "txt":
                    if re.match(level_trigger_dict[key], line, re.M | re.I):
                        cur_leve_no = i + 1
                        # 把当前层的孩子及同层全部弹出
                        pop_items_stack(pre_key, cur_leve_no)
                        # 获取父层
                        p_cur_leve, p_id = pre_key.gettop()
                        cur_key = '%s_%s' % (cur_leve_no, level_sub_key[key][0](line, level_trigger_dict[key]))
                        # print("-" * i, line, '->', key, level_trigger_dict[key], cur_key)
                        id_key = generate_only_key()
                        node = Node(tag=cur_key, identifier=id_key)
                        # 可解释相关内容
                        if level_sub_key[key][1] is not None:
                            node.data = level_sub_key[key][1](line)
                        tree.add_node(node, parent=p_id)
                        pre_key.push((cur_leve_no, id_key))
                        break
                # 文本是一种特殊的情况
                else:
                    p_cur_leve, p_id = pre_key.gettop()
                    node = tree.get_node(p_id)
                    node.data = "%s%s" % (node.data if node.data else '', line)
        except Exception as e:
            print(e)
    # tree.subtree(nid=20).show()
    with open(out_file, 'wb') as tree_file:  ##注意打开方式一定要二进制形式打开
        pickle.dump(tree, tree_file)  ##把列表永久保存到文件中


if __name__ == '__main__':
    built_tcm_tree(tag="中医诊断学", in_file="./data/中医诊断学2.txt", out_file="./data/中医诊断学2_tree.pkl")
