# -*- coding: utf-8 -*-
"""生成 20 个动漫风格、透明背景的餐点 SVG。风格统一：软厚棕描边 + 马卡龙配色 + 萌系表情。"""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'src', 'assets', 'food')
STROKE = '#7a4a2b'


def svg(inner):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
            f'<g stroke="{STROKE}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round">'
            + inner + '</g></svg>\n')


def steam():
    return ('<g fill="none" stroke="#c6cdda" stroke-width="5" opacity="0.85">'
            '<path d="M70,90 q-9,-8 0,-16 q9,-8 0,-16"/>'
            '<path d="M100,88 q-9,-8 0,-16 q9,-8 0,-16"/>'
            '<path d="M130,90 q-9,-8 0,-16 q9,-8 0,-16"/></g>')


def chop():
    return ('<g stroke="#b9824f" stroke-width="5.5">'
            '<line x1="158" y1="38" x2="116" y2="106"/>'
            '<line x1="168" y1="46" x2="126" y2="114"/></g>')


def face(cx=100, cy=141, dark=True):
    eye = '#4a3320' if dark else '#ffffff'
    blush = '#ff9fb0'
    smile = '#4a3320' if dark else '#ffffff'
    return (f'<g stroke="none">'
            f'<ellipse cx="{cx-13}" cy="{cy-2}" rx="4.2" ry="5" fill="{eye}"/>'
            f'<ellipse cx="{cx+13}" cy="{cy-2}" rx="4.2" ry="5" fill="{eye}"/>'
            f'<ellipse cx="{cx-24}" cy="{cy+8}" rx="7" ry="4" fill="{blush}" opacity="0.55"/>'
            f'<ellipse cx="{cx+24}" cy="{cy+8}" rx="7" ry="4" fill="{blush}" opacity="0.55"/>'
            f'</g>'
            f'<path d="M{cx-9},{cy+6} Q{cx},{cy+14} {cx+9},{cy+6}" fill="none" stroke="{smile}" stroke-width="3.4"/>')


def noodles(color, ys=(98, 104, 110, 116), w=5, x0=40, x1=160):
    out = [f'<g fill="none" stroke="{color}" stroke-width="{w}">']
    for y in ys:
        d = f'M{x0},{y} q15,-9 30,0 t30,0 t30,0 t30,0'
        out.append(f'<path d="{d}"/>')
    out.append('</g>')
    return ''.join(out)


def bowl(broth='#f4c95d', middle='', top='', use_steam=True, ceramic='#ffffff',
         face_dark=True, use_chop=False, broth_stroke=None):
    p = []
    if use_steam:
        p.append(steam())
    if use_chop:
        p.append(chop())
    # 碗身
    p.append('<path d="M32,112 C30,162 56,174 100,174 C144,174 170,162 168,112 Z" fill="%s"/>' % ceramic)
    # 汤面
    p.append('<ellipse cx="100" cy="112" rx="66" ry="17" fill="%s"/>' % broth)
    p.append(middle)
    p.append(top)
    p.append('<ellipse cx="100" cy="112" rx="66" ry="17" fill="none"/>')
    p.append('<path d="M64,168 q36,10 72,0" fill="none" opacity="0.45"/>')
    p.append(face(100, 141, face_dark))
    return ''.join(p)


def dot(cx, cy, r, fill):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'


def ell(cx, cy, rx, ry, fill, rot=None):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"{t}/>'


# ---------- 各餐点 ----------
def d_lanzhou():
    mid = noodles('#f2d27a')
    top = (ell(78, 106, 13, 6, '#fbeecf') + ell(122, 109, 13, 6, '#fbeecf')
           + dot(96, 104, 7, '#8a4b26') + dot(112, 110, 6, '#8a4b26')
           + ell(62, 111, 5, 3, '#d83a2a', -15) + ell(138, 105, 5, 3, '#d83a2a', 20)
           + '<path d="M86,100 l5,-7 M108,99 l5,-7 M130,112 l5,-6" stroke="#3f9d4d" stroke-width="4"/>'
           + dot(70, 103, 3.5, '#3f9d4d') + dot(146, 110, 3.5, '#3f9d4d')
           + ell(96, 112, 12, 4, '#e0452f', 8))
    return bowl('#f6d58a', mid, top)


def d_xiaomian():
    mid = noodles('#f0c66a')
    top = (ell(100, 108, 50, 10, '#d94326', 0).replace('<ellipse', '<ellipse opacity="0.85"')
           + dot(70, 105, 5, '#f3e2b0') + dot(88, 112, 5, '#f3e2b0') + dot(128, 104, 5, '#f3e2b0')
           + '<path d="M76,100 l5,-6 M118,99 l5,-6 M140,110 l5,-6" stroke="#4aa85a" stroke-width="4"/>'
           + dot(96, 102, 3.5, '#4aa85a') + dot(134, 112, 3.5, '#4aa85a')
           + ell(60, 110, 8, 4, '#5aa854'))
    return bowl('#c93a24', mid, top)


def d_luosifen():
    mid = noodles('#f3ead6', ys=(100, 105, 110, 115), w=4)
    top = (ell(80, 105, 12, 7, '#9a6b3a') + ell(120, 110, 12, 7, '#9a6b3a')
           + dot(66, 110, 6, '#f6f1e2') + dot(138, 105, 6, '#f6f1e2')
           + ell(100, 104, 9, 5, '#e0452f')
           + '<path d="M90,100 l5,-6 M112,106 l5,-6" stroke="#4aa85a" stroke-width="4"/>'
           + dot(130, 112, 3.5, '#4aa85a') + ell(58, 104, 7, 4, '#5aa854', -10))
    return bowl('#e9c15e', mid, top)


def d_regan():
    mid = noodles('#b08145', ys=(99, 105, 111, 116), w=6)
    top = ('<g stroke="none">' + ''.join(dot(x, y, 2.4, '#f4ead0') for x, y in
           [(70, 102), (86, 109), (104, 103), (120, 110), (138, 104), (96, 114), (128, 115), (78, 115)]) + '</g>'
           + '<path d="M74,99 l5,-6 M116,98 l5,-6 M140,109 l5,-6 M88,100 l5,-6" stroke="#4aa85a" stroke-width="4"/>')
    return bowl('#a97942', mid, top, use_steam=False)


def d_zhajiang():
    mid = noodles('#f2d27a')
    top = (ell(100, 106, 22, 10, '#5b3a22')
           + '<g stroke="none">' + dot(94, 104, 2.6, '#8a5a38') + dot(106, 108, 2.6, '#8a5a38') + dot(100, 110, 2.6, '#8a5a38') + '</g>'
           + '<path d="M60,112 h22 M120,112 h22" stroke="#7ec24a" stroke-width="5"/>'
           + dot(64, 104, 4.5, '#f6f1e2') + dot(140, 105, 4.5, '#f6f1e2')
           + ell(72, 108, 5, 4, '#8fc15a') + ell(132, 109, 5, 4, '#8fc15a'))
    return bowl('#e7d3a4', mid, top)


def d_jianbing():
    # 煎饼（折叠方形）
    inner = ('<rect x="38" y="46" width="124" height="124" rx="22" fill="#e9b95f"/>'
             '<g stroke="none">'
             + ell(72, 84, 12, 8, '#d99b3f', 20) + ell(128, 120, 14, 9, '#d99b3f', -15)
             + ell(130, 76, 9, 6, '#cf9038', 10)
             + ''.join(dot(x, y, 3.2, '#4aa85a') for x, y in
                       [(70, 120), (96, 96), (122, 132), (138, 96), (84, 150), (60, 104)])
             + '</g>'
             '<rect x="82" y="78" width="36" height="14" rx="7" fill="#fbf6e9" transform="rotate(-12 100 85)"/>'
             '<path d="M150,46 L162,46 L162,58 Z" fill="#f4d98f"/>'
             + face(100, 120))
    return svg(inner)


def d_changfen():
    inner = ('<ellipse cx="100" cy="150" rx="80" ry="16" fill="#eceef2"/>'
             '<ellipse cx="100" cy="140" rx="66" ry="11" fill="#6d4525"/>'
             '<rect x="30" y="98" width="124" height="36" rx="18" fill="#fbfbfd"/>'
             '<path d="M40,106 h104 M40,118 h104" stroke="#e2e5ec" stroke-width="3" fill="none"/>'
             '<rect x="44" y="68" width="104" height="34" rx="17" fill="#ffffff"/>'
             '<path d="M54,78 h84 M54,90 h84" stroke="#e7eaef" stroke-width="3" fill="none"/>'
             '<path d="M120,84 a11,9 0 1,1 -9,12 q4,-8 9,-12 Z" fill="#ff8a4c"/>'
             + dot(116, 86, 2.4, '#e06a2e')
             + face(96, 116))
    return svg(inner)


def d_guoqiao():
    mid = noodles('#f6efe0', ys=(100, 105, 110, 115), w=4)
    top = (ell(82, 105, 13, 7, '#f3b8b8') + ell(120, 109, 12, 7, '#fbeecf')
           + dot(100, 112, 7, '#ffd76b')
           + '<path d="M66,104 q10,-8 20,0 M120,100 q10,-8 20,0" stroke="#4aa85a" stroke-width="4" fill="none"/>'
           + dot(60, 110, 3.5, '#4aa85a') + dot(142, 104, 3.5, '#4aa85a'))
    return bowl('#f2e2b0', mid, top, use_chop=True)


def d_dandan():
    mid = noodles('#f0c66a')
    top = (ell(100, 107, 24, 10, '#8a5230')
           + '<g stroke="none">' + ''.join(dot(x, y, 2.6, '#5b3417') for x, y in
           [(90, 104), (104, 106), (112, 110), (96, 110), (108, 102)]) + '</g>'
           + dot(70, 105, 4.5, '#e8c98f') + dot(132, 104, 4.5, '#e8c98f') + dot(84, 112, 4, '#e8c98f')
           + '<path d="M76,100 l5,-6 M122,100 l5,-6 M140,110 l5,-6" stroke="#4aa85a" stroke-width="4"/>'
           + ell(62, 110, 7, 4, '#e0452f', -10))
    return bowl('#d99b3f', mid, top)


def d_shengjian():
    inner = ('<ellipse cx="100" cy="146" rx="60" ry="20" fill="#d99a3d"/>'
             '<path d="M44,140 Q44,66 100,66 Q156,66 156,140 Z" fill="#fbf6ee"/>'
             '<g stroke="#e3d6c2" stroke-width="3" fill="none">'
             '<path d="M100,70 l0,16 M78,76 l8,14 M122,76 l-8,14 M62,92 l12,10 M138,92 l-12,10"/></g>'
             '<circle cx="100" cy="68" r="6" fill="#f0e4d2"/>'
             + '<g stroke="none">' + ''.join(dot(x, y, 2.6, '#f6ead0') for x, y in
             [(84, 74), (100, 72), (116, 74), (92, 80), (108, 80)])
             + ''.join(dot(x, y, 3, '#4aa85a') for x, y in [(80, 84), (120, 84)]) + '</g>'
             + face(100, 112))
    return svg(inner)


def d_chou():
    inner = ('<rect x="60" y="78" width="58" height="58" rx="10" fill="#3a3a3a" transform="rotate(-7 89 107)"/>'
             '<rect x="86" y="66" width="58" height="58" rx="10" fill="#333333" transform="rotate(6 115 95)"/>'
             '<rect x="48" y="98" width="100" height="70" rx="12" fill="#262626"/>'
             '<rect x="48" y="98" width="100" height="14" rx="7" fill="#4a4038"/>'
             + ell(72, 120, 8, 5, '#d23b2a', 15) + ell(128, 118, 8, 5, '#d23b2a', -12)
             + '<g stroke="none">' + dot(66, 108, 3, '#4aa85a') + dot(136, 108, 3, '#4aa85a') + dot(100, 106, 3, '#4aa85a') + '</g>'
             + face(100, 138, dark=False))
    return svg(inner)


def d_chuan():
    chunks = [(66, 134, '#a8502f'), (88, 112, '#e6c39a'), (110, 90, '#a8502f'), (132, 68, '#e6c39a')]
    s = ('<line x1="40" y1="160" x2="158" y2="42" stroke="#caa06a" stroke-width="6"/>')
    for (cx, cy, col) in chunks:
        s += f'<rect x="{cx-18}" y="{cy-15}" width="36" height="30" rx="9" fill="{col}" transform="rotate(-44 {cx} {cy})"/>'
    s += '<g stroke="none">' + ''.join(dot(x, y, 2.2, '#f3e2b0') for x, y in
         [(62, 130), (72, 138), (108, 86), (114, 94), (86, 108), (130, 64)]) + '</g>'
    s += '<g stroke="none">' + dot(106, 88, 3.4, '#4a3320') + dot(115, 92, 3.4, '#4a3320') + '</g>'
    s += '<path d="M100,98 q6,6 12,0" stroke="#4a3320" stroke-width="3" fill="none"/>'
    return svg(s)


def d_shandong():
    inner = ('<rect x="34" y="84" width="132" height="56" rx="28" fill="#ecc978"/>'
             '<ellipse cx="48" cy="112" rx="16" ry="26" fill="#f3dc9e"/>'
             '<g fill="none" stroke="#d9b25e" stroke-width="3.5">'
             '<path d="M48,96 a16,26 0 0,0 0,32 M48,101 a11,20 0 0,0 0,22 M48,107 a6,13 0 0,0 0,10"/></g>'
             '<rect x="60" y="100" width="92" height="12" rx="6" fill="#7ec24a"/>'
             '<rect x="120" y="96" width="30" height="10" rx="5" fill="#f6f1e2" transform="rotate(-8 135 101)"/>'
             + face(112, 118))
    return svg(inner)


def d_lengmian():
    inner = ('<ellipse cx="100" cy="112" rx="80" ry="54" fill="#e7b34d"/>'
             '<ellipse cx="100" cy="106" rx="64" ry="40" fill="#f0c663"/>'
             '<g fill="none" stroke="#b9762e" stroke-width="4">'
             '<path d="M52,96 h40 M60,112 h48 M54,128 h34"/></g>'
             '<ellipse cx="132" cy="96" rx="20" ry="12" fill="#ffe98a" transform="rotate(-12 132 96)"/>'
             '<rect x="112" y="120" width="46" height="15" rx="7" fill="#c8482f" transform="rotate(-14 135 127)"/>'
             '<g stroke="none">' + ''.join(dot(x, y, 3, '#4aa85a') for x, y in
             [(74, 100), (96, 118), (120, 110), (84, 132), (138, 118)]) + '</g>'
             + face(96, 122))
    return svg(inner)


def d_yaxue():
    mid = noodles('#eef0f4', ys=(103, 109, 115), w=3.5)
    top = (('<rect x="64" y="100" width="18" height="16" rx="4" fill="#a8462f"/>'
            '<rect x="114" y="101" width="18" height="16" rx="4" fill="#96402b"/>'
            '<rect x="90" y="105" width="15" height="13" rx="4" fill="#b0533a"/>')
           + '<path d="M70,96 l5,-6 M126,98 l5,-6 M100,96 l5,-6" stroke="#4aa85a" stroke-width="4"/>'
           + dot(60, 112, 3.5, '#4aa85a') + dot(142, 110, 3.5, '#4aa85a'))
    return bowl('#f0e6d2', mid, top)


def d_daoxiao():
    mid = ('<g fill="none" stroke="#f4d789" stroke-width="9">'
           '<path d="M52,100 q24,-12 48,0 t48,0"/>'
           '<path d="M46,114 q24,-12 48,0 t52,0"/></g>')
    top = (dot(70, 104, 7, '#e0523c') + dot(128, 110, 6, '#f6f1e2')
           + '<path d="M86,96 q12,-10 24,0 M110,100 q12,-10 24,0" stroke="#4aa85a" stroke-width="4" fill="none"/>'
           + dot(100, 116, 5, '#f3e2b0') + dot(60, 110, 4, '#4aa85a') + dot(142, 104, 4, '#4aa85a'))
    return bowl('#eccf86', mid, top)


def d_hula():
    mid = ('<g stroke="none">'
           + ell(78, 108, 10, 6, '#7a5230') + ell(120, 110, 9, 6, '#8a5e38')
           + '<rect x="96" y="100" width="14" height="12" rx="3" fill="#e9dcc0"/>'
           + '<rect x="66" y="100" width="12" height="12" rx="3" fill="#f3ead2"/>'
           + dot(132, 104, 6, '#9c6b3e') + '<path d="M56,112 q10,-6 20,0 M108,114 q10,-6 20,0" stroke="#4a3a28" stroke-width="3.5" fill="none"/>'
           + '<path d="M84,104 l5,-6 M126,100 l5,-6" stroke="#4aa85a" stroke-width="4"/>'
           + '</g>')
    return bowl('#7b4a2b', mid, '', use_steam=True)


def d_yanshui():
    # 盘子 + 几片切肉 + 一只整鸭（带鸭头与萌脸）
    slices = (ell(60, 132, 15, 9, '#efe6d0', -10) + ell(60, 128, 12, 6, '#fbf4e4', -10)
              + ell(78, 138, 15, 9, '#efe6d0', 6) + ell(78, 134, 12, 6, '#fbf4e4', 6))
    inner = ('<ellipse cx="100" cy="152" rx="84" ry="18" fill="#eceef2"/>'
             + slices
             + '<path d="M52,146 q26,-12 50,-4" stroke="#5aa84f" stroke-width="6" fill="none"/>'
             # 鸭身
             + '<path d="M88,150 C86,118 110,106 132,112 C150,117 156,134 146,146 C132,156 102,158 88,150 Z" fill="#e8d3ad"/>'
             + '<path d="M100,146 C104,128 124,120 140,126 C148,134 146,144 136,148 C122,152 106,152 100,146 Z" fill="#f7ecd2"/>'
             + '<path d="M140,112 C150,96 152,80 142,72 C132,66 120,74 120,88 C120,98 128,102 132,104" fill="#efe1bd"/>'
             + '<path d="M118,86 l-12,3 11,7 Z" fill="#f0b42e"/>'
             + dot(130, 84, 3.6, '#4a3320')
             + '<ellipse cx="123" cy="91" rx="5" ry="3" fill="#ff9fb0" opacity="0.55" stroke="none"/>'
             + '<path d="M125,92 q3,3 7,1" stroke="#4a3320" stroke-width="2.6" fill="none"/>')
    return svg(inner)


def d_huoguo():
    inner = (steam()
             + '<circle cx="26" cy="118" r="9" fill="#6b7280"/><circle cx="174" cy="118" r="9" fill="#6b7280"/>'
             '<rect x="30" y="100" width="140" height="72" rx="24" fill="#6b7280"/>'
             '<path d="M30,118 a70,20 0 0,0 140,0 l0,8 a70,20 0 0,1 -140,0 Z" fill="#5b6270"/>'
             '<path d="M32,110 a68,18 0 0,1 136,0 l0,4 a68,18 0 0,1 -136,0 Z" fill="#d94a38"/>'
             '<path d="M100,94 a34,18 0 0,1 66,4 l-66,0 Z" fill="#f3e6c8"/>'
             '<line x1="100" y1="94" x2="100" y2="128"/>'
             + '<g stroke="none">'
             + dot(58, 108, 5, '#7a4a2b') + dot(80, 112, 5, '#f3e2b0') + dot(70, 116, 4, '#4aa85a')
             + dot(124, 104, 5, '#e0452f') + dot(142, 110, 5, '#fbf6e9') + dot(130, 116, 4, '#4aa85a')
             + '</g>'
             + face(100, 152, dark=False))
    return svg(inner)


def d_roujiamo():
    # 肉夹馍：白吉馍夹腊汁肉与生菜
    inner = ('<path d="M36,146 C36,116 52,104 100,104 C148,104 164,116 164,146 Z" fill="#f0d39c"/>'
             '<path d="M44,116 q56,-18 112,0 l-9,22 q-47,-13 -94,0 Z" fill="#7d4326"/>'
             '<g stroke="none">'
             + ell(72, 120, 10, 6, '#9a5a36', -12) + ell(104, 116, 11, 6, '#96552f', 8)
             + ell(132, 121, 10, 6, '#9a5a36', -6)
             + dot(88, 128, 3.4, '#c98a5a') + dot(120, 129, 3.4, '#c98a5a') + '</g>'
             '<path d="M42,112 q14,-13 28,0 t28,0 t28,0 t30,0" fill="none" stroke="#5aa84f" stroke-width="9"/>'
             '<path d="M42,108 C42,66 66,56 100,56 C134,56 158,66 158,108 Z" fill="#f6e2b4"/>'
             '<g stroke="none">'
             + ell(66, 86, 8, 5, '#e0b878', -18) + ell(132, 92, 7, 4, '#e0b878', 14)
             + ell(80, 70, 6, 4, '#e8c48c', 10)
             + ''.join(dot(x, y, 2.6, '#fff6e0') for x, y in
                       [(80, 80), (96, 72), (112, 76), (126, 82), (70, 98), (132, 100), (100, 64)])
             + '</g>'
             + face(100, 92))
    return svg(inner)


FILES = {
    'lanzhou_niurou_noodle': d_lanzhou,
    'roujiamo': d_roujiamo,
    'chongqing_xiaomian': d_xiaomian,
    'luosifen': d_luosifen,
    'reganmian': d_regan,
    'zhajiangmian': d_zhajiang,
    'jianbing_guozi': d_jianbing,
    'changfen': d_changfen,
    'guoqiao_mixian': d_guoqiao,
    'dandan_noodle': d_dandan,
    'shengjianbao': d_shengjian,
    'choudoufu': d_chou,
    'yangrou_chuan': d_chuan,
    'shandong_jianbing': d_shandong,
    'kao_lengmian': d_lengmian,
    'yaxue_fensi': d_yaxue,
    'daoxiaomian': d_daoxiao,
    'hulatang': d_hula,
    'yanshuiya': d_yanshui,
    'chongqing_huoguo': d_huoguo,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in FILES.items():
        with open(os.path.join(OUT, name + '.svg'), 'w', encoding='utf-8') as f:
            f.write(svg(fn()))
    print('generated', len(FILES), 'svg ->', os.path.normpath(OUT))


if __name__ == '__main__':
    main()
