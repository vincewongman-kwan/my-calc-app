import flet as ft
import asyncio

# 材料密度
densities = {
    '铝': 2.71, '钢': 7.85, '铁': 7.87, 
    '金': 19.32, '银': 10.49, '铜': 8.96
}

async def main(page: ft.Page):
    page.title = "米重换算"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 15

    result_labels = {}

    area_input = ft.TextField(
        label="输入截面积 (mm²)", 
        keyboard_type=ft.KeyboardType.NUMBER,
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
            try:
                await page.set_clipboard(val)
            except Exception:
                pass
            btn.text = "已复制"
            btn.bgcolor = "green"
            page.update()
            await asyncio.sleep(0.8)
            btn.text = "复制"
            btn.bgcolor = ft.Colors.TRANSPARENT
            page.update()

    # 统一参数
    col_width = 70
    row_spacing = 10

    # 构建表格行
    table_rows = []

    # 1. 表头（分离的灰底色块，带圆角，使用 "center" 防报错）
    header_row = ft.Row(
        controls=[
            ft.Container(content=ft.Text("材料", weight=ft.FontWeight.BOLD), width=col_width, bgcolor="grey200", padding=10, alignment="center", border_radius=4),
            ft.Container(content=ft.Text("米重", weight=ft.FontWeight.BOLD), width=col_width, bgcolor="grey200", padding=10, alignment="center", border_radius=4),
            ft.Container(content=ft.Text("单位", weight=ft.FontWeight.BOLD), width=col_width, bgcolor="grey200", padding=10, alignment="center", border_radius=4),
            ft.Container(content=ft.Text("操作", weight=ft.FontWeight.BOLD), width=col_width, bgcolor="grey200", padding=10, alignment="center", border_radius=4),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=row_spacing
    )
    table_rows.append(header_row)
    table_rows.append(ft.Container(height=10)) # 表头和数据之间的额外留白

    # 2. 数据行（无横线，靠间距分开，所有文字居中对齐）
    for mat in densities.keys():
        lbl = ft.Text("0.000", size=20, weight=ft.FontWeight.BOLD, color="red", width=col_width, text_align="center")
        result_labels[mat] = lbl
        
        btn = ft.Button("复制", bgcolor=ft.Colors.TRANSPARENT)
        btn.on_click = lambda e, m=mat, b=btn: copy_result(e, m, b)
        
        row = ft.Row([
            ft.Text(mat, size=20, weight=ft.FontWeight.BOLD, width=col_width, text_align="center"),
            lbl,
            ft.Text("KG/M", size=16, weight=ft.FontWeight.BOLD, width=col_width, text_align="center"),
            ft.Container(content=btn, width=col_width, alignment="center")
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=row_spacing)
        
        table_rows.append(row)

    # 3. 套上外黑框（使用绝对不报错的 ft.Border 手写四边）
    table_column = ft.Column(table_rows, spacing=15) 
    
    framed_table = ft.Container(
        content=table_column,
        border=ft.Border(
            top=ft.BorderSide(1.5, "black"),
            bottom=ft.BorderSide(1.5, "black"),
            left=ft.BorderSide(1.5, "black"),
            right=ft.BorderSide(1.5, "black")
        ),
        border_radius=10,                   
        padding=20                          
    )

    items = [
        ft.Row([ft.Text("米重换算", size=26, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([
            ft.Container(content=area_input, width=220),
            ft.Button("粘贴", on_click=paste_area)
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=10), # 透明留白
        framed_table
    ]

    page.add(ft.Column(items, scroll=ft.ScrollMode.AUTO))

ft.run(main)
