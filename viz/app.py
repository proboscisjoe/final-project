import wx
from PIL import Image
from pygraphviz import AGraph

SIZE = (1280, 800)
LOG_PATH = '/var/log/syslog'
TIMESTAMP = 0.0


def get_image():
    global TIMESTAMP
    ip_dict = {}  # maps source-destination IP pairs to their number of occurrences

    trace_file = open(LOG_PATH, newline='')

    local_timestamp = TIMESTAMP
    for line in trace_file.readlines():
        split_line = line.split('|')

        if len(split_line) == 4:
            timestamp = float(split_line[0].split('[')[1].split(']')[0])

            if timestamp > local_timestamp:

                src_dst_pair = (split_line[1], split_line[2])

                if src_dst_pair in ip_dict.keys():
                    ip_dict[src_dst_pair] = ip_dict[src_dst_pair] + 1
                else:
                    ip_dict[src_dst_pair] = 1

                local_timestamp = timestamp

    if local_timestamp > TIMESTAMP:
        ip_graph = AGraph(directed=True)

        for (src_ip, dst_ip), packet_count in ip_dict.items():
            ip_graph.add_edge(
                src_ip, dst_ip, color='brown', label=packet_count, labelangle=45, len=1.95)

        ip_graph.layout()

        ip_graph.draw('graph.png')

        TIMESTAMP = local_timestamp

    graph_img = Image.open('graph.png')
    background_image = Image.new('RGB', SIZE, color=(255, 255, 255))

    x = round((SIZE[0] / 2.0) - graph_img.width)
    y = round((SIZE[1] / 4.0) - (graph_img.height / 4.0))

    background_image.paste(graph_img, (x, y))

    return background_image


def pil_to_wx(image):
    width, height = image.size
    buffer = image.convert('RGB').tobytes()
    bitmap = wx.Bitmap.FromBuffer(width, height, buffer)
    return bitmap


class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent, -1)
        self.SetSize(SIZE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.update()

    def update(self):
        self.Refresh()
        self.Update()
        self.Center()
        wx.CallLater(250, self.update)

    def create_bitmap(self):
        image = get_image()
        bitmap = pil_to_wx(image)

        return bitmap

    def on_paint(self, event):
        bitmap = self.create_bitmap()
        dc = wx.AutoBufferedPaintDC(self)

        dc.DrawBitmap(bitmap, 0, 0)


class Frame(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX
        super(Frame, self).__init__(None, -1, 'Network Topology', style=style)
        _ = Panel(self)
        self.Fit()


def main():
    app = wx.App()
    frame = Frame()
    frame.Center()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
