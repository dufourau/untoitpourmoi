"""The site's QR code drawn as a house: the code is the wall, with the logo's roof and sun above it,
a heart at its centre and a little garden at its foot.

    svg = house_qr("https://...")      # an SVG string, any size

Error correction is H (30 %), so the heart in the middle costs nothing; make_flyer.py checks that
every picture still scans.
"""
import math
import segno

FOREST, LEAF, MOSS = "#13281c", "#2f6b43", "#1f3a2a"
LAVENDER, SUN, SAGE, PAPER = "#5b4a91", "#f4b223", "#a9c39a", "#ffffff"


def _rounded_ring(x, y, size, r, w, colour):
    """A square ring (finder pattern edge), drawn as one even-odd path."""
    def rr(x, y, s, r):
        return (f"M{x+r},{y}h{s-2*r}a{r},{r} 0 0 1 {r},{r}v{s-2*r}a{r},{r} 0 0 1 {-r},{r}"
                f"h{-(s-2*r)}a{r},{r} 0 0 1 {-r},{-r}v{-(s-2*r)}a{r},{r} 0 0 1 {r},{-r}z")
    return f'<path fill="{colour}" fill-rule="evenodd" d="{rr(x, y, size, r)}{rr(x+w, y+w, size-2*w, max(r-w, .3))}"/>'


def house_qr(url, garden=True):
    qr = segno.make(url, error="h", boost_error=False)
    m = [list(row) for row in qr.matrix]
    n = len(m)
    c = n / 2
    hole = 4.5                      # half side of the clear square in the middle, in modules
    finders = [(0, 0), (n - 7, 0), (0, n - 7)]

    def in_finder(x, y):
        return any(fx <= x < fx + 7 and fy <= y < fy + 7 for fx, fy in finders)

    def in_hole(x, y):
        return abs(x + .5 - c) < hole and abs(y + .5 - c) < hole

    # canvas in module units: the wall (the QR plus a quiet zone), the roof above, the garden below
    pad = 3
    roof_h = n * .42
    top = -pad - roof_h - 2
    left, right = -pad - 5, n + pad + 5
    bottom = n + pad + (4 if garden else 1)
    W, H = right - left, bottom - top
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{left} {top:.2f} {W} {H:.2f}">',
           f'<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="{n}" x2="0" y2="0">'
           f'<stop offset="0" stop-color="{FOREST}"/><stop offset="1" stop-color="{LEAF}"/></linearGradient></defs>']

    # the logo's sun, half behind the roof on the left
    sx, sy, sr = c - n * .28, -pad - roof_h * .55, n * .13
    for k in range(9):
        a = math.radians(150 + k * 22)
        out.append(f'<line x1="{sx + math.cos(a)*(sr+1.2):.2f}" y1="{sy + math.sin(a)*(sr+1.2):.2f}" '
                   f'x2="{sx + math.cos(a)*(sr+3):.2f}" y2="{sy + math.sin(a)*(sr+3):.2f}" '
                   f'stroke="{SUN}" stroke-width=".9" stroke-linecap="round"/>')
    out.append(f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="{sr:.2f}" fill="{SUN}"/>')

    # the wall: a white panel with soft corners
    out.append(f'<rect x="{-pad}" y="{-pad}" width="{n + 2*pad}" height="{n + 2*pad}" rx="2.2" fill="{PAPER}"/>')

    # the roof, like the logo's brush stroke: two strokes meeting above the middle
    eave = -pad - .3
    out.append(f'<path d="M{-pad - 4},{eave + 1.6} L{c},{-pad - roof_h} L{n + pad + 4},{eave + 1.6}" fill="none" '
               f'stroke="{MOSS}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/>')
    # a chimney with a leaf growing out of it
    chx = c + n * .24
    chy = -pad - roof_h + (chx - c) * roof_h / (c + pad + 4)
    out.append(f'<rect x="{chx - 1.2:.2f}" y="{chy - 4:.2f}" width="2.6" height="4.2" rx=".4" fill="{MOSS}"/>')
    out.append(f'<path transform="translate({chx + .1:.2f},{chy - 4.3:.2f}) scale(.075) rotate(-10)" fill="{LEAF}" '
               f'd="M0 0C0-22 14-36 34-40C34-18 22-4 0 0ZM0 0C-2-14-12-24-26-26C-26-12-16-2 0 0Z"/>')

    # data modules as dots, darker at the foot like a plant growing up
    dots = []
    for y in range(n):
        for x in range(n):
            if m[y][x] and not in_finder(x, y) and not in_hole(x, y):
                dots.append(f'<circle cx="{x + .5}" cy="{y + .5}" r=".44"/>')
    out.append(f'<g fill="url(#g)">' + "".join(dots) + "</g>")

    # the three eyes: rounded windows, lavender pane
    for fx, fy in finders:
        out.append(_rounded_ring(fx, fy, 7, 2.2, 1, MOSS))
        out.append(f'<rect x="{fx + 2}" y="{fy + 2}" width="3" height="3" rx="1" fill="{LAVENDER}"/>')

    # the heart at the centre: what the house holds
    hs = hole * 2 - 1.6
    out.append(f'<path transform="translate({c - hs/2:.2f},{c - hs/2 + .3:.2f}) scale({hs/24:.3f})" fill="{LAVENDER}" '
               'd="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.7 4.5c2.1 0 3.6 1.1 4.3 2.4.7-1.3 2.2-2.4 4.3-2.4 3.7 0 5.8 3.9 4.3 7.3C19.5 16.4 12 21 12 21z"/>')

    if garden:
        # grass line and a few leaves at the foot of the wall
        gy = n + pad + 1.1
        out.append(f'<path d="M{left + 1},{gy} H{right - 1}" stroke="{SAGE}" stroke-width=".9" stroke-linecap="round"/>')
        for gx, s, rot, col in [(-pad - 3, .085, -25, LEAF), (-pad - 1.2, .06, 15, SAGE), (n + pad + 1.6, .07, -10, SAGE),
                                (n + pad + 3.3, .09, 25, LEAF), (c - 9, .05, 0, SAGE), (c + 8, .055, -20, LEAF)]:
            out.append(f'<path transform="translate({gx},{gy}) scale({s}) rotate({rot})" fill="{col}" '
                       'd="M0 0C0-22 14-36 34-40C34-18 22-4 0 0ZM0 0C-2-14-12-24-26-26C-26-12-16-2 0 0Z"/>')
    out.append("</svg>")
    return "\n".join(out)
