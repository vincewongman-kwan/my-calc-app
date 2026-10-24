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
        on_change=lambda e: calculate(),
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
        text = None
        try:
            text = await page.get_clipboard()
        except Exception:
            try: text = page.get_clipboard()
            except Exception: pass
        if text:
            clean_text = ''.join(c for c in str(text) if c.isdigit() or c == '.')
            if clean_text:
                area_input.value = clean_text
                calculate()

    async def copy_result(e, mat, btn):
        val = result_labels[mat].value
        if val and val != "0.000":
            try: await page.set_clipboard(val)
            except Exception:
                try: page.set_clipboard(val)
                except Exception: pass
            btn.text = "已复制"
            btn.bgcolor = "green"
            btn.color = "white"
            page.update()
            await asyncio.sleep(0.8)
            btn.text = "复制"
            btn.bgcolor = ft.Colors.TRANSPARENT
            btn.color = "black"
            page.update()

    header_bg = "grey200"
    cell_padding = 10

    # 👇 表头：强制首尾两个 Container 加圆角
    header_row = ft.Row(
        controls=[
            ft.Container(content=ft.Text("材料", weight="bold"), alignment="center", bgcolor=header_bg, padding=cell_padding, expand=1, border_radius=ft.border_radius.only(top_left=9)),
            ft.Container(content=ft.Text("米重", weight="bold"), alignment="center", bgcolor=header_bg, padding=cell_padding, expand=1),
            ft.Container(content=ft.Text("单位", weight="bold"), alignment="center", bgcolor=header_bg, padding=cell_padding, expand=1),
            ft.Container(content=ft.Text("操作", weight="bold"), alignment="center", bgcolor=header_bg, padding=cell_padding, expand=1, border_radius=ft.border_radius.only(top_right=9)),
        ],
        spacing=1
    )

    data_rows = []
    mats = list(densities.keys())
    for i, mat in enumerate(mats):
        lbl = ft.Text("0.000", size=18, weight="bold", color="red")
        result_labels[mat] = lbl
        
        btn = ft.Button("复制", style=ft.ButtonStyle(padding=5))
        btn.on_click = lambda e, m=mat, b=btn: copy_result(e, m, b)

        # 👇 判断是否是最后一行，如果是，给首尾加底部圆角
        is_last = (i == len(mats) - 1)
        
        first_cell_radius = ft.border_radius.only(bottom_left=9) if is_last else None
        last_cell_radius = ft.border_radius.only(bottom_right=9) if is_last else None

        row = ft.Row(
            controls=[
                ft.Container(content=ft.Text(mat, size=18, weight="bold"), alignment="center", bgcolor="white", padding=cell_padding, expand=1, border_radius=first_cell_radius),
                ft.Container(content=lbl, alignment="center", bgcolor="white", padding=cell_padding, expand=1),
                ft.Container(content=ft.Text("KG/M", weight="bold"), alignment="center", bgcolor="white", padding=cell_padding, expand=1),
                ft.Container(content=btn, alignment="center", bgcolor="white", padding=cell_padding, expand=1, border_radius=last_cell_radius),
            ],
            spacing=1
        )
        data_rows.append(row)

    table_container = ft.Container(
        content=ft.Column(controls=[header_row] + data_rows, spacing=1),
        bgcolor="black",
        border_radius=10,
        padding=1
    )

    top_row = ft.Row(
        controls=[
            ft.Container(content=area_input, expand=True),
            ft.Button("粘贴", on_click=paste_area)
        ]
    )

    page.add(
        ft.ListView(
            controls=[
                ft.Container(height=30),
                ft.Row([ft.Text("米重换算", size=24, weight="bold")], alignment="center"),
                ft.Divider(),
                top_row,
                ft.Divider(),
                table_container
            ],
            spacing=10,
            expand=True
        )
    )

ft.run(main)
