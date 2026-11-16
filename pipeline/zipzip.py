"""Zıpzıp the rabbit - Tosbi's quick, impatient little friend. Original design, drawn as SVG.
Faces left (towards Tosbi) by default. (x, y) = point on the ground under the feet."""
import math
from tosbi import INK

FUR = "#F6D7B8"        # warm peach fur
FUR_DARK = "#E8B98F"   # paws / shading
EAR_IN = "#FF9AA2"     # inner ears, cheeks
BELLY = "#FFF4E6"
SCARF = "#2BB3A3"      # teal scarf
SCARF_DOT = "#FFE066"
SW = 6


def _eye(cx, cy, blink, look):
    ry = max(2, 17 * (1 - blink))
    s = f'<ellipse cx="{cx}" cy="{cy}" rx="13" ry="{ry:.1f}" fill="#fff" stroke="{INK}" stroke-width="5"/>'
    if blink < 0.7:
        px, py = cx - 3 + look[0], cy + 1 + look[1]
        s += f'<circle cx="{px}" cy="{py}" r="{8*(1-blink):.1f}" fill="{INK}"/>'
        s += f'<circle cx="{px-2}" cy="{py-4}" r="{3*(1-blink):.1f}" fill="#fff"/>'
    return s


def zipzip(x, y, scale=1.0, expr="happy", blink=0.0, ear=0.0, look=(0, 0), flip=False, squash=0.0):
    """expr: happy | talk | surprised. ear: -1..1 ear wiggle. squash: landing squash 0..1."""
    sx = (-scale if flip else scale) * (1 + 0.12 * squash)
    sy = scale * (1 - 0.15 * squash)
    g = [f'<g transform="translate({x:.1f},{y:.1f}) scale({sx:.3f},{sy:.3f})" stroke-linejoin="round" stroke-linecap="round">']
    g.append('<ellipse cx="0" cy="4" rx="85" ry="12" fill="#000" opacity="0.12"/>')
    # tail (fluffy, at the back = right side)
    g.append(f'<circle cx="62" cy="-60" r="20" fill="{BELLY}" stroke="{INK}" stroke-width="{SW}"/>')
    # feet
    g.append(f'<ellipse cx="-38" cy="-14" rx="38" ry="17" fill="{FUR_DARK}" stroke="{INK}" stroke-width="{SW}"/>')
    g.append(f'<ellipse cx="34" cy="-14" rx="34" ry="16" fill="{FUR_DARK}" stroke="{INK}" stroke-width="{SW}"/>')
    # body
    g.append(f'<ellipse cx="0" cy="-78" rx="58" ry="66" fill="{FUR}" stroke="{INK}" stroke-width="{SW}"/>')
    g.append(f'<ellipse cx="-8" cy="-68" rx="34" ry="42" fill="{BELLY}"/>')
    # arms
    g.append(f'<path d="M -40 -100 Q -62 -78 -52 -60" fill="none" stroke="{INK}" stroke-width="{SW+16}"/>'
             f'<path d="M -40 -100 Q -62 -78 -52 -60" fill="none" stroke="{FUR}" stroke-width="16"/>')
    # ears (behind head), wiggle around their base
    for bx, base_ang, k in [(-22, -12, 1), (20, 10, -1)]:
        a = base_ang + 10 * ear * k
        g.append(f'<g transform="rotate({a:.1f} {bx} -190)">'
                 f'<ellipse cx="{bx}" cy="-262" rx="22" ry="70" fill="{FUR}" stroke="{INK}" stroke-width="{SW}"/>'
                 f'<ellipse cx="{bx}" cy="-258" rx="10" ry="50" fill="{EAR_IN}"/></g>')
    # head
    g.append(f'<circle cx="-6" cy="-178" r="60" fill="{FUR}" stroke="{INK}" stroke-width="{SW}"/>')
    # scarf
    g.append(f'<path d="M -58 -128 Q -6 -108 50 -128 L 48 -112 Q -6 -92 -58 -112 Z" fill="{SCARF}" stroke="{INK}" stroke-width="5"/>')
    g.append(f'<path d="M 30 -118 L 48 -84 L 26 -88 Z" fill="{SCARF}" stroke="{INK}" stroke-width="5"/>')
    for cx in (-40, -14, 14):
        g.append(f'<circle cx="{cx}" cy="-116" r="4" fill="{SCARF_DOT}"/>')
    # face (looking left)
    g.append(_eye(-40, -190, blink, look))
    g.append(_eye(-4, -190, blink, look))
    g.append(f'<ellipse cx="-58" cy="-160" rx="11" ry="7" fill="{EAR_IN}" opacity="0.9"/>')
    g.append(f'<ellipse cx="16" cy="-160" rx="11" ry="7" fill="{EAR_IN}" opacity="0.9"/>')
    g.append(f'<path d="M -29 -168 L -17 -168 L -23 -161 Z" fill="#E86A7E" stroke="{INK}" stroke-width="3"/>')
    if expr == "talk":
        g.append(f'<path d="M -40 -158 Q -23 -126 -6 -158 Z" fill="#7A2E2E" stroke="{INK}" stroke-width="4"/>')
    elif expr == "surprised":
        g.append(f'<ellipse cx="-23" cy="-148" rx="8" ry="10" fill="#7A2E2E" stroke="{INK}" stroke-width="4"/>')
    else:
        g.append(f'<path d="M -42 -158 Q -23 -140 -4 -158" fill="none" stroke="{INK}" stroke-width="4"/>')
    # two little front teeth when talking/happy
    if expr != "surprised":
        g.append('<rect x="-29" y="-159" width="12" height="9" rx="2" fill="#fff" stroke="#3B2A20" stroke-width="2"/>')
    g.append('</g>')
    return "".join(g)
