import flet as ft

# 材料密度 (g/cm³)
densities = {
    '铝': 2.71, '钢': 7.85, '铁': 7.87, 
    '金': 19.32, '银': 10.49, '铜': 8.96
}

def main(page: ft.Page):
    page.title = "材料米重换算"
    page.padding = 20

    # 结果展示的文字控件
    result_text = ft.Text(size=20, weight=ft.FontWeight.BOLD)

    # 截面积输入框
    area_input = ft.TextField(
        label="输入截面积 (mm²)", 
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: calculate(e)
    )

    def calculate(e):
        try:
            area = float(area_input.value)
            # 计算所有材料的米重
            results = []
            for name, density in densities.items():
                weight = (area * density) / 1000
                results.append(f"{name}: {weight:.3f} KG/M")
            result_text.value = "\n".join(results)
        except (ValueError, TypeError):
            result_text.value = "请输入有效的数字"
        page.update()

    # 添加控件到页面
    page.add(
        ft.Text("材料米重换算", size=24, weight=ft.FontWeight.BOLD),
        area_input,
        ft.Divider(),
        result_text,
    )

ft.run(main)
