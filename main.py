import flet as ft
import asyncio

densities = {
    '铝': 2.71, '钢': 7.85, '铁': 7.87, 
    '金': 19.32, '银': 10.49, '铜': 8.96
}

async def main(page: ft.Page):
    page.title = "米重换算"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 15
    page.bgcolor = "white" # 强制页面底色，防灰

    result_labels = {}

    area_input = ft.TextField(
        label="输入截面积 (mm²)", 
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: calculate(),
        height=45
    )

    async def paste_area(e):
        try:
            text = await page.get_clipboard()
            if text:
                clean_text = ''.join(c for c in str(text) if c.isdigit() or c == '.')
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

    async def copy_result(e, mat):
        val = result_labels[mat].value
        if val and val != "0.000":
            try:
                await page.set_clipboard(val)
            except Exception:
                pass

    # 尺寸死死锁定
    col_width = 70
    header_height = 40
    row_height = 40
    gap = 8 
    row_gap = 12 

    # 1. 表头：纯手工锁死尺寸的色块
    header_row = ft.Row(
        controls=[
            ft.Container(content=ft.Text("材料", weight=ft.FontWeight.BOLD, size=15), width=col_width, height=header_height, bgcolor="grey200", alignment="center", border_radius=4),
            ft.Container(content=ft.Text("米重", weight=ft.FontWeight.BOLD, size=15), width=col_width, height=header_height, bgcolor="grey200", alignment="center", border_radius=4),
            ft.Container(content=ft.Text("单位", weight=ft.FontWeight.BOLD, size=15), width=col_width, height=header_height, bgcolor="grey200", alignment="center", border_radius=4),
            ft.Container(content=ft.Text("操作", weight=ft.FontWeight.BOLD, size=15), width=col_width, height=header_height, bgcolor="grey200", alignment="center", border_radius=4),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=gap
    )
    
    table_rows = [header_row]

    # 2. 数据行：全部用官方自带按钮，放弃手工容器
    for mat in densities.keys():
        lbl = ft.Text("0.000", size=20, weight=ft.FontWeight.BOLD, color="red", text_align="center")
        result_labels[mat] = lbl
        
        # 官方按钮，带边框和浅灰底色，尺寸写死，去除了ink
        btn = ft.ElevatedButton(
            text="复制",
            width=56,
            height=28,
            style=ft.ButtonStyle(
                color="blue",
                bgcolor="#F5F5F5",
                side=ft.BorderSide(1, "grey300"),
                shape=ft.RoundedRectangleBorder(radius=15),
                padding=0
            ),
            on_click=lambda e, m=mat: copy_result(e, m)
        )
        
        row = ft.Row([
            ft.Container(content=ft.Text(mat, size=20, weight=ft.FontWeight.BOLD), width=col_width, height=row_height, alignment="center"),
            ft.Container(content=lbl, width=col_width, height=row_height, alignment="center"),
            ft.Container(content=ft.Text("KG/M", size=15, weight=ft.FontWeight.BOLD), width=col_width, height=row_height, alignment="center"),
            ft.Container(content=btn, width=col_width, height=row_height, alignment="center")
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=gap)
        
        table_rows.append(row)

    # 3. 大外框
    table_column = ft.Column(table_rows, spacing=row_gap) 
    
    framed_table = ft.Container(
        content=table_column,
        border=ft.Border(
            top=ft.BorderSide(1.5, "black"),
            bottom=ft.BorderSide(1.5, "black"),
            left=ft.BorderSide(1.5, "black"),
            right=ft.BorderSide(1.5, "black")
        ),
        border_radius=8,
        padding=15,
        bgcolor="white"
    )

    # 官方按钮
    paste_btn = ft.ElevatedButton(
        text="粘贴",
        width=56,
        height=36,
        style=ft.ButtonStyle(
            color="blue",
            bgcolor="#F5F5F5",
            side=ft.BorderSide(1, "grey300"),
            shape=ft.RoundedRectangleBorder(radius=15),
            padding=0
        ),
        on_click=paste_area
    )

    # 4. 页面组装
    page.add(
        ft.Column([
            ft.Container(height=10),
            ft.Row([ft.Text("米重换算", size=24, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=15, color="grey300", thickness=1),
            ft.Row([
                ft.Container(content=area_input, width=220),
                paste_btn
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Divider(height=20, color="grey300", thickness=1),
            framed_table
        ])
    )

ft.run(main)
