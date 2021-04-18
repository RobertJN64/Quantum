import numpy as np

def drawPieMarker(x, y, ratios, size, colors, ax):
    xs = [x]
    ys = [y]
    sizes = [size]
    markers = []
    previous = 0
    # calculate the points of the pie pieces
    for color, ratio in zip(colors, ratios):
        this = 2 * np.pi * ratio + previous
        x  = [0] + np.cos(np.linspace(previous, this, 50)).tolist() + [0]
        y  = [0] + np.sin(np.linspace(previous, this, 50)).tolist() + [0]
        xy = np.column_stack([x, y])
        previous = this
        markers.append({'marker':xy, 's':np.abs(xy).max()**2*np.array(sizes), 'facecolor':color})

    # scatter each of the pie pieces to create pies
    ax.scatter(xs, ys, s=size+150, color="black")
    for marker in markers:
        ax.scatter(xs, ys, **marker)