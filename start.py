from game.pvp import Application
from game.pve import runitapp
import tensorflow as tf
import tkinter


global graph
global mode_num, newApp
mode_num = 19
newApp = False


def pvp_start():
    app = Application(19)
    app.title('围棋人人对战')
    app.mainloop()


def pve_start():
    graph = tf.get_default_graph()
    runitapp(graph)


global graph
if __name__ == '__main__':
    top = tkinter.Tk()
    top.title('围棋游戏启动器')
    top.geometry('500x500')
    top.pvpButton = tkinter.Button(text='人人对战')
    top.pveButton = tkinter.Button(text='人机对战')
    top.mainloop()
