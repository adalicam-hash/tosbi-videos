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


# ---- week 2026-11-16: farm animals, everyday things, vehicles (original designs)
def cow(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<ellipse cx="-66" cy="-30" rx="26" ry="14" fill="#fff" stroke="{INK}" stroke-width="{SW}" transform="rotate(-20 -66 -30)"/>'
         f'<ellipse cx="66" cy="-30" rx="26" ry="14" fill="#fff" stroke="{INK}" stroke-width="{SW}" transform="rotate(20 66 -30)"/>'
         f'<path d="M -34 -58 Q -44 -88 -30 -92 Q -26 -74 -20 -60 Z" fill="#F2E3B3" stroke="{INK}" stroke-width="4"/>'
         f'<path d="M 34 -58 Q 44 -88 30 -92 Q 26 -74 20 -60 Z" fill="#F2E3B3" stroke="{INK}" stroke-width="4"/>'
         f'<ellipse cx="0" cy="-8" rx="62" ry="64" fill="#fff" stroke="{INK}" stroke-width="{SW}"/>'
         '<path d="M -50 -40 Q -30 -60 -14 -40 Q -26 -20 -50 -28 Z" fill="#3B2A20"/>'
         '<ellipse cx="34" cy="-36" rx="14" ry="10" fill="#3B2A20"/>'
         '<circle cx="-22" cy="-14" r="9" fill="#3B2A20"/><circle cx="22" cy="-14" r="9" fill="#3B2A20"/>'
         '<circle cx="-19" cy="-17" r="3" fill="#fff"/><circle cx="25" cy="-17" r="3" fill="#fff"/>'
         f'<ellipse cx="0" cy="32" rx="44" ry="28" fill="#FFB8C4" stroke="{INK}" stroke-width="{SW}"/>'
         '<ellipse cx="-14" cy="30" rx="6" ry="8" fill="#B5546A"/><ellipse cx="14" cy="30" rx="6" ry="8" fill="#B5546A"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def sheep(x, y, r, squash=0.0):
    s = r / 70
    puffs = [(-48, -40), (-10, -62), (32, -52), (58, -12), (50, 32), (10, 52), (-34, 46), (-60, 8)]
    wool = "".join(f'<circle cx="{cx}" cy="{cy}" r="30" fill="#fff" stroke="{INK}" stroke-width="{SW}"/>' for cx, cy in puffs)
    b = (wool + '<circle r="56" fill="#fff"/>'
         f'<ellipse cx="-52" cy="-2" rx="18" ry="10" fill="#6B5A4E" stroke="{INK}" stroke-width="4"/>'
         f'<ellipse cx="52" cy="-2" rx="18" ry="10" fill="#6B5A4E" stroke="{INK}" stroke-width="4"/>'
         f'<ellipse cx="0" cy="8" rx="36" ry="42" fill="#6B5A4E" stroke="{INK}" stroke-width="{SW}"/>'
         '<circle cx="-12" cy="-30" r="12" fill="#fff"/><circle cx="8" cy="-36" r="13" fill="#fff"/><circle cx="20" cy="-26" r="10" fill="#fff"/>'
         '<circle cx="-13" cy="0" r="7" fill="#fff"/><circle cx="13" cy="0" r="7" fill="#fff"/>'
         '<circle cx="-12" cy="1" r="4" fill="#3B2A20"/><circle cx="14" cy="1" r="4" fill="#3B2A20"/>'
         '<path d="M -8 26 Q 0 34 8 26" fill="none" stroke="#fff" stroke-width="4"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def chicken(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<path d="M 50 -10 Q 86 -40 80 0 Q 92 10 70 26 Z" fill="#fff" stroke="{INK}" stroke-width="{SW}"/>'
         f'<ellipse cx="0" cy="12" rx="64" ry="54" fill="#fff" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -6 10 Q 24 -6 40 22 Q 14 36 -6 10 Z" fill="#F2F2F2" stroke="{INK}" stroke-width="4"/>'
         f'<circle cx="-30" cy="-34" r="36" fill="#fff" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -46 -64 Q -46 -86 -32 -74 Q -28 -92 -16 -72 Q -6 -84 -8 -62 Z" fill="#E94B3C" stroke="{INK}" stroke-width="4"/>'
         f'<path d="M -64 -34 L -86 -28 L -64 -22 Z" fill="#FFB020" stroke="{INK}" stroke-width="4"/>'
         f'<path d="M -64 -18 Q -72 -4 -60 -6" fill="#E94B3C" stroke="{INK}" stroke-width="3"/>'
         '<circle cx="-42" cy="-40" r="7" fill="#3B2A20"/><circle cx="-40" cy="-42" r="2.5" fill="#fff"/>'
         f'<path d="M -16 64 L -16 80 M 14 64 L 14 80" stroke="#FFB020" stroke-width="7"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def cup(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<path d="M 46 -20 Q 86 -20 82 12 Q 78 40 40 34" fill="none" stroke="{INK}" stroke-width="{SW+16}"/>'
         f'<path d="M 46 -20 Q 86 -20 82 12 Q 78 40 40 34" fill="none" stroke="#4CA8E0" stroke-width="16"/>'
         f'<path d="M -56 -52 L 56 -52 L 46 52 Q 0 66 -46 52 Z" fill="#4CA8E0" stroke="{INK}" stroke-width="{SW}"/>'
         f'<ellipse cx="0" cy="-52" rx="56" ry="14" fill="#fff" stroke="{INK}" stroke-width="{SW}"/>'
         '<ellipse cx="0" cy="-50" rx="46" ry="9" fill="#F5F0E6"/>'
         '<circle cx="-14" cy="8" r="10" fill="#FFE066"/><circle cx="16" cy="18" r="8" fill="#FFE066"/><circle cx="2" cy="-18" r="6" fill="#FFE066"/>'
         '<rect x="-40" y="-36" width="10" height="56" rx="5" fill="#fff" opacity="0.5"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def hat(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<ellipse cx="0" cy="34" rx="84" ry="22" fill="#E94B3C" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -50 34 Q -56 -50 0 -56 Q 56 -50 50 34 Z" fill="#E94B3C" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -52 8 Q 0 20 52 8 L 51 24 Q 0 36 -51 24 Z" fill="#FFE066" stroke="{INK}" stroke-width="4"/>'
         f'<circle cx="0" cy="-62" r="16" fill="#fff" stroke="{INK}" stroke-width="4"/>'
         '<path d="M -30 -30 Q -24 -44 -10 -46" fill="none" stroke="#fff" stroke-width="7" opacity="0.6"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def shoe(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<path d="M -70 30 L -64 -40 Q -40 -52 -16 -40 L -10 -6 Q 40 -4 70 14 Q 82 30 70 40 L -66 40 Z" fill="#9B6BDF" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -74 40 L 76 40 Q 80 54 66 56 L -70 56 Q -80 50 -74 40 Z" fill="#fff" stroke="{INK}" stroke-width="{SW}"/>'
         '<path d="M -48 -22 L -22 -10 M -50 -6 L -20 4 M -48 -22 L -20 4" stroke="#fff" stroke-width="5"/>'
         '<circle cx="34" cy="20" r="9" fill="#FFE066"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def _wheel(cx, cy, rr):
    return (f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="#3B2A20" stroke="{INK}" stroke-width="{SW}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{rr*0.45:.0f}" fill="#D9D9D9"/>')


def car(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<path d="M -84 30 L -84 -6 Q -80 -20 -60 -22 L -36 -58 Q -28 -66 -14 -66 L 30 -66 Q 44 -66 52 -56 L 70 -22 Q 88 -18 88 0 L 88 30 Z" fill="#E94B3C" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -28 -26 L -12 -52 L 6 -52 L 6 -26 Z" fill="#BFE7FF" stroke="{INK}" stroke-width="4"/>'
         f'<path d="M 18 -26 L 18 -52 L 36 -52 L 52 -26 Z" fill="#BFE7FF" stroke="{INK}" stroke-width="4"/>'
         '<circle cx="80" cy="-4" r="7" fill="#FFE066"/>'
         + _wheel(-46, 32, 22) + _wheel(50, 32, 22))
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def bus(x, y, r, squash=0.0):
    s = r / 70
    win = "".join(f'<rect x="{wx}" y="-52" width="30" height="30" rx="6" fill="#BFE7FF" stroke="{INK}" stroke-width="4"/>' for wx in (-78, -40, -2, 36))
    b = (f'<rect x="-92" y="-70" width="184" height="104" rx="22" fill="#FFC93C" stroke="{INK}" stroke-width="{SW}"/>'
         + win +
         f'<rect x="70" y="-52" width="16" height="66" rx="5" fill="#BFE7FF" stroke="{INK}" stroke-width="4"/>'
         '<rect x="-92" y="-8" width="184" height="10" fill="#E07A2E"/>'
         '<circle cx="84" cy="22" r="6" fill="#fff"/>'
         + _wheel(-52, 36, 20) + _wheel(50, 36, 20))
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


def boat(x, y, r, squash=0.0):
    s = r / 70
    b = (f'<path d="M -6 -84 L -6 18" stroke="{INK}" stroke-width="7"/>'
         f'<path d="M 0 -80 L 60 4 L 0 4 Z" fill="#fff" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -12 -66 L -58 4 L -12 4 Z" fill="#FFE066" stroke="{INK}" stroke-width="{SW}"/>'
         f'<path d="M -90 14 L 90 14 Q 74 56 50 58 L -50 58 Q -74 56 -90 14 Z" fill="#3C8DE9" stroke="{INK}" stroke-width="{SW}"/>'
         '<circle cx="-40" cy="34" r="7" fill="#fff"/><circle cx="0" cy="34" r="7" fill="#fff"/><circle cx="40" cy="34" r="7" fill="#fff"/>'
         f'<path d="M -6 -84 L 22 -76 L -6 -68" fill="#E94B3C" stroke="{INK}" stroke-width="3"/>')
    return _g(x, y, s * (1 + 0.2 * squash), s * (1 - 0.25 * squash), b)


DRAW.update({"cow": cow, "sheep": sheep, "chicken": chicken, "cup": cup, "hat": hat, "shoe": shoe,
             "car": car, "bus": bus, "boat": boat})
