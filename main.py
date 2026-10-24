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

    # 统一的提示框，保证用户看得到反馈
    def show_msg(msg):
        page.show_snack_bar(ft.SnackBar(ft.Text(msg), duration=2000))

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
                    show_msg(f"已粘贴: {clean_text}")
                else:
                    show_msg("剪贴板里没有数字")
            else:
                show_msg("剪贴板是空的")
        except Exception:
            show_msg("读取剪贴板失败，请手动输入")

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
                show_msg(f"已复制: {val}")
            except Exception:
                show_msg("复制失败，请长按数字手动复制")
        else:
            show_msg("暂无有效数字")

    # 尺寸死死锁定
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
    table_border = ft.Border(
        top=ft.BorderSide(1.5, "black"),
        bottom=ft.BorderSide(1.5, "black"),
        left=ft.BorderSide(1.5, "black"),
        right=ft.BorderSide(1.5, "black")
    )

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

    for mat in densities.keys():
        lbl = ft.Text("0.000", size=20, weight=ft.FontWeight.BOLD, color="red", text_align="center")
        result_labels[mat] = lbl
        
        # 加入 ink=True，点击时有点击水波纹效果
        btn = ft.Container(
            content=ft.Text("复制", color="blue", size=14),
            border=btn_border,
            border_radius=15,
            width=56,
            height=28,
            bgcolor="#F5F5F5",
            on_click=lambda e, m=mat: copy_result(e, m),
            alignment="center",
            ink=True 
        )
        
        row = ft.Row([
            ft.Container(content=ft.Text(mat, size=20, weight=ft.FontWeight.BOLD), width=col_width, height=row_height, alignment="center"),
            ft.Container(content=lbl, width=col_width, height=row_height, alignment="center"),
            ft.Container(content=ft.Text("KG/M", size=15, weight=ft.FontWeight.BOLD), width=col_width, height=row_height, alignment="center"),
            ft.Container(content=btn, width=col_width, height=row_height, alignment="center")
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=gap)
        
        table_rows.append(row)

    table_column = ft.Column(table_rows, spacing=row_gap) 
    
    framed_table = ft.Container(
        content=table_column,
        border=table_border,
        border_radius=8,
        padding=15
    )

    paste_btn = ft.Container(
        content=ft.Text("粘贴", color="blue", size=14),
        border=btn_border,
        border_radius=15,
        width=56,
        height=36,
        bgcolor="#F5F5F5",
        on_click=paste_area,
        alignment="center",
        ink=True
    )

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
