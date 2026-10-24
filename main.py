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

    result_labels = {}

    area_input = ft.TextField(
        label="输入截面积 (mm²)", 
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: calculate(),
        height=42
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

    async def copy_result(e, mat):
        val = result_labels[mat].value
        if val and val != "0.000":
            try:
                await page.set_clipboard(val)
            except Exception:
                pass
            btn = e.control
            btn.text = "已复制"
            page.update()
            await asyncio.sleep(0.8)
            btn.text = "复制"
            page.update()

    col_width = 70
    row_height = 40
    gap = 6
    
    # 1. 表头：高度死锁，绝对不会拉伸爆满
    header_row = ft.Row(
        controls=[
            ft.Container(
                content=ft.Row([ft.Text("材料", weight=ft.FontWeight.BOLD, size=15)], alignment=ft.MainAxisAlignment.CENTER), 
                width=col_width, height=row_height, bgcolor="grey300", border_radius=4
            ),
            ft.Container(
                content=ft.Row([ft.Text("米重", weight=ft.FontWeight.BOLD, size=15)], alignment=ft.MainAxisAlignment.CENTER), 
                width=col_width, height=row_height, bgcolor="grey300", border_radius=4
            ),
            ft.Container(
                content=ft.Row([ft.Text("单位", weight=ft.FontWeight.BOLD, size=15)], alignment=ft.MainAxisAlignment.CENTER), 
                width=col_width, height=row_height, bgcolor="grey300", border_radius=4
            ),
            ft.Container(
                content=ft.Row([ft.Text("操作", weight=ft.FontWeight.BOLD, size=15)], alignment=ft.MainAxisAlignment.CENTER), 
                width=col_width, height=row_height, bgcolor="grey300", border_radius=4
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=gap
    )

    table_rows = [header_row]

    # 2. 数据行：同样高度死锁
    for mat in densities.keys():
        lbl = ft.Text("0.000", size=20, weight=ft.FontWeight.BOLD, color="red")
        result_labels[mat] = lbl
        
        btn = ft.TextButton("复制", height=30, on_click=lambda e, m=mat: copy_result(e, m))
        
        row = ft.Row([
            ft.Container(content=ft.Row([ft.Text(mat, size=20, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER), width=col_width, height=row_height),
            ft.Container(content=ft.Row([lbl], alignment=ft.MainAxisAlignment.CENTER), width=col_width, height=row_height),
            ft.Container(content=ft.Row([ft.Text("KG/M", size=15, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER), width=col_width, height=row_height),
            ft.Container(content=ft.Row([btn], alignment=ft.MainAxisAlignment.CENTER), width=col_width, height=row_height)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=gap)
        
        table_rows.append(row)

    # 3. 外框
    table_column = ft.Column(table_rows, spacing=8) 
    
    framed_table = ft.Container(
        content=table_column,
        border=ft.Border(
            top=ft.BorderSide(1.5, "black"),
            bottom=ft.BorderSide(1.5, "black"),
            left=ft.BorderSide(1.5, "black"),
            right=ft.BorderSide(1.5, "black")
        ),
        border_radius=8,
        padding=10
    )

    # 4. 页面组装
    page.add(
        ft.Column([
            ft.Container(height=15),
            ft.Row([ft.Text("米重换算", size=24, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.Container(content=area_input, width=220),
                ft.TextButton("粘贴", on_click=paste_area, height=32)
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=10),
            framed_table
        ])
    )

ft.run(main)
