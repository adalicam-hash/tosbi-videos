"""Original item drawings that pop out of Tosbi's shell. Each draws centred at (x, y) with size r."""
from tosbi import ball, INK

SW = 6


def _g(x, y, sx, sy, body):
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({sx:.3f},{sy:.3f})" stroke-linejoin="round" stroke-linecap="round">{body}</g>'


def cat(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<path d="M -58 -30 L -48 -88 L -12 -55 Z" fill="#F4A259" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M 58 -30 L 48 -88 L 12 -55 Z" fill="#F4A259" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -46 -40 L -44 -72 L -22 -52 Z" fill="#FFC8B4"/><path d="M 46 -40 L 44 -72 L 22 -52 Z" fill="#FFC8B4"/>'
         f'<circle r="68" fill="#F4A259" stroke="{INK}" stroke-width="{SW}"/>'
         '<circle cx="-24" cy="-8" r="9" fill="#3B2A20"/><circle cx="24" cy="-8" r="9" fill="#3B2A20"/>'
         '<circle cx="-21" cy="-11" r="3" fill="#fff"/><circle cx="27" cy="-11" r="3" fill="#fff"/>'
         '<path d="M -7 12 L 7 12 L 0 20 Z" fill="#FF8FA3"/>'
         f'<path d="M 0 20 Q -10 32 -20 26 M 0 20 Q 10 32 20 26" fill="none" stroke="{INK}" stroke-width="4"/>'
         f'<path d="M -30 16 L -72 8 M -30 24 L -70 28 M 30 16 L 72 8 M 30 24 L 70 28" stroke="{INK}" stroke-width="3"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def dog(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<ellipse cx="-62" cy="-5" rx="22" ry="45" fill="#8B5E3C" stroke="{INK}" stroke-width="{SW}" transform="rotate(15 -62 -5)"/>'
         f'<ellipse cx="62" cy="-5" rx="22" ry="45" fill="#8B5E3C" stroke="{INK}" stroke-width="{SW}" transform="rotate(-15 62 -5)"/>'
         f'<circle r="66" fill="#E8C39E" stroke="{INK}" stroke-width="{SW}"/>'
         '<ellipse cx="22" cy="-20" rx="18" ry="16" fill="#C49A6C"/>'
         '<circle cx="-22" cy="-12" r="9" fill="#3B2A20"/><circle cx="22" cy="-12" r="9" fill="#3B2A20"/>'
         '<circle cx="-19" cy="-15" r="3" fill="#fff"/><circle cx="25" cy="-15" r="3" fill="#fff"/>'
         f'<ellipse cx="0" cy="14" rx="14" ry="10" fill="#3B2A20"/>'
         f'<path d="M 0 24 Q -12 38 -22 30 M 0 24 Q 12 38 22 30" fill="none" stroke="{INK}" stroke-width="4"/>'
         '<ellipse cx="0" cy="40" rx="9" ry="10" fill="#FF8FA3"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def duck(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<ellipse cx="0" cy="22" rx="70" ry="46" fill="#FFD93D" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -20 20 Q 10 0 34 26 Q 6 40 -20 20 Z" fill="#FFC300" stroke="{INK}" stroke-width="4"/>'
         f'<circle cx="-24" cy="-34" r="40" fill="#FFD93D" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -64 -34 Q -96 -30 -92 -18 Q -78 -10 -60 -20 Z" fill="#FF9F1C" stroke="{INK}" stroke-width="4"/>'
         '<circle cx="-36" cy="-44" r="7" fill="#3B2A20"/><circle cx="-34" cy="-46" r="2.5" fill="#fff"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def shape_circle(x, y, r, squash=0.0):
    return _g(x, y, 1 + 0.2 * squash, 1 - 0.25 * squash,
              f'<circle r="{r}" fill="#4CC38A" stroke="{INK}" stroke-width="{SW}"/>'
              f'<ellipse cx="{-r*0.35:.0f}" cy="{-r*0.4:.0f}" rx="{r*0.2:.0f}" ry="{r*0.12:.0f}" fill="#fff" opacity="0.7"/>')


def shape_square(x, y, r, squash=0.0):
    a = r * 0.9
    return _g(x, y, 1 + 0.2 * squash, 1 - 0.25 * squash,
              f'<rect x="{-a:.0f}" y="{-a:.0f}" width="{2*a:.0f}" height="{2*a:.0f}" rx="{a*0.18:.0f}" fill="#9B6BDF" stroke="{INK}" stroke-width="{SW}"/>'
              f'<rect x="{-a*0.7:.0f}" y="{-a*0.75:.0f}" width="{a*0.5:.0f}" height="{a*0.18:.0f}" rx="6" fill="#fff" opacity="0.6"/>')


def shape_triangle(x, y, r, squash=0.0):
    return _g(x, y, 1 + 0.2 * squash, 1 - 0.25 * squash,
              f'<path d="M 0 {-r*1.05:.0f} L {r*1.05:.0f} {r*0.8:.0f} L {-r*1.05:.0f} {r*0.8:.0f} Z" fill="#FF8C42" stroke="{INK}" stroke-width="{SW}"/>'
              f'<path d="M {-r*0.15:.0f} {-r*0.55:.0f} L {-r*0.45:.0f} {r*0.05:.0f}" stroke="#fff" stroke-width="8" opacity="0.6"/>')


def ball_of(color):
    return lambda x, y, r, squash=0.0: ball(x, y, r, color, squash)


DRAW = {
    "ball_red": ball_of("#E94B3C"), "ball_yellow": ball_of("#FFC93C"), "ball_blue": ball_of("#3C8DE9"),
    "cat": cat, "dog": dog, "duck": duck,
    "circle": shape_circle, "square": shape_square, "triangle": shape_triangle,
}


def apple(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<path d="M 0 -50 C -60 -80 -80 -10 -62 25 C -45 65 -15 70 0 58 C 15 70 45 65 62 25 C 80 -10 60 -80 0 -50 Z" fill="#E63946" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M 0 -50 Q 2 -72 10 -84" fill="none" stroke="#6B3E26" stroke-width="7"/>'
         f'<path d="M 8 -70 Q 35 -95 52 -70 Q 30 -58 8 -70 Z" fill="#6CC04A" stroke="{INK}" stroke-width="4"/>'
         '<ellipse cx="-30" cy="-22" rx="12" ry="20" fill="#fff" opacity="0.45" transform="rotate(20 -30 -22)"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def banana(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<path d="M -70 -30 Q -60 55 40 50 Q 80 45 82 20 Q 50 38 10 25 Q -40 5 -52 -40 Z" fill="#FFD93D" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -70 -30 L -60 -50 L -50 -42" fill="#6B3E26" stroke="{INK}" stroke-width="4"/>'
         '<path d="M -45 0 Q -20 30 30 36" fill="none" stroke="#E0B000" stroke-width="5"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def orange(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<circle r="66" fill="#FF9F1C" stroke="{INK}" stroke-width="{SW}"/>'
         + "".join(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#E07B00"/>' for cx, cy in [(-25, 10), (10, 25), (30, -10), (-10, -20), (20, 40), (-35, 35)])
         + f'<path d="M 0 -66 Q 20 -92 42 -76 Q 22 -60 0 -66 Z" fill="#6CC04A" stroke="{INK}" stroke-width="4"/>'
         '<ellipse cx="-28" cy="-28" rx="14" ry="9" fill="#fff" opacity="0.45"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


DRAW.update({"apple": apple, "banana": banana, "orange": orange})
