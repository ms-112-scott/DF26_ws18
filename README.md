# Python 基礎與機器學習教學課程

一套以繁體中文撰寫、完全自足的教學教材，涵蓋 Python 基礎、機器學習，以及整合範例。

## 關於本專案

本專案為 **DigitalFUTURES 2026 Workshop 18** 教學教材：

> **台灣陽明交通大學 ｜ 循環城市 AI——利益相關者到城市形態的雙向映射**

工作坊資訊：<https://mp.weixin.qq.com/s/PkTth3sbP-5PDIFz-uRMLQ>

## 專案結構

```
python_basics_course/
├── 00_workflow/            整合範例：用真實資料把多概念串成完整流程
├── 01_py基礎教學/          Python 基礎主課程（12 本 notebook）
├── 02_機器學習教學/        機器學習進階軌（13 本 notebook）
├── requirements.txt        Python 套件鎖定清單（pip freeze）
└── README.md               本檔
```

學習建議順序：先學 `01_py基礎教學` 打底，再進 `02_機器學習教學`；`00_workflow` 是把多概念整合的示範，適合學完基礎後回顧。

---

## 00_workflow — 整合範例

用真實資料、把前面學到的多個概念串成一條完整流程的示範筆記本。三本循序漸進：

| 檔案                       | 主題                                                           |
| -------------------------- | -------------------------------------------------------------- |
| `01_Python_基礎入門.ipynb` | Python 基礎 + 資料處理（import / pandas / numpy / matplotlib） |
| `02_ML_教學.ipynb`         | class / nn.Module / 訓練迴圈                                   |
| `03_PCA_AE_VAE_教學.ipynb` | PCA / AE / VAE 三種壓縮法的概念與視覺化                        |

`_build_notebook.py` 為產生這些範例的輔助腳本。

---

## 01_py基礎教學 — Python 基礎主課程

12 本 notebook，由語法 → 科學運算 → 製圖 → 領域庫，逐步推進。

| #    | 主題                    | #    | 主題                    |
| ---- | ----------------------- | ---- | ----------------------- |
| PY01 | 核心語法                | PY07 | matplotlib 製圖（進階） |
| PY02 | 資料結構與推導式        | PY08 | 物件導向 OOP            |
| PY03 | 函式與程式組織          | PY09 | 例外與檔案 I/O          |
| PY04 | NumPy 數值運算          | PY10 | 命令列 CLI              |
| PY05 | pandas 表格資料         | PY11 | 地理空間與圖論          |
| PY06 | matplotlib 製圖（基礎） | PY12 | Web / API / 文件工具    |

---

## 02\_機器學習教學 — 機器學習進階軌

13 本 notebook（ML00–ML12），從機器學習總覽到生成模型。

| #    | 主題                    | #    | 主題                 |
| ---- | ----------------------- | ---- | -------------------- |
| ML00 | 機器學習總覽            | ML07 | 第一個神經網路 MLP   |
| ML01 | 資料與張量基礎          | ML08 | 訓練的藝術           |
| ML02 | 線性迴歸與梯度下降      | ML09 | CNN 卷積神經網路     |
| ML03 | 邏輯迴歸與分類          | ML10 | Autoencoder 自編碼器 |
| ML04 | PCA 降維                | ML11 | VAE 變分自編碼器     |
| ML05 | KMeans 分群             | ML12 | 進階選修：表徵與生成 |
| ML06 | PyTorch 張量與 autograd |      |                      |

---

## 環境設定

所有 notebook 需要 Python 環境與套件。

```bash
# 建立虛擬環境
python -m venv .venv

# 啟用（Windows PowerShell）
.venv\Scripts\Activate.ps1
# 啟用（macOS / Linux）
source .venv/bin/activate

# 安裝套件
pip install -r requirements.txt
```

主要套件：numpy、pandas、matplotlib、scipy、scikit-learn、torch / torchvision、shapely、geopandas、osmnx、networkx、requests、pillow、jupyter。

用 JupyterLab / Jupyter Notebook 或 VS Code 開啟 `.ipynb` 即可逐格執行。
