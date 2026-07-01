"""
plots/_base.py — 绘图共用核心(view 层 DRY)
=================================================================
这里只放「画图」会重复用到的东西:角色调色盘、footprint 著色、存档、
高度色阶、3D 几何面、图例摆放。算资料是 model(common.py)的事,这里不算。

设计:
  - common.py = model(载资料 / 贴角色 / 算高度 / 挤 OBJ),不碰 matplotlib。
  - plots/    = view(画),只收「已算好的」df / heights / scenarios。
  - 不在这里强制 matplotlib 后端 → notebook 用 inline、steps/*.py 在 __main__ 设 Agg。
"""
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np
import common  # model 契约(STAKEHOLDERS / FLOOR_H / _polys / OUT / ROOT / honest_note + 字型设置)

# 中文字型:用 common 的「**先确认存在再选**」逻辑(避免变成豆腐方块)
common._set_cjk_font()


# ---- 自动存图(view 层唯一存图出口):每个 plots.* 都把图落盘,学生不用逐张存 --------------
# 一次 run 开一个 timestamp 夹;所有图归在 out/<slug>/Step_<num>/<timestamp>/NN_name.png。
# 预设关闭 → 单跑脚本(走自己的 save_fig)不受影响;notebook 在 setup 呼叫 capture() 才开。
_CAPTURE = {"on": False, "num": None, "slug": None, "stamp": None, "seq": 0}


def capture(num, slug=None):
    """开启自动存图。num = notebook 前缀(如 '03')。slug 留空 = 存档当下的 config.SLUG
    (这样 05 换街道后,图会跟著存到新 slug 夹)。回传这次 run 的 timestamp 字串。"""
    _CAPTURE.update(on=True, num=str(num), slug=slug,
                    stamp=datetime.now().strftime("%Y%m%d_%H%M%S"), seq=0)
    return _CAPTURE["stamp"]


def autosave(fig, name):
    """capture() 开了才动作:把 fig 存成 out/<slug>/Step_<num>/<timestamp>/NN_name.png。
    slug 在存档当下取(config.SLUG 变了也跟著走);seq 自动编号、把同一 run 的图排序。"""
    if not _CAPTURE["on"] or fig is None:
        return None
    import config
    slug = _CAPTURE["slug"] or config.SLUG
    d = common.OUT / slug / ("Step_%s" % _CAPTURE["num"]) / _CAPTURE["stamp"]
    d.mkdir(parents=True, exist_ok=True)
    _CAPTURE["seq"] += 1
    p = d / ("%02d_%s.png" % (_CAPTURE["seq"], name))
    fig.savefig(p, dpi=120, bbox_inches="tight", pad_inches=0.083)   # 四周固定 ~10px padding
    print("  -> saved", p.relative_to(common.ROOT))
    return p

# ---- 角色调色盘(view):从 common 取(单一真相源,简体)-----------------------
SH_COLOR = common.SH_COLOR
SH_LABEL = common.SH_LABEL

HEIGHT_CMAP = plt.get_cmap("viridis")   # 高度色阶:低=深紫、高=黄,所有图共用可横比


# ---- footprint 著色(step1/2/4 共用):用 common 的批量版(快)-----------------
plot_footprints = common.plot_footprints


def legend_below(ax, handles, labels, ncol=None, fontsize=8):
    """图例放座标轴下方一排,不盖资料。"""
    ax.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, -0.04),
              ncol=ncol or len(labels), fontsize=fontsize, frameon=False)


def height_norm(*height_series):
    """跨多个情景共用的高度 Normalize(同色阶才能横向比对)。"""
    allh = np.concatenate([h.values for h in height_series])
    return Normalize(vmin=float(allh.min()), vmax=float(allh.max()))


def data_aspect(df_or_recs):
    """footprint 整体的 高/宽 比(dh/dw)。用来把 figure 尺寸配到内容,消掉等比留白。"""
    rows = (r for _, r in df_or_recs.iterrows()) if hasattr(df_or_recs, "iterrows") else iter(df_or_recs)
    x0 = y0 = float("inf"); x1 = y1 = float("-inf")
    for r in rows:
        for p in common._polys(r["geom"]):
            bx0, by0, bx1, by1 = p.bounds
            x0 = min(x0, bx0); y0 = min(y0, by0); x1 = max(x1, bx1); y1 = max(y1, by1)
    dw, dh = x1 - x0, y1 - y0
    return (dh / dw) if dw > 0 else 1.0


def panel_grid(ncols, nrows, aspect, *, panel_w=4.6, title_in=0.55, footer_in=0.36,
               left_in=0.16, right_in=0.16, top_in=0.14, wspace_in=0.28, hspace_in=0.62,
               cbar=False, cbar_w_in=0.16, cbar_gap_in=0.20, cbar_label_in=0.62):
    """等比 footprint 面板专用:figure 尺寸从 data aspect 反推,让每个 panel 刚好填满格子
    (不再等比缩水置中 → 消掉上/下留白);colorbar 高度 = 整个 axes 区高度 = 与 subplots 同高。
    回传 (fig, axes(list, 长度 ncols*nrows), cax 或 None)。单位都是英寸,再换算成 figure 分数。"""
    ph = panel_w * aspect                                    # 单一 panel 内容高(英寸)
    axes_w = ncols * panel_w + (ncols - 1) * wspace_in
    axes_h = nrows * ph + (nrows - 1) * hspace_in
    cbar_block = (cbar_gap_in + cbar_w_in + cbar_label_in) if cbar else 0.0
    fig_w = left_in + axes_w + right_in + cbar_block
    fig_h = top_in + title_in + axes_h + footer_in
    fig = plt.figure(figsize=(fig_w, fig_h))
    L = left_in / fig_w; R = (left_in + axes_w) / fig_w
    B = footer_in / fig_h; T = (footer_in + axes_h) / fig_h
    gs = fig.add_gridspec(nrows, ncols, left=L, right=R, bottom=B, top=T,
                          wspace=wspace_in / panel_w, hspace=hspace_in / ph)
    axes = [fig.add_subplot(gs[i // ncols, i % ncols]) for i in range(nrows * ncols)]
    cax = None
    if cbar:
        cx = (left_in + axes_w + cbar_gap_in) / fig_w
        cax = fig.add_axes([cx, B, cbar_w_in / fig_w, T - B])   # 高度 = T-B = axes 区全高
    return fig, axes, cax


def footer(fig, note=None, y=-0.02):
    """已停用:所有图都不显示最下一行灰色小字(诚实说明)。保留签名让呼叫端不用改。"""
    return


def save_fig(fig, name, dpi=120):
    """存图到 out/ 并关闭(headless steps 用)。"""
    p = common.OUT / name
    fig.savefig(p, dpi=dpi, bbox_inches="tight", pad_inches=0.083); plt.close(fig)
    print("  -> wrote", p.relative_to(common.ROOT)); return p


# ---- 3D 几何(step5 的 mpl 与 plotly 前处理共用)---------------------------
def origin_of(df):
    """整批楼的左下角(UTM 公尺座标很大,平移到原点附近好画)。"""
    ox = min(p.bounds[0] for g in df["geom"] for p in common._polys(g))
    oy = min(p.bounds[1] for g in df["geom"] for p in common._polys(g))
    return ox, oy


def building_faces(geom, h, ox, oy):
    """footprint → 3D 面:四周的墙 + 一个顶盖(近似:外环当一面)。"""
    faces = []
    for poly in common._polys(geom):
        ring = list(poly.exterior.coords)
        if len(ring) > 1 and ring[0] == ring[-1]:
            ring = ring[:-1]                       # 去掉重复的闭合点
        for i in range(len(ring)):                 # 每条边长出一面墙
            j = (i + 1) % len(ring)
            x0, y0 = ring[i]; x1, y1 = ring[j]
            faces.append([(x0 - ox, y0 - oy, 0), (x1 - ox, y1 - oy, 0),
                          (x1 - ox, y1 - oy, h), (x0 - ox, y0 - oy, h)])
        faces.append([(x - ox, y - oy, h) for (x, y) in ring])   # 顶盖
    return faces
