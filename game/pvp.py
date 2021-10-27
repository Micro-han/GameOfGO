from tkinter import *
from tkinter.ttk import *
import copy
import tkinter.messagebox


class Application(Tk):
    def __init__(self, my_mode_num=19, newApp=False):
        Tk.__init__(self)
        # mode_num 棋盘大小 size 窗口尺寸 gridLen 格子变长 boardProp 对应于九路棋盘的矫正比例
        self.mode_num = my_mode_num
        self.size = 1.8
        self.gridLen = 360 * self.size / (self.mode_num - 1)
        self.boardProp = 1 if self.mode_num == 9 else (2 / 3 if self.mode_num == 13 else 4 / 9)
        self.boardPosition = [[0 for i in range(self.mode_num + 2)] for i in range(self.mode_num + 2)]

        # boardPosition 棋盘 0代表无子 -1 代表边界 1是黑子 2是白子
        for i in range(self.mode_num + 2):
            for j in range(self.mode_num + 2):
                if i * j == 0 or i == self.mode_num + 1 or j == self.mode_num + 1:
                    self.boardPosition[i][j] = -1
                else:
                    self.boardPosition[i][j] = 0

        # 拷贝三份用于打劫和悔棋
        self.boardLast1 = copy.deepcopy(self.boardPosition)
        self.boardLast2 = copy.deepcopy(self.boardPosition)
        self.boardLast3 = copy.deepcopy(self.boardPosition)

        # lastCross 鼠标经过的位置 nowPlayer 现在轮到谁 playStop 停止运行 regretNum 后悔
        self.lastCross = None
        self.nowPlayer = 0
        self.playStop = True
        self.regretNum = 0
        self.cross = None
        self.image_added = None
        self.image_added_sign = None

        # 引用图片 坑点tkinter只能引用gif文件
        self.photoWhite = PhotoImage(file="./dlgo/httpfrontend/Pictures/W.gif")
        self.photoBlack = PhotoImage(file="./dlgo/httpfrontend/Pictures/B.gif")
        self.photoBlackDone = PhotoImage(file="./dlgo/httpfrontend/Pictures/" + "BD" + "-" + str(self.mode_num) + ".gif")
        self.photoWhiteDone = PhotoImage(file="./dlgo/httpfrontend/Pictures/" + "WD" + "-" + str(self.mode_num) + ".gif")
        self.photoBlackUse = PhotoImage(file="./dlgo/httpfrontend/Pictures/" + "BU" + "-" + str(self.mode_num) + ".gif")
        self.photoWhiteUse = PhotoImage(file="./dlgo/httpfrontend/Pictures/" + "WU" + "-" + str(self.mode_num) + ".gif")

        # 黑白棋子切换
        self.photoWhiteBlackUse_list = [self.photoBlackUse, self.photoWhiteUse]
        self.photoWhiteBlackDone_list = [self.photoBlackDone, self.photoWhiteDone]

        # 布局页面 设置画布按钮
        self.geometry(str(int(600 * self.size)) + 'x' + str(int(400 * self.size)))
        self.canvas_bottom = Canvas(self, bg='#369', bd=0, width=600 * self.size, height=400 * self.size)
        self.canvas_bottom.place(x=0, y=0)
        # 几个功能按钮
        self.startBottom = Button(self, text='开始游戏', command=self.start)
        self.startBottom.place(x=480 * self.size, y=200 * self.size)
        self.pass1Button = Button(self, text='放弃一轮', command=self.pass1)
        self.pass1Button.place(x=480 * self.size, y=225 * self.size)
        self.regretButton = Button(self, text='反悔上步', command=self.regret)
        self.regretButton.place(x=480 * self.size, y=250 * self.size)
        self.regretButton['state'] = DISABLED
        # self.newGameButton1 = Button(self, text=('十三' if self.mode_num == 9 else '九') + '路棋', command=self.newGame1)
        # self.newGameButton1.place(x=480 * self.size, y=300 * self.size)
        # self.newGameButton2 = Button(self, text=('十三' if self.mode_num == 19 else '十九') + '路棋', command=self.newGame2)
        # self.newGameButton2.place(x=480 * self.size, y=325 * self.size)
        self.replayButton = Button(self, text='重新开始', command=self.reload)
        self.replayButton.place(x=480 * self.size, y=275 * self.size)
        self.quitButton = Button(self, text='退出游戏', command=self.quit)
        self.quitButton.place(x=480 * self.size, y=350 * self.size)

        # 画棋盘 画九个点 画线
        self.canvas_bottom.create_rectangle(0 * self.size, 0 * self.size, 400 * self.size, 400 * self.size, fill='#c51')
        self.canvas_bottom.create_rectangle(20 * self.size, 20 * self.size, 380 * self.size, 380 * self.size, width=3)
        for m in [-1, 0, 1]:
            for n in [-1, 0, 1]:
                self.oval = self.canvas_bottom.create_oval(200 * self.size - self.size * 2,
                                                           200 * self.size - self.size * 2,
                                                           200 * self.size + self.size * 2,
                                                           200 * self.size + self.size * 2, fill='#000')
                self.canvas_bottom.move(self.oval,
                                        m * self.gridLen * (
                                            2 if self.mode_num == 9 else (3 if self.mode_num == 13 else 6)),
                                        n * self.gridLen * (
                                            2 if self.mode_num == 9 else (3 if self.mode_num == 13 else 6)))
        for i in range(1, self.mode_num - 1):
            self.canvas_bottom.create_line(20 * self.size, 20 * self.size + i * self.gridLen, 380 * self.size,
                                           20 * self.size + i * self.gridLen, width=2)
            self.canvas_bottom.create_line(20 * self.size + i * self.gridLen, 20 * self.size,
                                           20 * self.size + i * self.gridLen,
                                           380 * self.size, width=2)

        # 放置右侧初始图片
        self.placeWhite = self.canvas_bottom.create_image(500 * self.size + 11, 65 * self.size, image=self.photoWhite)
        self.placeBlack = self.canvas_bottom.create_image(500 * self.size - 11, 65 * self.size, image=self.photoBlack)
        # 每张图片都添加image标签，方便reload函数删除图片
        self.canvas_bottom.addtag_withtag('image', self.placeWhite)
        self.canvas_bottom.addtag_withtag('image', self.placeBlack)
        # 鼠标移动时，调用shadow函数，显示随鼠标移动的棋子
        self.canvas_bottom.bind('<Motion>', self.shadow)
        # 鼠标左键单击时，调用getdown函数，放下棋子
        self.canvas_bottom.bind('<Button-1>', self.getDown)

    def start(self):
        # 实现太极图的动态
        self.canvas_bottom.delete(self.placeWhite)
        self.canvas_bottom.delete(self.placeBlack)
        if self.nowPlayer == 0:
            self.create_placeBlack()
            self.delete_placeWhite()
        else:
            self.create_placeWhite()
            self.delete_placeBlack()
        # 开始游戏
        self.playStop = None

    def pass1(self):
        # 放弃一轮
        if not self.regretNum == 1:
            self.regretNum += 1
        else:
            self.regretButton['state'] = NORMAL

        self.boardLast3 = copy.deepcopy(self.boardLast2)
        self.boardLast2 = copy.deepcopy(self.boardLast1)
        self.boardLast1 = copy.deepcopy(self.boardPosition)
        self.canvas_bottom.delete('image_added_sign')

        if self.nowPlayer == 0:
            self.create_placeBlack()
            self.delete_placeWhite()
            self.nowPlayer = 1
        else:
            self.create_placeWhite()
            self.delete_placeBlack()
            self.nowPlayer = 0

    def regret(self):
        if self.regretNum != 1:
            return
        self.regretNum = 0
        self.regretButton['state'] = DISABLED
        list_of_black = []
        list_of_white = []
        self.canvas_bottom.delete('image')
        if self.nowPlayer == 0:
            self.create_placeBlack()
        else:
            self.create_placeWhite()
        for m in range(1, self.mode_num + 1):
            for n in range(1, self.mode_num + 1):
                self.boardPosition[m][n] = 0
        for m in range(len(self.boardLast3)):
            for n in range(len(self.boardLast3[m])):
                if self.boardLast3[m][n] == 1:
                    list_of_black += [[n, m]]
                elif self.boardLast3[m][n] == 2:
                    list_of_white += [[n, m]]
        self.recover(list_of_black, 0)
        self.recover(list_of_white, 1)
        self.boardLast1 = copy.deepcopy(self.boardLast3)
        for m in range(1, self.mode_num + 1):
            for n in range(1, self.mode_num + 1):
                self.boardLast2[m][n] = 0
                self.boardLast3[m][n] = 0

    def reload(self):
        if self.playStop == 1:
            self.playStop = 0
        self.canvas_bottom.delete('image')
        self.regretNum = 0
        self.nowPlayer = 0
        self.create_placeBlack()
        for m in range(1, self.mode_num + 1):
            for n in range(1, self.mode_num + 1):
                self.boardPosition[m][n] = 0
                self.boardLast3[m][n] = 0
                self.boardLast2[m][n] = 0
                self.boardLast1[m][n] = 0

    # 以下四个函数实现了右侧太极图的动态创建与删除
    def create_placeWhite(self):
        self.placeWhite = self.canvas_bottom.create_image(500 * self.size + 11, 65 * self.size, image=self.photoWhite)
        self.canvas_bottom.addtag_withtag('image', self.placeWhite)

    def create_placeBlack(self):
        self.placeBlack = self.canvas_bottom.create_image(500 * self.size - 11, 65 * self.size, image=self.photoBlack)
        self.canvas_bottom.addtag_withtag('image', self.placeBlack)

    def delete_placeWhite(self):
        self.canvas_bottom.delete(self.placeWhite)

    def delete_placeBlack(self):
        self.canvas_bottom.delete(self.placeBlack)

    def shadow(self, event):
        if self.playStop:
            return
        if (20 * self.size < event.x < 380 * self.size) and (20 * self.size < event.y < 380 * self.size):
            dx = (event.x - 20 * self.size) % self.gridLen
            dy = (event.y - 20 * self.size) % self.gridLen
            self.cross = self.canvas_bottom.create_image(
                event.x - dx + round(dx / self.gridLen) * self.gridLen + 22 * self.boardProp,
                event.y - dy + round(dy / self.gridLen) * self.gridLen - 27 * self.boardProp,
                image=self.photoWhiteBlackUse_list[self.nowPlayer])
            self.canvas_bottom.addtag_withtag('image', self.cross)
            if self.lastCross is not None:
                self.canvas_bottom.delete(self.lastCross)
            self.lastCross = self.cross

    def getDown(self, event):
        if not self.playStop:
            # 先找到最近格点
            if (20 * self.size - self.gridLen * 0.4 < event.x < self.gridLen * 0.4 + 380 * self.size) and (
                    20 * self.size - self.gridLen * 0.4 < event.y < self.gridLen * 0.4 + 380 * self.size):
                dx = (event.x - 20 * self.size) % self.gridLen
                dy = (event.y - 20 * self.size) % self.gridLen
                x = int((event.x - 20 * self.size - dx) / self.gridLen + round(dx / self.gridLen) + 1)
                y = int((event.y - 20 * self.size - dy) / self.gridLen + round(dy / self.gridLen) + 1)
                # 判断位置是否已经被占据
                if self.boardPosition[y][x] == 0:
                    # 未被占据，则尝试占据，获得占据后能杀死的棋子列表
                    self.boardPosition[y][x] = self.nowPlayer + 1
                    self.image_added = self.canvas_bottom.create_image(
                        event.x - dx + round(dx / self.gridLen) * self.gridLen + 4 * self.boardProp,
                        event.y - dy + round(dy / self.gridLen) * self.gridLen - 5 * self.boardProp,
                        image=self.photoWhiteBlackDone_list[self.nowPlayer])
                    self.canvas_bottom.addtag_withtag('image', self.image_added)
                    # 棋子与位置标签绑定，方便“杀死”
                    self.canvas_bottom.addtag_withtag('position' + str(x) + str(y), self.image_added)
                    deadlist = self.get_deadlist(x, y)
                    self.kill(deadlist)
                    # 判断是否重复棋局
                    if not self.boardLast2 == self.boardPosition:
                        # 判断是否属于有气和杀死对方其中之一
                        if len(deadlist) > 0 or self.if_dead([[x, y]], self.nowPlayer + 1, [x, y]) == False:
                            # 当不重复棋局，且属于有气和杀死对方其中之一时，落下棋子有效
                            if not self.regretNum == 1:
                                self.regretNum += 1
                            else:
                                self.regretButton['state'] = NORMAL
                            self.boardLast3 = copy.deepcopy(self.boardLast2)
                            self.boardLast2 = copy.deepcopy(self.boardLast1)
                            self.boardLast1 = copy.deepcopy(self.boardPosition)
                            # 删除上次的标记，重新创建标记
                            self.canvas_bottom.delete('image_added_sign')
                            self.image_added_sign = self.canvas_bottom.create_oval(
                                event.x - dx + round(dx / self.gridLen) * self.gridLen + 0.5 * self.gridLen,
                                event.y - dy + round(dy / self.gridLen) * self.gridLen + 0.5 * self.gridLen,
                                event.x - dx + round(dx / self.gridLen) * self.gridLen - 0.5 * self.gridLen,
                                event.y - dy + round(dy / self.gridLen) * self.gridLen - 0.5 * self.gridLen, width=3, outline='#3ae')
                            self.canvas_bottom.addtag_withtag('image', self.image_added_sign)
                            self.canvas_bottom.addtag_withtag('image_added_sign', self.image_added_sign)
                            if self.nowPlayer == 0:
                                self.create_placeWhite()
                                self.delete_placeBlack()
                                self.nowPlayer = 1
                            else:
                                self.create_placeBlack()
                                self.delete_placeWhite()
                                self.nowPlayer = 0
                        else:
                            # 不属于杀死对方或有气，则判断为无气，警告并弹出警告框
                            self.boardPosition[y][x] = 0
                            self.canvas_bottom.delete('position' + str(x) + str(y))
                            self.bell()
                            self.showWarningBox('无气', "你不能下在这！")
                    else:
                        # 重复棋局，警告打劫
                        self.boardPosition[y][x] = 0
                        self.canvas_bottom.delete('position' + str(x) + str(y))
                        self.recover(deadlist, (1 if self.nowPlayer == 0 else 0))
                        self.bell()
                        self.showWarningBox("打劫", "你不能下在这！")
                else:
                    # 覆盖，声音警告
                    self.bell()
            else:
                # 超出边界，声音警告
                self.bell()

    def showWarningBox(self, title, message):
        self.canvas_bottom.delete(self.cross)
        tkinter.messagebox.showwarning(title, message)

    # 一个写的很丑的判断是否有气的函数，初始deadlist只包含了自己的位置，每次执行时，函数尝试寻找yourPosition周围有没有空的位置，有则结束，返回False代表有气
    # 若找不到，则找自己四周的同类（不在deadlist中的）是否有气，即调用本函数，无气，则把该同类加入到deadlist，然后找下一个邻居，只要有一个有气，返回False代表有气；
    # 若四周没有一个有气的同类，返回deadlist,至此结束递归
    def if_dead(self, deadList, yourChessman, yourPosition):
        for i in [-1, 1]:
            if [yourPosition[0] + i, yourPosition[1]] not in deadList:
                if self.boardPosition[yourPosition[1]][yourPosition[0] + i] == 0:
                    return False
            if [yourPosition[0], yourPosition[1] + i] not in deadList:
                if self.boardPosition[yourPosition[1] + i][yourPosition[0]] == 0:
                    return False
        if ([yourPosition[0] + 1, yourPosition[1]] not in deadList) and (
                self.boardPosition[yourPosition[1]][yourPosition[0] + 1] == yourChessman):
            midvar = self.if_dead(deadList + [[yourPosition[0] + 1, yourPosition[1]]], yourChessman,
                                  [yourPosition[0] + 1, yourPosition[1]])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        if ([yourPosition[0] - 1, yourPosition[1]] not in deadList) and (
                self.boardPosition[yourPosition[1]][yourPosition[0] - 1] == yourChessman):
            midvar = self.if_dead(deadList + [[yourPosition[0] - 1, yourPosition[1]]], yourChessman,
                                  [yourPosition[0] - 1, yourPosition[1]])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        if ([yourPosition[0], yourPosition[1] + 1] not in deadList) and (
                self.boardPosition[yourPosition[1] + 1][yourPosition[0]] == yourChessman):
            midvar = self.if_dead(deadList + [[yourPosition[0], yourPosition[1] + 1]], yourChessman,
                                  [yourPosition[0], yourPosition[1] + 1])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        if ([yourPosition[0], yourPosition[1] - 1] not in deadList) and (
                self.boardPosition[yourPosition[1] - 1][yourPosition[0]] == yourChessman):
            midvar = self.if_dead(deadList + [[yourPosition[0], yourPosition[1] - 1]], yourChessman,
                                  [yourPosition[0], yourPosition[1] - 1])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        return deadList

    # 落子后，依次判断四周是否有棋子被杀死，并返回死棋位置列表
    def get_deadlist(self, x, y):
        deadlist = []
        for i in [-1, 1]:
            if self.boardPosition[y][x + i] == (2 if self.nowPlayer == 0 else 1) and ([x + i, y] not in deadlist):
                killList = self.if_dead([[x + i, y]], (2 if self.nowPlayer == 0 else 1), [x + i, y])
                if not killList == False:
                    deadlist += copy.deepcopy(killList)
            if self.boardPosition[y + i][x] == (2 if self.nowPlayer == 0 else 1) and ([x, y + i] not in deadlist):
                killList = self.if_dead([[x, y + i]], (2 if self.nowPlayer == 0 else 1), [x, y + i])
                if not killList == False:
                    deadlist += copy.deepcopy(killList)
        return deadlist

    # 恢复位置列表list_to_recover为b_or_w指定的棋子
    def recover(self, list_to_recover, b_or_w):
        if len(list_to_recover) > 0:
            for i in range(len(list_to_recover)):
                self.boardPosition[list_to_recover[i][1]][list_to_recover[i][0]] = b_or_w + 1
                self.image_added = self.canvas_bottom.create_image(
                    20 * self.size + (list_to_recover[i][0] - 1) * self.gridLen + 4 * self.boardProp,
                    20 * self.size + (list_to_recover[i][1] - 1) * self.gridLen - 5 * self.boardProp,
                    image=self.photoWhiteBlackDone_list[b_or_w])
                self.canvas_bottom.addtag_withtag('image', self.image_added)
                self.canvas_bottom.addtag_withtag('position' + str(list_to_recover[i][0]) + str(list_to_recover[i][1]),
                                                  self.image_added)

    # 杀死位置列表killList中的棋子，即删除图片，位置值置0
    def kill(self, killList):
        if len(killList) > 0:
            for i in range(len(killList)):
                self.boardPosition[killList[i][1]][killList[i][0]] = 0
                self.canvas_bottom.delete('position' + str(killList[i][0]) + str(killList[i][1]))


global mode_num, newApp
mode_num = 19
newApp = False
if __name__ == '__main__':
    while True:
        newApp = False
        app = Application(mode_num)
        app.title('围棋')
        app.mainloop()
        if newApp:
            app.destroy()
        else:
            break
