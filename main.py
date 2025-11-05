import calendar
import json
import os
import time
from tkinter import Event, filedialog, messagebox

import tkintertools

__version__ = '1.0'

config, theme, S = {}, {}, tkintertools.S


def configure(modify: bool = False, **kw):
    """ 配置设定 """
    global config, theme
    with open('config.json', 'r') as file:
        config = json.load(file)
    if modify:
        config.update(kw)
        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4)
    else:
        with open('theme.json', 'r') as file:
            theme = json.load(file)[config['theme']]
        if config['transparent']:
            for widget in ('Label', 'Button', 'Entry', 'Text'):
                theme['Canvas' + widget]['color_fill'] = tkintertools.COLOR_NONE


configure()


class MainWindow:
    """ 主界面 """

    root = tkintertools.Tk(geometry='300x500+300+100')
    root.overrideredirect(True)
    root.iconbitmap('task.ico')

    rootcanvas = tkintertools.Canvas(
        root, 298, 498, bg=theme['rootcanvas']['bg'])
    rootcanvas.configure(
        highlightthickness=1, highlightbackground=theme['rootcanvas']['highlightbackground'])
    canvas = tkintertools.Canvas(root, 298, 445, bg=theme['canvas']['bg'])
    rootcanvas.place(x=0, y=0)
    canvas.place(x=1, y=30)
    bg = canvas.create_image(150, 222.5)
    rootcanvas.bind('<B1-Motion>', lambda event: MainWindow.move(event))
    rootcanvas.bind('<Button-1>', lambda event: MainWindow.move(event))
    canvas.bind('<MouseWheel>', lambda event: TaskCard.scroll(event))

    widgets_tool: list[tkintertools._BaseWidget | int] = [
        tkintertools.CanvasButton(
        rootcanvas, 165, 5, 20, 20, 0, '⏰',
            font=('楷体', 12),
            color_fill=('', 'skyblue', theme['MainColor'][4]),
            color_text=theme['ToolButton']['color_text'],
            color_outline=tkintertools.COLOR_NONE,
            command=lambda: open_pomodoro()),
        tkintertools.CanvasButton(
            rootcanvas, 187, 5, 20, 20, 0, '+',
            font=('楷体', 18),
            color_fill=(
                '', 'green', theme['MainColor'][4], theme['MainColor'][1]),
            color_text=theme['ToolButton']['color_text']+['grey'],
            color_outline=tkintertools.COLOR_NONE,
            command=lambda: switchtonew()),
        tkintertools.CanvasButton(
            rootcanvas, 209, 5, 20, 20, 0, '📌',
            font=('楷体', 12),
            color_fill=('', 'orange', theme['MainColor'][4]),
            color_text=theme['ToolButton']['color_text'],
            color_outline=tkintertools.COLOR_NONE,
            command=lambda: MainWindow.topmost()),
        tkintertools.CanvasButton(
            rootcanvas, 231, 5, 20, 20, 0, '⚙',
            font=('楷体', 12),
            color_fill=('', 'purple', theme['MainColor'][4]),
            color_text=theme['ToolButton']['color_text'],
            color_outline=tkintertools.COLOR_NONE,
            command=lambda: openset()),
        tkintertools.CanvasButton(
            rootcanvas, 253, 5, 20, 20, 0, '-',
            font=('楷体', 15),
            color_fill=('', '#777', theme['MainColor'][4]),
            color_text=theme['ToolButton']['color_text'],
            color_outline=tkintertools.COLOR_NONE,
            command=lambda: windowswitch(True)),
        tkintertools.CanvasButton(
            rootcanvas, 275, 5, 20, 20, 0, '×',
            font=('楷体', 15),
            color_fill=('', 'red', theme['MainColor'][4]),
            color_text=theme['ToolButton']['color_text'],
            color_outline=tkintertools.COLOR_NONE,
            command=root.quit),

        rootcanvas.create_text(
            5, 14, text='📃', fill=theme['MainColor'][0], anchor='w', font=('楷体', 12)),
        rootcanvas.create_text(
            20, 15, text='学习工具箱', fill=theme['MainColor'][0], anchor='w', font=('楷体', 12)),
        rootcanvas.create_text(
            5, 487, text='任务个数:', anchor='w', fill=theme['MainColor'][0], font=('楷体', 12)),
        rootcanvas.create_text(80, 487, anchor='w', font=('楷体', 12)),
        rootcanvas.create_text(295, 487, anchor='e', font=('楷体', 12))]

    widgets_new: list[tkintertools._BaseWidget] = [
        canvas.create_text(
            -150, 20, text='新建任务', fill=theme['MainColor'][0], font=('楷体', 20)),
        canvas.create_line(-240, 40, -60, 40, fill=theme['MainColor'][0]),
        canvas.create_text(
            -275, 70, text='任务名称', fill=theme['MainColor'][0], anchor='w', font=('楷体', 12)),
        canvas.create_text(
            -275, 100, text='截止日期', fill=theme['MainColor'][0], anchor='w', font=('楷体', 12)),
        canvas.create_text(
            -275, 130, text='重要程度', fill=theme['MainColor'][0], anchor='w', font=('楷体', 12)),
        canvas.create_text(
            -150, 160, text='任务描述', fill=theme['MainColor'][0], font=('楷体', 12)),
        tkintertools.CanvasEntry(  # 6
            canvas, -205, 59, 180, 22, 0, '',
            limit=8, font=('楷体', 14),
            color_outline=theme['CanvasEntry']['color_outline'],
            color_fill=theme['CanvasEntry']['color_fill'],
            color_text=theme['CanvasEntry']['color_text']),
        tkintertools.CanvasButton(  # 7
            canvas, -47, 89, 22, 22, 0, '🕒',
            font=('楷体', 12),
            color_fill=theme['CanvasButton']['color_fill'],
            color_text=theme['CanvasButton']['color_text'],
            color_outline=theme['CanvasButton']['color_outline'],
            command=lambda: timechoose()),
        tkintertools.CanvasLabel(
            canvas, -205, 89, 155, 22,
            font=('楷体', 11),
            color_outline=theme['CanvasLabel']['color_outline'],
            color_fill=theme['CanvasLabel']['color_fill'],
            color_text=theme['CanvasLabel']['color_text']),
        tkintertools.CanvasButton(  # 8
            canvas, -205, 120, 20, 20,
            color_fill=theme['CanvasButton']['color_fill'],
            color_text=theme['CanvasButton']['color_text'],
            color_outline=theme['CanvasButton']['color_outline'],
            command=lambda: levelchoose(1)),
        tkintertools.CanvasButton(  # 9
            canvas, -180, 120, 20, 20,
            color_fill=theme['CanvasButton']['color_fill'],
            color_text=theme['CanvasButton']['color_text'],
            color_outline=theme['CanvasButton']['color_outline'],
            command=lambda: levelchoose(2)),
        tkintertools.CanvasButton(  # 10
            canvas, -155, 120, 20, 20,
            color_fill=theme['CanvasButton']['color_fill'],
            color_text=theme['CanvasButton']['color_text'],
            color_outline=theme['CanvasButton']['color_outline'],
            command=lambda: levelchoose(3)),
        tkintertools.CanvasButton(  # 11
            canvas, -130, 120, 20, 20,
            color_fill=theme['CanvasButton']['color_fill'],
            color_text=theme['CanvasButton']['color_text'],
            color_outline=theme['CanvasButton']['color_outline'],
            command=lambda: levelchoose(4)),
        tkintertools.CanvasButton(  # 12
            canvas, -105, 120, 20, 20,
            color_fill=theme['CanvasButton']['color_fill'],
            color_text=theme['CanvasButton']['color_text'],
            color_outline=theme['CanvasButton']['color_outline'],
            command=lambda: levelchoose(5)),
        tkintertools.CanvasButton(  # 13
            canvas, -80, 120, 20, 20,
            color_fill=theme['CanvasButton']['color_fill'],
            color_text=theme['CanvasButton']['color_text'],
            color_outline=theme['CanvasButton']['color_outline'],
            command=lambda: levelchoose(6)),
        tkintertools.CanvasButton(  # 14
            canvas, -55, 120, 20, 20,
            color_fill=theme['CanvasButton']['color_fill'],
            color_text=theme['CanvasButton']['color_text'],
            color_outline=theme['CanvasButton']['color_outline'],
            command=lambda: levelchoose(7)),
        tkintertools.CanvasText(  # 15
            canvas, -275, 180, 250, 210, 0,
            font=('楷体', 12),
            color_outline=theme['CanvasText']['color_outline'],
            color_fill=theme['CanvasText']['color_fill'],
            color_text=theme['CanvasText']['color_text']),
        tkintertools.CanvasButton(  # 16
            canvas, -275, 400, 100, 25, 0, '创建',
            font=('楷体', 12),
            color_fill=theme['CanvasButton']['color_fill'],
            color_text=theme['CanvasButton']['color_text'],
            color_outline=theme['CanvasButton']['color_outline'],
            command=lambda: createtask()),
        tkintertools.CanvasButton(  # 17
            canvas, -125, 400, 100, 25, 0, '取消',
            font=('楷体', 12),
            color_fill=theme['CanvasButton']['color_fill'],
            color_text=theme['CanvasButton']['color_text'],
            color_outline=theme['CanvasButton']['color_outline'],
            command=lambda: switchtonew())]

    @classmethod
    def move(cls, event: Event, coords: list = [0, 0]):
        """ 拖动窗口 """
        if 0 <= event.x/S <= 160 and 0 <= event.y/S <= 30:
            if event.type.__str__() == '4':
                coords[0], coords[1] = event.x, event.y
            else:
                x, y = event.x - coords[0], event.y - coords[1]
                lx, ly = map(int, cls.root.geometry().split('+')[-2:])
                cls.root.geometry('300x500+%d+%d' % (lx+x, ly+y))

    @classmethod
    def topmost(cls, switch: list = [True]):
        """ 窗口置顶 """
        cls.root.attributes('-topmost', switch[0])
        switch[0] = not switch[0]
        if switch[0]:
            cls.widgets_tool[2].configure(
                color_text=('grey', 'white', 'white'))
        else:
            cls.widgets_tool[2].configure(
                color_text=('springgreen', 'springgreen', 'springgreen'))


class MiniWindow:
    """ 迷你小窗 """

    toplevel = tkintertools.Toplevel(
        MainWindow.root, geometry='30x30+1000+100')
    toplevel.attributes('-transparentcolor', 'white')
    toplevel.attributes('-topmost', True)
    toplevel.overrideredirect(True)
    toplevel.withdraw()
    toplevel.bind('<Double-Button-1>', lambda _: windowswitch(False))
    toplevel.bind('<Button-1>', lambda event: MiniWindow.move(event))
    toplevel.bind('<B1-Motion>', lambda event: MiniWindow.move(event))

    canvas = tkintertools.Canvas(toplevel, 30, 30, bg='white')
    canvas.create_text(15, 15, text='👀', font=('楷体', 20))
    canvas.place(x=0, y=0)

    @classmethod
    def move(cls, event: Event, coords: list = [0, 0]):
        """ 拖动小窗 """
        if event.type.__str__() == '4':
            coords[0], coords[1] = event.x/S, event.y/S
        else:
            x, y = event.x/S - coords[0], event.y/S - coords[1]
            lx, ly = map(int, cls.toplevel.geometry().split('+')[-2:])
            cls.toplevel.geometry('30x30+%d+%d' % (lx+x, ly+y))


class ReadWindow:
    """ 任务详情 """

    def __init__(self, data: dict):
        geometry = tuple(int(i)
                         for i in MainWindow.root.geometry().split('+')[-2:])
        self.toplevel = tkintertools.Toplevel(
            MainWindow.root, geometry='300x400+%d+%d' % (geometry[0]+300*S, geometry[1]))
        self.toplevel.overrideredirect(True)
        self.toplevel.bind('<B1-Motion>', self.move)
        self.toplevel.bind('<Button-1>', self.move)
        self.canvas = tkintertools.Canvas(
            self.toplevel, 298, 398,
            bg=theme['ReadWindow']['bg'], highlightbackground=theme['ReadWindow']['highlightbackground'])
        self.canvas.configure(highlightthickness=1)
        self.canvas.place(x=0, y=0)
        self.image = self.canvas.create_image(150, 200)
        self.canvas.create_text(
            150, 25, text='—— 任务详情 ——', font=('楷体', 15), fill=theme['MainColor'][3])
        tkintertools.CanvasLabel(
            self.canvas, 10, 50, 280, 40, 5, '任务名称:%s' % data['name'],
            justify='left', font=('楷体', 13),
            color_outline=theme['CanvasLabel']['color_outline'],
            color_fill=theme['CanvasLabel']['color_fill'],
            color_text=theme['CanvasLabel']['color_text'])
        tkintertools.CanvasLabel(
            self.canvas, 10, 100, 280, 40, 5, '截止时间:%s' % data['date'],
            justify='left', font=('楷体', 13),
            color_outline=theme['CanvasLabel']['color_outline'],
            color_fill=theme['CanvasLabel']['color_fill'],
            color_text=theme['CanvasLabel']['color_text'])
        tkintertools.CanvasLabel(
            self.canvas, 10, 150, 280, 40, 5, '创建时间:%s' % data['create'],
            justify='left', font=('楷体', 13),
            color_outline=theme['CanvasLabel']['color_outline'],
            color_fill=theme['CanvasLabel']['color_fill'],
            color_text=theme['CanvasLabel']['color_text'])
        tkintertools.CanvasLabel(
            self.canvas, 10, 200, 280, 40, 5, '重要程度:%s' % (
                int(data['level'])*'★'),
            justify='left', font=('楷体', 13),
            color_outline=theme['CanvasLabel']['color_outline'],
            color_fill=theme['CanvasLabel']['color_fill'],
            color_text=theme['CanvasLabel']['color_text'])
        tkintertools.CanvasLabel(
            self.canvas, 10, 250, 280, 100, 5, '%s' % data['description'],
            font=('楷体', 12),
            color_outline=theme['CanvasLabel']['color_outline'],
            color_fill=theme['CanvasLabel']['color_fill'],
            color_text=theme['CanvasLabel']['color_text'])
        tkintertools.CanvasButton(
            self.canvas, 100, 360, 100, 30, 5, '确定',
            color_fill=theme['CanvasButton']['color_fill'],
            color_text=theme['CanvasButton']['color_text'],
            color_outline=theme['CanvasButton']['color_outline'],
            command=self.toplevel.destroy)
        self.button = tkintertools.CanvasButton(
            self.canvas, 270, 10, 20, 20, 0, '📌',
            font=('楷体', 12),
            color_fill=('', theme['MainColor'][4], theme['MainColor'][3]),
            color_text=theme['ToolButton']['color_text'],
            color_outline=tkintertools.COLOR_NONE,
            command=self.topmost)
        self.setbg()

    def move(self, event: Event, coords: list = [0, 0]):
        """ 窗口拖动 """
        if event.y <= 350:
            if event.type.__str__() == '4':
                coords[0], coords[1] = event.x, event.y
            else:
                x, y = event.x - coords[0], event.y - coords[1]
                lx, ly = map(int, self.toplevel.geometry().split('+')[-2:])
                self.toplevel.geometry('300x400+%d+%d' % (lx+x, ly+y))

    def topmost(self, switch: list = [True]):
        """ 窗口置顶 """
        self.toplevel.attributes('-topmost', switch[0])
        switch[0] = not switch[0]
        if switch[0]:
            self.button.configure(color_text=theme['ToolButton']['color_text'])
        else:
            self.button.configure(color_text=('springgreen',)*3)

    def setbg(self):
        """ 设置背景 """
        if SetWindow.image and SetWindow.image.file[-3:] == 'gif':
            SetWindow.image.play(self.canvas, self.image, config['interval'])
        elif SetWindow.image:
            self.bg = tkintertools.PhotoImage(config['bgpath'])
            self.canvas.itemconfigure(self.image, image=self.bg)


class SetWindow:
    """ 设置界面 """

    image = None
    toplevel = tkintertools.Toplevel(MainWindow.root, geometry='300x500')
    toplevel.overrideredirect(True)
    toplevel.withdraw()
    toplevel.bind('<Button-1>', lambda event: SetWindow.move(event))
    toplevel.bind('<B1-Motion>', lambda event: SetWindow.move(event))
    canvas = tkintertools.Canvas(
        toplevel, 298, 498, bg=theme['SetWindow']['bg'])
    canvas.configure(highlightthickness=1,
                     highlightbackground=theme['SetWindow']['highlightbackground'])
    canvas.place(x=0, y=0)
    bg = canvas.create_image(150, 250)
    canvas.create_rectangle(0, 0, 300, 30, fill=theme['MainColor'][1], width=0)
    canvas.create_text(
        5, 15, text='⚙设置', anchor='w', font=('楷体', 12), fill=theme['MainColor'][0])
    canvas.create_text(
        150, 470, fill=theme['MainColor'][0], justify='center', font=('楷体', 10),
        text='本工具由Group7\n—— 基于@Xiaokang2022 thinkertools工具 ——\n使用Python的tkinter模块打造(版本号:%s)' % __version__)
    
    # 添加主题切换按钮
    theme_button = tkintertools.CanvasButton(
        canvas, 100, 150, 100, 30, 5, '深色主题' if config['theme'] == 'light' else '浅色主题',
        font=('楷体', 12),
        color_fill=theme['CanvasButton']['color_fill'],
        color_text=theme['CanvasButton']['color_text'],
        color_outline=theme['CanvasButton']['color_outline'],
        command=lambda: SetWindow.toggle_theme())
    
    # 添加跳转链接按钮
    tkintertools.CanvasButton(
        canvas, 100, 200, 100, 30, 5, '访问Github',
        font=('楷体', 12),
        color_fill=theme['CanvasButton']['color_fill'],
        color_text=theme['CanvasButton']['color_text'],
        color_outline=theme['CanvasButton']['color_outline'],
        command=lambda: os.system('start https://github.com/tsuimin888/learningbox'))
    
    # 保留关闭按钮
    tkintertools.CanvasButton(
        canvas, 275, 5, 20, 20, 0, '×',
        font=('楷体', 15),
        color_fill=('', 'red', theme['MainColor'][4]),
        color_text=theme['ToolButton']['color_text'],
        color_outline=tkintertools.COLOR_NONE,
        command=lambda: openset())

    @classmethod
    def move(cls, event: Event, coords: list = [0, 0]):
        """ 拖动窗口 """
        if 0 <= event.x/S <= 260 and 0 <= event.y/S <= 30:
            if event.type.__str__() == '4':
                coords[0], coords[1] = event.x, event.y
            else:
                x, y = event.x - coords[0], event.y - coords[1]
                lx, ly = map(int, cls.toplevel.geometry().split('+')[-2:])
                cls.toplevel.geometry('300x500+%d+%d' % (lx+x, ly+y))

    @classmethod
    def loadbg(cls):
        """ 加载并显示背景 """
        try:
            cls.image = tkintertools.PhotoImage(
                config['bgpath']) if config['bgpath'] else ''
            if cls.image and cls.image.file[-3:] == 'gif':
                [None for _ in cls.image.parse()]
                cls.image.play(MainWindow.canvas, MainWindow.bg,
                               config['interval'])
                cls.image.play(SetWindow.canvas, SetWindow.bg,
                               config['interval'])
            else:
                MainWindow.canvas.itemconfigure(MainWindow.bg, image=cls.image)
                SetWindow.canvas.itemconfigure(SetWindow.bg, image=cls.image)
        except:
            messagebox.showerror('图片错误', '所选背景图片无法显示！')
    
    @classmethod
    def toggle_theme(cls):
        """ 切换主题 """
        # 更新配置文件
        if config['theme'] == 'light':
            configure(True, theme='dark')
            cls.theme_button.configure(text='浅色主题')
        else:
            configure(True, theme='light')
            cls.theme_button.configure(text='深色主题')
        
        # 显示提示信息
        messagebox.showinfo("主题切换", "主题已切换，重启应用以完全生效")

    @classmethod
    def update_theme_button(cls):
        """ 更新主题按钮文本 """
        if config['theme'] == 'light':
            cls.theme_button.configure(text='深色主题')
        else:
            cls.theme_button.configure(text='浅色主题')

class TaskCard:
    """ 任务卡片 """

    taskspool = []
    key = 0
    flag = True
    bar = MainWindow.canvas.create_line(
        295, 5, 295, 5, fill=theme['MainColor'][0])

    def __init__(self, canvas: tkintertools.Canvas, data: dict):
        self.taskspool.append(self)
        self.color = ['grey', 'yellow', 'green',
                      'skyblue', 'purple', 'orange', 'red']
        self.canvas = canvas
        self.data = data
        self.interface()
        self.setflag(True)

    def interface(self):
        """ 图形接口 """
        self.y = (len(self.taskspool) + self.key)*55 - 50
        self.widgets: list[tkintertools._BaseWidget] = [
            tkintertools.CanvasLabel(
                self.canvas, 10, self.y, 280, 50,
                color_outline=theme['CanvasLabel']['color_outline'],
                color_fill=theme['CanvasLabel']['color_fill'],
                color_text=theme['CanvasLabel']['color_text']),
            tkintertools.CanvasButton(
                self.canvas, 265, self.y+5, 20, 20, 0, '…',
                font=('楷体', 12),
                color_fill=theme['CanvasButton']['color_fill'],
                color_text=theme['CanvasButton']['color_text'],
                color_outline=theme['CanvasButton']['color_outline'],
                command=lambda: ReadWindow(self.data)),
            tkintertools.CanvasButton(
                self.canvas, 240, self.y+5, 20, 20, 0, '✔',
                font=('楷体', 12),
                color_fill=theme['CanvasButton']['color_fill'],
                color_text=theme['CanvasButton']['color_text'],
                color_outline=theme['CanvasButton']['color_outline'],
                command=self.destroy),
            tkintertools.CanvasButton(
                self.canvas, 215, self.y+5, 20, 20, 0, '✏️',
                font=('楷体', 12),
                color_fill=theme['CanvasButton']['color_fill'],
                color_text=theme['CanvasButton']['color_text'],
                color_outline=theme['CanvasButton']['color_outline'],
                command=lambda: switchtoedit(self))]
        self.items = [
            self.canvas.create_text(
                15, self.y+17, text=self.data['name'], font=('楷体', 15), anchor='w', fill=theme['MainColor'][0]),
            self.canvas.create_text(
                15, self.y+38, text=self.data['date'], font=('楷体', 12), anchor='w', fill=theme['MainColor'][0]),
            self.canvas.create_text(287, self.y+38, text=int(self.data['level'])*'★', font=('楷体', 12),
                                    anchor='e', fill=self.color[int(self.data['level'])-1])]

    def destroy(self, switch: bool = False):
        """ 删除任务 """
        if not switch and not messagebox.askyesno('完成确认', '是否完成任务：%s？' % self.data['name']):
            return
        tkintertools.move(MainWindow.canvas, self, 300, 0, 300, 'smooth')
        if switch:
            self.sort(self.taskspool.index(self)+1)
            for widget in self.widgets:
                widget.destroy()
            for item in self.items:
                self.canvas.delete(item)
            self.taskspool.remove(self)
            deletetask(self.data['create'])
            updatestate()
            self.setflag(True)
        else:
            MainWindow.root.after(500, self.destroy, True)

    def update(self):
        """ 更新信息 """
        MainWindow.canvas.itemconfigure(self.items[0], text=self.data['name'])
        MainWindow.canvas.itemconfigure(self.items[1], text=self.data['date'])
        MainWindow.canvas.itemconfigure(self.items[2], text=int(
            self.data['level'])*'★', fill=self.color[int(self.data['level'])-1])

    def move(self, x: int, y: int):
        """ 移动任务卡片 """
        self.y += y
        for widget in self.widgets:
            widget.move(x, y)
        for item in self.items:
            self.canvas.move(item, x, y)

    @classmethod
    def sort(cls, key: int = None, flag: bool = False):
        """ 排序 """
        if key != None:
            if len(cls.taskspool) > 8:
                if cls.key == 8-len(cls.taskspool):
                    flag = True
            if flag:
                cls.key += 1
            for ind, task in enumerate(cls.taskspool):
                if ind >= key and not flag:
                    tkintertools.move(MainWindow.canvas, task,
                                      0, -55, 300, 'smooth')
                elif ind < key and flag:
                    tkintertools.move(MainWindow.canvas, task,
                                      0, 55, 300, 'smooth')
        else:
            for ind, task in enumerate(cls.taskspool):
                dy = 5 + (ind + cls.key) * 55 - task.y
                tkintertools.move(MainWindow.canvas, task,
                                  0, dy, 300, 'smooth')

    @classmethod
    def scroll(cls, event: Event):
        """ 滚动 """
        key, length = (1 if event.delta > 0 else -1), len(cls.taskspool)
        if length < 9 or not 0 >= cls.key+key >= 8-length or not cls.flag:
            return
        cls.key += key
        tkintertools.move(MainWindow.canvas, cls.bar, 0, -
                          55*key*8/length, 300, 'smooth')
        for task in cls.taskspool:
            tkintertools.move(MainWindow.canvas, task,
                              0, 55*key, 300, 'smooth')

    @classmethod
    def setflag(cls, boolean: bool):
        """ 设置标志 """
        cls.flag = boolean
        coords = MainWindow.canvas.coords(TaskCard.bar)
        if cls.flag and (key := len(TaskCard.taskspool)) > 8:
            length = 435*8/key
            coords[1] = 5 + (435-length)*cls.key/(8-key)
            coords[3] = coords[1] + length
        else:
            coords[3] = coords[1]
        MainWindow.canvas.coords(TaskCard.bar, *coords)


class TimeChooser:
    """ 日期时间选择界面 """

    canvas = tkintertools.Canvas(
        MainWindow.root, 250, 160, bg=theme['TimeChooser']['bg'],
        highlightbackground=theme['TimeChooser']['highlightbackground'])
    canvas.configure(highlightthickness=1)
    canvas.bind('<MouseWheel>', lambda event: TimeChooser.move(event))
    canvas.create_rectangle(
        160, 60, 250, 75, fill=theme['MainColor'][4], width=0)
    canvas.create_line(160, 5, 160, 155, fill=theme['MainColor'][0])
    canvas.create_text(205, 65, text=':   :', font=(
        '楷体', 12), fill=theme['MainColor'][0])
    date = canvas.create_text(
        80, 15, fill=theme['MainColor'][0], font=('楷体', 12),
        text=time.strftime('%Y-%m', time.localtime()))
    hour = canvas.create_text(
        175, 60, fill=theme['MainColor'][0], font=('楷体', 11), anchor='n',
        text='\n'.join('%02d' % i for i in range(24)))
    minute = canvas.create_text(
        205, 60, fill=theme['MainColor'][0], font=('楷体', 11), anchor='n',
        text='\n'.join('%02d' % i for i in range(60)))
    second = canvas.create_text(
        235, 60, fill=theme['MainColor'][0], font=('楷体', 11), anchor='n',
        text='\n'.join('%02d' % i for i in range(60)))
    timelist = [0, 0, 0]
    canvas.create_rectangle(
        162, 130, 248, 165, fill=theme['TimeChooser']['bg'], width=0)
    canvas.create_rectangle(
        162, -5, 248, 6, fill=theme['TimeChooser']['bg'], width=0)
    tkintertools.CanvasButton(
        canvas, 27, 5, 20, 20, 0, '‹',
        font=('楷体', 20),
        color_fill=('', theme['MainColor'][4], theme['MainColor'][3]),
        color_outline=tkintertools.COLOR_NONE,
        color_text=theme['ToolButton']['color_text'],
        command=lambda: TimeChooser.modify(0, -1))
    tkintertools.CanvasButton(
        canvas, 113, 5, 20, 20, 0, '›',
        font=('楷体', 20),
        color_fill=('', theme['MainColor'][4], theme['MainColor'][3]),
        color_outline=tkintertools.COLOR_NONE,
        color_text=theme['ToolButton']['color_text'],
        command=lambda: TimeChooser.modify(0, 1))
    tkintertools.CanvasButton(
        canvas, 5, 5, 20, 20, 0, '«',
        font=('楷体', 20),
        color_fill=('', theme['MainColor'][4], theme['MainColor'][3]),
        color_outline=tkintertools.COLOR_NONE,
        color_text=theme['ToolButton']['color_text'],
        command=lambda: TimeChooser.modify(-1, 0))
    tkintertools.CanvasButton(
        canvas, 135, 5, 20, 20, 0, '»',
        font=('楷体', 20),
        color_fill=('', theme['MainColor'][4], theme['MainColor'][3]),
        color_outline=tkintertools.COLOR_NONE,
        color_text=theme['ToolButton']['color_text'],
        command=lambda: TimeChooser.modify(1, 0))
    tkintertools.CanvasButton(
        canvas, 165, 135, 80, 20, 0, '确定',
        font=('楷体', 12),
        color_fill=theme['CanvasButton']['color_fill'],
        color_text=theme['CanvasButton']['color_text'],
        color_outline=theme['CanvasButton']['color_outline'],
        command=lambda: TimeChooser.settime())
    datelist = []

    @classmethod
    def updatedate(cls):
        """ 加载日期 """
        for button in cls.datelist:
            button.destroy()
        cls.datelist.clear()
        year, month = map(int, cls.canvas.itemcget(
            cls.date, 'text').split('-'))
        monthdata = calendar.monthcalendar(year, month)
        for x, line in enumerate(monthdata):
            for y, value in enumerate(line):
                if value:
                    cls.datelist.append(
                        tkintertools.CanvasButton(
                            cls.canvas, 5+y*22, 27+x*22, 20, 20, 0, str(value),
                            font=('楷体', 10),
                            color_outline=tkintertools.COLOR_NONE,
                            color_text=(theme['MainColor'][0],)*3,
                            color_fill=(
                                '', theme['MainColor'][4], theme['MainColor'][3]),
                            command=lambda value=value: cls.setdate(value)))

    @classmethod
    def modify(cls, y: int = 0, m: int = 0):
        """ 修改年月 """
        year, month = map(int, cls.canvas.itemcget(
            cls.date, 'text').split('-'))
        if month+m == 0:
            year -= 1
            month = 13
        if month+m == 13:
            year += 1
            month = 0
        cls.canvas.itemconfigure(cls.date, text='%d-%02d' % (year+y, month+m))
        cls.updatedate()

    @classmethod
    def move(cls, event: Event):
        """ 移动时间柱 """
        if event.y/S >= 130 or event.y/S <= 5:
            return
        key = 1 if event.delta > 0 else -1
        if 160 < event.x/S < 190:
            if cls.timelist[0] >= 0 and key == 1:
                return
            if cls.timelist[0] <= -23 and key == -1:
                return
            tkintertools.move(
                cls.canvas, cls.hour, 0, 15*key, 200, 'smooth', 10)
            cls.timelist[0] += key
        elif 190 < event.x/S < 220:
            if cls.timelist[1] >= 0 and key == 1:
                return
            if cls.timelist[1] <= -59 and key == -1:
                return
            tkintertools.move(
                cls.canvas, cls.minute, 0, 15*key, 200, 'smooth', 10)
            cls.timelist[1] += key
        elif 220 < event.x/S < 250:
            if cls.timelist[2] >= 0 and key == 1:
                return
            if cls.timelist[2] <= -59 and key == -1:
                return
            tkintertools.move(
                cls.canvas, cls.second, 0, 15*key, 200, 'smooth', 10)
            cls.timelist[2] += key

    @classmethod
    def setdate(cls, day: int):
        """ 确定日期 """
        year, month = map(int, cls.canvas.itemcget(
            cls.date, 'text').split('-'))
        date = MainWindow.widgets_new[8].configure('text')
        date = '%d/%02d/%02d' % (year, month, day) + date[10:]
        MainWindow.widgets_new[8].configure(text=date)

    @classmethod
    def settime(cls):
        """ 确定时间 """
        date = MainWindow.widgets_new[8].configure('text')
        date = date[:11] + ':'.join('%02d' % -i for i in cls.timelist)
        MainWindow.widgets_new[8].configure(text=date)
        timechoose()


def windowswitch(mini: bool):
    """ 窗口切换 """
    if mini:
        MainWindow.root.withdraw()
        MiniWindow.toplevel.deiconify()
    else:
        MainWindow.root.deiconify()
        MiniWindow.toplevel.withdraw()


def redmask(widget: tkintertools._BaseWidget, ind=0):
    """ 红色标记 """
    if ind & 1:
        widget.configure(color_outline=theme['CanvasEntry']['color_outline'])
    else:
        widget.configure(color_outline=('red',)*3)
    widget.state()
    if ind < 5:
        MainWindow.root.after(100, redmask, widget, ind+1)


def checkargument():
    """ 参数检查 """
    if not (name := MainWindow.widgets_new[6].get()):
        redmask(MainWindow.widgets_new[6])
        return
    if not (level := levelchoose()):
        for i in range(7):
            redmask(MainWindow.widgets_new[9+i])
        return
    return name, MainWindow.widgets_new[8].configure('text'), level


def createtask():
    """ 创建任务 """
    if args := checkargument():
        name, time_, level = args
    else:
        return

    create = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
    data = {
        'name': name,
        'date': time_,
        'level': level,
        'create': create,
        'description': MainWindow.widgets_new[-3].get(),
        'time': time.mktime(time.strptime(time_, '%Y/%m/%d %H:%M:%S'))
    }
    with open('tasks.json', 'r', encoding='utf-8') as file:
        dic: dict = json.load(file)
    dic[create] = data
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(dic, file, indent=4)

    TaskCard(MainWindow.canvas, data).move(300, 0)
    TaskCard.taskspool.sort(
        key=lambda task: task.data[config['sort']], reverse=config['reverse'])
    TaskCard.sort()
    switchtonew()


def deletetask(create: str):
    """ 删除任务 """
    with open('tasks.json', 'r', encoding='utf-8') as file:
        dic: dict = json.load(file)
    del dic[create]
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(dic, file, indent=4)


def edittask(task: TaskCard):
    """ 编辑任务 """
    if args := checkargument():
        name, time_, level = args
    else:
        return

    data = {
        'name': name,
        'date': time_,
        'level': level,
        'description': MainWindow.widgets_new[-3].get(),
        'time': time.mktime(time.strptime(time_, '%Y/%m/%d %H:%M:%S'))
    }
    with open('tasks.json', 'r', encoding='utf-8') as file:
        dic: dict[str, dict] = json.load(file)
    task.data.update(data)
    task.update()
    dic[task.data['create']].update(data)
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(dic, file, indent=4)

    TaskCard.taskspool.sort(
        key=lambda task: task.data[config['sort']], reverse=config['reverse'])
    TaskCard.sort()
    switchtoedit(None)


def loadtask():
    """ 加载任务 """
    with open('tasks.json', 'r+', encoding='utf-8') as file:
        data = file.read()
    if data:
        tasks = json.loads(data)
        for task in tasks:
            TaskCard(MainWindow.canvas, tasks[task])
    TaskCard.taskspool.sort(
        key=lambda task: task.data[config['sort']], reverse=config['reverse'])
    TaskCard.sort()


def timechoose(switch: list = [True]):
    """ 时间选择 """
    if switch[0]:
        TimeChooser.canvas.place(x=25, y=150)
    else:
        TimeChooser.canvas.place_forget()
    switch[0] = not switch[0]


def levelchoose(key: int = 0, cache: list = [0]):
    """ 等级选择 """
    color = ['grey', 'yellow', 'green', 'skyblue', 'purple', 'orange', 'red']
    for ind, button in enumerate(MainWindow.widgets_new[9:16]):
        if ind < key:
            button.configure(color_fill=(color[key-1],)*3)
        else:
            button.configure(color_fill=theme['CanvasButton']['color_fill'])
        button.state()
    cache[0], temp = key, cache[0]
    if not key:
        return temp


def updatestate():
    """ 更新状态栏 """
    num = len(TaskCard.taskspool)
    color = 'springgreen' if not num else 'orange' if num <= config['taskcolor'] else 'red'
    MainWindow.rootcanvas.itemconfigure(
        MainWindow.widgets_tool[-2], text=num, fill=color)
    today = (int(time.time()/86400)+1)*86400
    taskleave = 0
    for task in TaskCard.taskspool:
        if task.data['time'] <= today:
            taskleave += 1
    if taskleave:
        color = 'orange' if taskleave <= config['donecolor'] else 'red'
        MainWindow.rootcanvas.itemconfigure(
            MainWindow.widgets_tool[-1], text='剩余%d个' % taskleave, fill=color)
    else:
        MainWindow.rootcanvas.itemconfigure(
            MainWindow.widgets_tool[-1], text='已完成', fill='springgreen')
    MainWindow.widgets_new[6].set('')
    MainWindow.widgets_new[8].configure(
        text=time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))
    MainWindow.widgets_new[-3].set('')
    levelchoose()


def openset(switch: list = [True]):
    """ 打开设置界面 """
    if switch[0]:
        SetWindow.toplevel.deiconify()
        SetWindow.update_theme_button()  # 更新主题按钮文本
        geo = [int(i) for i in MainWindow.root.geometry().split('+')[-2:]]
        SetWindow.toplevel.geometry('300x500+%d+%d' % (geo[0]+300*S, geo[1]))
    else:
        SetWindow.toplevel.withdraw()
    switch[0] = not switch[0]
    
def open_pomodoro():
    """ 打开番茄时钟 """
    PomodoroWindow.open()


def switchtoedit(task: TaskCard, ind=0, switch: list = [1]):
    """ 切换编辑界面 """
    widget = TaskCard.taskspool + MainWindow.widgets_new
    if ind == len(widget):
        switch[0] = -switch[0]
        if switch[0] == 1:
            TaskCard.setflag(True)
            MainWindow.widgets_tool[1].set_live(True)
            MainWindow.canvas.itemconfigure(
                MainWindow.widgets_new[0], text='新建任务')
            MainWindow.widgets_new[-2].configure(text='创建')
            MainWindow.widgets_new[-1].command = lambda: switchtonew()
            MainWindow.widgets_new[-2].command = lambda: createtask()
            updatestate()
        return
    elif not ind:
        if switch[0] == 1:
            TaskCard.setflag(False)
            MainWindow.widgets_tool[1].set_live(False)
            MainWindow.canvas.itemconfigure(
                MainWindow.widgets_new[0], text='编辑任务')
            MainWindow.widgets_new[-2].configure(text='完成')
            MainWindow.widgets_new[-1].command = lambda: switchtoedit(None)
            MainWindow.widgets_new[-2].command = lambda: edittask(task)
            MainWindow.widgets_new[6].set(task.data['name'])
            MainWindow.widgets_new[8].configure(text=task.data['date'])
            MainWindow.widgets_new[-3].set(task.data['description'])
            MainWindow.widgets_new[task.data['level']+8].command()
    key = ind if switch[0] == 1 else -ind-1
    tkintertools.move(
        MainWindow.canvas, widget[key], 300*switch[0], 0, 200, 'rebound')
    MainWindow.root.after(30, switchtoedit, task, ind+1)


def switchtonew(ind=0, switch: list = [1]):
    """ 切换新建界面 """
    widget = TaskCard.taskspool + MainWindow.widgets_new
    if ind == len(widget):
        switch[0] = -switch[0]
        if switch[0] == 1:
            TaskCard.setflag(True)
            updatestate()
        MainWindow.widgets_tool[1].set_live(True)
        return
    elif not ind:
        if switch[0] == 1:
            TaskCard.setflag(False)
        MainWindow.widgets_tool[1].set_live(False)
    key = ind if switch[0] == 1 else -ind-1
    tkintertools.move(
        MainWindow.canvas, widget[key], 300*switch[0], 0, 200, 'rebound')
    MainWindow.root.after(30, switchtonew, ind+1)

class PomodoroWindow:
    """ 番茄时钟界面 """
    
    toplevel = None
    canvas = None
    timer_text = None
    status_text = None
    start_button = None
    reset_button = None
    
    # 番茄时钟状态
    is_running = False
    is_break = False
    time_left = 25 * 60  # 25分钟工作时间
    timer_id = None
    
    @classmethod
    def init_window(cls):
        """ 初始化窗口 """
        if cls.toplevel is None:
            cls.toplevel = tkintertools.Toplevel(
                MainWindow.root, geometry='300x400')
            cls.toplevel.overrideredirect(True)
            cls.toplevel.bind('<B1-Motion>', cls.move)
            cls.toplevel.bind('<Button-1>', cls.move)
            
            cls.canvas = tkintertools.Canvas(
                cls.toplevel, 298, 398,
                bg=theme['ReadWindow']['bg'], highlightbackground=theme['ReadWindow']['highlightbackground'])
            cls.canvas.configure(highlightthickness=1)
            cls.canvas.place(x=0, y=0)
            
            # 标题
            cls.canvas.create_text(
                150, 25, text='—— 番茄时钟 ——', font=('楷体', 15), fill=theme['MainColor'][3])
            
            # 时间显示
            cls.timer_text = cls.canvas.create_text(
                150, 120, text='25:00', font=('楷体', 30), fill=theme['MainColor'][0])
            
            # 状态显示
            cls.status_text = cls.canvas.create_text(
                150, 170, text='专注时间', font=('楷体', 15), fill=theme['MainColor'][0])
            
            # 控制按钮
            cls.start_button = tkintertools.CanvasButton(
                cls.canvas, 75, 220, 60, 30, 5, '开始',
                font=('楷体', 12),
                color_fill=theme['CanvasButton']['color_fill'],
                color_text=theme['CanvasButton']['color_text'],
                color_outline=theme['CanvasButton']['color_outline'],
                command=cls.toggle_timer)
            
            cls.reset_button = tkintertools.CanvasButton(
                cls.canvas, 165, 220, 60, 30, 5, '重置',
                font=('楷体', 12),
                color_fill=theme['CanvasButton']['color_fill'],
                color_text=theme['CanvasButton']['color_text'],
                color_outline=theme['CanvasButton']['color_outline'],
                command=cls.reset_timer)
            
            # 关闭按钮
            tkintertools.CanvasButton(
                cls.canvas, 270, 10, 20, 20, 0, '×',
                font=('楷体', 15),
                color_fill=('', 'red', theme['MainColor'][4]),
                color_text=theme['ToolButton']['color_text'],
                color_outline=tkintertools.COLOR_NONE,
                command=cls.close)
            
            # 说明文字
            cls.canvas.create_text(
                150, 300, text='专注时间: 25分钟\n休息时间: 5分钟', 
                font=('楷体', 12), fill=theme['MainColor'][0], justify='center')
    
    @classmethod
    def open(cls):
        """ 打开番茄时钟 """
        cls.init_window()
        geometry = tuple(int(i)
                         for i in MainWindow.root.geometry().split('+')[-2:])
        cls.toplevel.geometry('300x400+%d+%d' % (geometry[0]+300*S, geometry[1]))
        cls.toplevel.deiconify()
        cls.toplevel.lift()
        cls.update_display()
    
    @classmethod
    def close(cls):
        """ 关闭番茄时钟 """
        if cls.timer_id:
            MainWindow.root.after_cancel(cls.timer_id)
            cls.timer_id = None
        cls.toplevel.withdraw()
    
    @classmethod
    def toggle_timer(cls):
        """ 开始/暂停计时器 """
        cls.is_running = not cls.is_running
        cls.start_button.configure(text='暂停' if cls.is_running else '继续')
        
        if cls.is_running:
            cls.countdown()
    
    @classmethod
    def reset_timer(cls):
        """ 重置计时器 """
        if cls.timer_id:
            MainWindow.root.after_cancel(cls.timer_id)
            cls.timer_id = None
        
        cls.is_running = False
        cls.is_break = False
        cls.time_left = 25 * 60
        cls.start_button.configure(text='开始')
        cls.update_display()
    
    @classmethod
    def countdown(cls):
        """ 倒计时 """
        if not cls.is_running:
            return
        
        if cls.time_left > 0:
            cls.time_left -= 1
            cls.update_display()
            cls.timer_id = MainWindow.root.after(1000, cls.countdown)
        else:
            # 时间到，切换状态
            cls.is_break = not cls.is_break
            cls.time_left = 5 * 60 if cls.is_break else 25 * 60  # 休息5分钟或工作25分钟
            
            # 显示提示信息
            message = "休息时间到了！" if cls.is_break else "专注时间到了！"
            messagebox.showinfo("番茄时钟", message)
            
            # 更新状态显示
            cls.canvas.itemconfigure(cls.status_text, 
                                   text='休息时间' if cls.is_break else '专注时间')
            
            # 继续倒计时
            cls.update_display()
            cls.timer_id = MainWindow.root.after(1000, cls.countdown)
    
    @classmethod
    def update_display(cls):
        """ 更新显示 """
        minutes = cls.time_left // 60
        seconds = cls.time_left % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        cls.canvas.itemconfigure(cls.timer_text, text=time_str)
    
    @classmethod
    def move(cls, event: Event, coords: list = [0, 0]):
        """ 窗口拖动 """
        if event.y <= 350:
            if event.type.__str__() == '4':
                coords[0], coords[1] = event.x, event.y
            else:
                x, y = event.x - coords[0], event.y - coords[1]
                lx, ly = map(int, cls.toplevel.geometry().split('+')[-2:])
                cls.toplevel.geometry('300x400+%d+%d' % (lx+x, ly+y))

if __name__ == '__main__':
    """ 初始加载 """
    loadtask()
    updatestate()
    SetWindow.loadbg()
    TimeChooser.updatedate()
    MainWindow.root.mainloop()
