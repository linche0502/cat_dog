# 使用python-embed版時要加這2行
import sys, os
sys.path.append(os.path.dirname(__file__))


from dlclive import DLCLive, Processor

dlc_proc = Processor()
dlc_live = DLCLive("data/", processor=dlc_proc)
dlc_live.init_inference("")
dlc_live.get_pose("")

