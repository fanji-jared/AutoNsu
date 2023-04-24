from shelve import Shelf
import threading
import win32gui
import win32con
import time
# 弹窗类


class TestTaskbarIcon:
    def __init__(self):
        # 注册一个窗口类
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = "Test"
        wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy, }
        classAtom = win32gui.RegisterClass(wc)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom, "Taskbar Demo", style,
                                          0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        nid = (self.hwnd, 0, win32gui.NIF_ICON,
               win32con.WM_USER + 20, hicon, "Demo")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)

    def showMsg(self, title, msg, TU):
        # 原作者使用Shell_NotifyIconA方法代替包装后的Shell_NotifyIcon方法
        # 据称是不能win32gui structure, 我稀里糊涂搞出来了.
        # 具体对比原代码.
        nid = (self.hwnd,  # 句柄
               0,  # 托盘图标ID
               win32gui.NIF_INFO,  # 标识
               0,  # 回调消息ID
               0,  # 托盘图标句柄
               "Test",  # 图标字符串
               msg,  # 气球提示字符串
               0,  # 提示的显示时间
               title,  # 提示标题
               TU  # 提示用到的图标
               )
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIF_MESSAGE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.


def chuang(H1, H2, i):
    t = TestTaskbarIcon()
    TU = [win32gui.NIIF_NONE, win32gui.NIIF_INFO,
          win32gui.NIIF_ERROR, win32gui.NIIF_WARNING, win32gui.NIIF_NOSOUND]
    t.showMsg(H1, H2, TU[i])
    win32gui.DestroyWindow(t.hwnd)


def new():
    t = TestTaskbarIcon()
    return t


# 再次封装
def chuangs(H1, H2, i, t):
    TU = [win32gui.NIIF_NONE, win32gui.NIIF_INFO,
          win32gui.NIIF_ERROR, win32gui.NIIF_WARNING, win32gui.NIIF_NOSOUND]
    t.showMsg(H1, H2, TU[i])
    time.sleep(2)
    return t


def dels(t):
    win32gui.DestroyWindow(t.hwnd)


# 测试方法
if __name__ == '__main__':
    """ t = TestTaskbarIcon()
    t.showMsg("您有新的文件，请登录查看", "Mr a2man!", win32gui.NIIF_INFO)
    time.sleep(2)
    win32gui.DestroyWindow(t.hwnd)
    t.showMsg("请登录查看", "Mr a2man!", win32gui.NIIF_INFO)
    time.sleep(2)
    win32gui.DestroyWindow(t.hwnd) """
    dels(chuangs("3", "3", 3, new()))
    dels(chuangs("2", "2", 2, chuangs("1", "1", 1, new())))
