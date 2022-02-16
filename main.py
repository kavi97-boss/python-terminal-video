import cv2 as cv
import curses as crs
import win32gui
import win32con

hwnd = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


density = '_.,-=+:;cba!?0123456789$W#@Ñ'
density1 = 'Ñ@#W$9876543210?!abc;:+=-,._'
# density = '.,-~:;=!*#$@'
# density1 = '@$#*!=;:~-,.'


cap = cv.VideoCapture(0)


def main(std):
    crs.curs_set(0)
    std.nodelay(1)
    std.timeout(100)

    run = True

    while run:
        key = std.getch()
        if key == 27:
            run = False

        ret, img = cap.read()
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        img = cv.flip(img, 1)

        width, height, = 0, 0

        if img.shape[1] > img.shape[0]:  # width > height in image
            height, max_rows = std.getmaxyx()
            scale_percent = int(100 * height / img.shape[0])
            width = int(img.shape[1] * scale_percent / 100)

        else:
            max_cols, width = std.getmaxyx()
            scale_percent = int(100 * width / img.shape[0])
            height = int(img.shape[1] * scale_percent / 100)

        dim = (width, height)

        resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)

        for p in range(len(resized)):
            for i in range(len(resized[0])):
                val = resized[p][i]
                pos = int(((len(density) - 1) / 255)*val)
                std.addstr(p, i*2, f"{density[pos]}")

        std.refresh()
    cap.release()
    cv.destroyAllWindows()


crs.wrapper(main)
