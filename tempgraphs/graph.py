import PySimpleGUI as sg
import time

RANGES = {"temp": (5, 45)}
RANGES.update({"accel" + d: (-4, 4) for d in "xy"})
RANGES.update({"accelz": (-12, -8)})
RANGES.update({"mag" + d: (-100, 100) for d in "xyz"})
RANGES.update({"gyro" + d: (-4, +4) for d in "xyz"})

ORDERED_KEYS = list(RANGES.keys())

HISTDAT = {key: [] for key in ORDERED_KEYS}
CUR_DRAWN = {key: [] for key in ORDERED_KEYS}

sg.theme("DarkPurple4")


def makeGraph(gKey, gRange):
    return sg.Graph(canvas_size=(300, 150),
                    graph_bottom_left=(300, gRange[0]),
                    graph_top_right=(0, gRange[1]),
                    key=gKey,
                    background_color='white')


def makeWindow():
    controlSection = [sg.Text("look its graphs")]

    layout = [[makeGraph(ORDERED_KEYS[0], RANGES[ORDERED_KEYS[0]])] +
              controlSection,
              [makeGraph(key, RANGES[key]) for key in ORDERED_KEYS[1:4]],
              [makeGraph(key, RANGES[key]) for key in ORDERED_KEYS[4:7]],
              [makeGraph(key, RANGES[key]) for key in ORDERED_KEYS[7:10]]]

    window = sg.Window("window title", layout, finalize=True)
    return window


def initGraphs(window):
    for graphKey in ORDERED_KEYS:
        graph = window[graphKey]
        cRange = RANGES[graphKey]
        graph.DrawText(graphKey, (80, cRange[1] // 2))
        for y in range(cRange[0], cRange[1], (cRange[1] - cRange[0]) // 3):
            graph.DrawLine((300, y), (0, y), color="#CCCCCC")
            graph.DrawText(y, (250, y), font="arial 10")
        graph.DrawLine((300, 0), (0, 0))


def updateGraphs(window):
    for graphKey in ORDERED_KEYS:
        graph = window[graphKey]
        for figID in CUR_DRAWN[graphKey]:
            graph.delete_figure(figID)
        CUR_DRAWN[graphKey] = []

        for valIdx, val in enumerate(HISTDAT[graphKey][::-1]):
            CUR_DRAWN[graphKey].append(
                graph.DrawCircle((valIdx * 10, val), 2, line_color="purple"))


def main():
    window = makeWindow()
    initGraphs(window)
    fpsCount = 0
    start_time = time.time()
    while True:

        event, values = window.read(timeout=0.005)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        inLine = input().strip().split(" ")
        for valIdx, val in enumerate(inLine[1:]):
            HISTDAT[ORDERED_KEYS[valIdx]].append(float(val))
            HISTDAT[ORDERED_KEYS[valIdx]] = HISTDAT[
                ORDERED_KEYS[valIdx]][-30::]
        #print(inLine)
        updateGraphs(window)

        fpsCount += 1
        if (time.time() - start_time) > 1:
            print("FPS: ", fpsCount / (time.time() - start_time))
            fpsCount = 0
            start_time = time.time()


if __name__ == "__main__":
    main()
