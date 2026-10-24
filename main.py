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

    # 存储结果的文字控件
    result_labels = {}

    # 输入框
    area_input = ft.TextField(
        label="输入截面积 (mm²)", 
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: calculate()
    )

    # 粘贴功能
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

    # 计算逻辑
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

    # 复制功能
    async def copy_result(e, mat, btn):
        val = result_labels[mat].value
        if val and val != "0.000":
            await page.set_clipboard(val)
            btn.text = "已复制"
            btn.bgcolor = "green"
            page.update()
            await asyncio.sleep(0.8)
            btn.text = "复制"
            btn.bgcolor = ft.Colors.TRANSPARENT
            page.update()

    # 构建界面
    items = [
        ft.Text("材料米重换算", size=26, weight=ft.FontWeight.BOLD),
        ft.Row([
            ft.Container(content=area_input, width=220),
            ft.Button("粘贴", on_click=paste_area)
        ]),
        ft.Divider(),
    ]

    for mat in densities.keys():
        lbl = ft.Text("0.000", size=20, weight=ft.FontWeight.BOLD, color="red")
        result_labels[mat] = lbl
        
        btn = ft.Button("复制", bgcolor=ft.Colors.TRANSPARENT)
        btn.on_click = lambda e, m=mat, b=btn: copy_result(e, m, b)
        
        items.append(
            ft.Row([
                ft.Text(mat, size=20, weight=ft.FontWeight.BOLD, width=40),
                ft.Container(content=lbl, width=100),
                ft.Text("KG/M", size=16, weight=ft.FontWeight.BOLD),
                btn
            ])
        )

    page.add(ft.Column(items, scroll=ft.ScrollMode.AUTO))

ft.run(main)
