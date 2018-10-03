# # 关于表的 **增** **删** **改**

# from pathlib import Path
# import csv
# import re
# from common import print_infos,check_item_condition

# base_dir = Path(__file__).cwd()
# data = base_dir.joinpath("data")


# class Table():
#     """
#         表类
#     """
#     def __init__(self,table,share_lock,exclude_lock):
#         """
#             table:  type:Path 表的路径对象
#             share_lock: type: bool 共享锁
#             exclude_lock: type:bool 排他锁
#         """
#         self.table = table
#         self.share_lock = share_lock
#         self.exclude_lock = exclude_lock

    
