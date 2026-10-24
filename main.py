import flet as ft
import asyncio

# 材料密度
densities = {
    '铝': 2.71, '钢': 7.85, '铁': 7.87, 
    '金': 19.32, '银': 10.49, '铜': 8.96
}

# 统一定义黑线边框
BLACK_BORDER = ft.Border(
    top=ft.BorderSide(1, "black"),
    bottom=ft.BorderSide(1, "black"),
    left=ft.BorderSide(1, "black"),
    right=ft.BorderSide(1, "black")
)

async def main(page: ft.Page):
    page.title = "米重换算"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(font_family="Microsoft YaHei")

    result_labels = {}

    # ================= 1. 顶部输入区 =================
    area_input = ft.TextField(
        label="输入截面积 (mm²)", 
        keyboard_type=ft.KeyboardType.NUMBER,
        text_size=18,
        text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        on_change=lambda e: calculate()
    )

    async def paste_area(e):
        try:
            text = await page.get_clipboard()
            if text:
                clean_text = ''.join(c for c in text if c.isdigit() or c == '.')
                if clean_text:
                    area_input.value = clean_text
                    calculate()
        except Exception:
            pass

    def calculate():
        val = area_input.value
        try:
            area = float(val)
            for mat, density in densities.items():
                weight = (area * density) / 1000
                result_labels[mat].value = f"{weight:.3f}"
        except (ValueError, TypeError):
            for mat in densities.keys():
                result_labels[mat].value = "0.000"
        page.update()

    async def copy_result(e, mat, btn):
        val = result_labels[mat].value
        if val and val != "0.000":
            await page.set_clipboard(val)
            btn.text = "已复制"
            btn.bgcolor = ft.Colors.GREEN
            btn.color = ft.Colors.WHITE
            page.update()
            await asyncio.sleep(0.8)
            btn.text = "复制"
            btn.bgcolor = ft.Colors.TRANSPARENT
            btn.color = ft.Colors.BLACK
            page.update()

    # ================= 2. 构建表格 =================
    
    # --- 输入框行 ---
    input_row = ft.Row(
        controls=[
            ft.Container(content=area_input, expand=True, padding=5),
            ft.Container(
                content=ft.Button("粘贴", on_click=paste_area, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4))),
                padding=5
            )
        ]
    )

    # --- 表头行 ---
    def make_header_cell(text, expand_val=False):
        return ft.Container(
            content=ft.Text(text, size=16, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            padding=10,
            bgcolor=ft.Colors.GREY_200,
            border=ft.Border(bottom=ft.BorderSide(1, "black"), right=ft.BorderSide(1, "black")),
            expand=expand_val
        )

    header_row = ft.Row(
        controls=[
            make_header_cell("材料"),
            make_header_cell("米重"),
            make_header_cell("单位"),
            ft.Container( # 最后一列去掉右边框
                content=ft.Text("操作", size=16, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center,
                padding=10,
                bgcolor=ft.Colors.GREY_200,
                border=ft.Border(bottom=ft.BorderSide(1, "black")),
            )
        ],
        spacing=0
    )

    # --- 数据行 ---
    table_rows = []
    for mat in densities.keys():
        # 数值控件
        lbl = ft.Text("0.000", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.RED)
        result_labels[mat] = lbl
        
        # 复制按钮
        btn = ft.Button(
            "复制", 
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4), padding=5)
        )
        btn.on_click = lambda e, m=mat, b=btn: copy_result(e, m, b)

        # 构建当前行
        row = ft.Row(
            controls=[
                ft.Container(content=ft.Text(mat, size=18, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center, padding=10, border=ft.Border(right=ft.BorderSide(1, "black"))),
                ft.Container(content=lbl, alignment=ft.alignment.center, padding=10, border=ft.Border(right=ft.BorderSide(1, "black"))),
                ft.Container(content=ft.Text("KG/M", size=14, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center, padding=10, border=ft.Border(right=ft.BorderSide(1, "black"))),
                ft.Container(content=btn, alignment=ft.alignment.center, padding=10)
            ],
            spacing=0 # 确保没有默认间距，完美拼合边框
        )
        
        # 每一行底部加黑线（最后一行通常不需要，但加上更像格子）
        row_container = ft.Container(
            content=row,
            border=ft.Border(bottom=ft.BorderSide(1, "black")) if mat != '铜' else None
        )
        table_rows.append(row_container)

    # --- 整个表格的外框 ---
    table_card = ft.Container(
        content=ft.Column(
            controls=[
                header_row,
                *table_rows
            ],
            spacing=0
        ),
        border=BLACK_BORDER,
        border_radius=8,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS # 让圆角更平滑
    )

    # ================= 3. 组装页面 =================
    page.add(
        ft.Text("米重换算", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        input_row,
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        table_card
    )

ft.run(main)
