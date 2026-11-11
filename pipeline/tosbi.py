"""Tosbi the turtle - original character, drawn as SVG so every pose is reusable."""
import math

INK = "#3B2A20"
SKIN = "#8FD694"
SKIN_DARK = "#6FBF7A"
SHELL = "#F59E3B"
SHELL_DARK = "#D9762B"
PATCH = "#FFD27A"
CHEEK = "#FF9AA2"
SW = 6  # outline width


def _eye(cx, cy, blink, look):
    ry = max(2, 26 * (1 - blink))
    s = f'<ellipse cx="{cx}" cy="{cy}" rx="20" ry="{ry:.1f}" fill="#fff" stroke="{INK}" stroke-width="{SW}"/>'
    if blink < 0.7:
        px, py = cx + 6 + look[0], cy + 2 + look[1]
        pr = 11 * (1 - blink)
        s += f'<circle cx="{px}" cy="{py}" r="{pr:.1f}" fill="{INK}"/>'
        s += f'<circle cx="{px+4}" cy="{py-5}" r="{4*(1-blink):.1f}" fill="#fff"/>'
    return s


def tosbi(x, y, scale=1.0, expr="happy", lid=0.0, blink=0.0, legs=0.0,
          look=(0, 0), flip=False, squash=0.0):
    """Return an SVG <g> of Tosbi. (x,y) = point on the ground under the body.
    lid: 0 closed .. 1 fully open. legs: walk phase (radians). squash: -1..1 bounce."""
    sx = -scale if flip else scale
    sy = scale * (1 - 0.08 * squash)
    sxx = sx * (1 + 0.06 * squash)
    g = [f'<g transform="translate({x},{y}) scale({sxx:.3f},{sy:.3f})" stroke-linejoin="round" stroke-linecap="round">']
    # shadow
    g.append('<ellipse cx="20" cy="4" rx="210" ry="18" fill="#000" opacity="0.12"/>')
    # legs (walk swing)
    for i, lx in enumerate([-140, -80, 60, 120]):
        off = math.sin(legs + (i % 2) * math.pi) * 10
        g.append(f'<rect x="{lx-20+off:.1f}" y="-62" width="42" height="64" rx="19" fill="{SKIN}" stroke="{INK}" stroke-width="{SW}"/>')
    # tail
    g.append(f'<path d="M -170 -70 Q -215 -62 -205 -48 Q -190 -50 -165 -52 Z" fill="{SKIN}" stroke="{INK}" stroke-width="{SW}"/>')
    # neck + head
    g.append(f'<path d="M 120 -95 Q 150 -120 185 -125 L 200 -70 Q 160 -55 125 -60 Z" fill="{SKIN}" stroke="{INK}" stroke-width="{SW}"/>')
    g.append(f'<circle cx="215" cy="-140" r="72" fill="{SKIN}" stroke="{INK}" stroke-width="{SW}"/>')
    g.append(f'<ellipse cx="258" cy="-102" rx="16" ry="10" fill="{CHEEK}" opacity="0.9"/>')
    g.append(_eye(200, -158, blink, look))
    g.append(_eye(246, -158, blink, look))
    if expr == "surprised":
        g.append(f'<ellipse cx="238" cy="-112" rx="11" ry="14" fill="#7A2E2E" stroke="{INK}" stroke-width="5"/>')
    elif expr == "talk":
        g.append(f'<path d="M 214 -118 Q 236 -92 260 -118 Z" fill="#7A2E2E" stroke="{INK}" stroke-width="5"/>')
    else:
        g.append(f'<path d="M 214 -116 Q 236 -98 258 -116" fill="none" stroke="{INK}" stroke-width="5"/>')
    # shell body (lower band of dome)
    g.append(f'<path d="M -185 -55 A 175 150 0 0 1 165 -55 Z" fill="{SHELL}" stroke="{INK}" stroke-width="{SW}"/>')
    g.append(f'<rect x="-195" y="-70" width="375" height="28" rx="14" fill="{SHELL_DARK}" stroke="{INK}" stroke-width="{SW}"/>')
    for cx, cy, r in [(-120, -105, 26), (-55, -135, 30), (20, -140, 30), (95, -110, 26)]:
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PATCH}" opacity="0.85"/>')
    # lid (top cap) hinged at back
    ang = -55 * lid
    g.append(f'<g transform="rotate({ang:.1f} -115 -160)">')
    g.append(f'<path d="M -118 -160 A 110 62 0 0 1 102 -160 Q -8 -150 -118 -160 Z" fill="{SHELL}" stroke="{INK}" stroke-width="{SW}"/>')
    g.append(f'<circle cx="-8" cy="-190" r="20" fill="{PATCH}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<path d="M -8 -203 L -4 -194 L 5 -193 L -2 -187 L 0 -178 L -8 -183 L -16 -178 L -14 -187 L -21 -193 L -12 -194 Z" fill="#fff"/>')
    g.append('</g>')
    if lid > 0.15:
        a = min(1, (lid - 0.15) * 2)
        g.append(f'<ellipse cx="-8" cy="-162" rx="95" ry="14" fill="#5A2E12" opacity="{0.8*a:.2f}"/>')
    g.append('</g>')
    return "".join(g)


def ball(x, y, r, color, squash=0.0):
    sy = 1 - 0.25 * squash
    sx = 1 + 0.2 * squash
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({sx:.3f},{sy:.3f})">'
            f'<circle r="{r}" fill="{color}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M {-r*0.95:.0f} 0 Q 0 {r*0.35:.0f} {r*0.95:.0f} 0" fill="none" stroke="#fff" stroke-width="5" opacity="0.6"/>'
            f'<ellipse cx="{-r*0.35:.0f}" cy="{-r*0.4:.0f}" rx="{r*0.22:.0f}" ry="{r*0.14:.0f}" fill="#fff" opacity="0.8"/>'
            '</g>')


def sparkle(x, y, s, op=1.0, color="#FFE066"):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.2f})" opacity="{op:.2f}">'
            f'<path d="M 0 -30 Q 4 -4 30 0 Q 4 4 0 30 Q -4 4 -30 0 Q -4 -4 0 -30 Z" fill="{color}" stroke="{INK}" stroke-width="3"/></g>')
