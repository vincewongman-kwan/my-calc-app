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
        text_size=16,
        on_change=lambda e: calculate()
    )

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

    async def copy_result(e, mat, btn):
        val = result_labels[mat].value
        if val and val != "0.000":
            await page.set_clipboard(val)
            btn.text = "已复制"
            btn.bgcolor = "green"
            btn.color = "white"
            page.update()
            await asyncio.sleep(0.8)
            btn.text = "复制"
            btn.bgcolor = ft.Colors.TRANSPARENT
            btn.color = "black"
            page.update()

    header_style = {"bgcolor": "grey200", "padding": 10}
    cell_style = {"padding": 8}

    top_row = ft.Row(
        controls=[
            ft.Container(content=area_input, expand=True),
            ft.Button("粘贴", on_click=paste_area)
        ]
    )

    header_row = ft.Row(
        controls=[
            ft.Container(content=ft.Text("材料", weight="bold"), **header_style, expand=1),
            ft.Container(content=ft.Text("米重", weight="bold"), **header_style, expand=1),
            ft.Container(content=ft.Text("单位", weight="bold"), **header_style, expand=1),
            ft.Container(content=ft.Text("操作", weight="bold"), **header_style, expand=1),
        ]
    )

    data_rows = []
    for mat, density in densities.items():
        lbl = ft.Text("0.000", size=18, weight="bold", color="red")
        result_labels[mat] = lbl
        
        btn = ft.Button("复制", style=ft.ButtonStyle(padding=5))
        btn.on_click = lambda e, m=mat, b=btn: copy_result(e, m, b)

        row = ft.Row(
            controls=[
                ft.Container(content=ft.Text(mat, size=18, weight="bold"), **cell_style, expand=1),
                ft.Container(content=lbl, **cell_style, expand=1),
                ft.Container(content=ft.Text("KG/M", weight="bold"), **cell_style, expand=1),
                ft.Container(content=btn, **cell_style, expand=1),
            ]
        )
        data_rows.append(row)

    table_content = ft.Column(controls=[header_row] + data_rows, spacing=0)

    table_box = ft.Container(
        content=table_content,
        border=ft.Border(
            top=ft.BorderSide(1, "black"), bottom=ft.BorderSide(1, "black"),
            left=ft.BorderSide(1, "black"), right=ft.BorderSide(1, "black")
        ),
        border_radius=5, padding=5
    )

    page.add(ft.Text("米重换算", size=24, weight="bold"), ft.Divider(), top_row, ft.Divider(), table_box)

ft.run(main)
