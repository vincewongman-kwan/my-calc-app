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
    page.bgcolor = "white"

    result_labels = {}

    area_input = ft.TextField(
        label="输入截面积 (mm²)", 
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: calculate(),
        height=45
    )

    async def paste_area(e):
        btn_text = e.control.content
        try:
            text = await page.get_clipboard()
            if text:
                clean_text = ''.join(c for c in str(text) if c.isdigit() or c == '.')
                if clean_text:
                    area_input.value = clean_text
                    calculate()
                    btn_text.value = "已粘贴"
                else:
                    btn_text.value = "无数字"
            else:
                btn_text.value = "空"
        except Exception:
            btn_text.value = "失败"
            
        page.update()
        await asyncio.sleep(0.8)
        btn_text.value = "粘贴"
        page.update()

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
        btn_text = e.control.content
        
        if val and val != "0.000":
            btn_text.value = "已复制"
            page.update()
            try:
                await page.set_clipboard(val)
            except Exception:
                btn_text.value = "失败"
                page.update()
            
            await asyncio.sleep(0.8)
            btn_text.value = "复制"
            page.update()

    # 绝对尺寸限制
    col_width = 70
    header_height = 40
    row_height = 40
    gap = 8 
    row_gap = 12 

    btn_border = ft.Border(
        top=ft.BorderSide(1, "grey300"),
        bottom=ft.BorderSide(1, "grey300"),
        left=ft.BorderSide(1, "grey300"),
        right=ft.BorderSide(1, "grey300")
    )

    # 👇 核心防爆修复：不用 alignment="center"，改用 Row 强制居中
    def make_header_cell(text):
        return ft.Container(
            width=col_width, 
            height=header_height, 
            bgcolor="grey200", 
            border_radius=4,
            content=ft.Row([ft.Text(text, weight=ft.FontWeight.BOLD, size=15)], alignment=ft.MainAxisAlignment.CENTER)
        )

    header_row = ft.Row(
        controls=[
            make_header_cell("材料"),
            make_header_cell("米重"),
            make_header_cell("单位"),
            make_header_cell("操作"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=gap
    )
    
    table_rows = [header_row]

    for mat in densities.keys():
        lbl = ft.Text("0.000", size=20, weight=ft.FontWeight.BOLD, color="red")
        result_labels[mat] = lbl
        
        btn = ft.Container(
            content=ft.Text("复制", color="blue", size=14),
            border=btn_border,
            border_radius=15,
            width=56,
            height=28,
            bgcolor="#F5F5F5", 
            on_click=lambda e, m=mat: copy_result(e, m),
        )
        
        # 同样不用 alignment，全部用 Row 包裹居中
        row = ft.Row([
            ft.Container(content=ft.Row([ft.Text(mat, size=20, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER), width=col_width, height=row_height),
            ft.Container(content=ft.Row([lbl], alignment=ft.MainAxisAlignment.CENTER), width=col_width, height=row_height),
            ft.Container(content=ft.Row([ft.Text("KG/M", size=15, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER), width=col_width, height=row_height),
            ft.Container(content=ft.Row([btn], alignment=ft.MainAxisAlignment.CENTER), width=col_width, height=row_height)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=gap)
        
        table_rows.append(row)

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

    paste_btn = ft.Container(
        content=ft.Text("粘贴", color="blue", size=14),
        border=btn_border,
        border_radius=15,
        width=56,
        height=36,
        bgcolor="#F5F5F5",
        on_click=paste_area,
    )

    page.add(
        ft.Column([
            ft.Container(height=10),
            ft.Row([ft.Text("米重换算", size=24, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=15, color="grey300", thickness=1),
            ft.Row([
                ft.Container(content=area_input, width=220),
                ft.Container(content=ft.Row([paste_btn], alignment=ft.MainAxisAlignment.CENTER), width=60, height=40)
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Divider(height=20, color="grey300", thickness=1),
            framed_table
        ])
    )

ft.run(main)
