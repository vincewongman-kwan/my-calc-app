import tkinter as tk
import tkinter.font as tkfont
import json
import os

# ================= 数据配置 =================
# 材料密度 (g/cm³)
densities = {
    'Al': 2.71,
    'Steel': 7.85,
    'Iron': 7.87,
    'Gold': 19.32,
    'Silver': 10.49,
    'Copper': 8.96
}

# 颜色与字体配置
BG_COLOR = "white"
LINE_COLOR = "black"
RED_COLOR = "#d32f2f"
BTN_BG = "#e5e5e5"
FONT_FAMILY = "微软雅黑"

# 配置文件路径（保存到当前用户的文件夹下，确保C盘没有管理员权限也能写入）
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".material_weight_config.json")

# ================= 界面初始化 =================
root = tk.Tk()
root.title("材料米重换算")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# ================= 窗口位置记忆逻辑 =================
win_width, win_height = 980, 280
default_x, default_y = 100, 100  # 默认初始位置

# 尝试读取上次保存的位置
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            default_x = config.get('x', default_x)
            default_y = config.get('y', default_y)
    except Exception:
        pass # 如果文件损坏就使用默认位置

# 设置窗口大小和位置 (格式：宽度x高度+X+Y)
root.geometry(f"{win_width}x{win_height}+{default_x}+{default_y}")

# 窗口关闭时的操作
def on_closing():
    # 获取当前窗口左上角的坐标
    x = root.winfo_x()
    y = root.winfo_y()
    # 保存到配置文件
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'x': x, 'y': y}, f)
    except Exception:
        pass
    # 销毁窗口
    root.destroy()

# 绑定窗口右上角X号的关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)

# ================= 全局字体 =================
font_title = tkfont.Font(family=FONT_FAMILY, size=16, weight="bold")
font_header = tkfont.Font(family=FONT_FAMILY, size=11, weight="bold")
font_val = tkfont.Font(family=FONT_FAMILY, size=13, weight="bold")
font_normal = tkfont.Font(family=FONT_FAMILY, size=11)

# ================= 布局框架 =================
# 使用最外层 Frame 模拟黑色表格外边框
main_frame = tk.Frame(root, bg=LINE_COLOR, bd=1)
main_frame.pack(padx=15, pady=15, fill="both", expand=True)

# 内部白色画板
table_frame = tk.Frame(main_frame, bg=BG_COLOR)
table_frame.pack(fill="both", expand=True, padx=1, pady=1)

# 配置列宽：第一列稍宽，其余等宽
table_frame.grid_columnconfigure(0, weight=2, minsize=180)
for i in range(1, 7):
    table_frame.grid_columnconfigure(i, weight=1, minsize=120)

# ================= 第一行：标题 =================
title_frame = tk.Frame(table_frame, bg=BG_COLOR)
title_frame.grid(row=0, column=0, columnspan=7, sticky="nsew", pady=(15, 15))
tk.Label(title_frame, text="材料米重换算", font=font_title, bg=BG_COLOR).pack()

# 标题下方的黑色横线
tk.Frame(table_frame, bg=LINE_COLOR, height=1).grid(row=1, column=0, columnspan=7, sticky="ew")

# ================= 第二行：表头 =================
headers = ["截面积\nmm²", "铝\nKG/M", "钢\nKG/M", "铁\nKG/M", "金\nKG/M", "银\nKG/M", "铜\nKG/M"]

for i, text in enumerate(headers):
    # 每个单元格用白色 Frame 覆盖，右侧留出 1px 黑线（最后一列不留）
    pad_right = 1 if i < 6 else 0
    cell = tk.Frame(table_frame, bg=BG_COLOR)
    cell.grid(row=2, column=i, sticky="nsew", padx=(0, pad_right), pady=0)
    tk.Label(cell, text=text, font=font_header, bg=BG_COLOR, justify="center").pack(expand=True, pady=12)

# 表头下方的黑色横线
tk.Frame(table_frame, bg=LINE_COLOR, height=1).grid(row=3, column=0, columnspan=7, sticky="ew")

# ================= 第三行：输入与结果 =================
# 1. 截面积输入框 (带占位符功能)
input_cell = tk.Frame(table_frame, bg=BG_COLOR)
input_cell.grid(row=4, column=0, sticky="nsew", padx=(0, 1), pady=0)

entry_area = tk.Entry(input_cell, font=font_normal, justify="center", fg="gray", 
                      relief="solid", bd=1, highlightthickness=0)
entry_area.pack(padx=15, pady=10, expand=True, fill="x")
entry_area.insert(0, "输入面积")

# 2. 结果数值
res_labels = {}
materials = list(densities.keys())

for i, mat in enumerate(materials):
    pad_right = 1 if i < 5 else 0
    cell = tk.Frame(table_frame, bg=BG_COLOR)
    cell.grid(row=4, column=i+1, sticky="nsew", padx=(0, pad_right), pady=0)
    lbl = tk.Label(cell, text="0.000", font=font_val, fg=RED_COLOR, bg=BG_COLOR)
    lbl.pack(expand=True, pady=10)
    res_labels[mat] = lbl

# 输入与结果下方的黑色横线
tk.Frame(table_frame, bg=LINE_COLOR, height=1).grid(row=5, column=0, columnspan=7, sticky="ew")

# ================= 第四行：操作按钮 =================
# 1. 粘贴按钮
paste_cell = tk.Frame(table_frame, bg=BG_COLOR)
paste_cell.grid(row=6, column=0, sticky="nsew", padx=(0, 1), pady=0)
btn_paste = tk.Button(paste_cell, text="粘贴", font=font_normal, bg=BTN_BG, 
                      relief="solid", bd=1, width=8, cursor="hand2")
btn_paste.pack(pady=10)

# 2. 复制按钮
for i, mat in enumerate(materials):
    pad_right = 1 if i < 5 else 0
    cell = tk.Frame(table_frame, bg=BG_COLOR)
    cell.grid(row=6, column=i+1, sticky="nsew", padx=(0, pad_right), pady=0)
    btn = tk.Button(cell, text="复制", font=font_normal, bg=BTN_BG, 
                    relief="solid", bd=1, width=8, cursor="hand2")
    btn.pack(pady=10)

# ================= 交互逻辑 =================
def on_focus_in(event):
    if entry_area.get() == "输入面积":
        entry_area.delete(0, tk.END)
        entry_area.config(fg="black")

def on_focus_out(event):
    if entry_area.get() == "":
        entry_area.insert(0, "输入面积")
        entry_area.config(fg="gray")

def calculate(event=None):
    val = entry_area.get()
    if val == "输入面积":
        val = ""
    try:
        area = float(val)
        for mat, density in densities.items():
            weight = (area * density) / 1000
            res_labels[mat].config(text=f"{weight:.3f}")
    except ValueError:
        for mat in materials:
            res_labels[mat].config(text="0.000")

def paste_area():
    try:
        text = root.clipboard_get()
        entry_area.delete(0, tk.END)
        entry_area.insert(0, text.strip())
        entry_area.config(fg="black")
        calculate()
    except tk.TclError:
        pass

def copy_result(mat, btn):
    val = res_labels[mat].cget("text")
    if val and val != "0.000":
        root.clipboard_clear()
        root.clipboard_append(val)
        # 复制成功时的按钮视觉反馈 (变成绿色)
        original_text = btn.cget("text")
        original_bg = btn.cget("bg")
        btn.config(text="已复制", bg="#4CAF50", fg="white")
        root.after(800, lambda: btn.config(text=original_text, bg=original_bg, fg="black"))

# 绑定事件
entry_area.bind("<FocusIn>", on_focus_in)
entry_area.bind("<FocusOut>", on_focus_out)
entry_area.bind("<KeyRelease>", calculate)
btn_paste.config(command=paste_area)

# 绑定各个复制按钮
for i, mat in enumerate(materials):
    # 从 grid 布局中找到对应的按钮组件
    btn = table_frame.grid_slaves(row=6, column=i+1)[0].winfo_children()[0]
    btn.config(command=lambda m=mat, b=btn: copy_result(m, b))

root.mainloop()