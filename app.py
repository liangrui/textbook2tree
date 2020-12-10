# -*- coding: utf-8 -*-
"""
@author:liangrui
@file:app.py
@time:2020/12/10 17:27
@file_dese: 
"""
import pickle

if __name__ == '__main__':
    with open('./data/中医诊断学2_tree.pkl', 'rb') as tree_file:  ##注意打开方式一定要二进制形式打开
        tree = pickle.load(tree_file)
    tree.show()
