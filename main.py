import flet as ft
import asyncio

densities = {
    '铝': 2.71, '钢': 7.85, '铁': 7.87, 
    '金': 19.32, '银': 10.49, '铜': 8.96
}

async def main(page: ft.Page):
    page.title = "米重换算"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(font_family="Microsoft YaHei")

    result_labels = {}

    area_input = ft.TextField(
        label="输入截面积 (mm²)", 
        keyboard_type=ft.KeyboardType.NUMBER,
        text_size=20,
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
            original_text = btn.text
            btn.text = "已复制"
            btn.style.color = ft.Colors.WHITE
            btn.bgcolor = ft.Colors.GREEN
            page.update()
            await asyncio.sleep(0.8)
            btn.text = original_text
            btn.style.color = ft.Colors.BLACK
            btn.bgcolor = ft.Colors.TRANSPARENT
            page.update()

    table_rows = []
    table_rows.append(
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Container(content=area_input, width=220, padding=10)),
                ft.DataCell(
                    ft.Button(  # 👈 这里已改为 Button
                        "粘贴", on_click=paste_area,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), text_style=ft.TextStyle(weight=ft.FontWeight.BOLD))
                    )
                )
            ]
        )
    )

    for mat in densities.keys():
        lbl = ft.Text("0.000", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700)
        result_labels[mat] = lbl
        btn = ft.Button(  # 👈 这里也已改为 Button
            "复制", 
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), text_style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
            bgcolor=ft.Colors.TRANSPARENT, color=ft.Colors.BLACK
        )
        btn.on_click = lambda e, m=mat, b=btn: copy_result(e, m, b)
        table_rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(mat, size=20, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(lbl),
                    ft.DataCell(ft.Text("KG/M", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
                    ft.DataCell(btn)
                ]
            )
        )

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("材料", size=18, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("米重", size=18, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("单位", size=18, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("操作", size=18, weight=ft.FontWeight.BOLD)),
        ],
        rows=table_rows,
        border=ft.border.all(1, ft.Colors.BLACK),
        border_radius=10,
        horizontal_lines=ft.BorderSide(1, ft.Colors.BLACK12),
        vertical_lines=ft.BorderSide(1, ft.Colors.BLACK12),
        heading_row_color=ft.Colors.GREY_200,
        column_spacing=20,
    )

    page.add(
        ft.Text("材料米重换算", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Row([data_table], scroll=ft.ScrollMode.AUTO)
    )

ft.run(main)
