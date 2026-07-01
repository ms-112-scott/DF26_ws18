"""
ws05.py —— 把隔壁 05 工作坊的引擎接进来(07 不重复一份数据/算子/形态逻辑)。
=================================================================
做的事:把 05 的根目录(含 config.py)和 05/engine(含 common/operators/measure/plots)
加进 sys.path,设好 05 的 config.SLUG,再把这些模块暴露给 07 用。

为什么命名讲究:05 的 common.py 里写的是 `import config`,它要找到的是 **05 的 config.py**。
所以 07 自己的总开关命名为 `settings.py`(不是 config.py),否则会和 05 的 config 撞名。
"""
import sys
from pathlib import Path
import importlib
# 让本模块无论从 07 根(notebook)还是 engine/ 内(脚本)被导入,都找得到 07 的 settings.py
_07ROOT = Path(__file__).resolve().parent.parent
if str(_07ROOT) not in sys.path:
    sys.path.insert(0, str(_07ROOT))
import settings   # 07 的总开关(settings.py,在 07 根)

WS05 = Path(settings.WS05).resolve()
_ENGINE = WS05 / "engine"
for p in (str(WS05), str(_ENGINE)):     # 根(有 config.py)+ engine(有 common 等)都要在路径上
    if p not in sys.path:
        sys.path.insert(0, p)

import config as ws05_config            # 这是 05 的 config.py(因为 WS05 根在 path 上)
import common as C                       # 05 引擎:载缓存/贴角色/只调高度/recs桥/挤OBJ
import operators as ops                  # 05 引擎:9 算子 + 配方引擎
import measure as M                      # 05 引擎:形态指纹
import plots                             # 05 引擎:绘图(含 building_faces / city_3d)


def use_site(slug=None):
    """切到某站点(把 05 的 config.SLUG 设好,后续 C.current_buildings 就读它)。返回 slug。"""
    slug = slug or settings.SLUG
    ws05_config.SLUG = slug
    importlib.reload  # noqa(占位:提醒 config 是模块级状态)
    return slug


def load_recs(slug=None):
    """读某站点的楼 → recs 列表 [{geom,h,sh,frozen}](算子/挤体/出图的工作单位)。"""
    slug = use_site(slug)
    df = C.assign_all(C.current_buildings(slug))
    return C.to_recs(df), df


def regime_recs(slug=None, regimes=None):
    """对某站点施加各权力体制 → {regime: recs}(current = 现状基线)。"""
    regimes = regimes or settings.REGIMES
    recs, _ = load_recs(slug)
    regs = ops.load_regimes(WS05 / "regimes.yaml")
    out = {}
    for name in regimes:
        out[name] = recs if name == "current" else ops.apply_regime(recs, regs[name])
    return out, regs


def regime_label(regs, name):
    return "现状" if name == "current" else regs.get(name, {}).get("label", name)
