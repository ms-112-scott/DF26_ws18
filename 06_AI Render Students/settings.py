# settings.py —— 07 的总开关(学生主要改这里)。命名为 settings 而非 config,避免和 05 的 config.py 撞名。
# ===========================================================================
# 07 = 把 05 算出来的「权力 → 形态」体块,变成 AI 渲染影像 + 过渡动画。
# 它**依赖 05**:数据、引擎、权力体制都从隔壁 05 文件夹读,不重复一份。
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS05 = HERE.parent / "05_Shanghai Power to Form Students"   # 依赖:05 的数据/引擎/regimes.yaml

SLUG = "lujiazui"     # ✏️ 用哪个站点(05 随包 9 街道之一):lujiazui / caoyang / yuyuan / waitan ...

# build_canvas.py / 批量出图默认跑这几个站点(不带参数时)。单站:python3 build_canvas.py caoyang
REPORT_SITES = ["lujiazui", "caoyang", "yuyuan"]

# 要渲染/比较的权力体制(05 regimes.yaml 里的 key + current 基线)。
# 注:用 05 的**算子体制**(regimes.yaml,形态差异大、利于出图),不是只调高度的 power_scenarios。
REGIMES = ["current", "developer_led", "state_led", "resident_self_build", "shared"]

# AI 图像模型(Replicate 上的「1 张参考图 + 文字 → 图」模型)。
#   google/nano-banana    = Gemini Flash Image,"保结构改外观"目前最稳(默认)
#   black-forest-labs/flux-kontext  = 备选,图+文编辑、保构图
MODEL = "google/nano-banana"

# 固定机位(动画里**唯一不变**的东西 → 让画面里动起来的只有形态 = 纯权力信号)。
CAM = {"elev": 34, "azim": -58}

# 出图清晰度等(体块参考图)
MASSING_DPI = 140
