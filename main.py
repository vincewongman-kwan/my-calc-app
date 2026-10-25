<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>米重换算预览</title>
    <style>
        * {
            font-family: "Microsoft YaHei", "微软雅黑", sans-serif !important;
            font-weight: bold !important;
            box-sizing: border-box;
        }

        body {
            background-color: #e5e5e5;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding-top: 20px;
            min-height: 100vh;
        }

        .phone-mockup {
            width: 375px;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            padding: 15px;
        }

        .title {
            text-align: center;
            font-size: 24px;
            color: #000;
            margin: 10px 0;
        }

        .divider {
            height: 1px;
            background-color: #e0e0e0;
            margin: 10px 0;
        }

        .input-row {
            display: flex;
            justify-content: center;
            align-items: center; 
            gap: 10px;
        }

        .input-row input {
            width: 220px;
            padding: 0 10px;
            font-size: 16px;
            border: 1px solid #999;
            border-radius: 5px;
            outline: none;
            height: 45px; 
            font-weight: normal !important;
            color: #333;
        }
        
        .input-row input::placeholder {
            color: #666;
        }

        /* 按钮完美居中 */
        .btn-paste {
            width: 56px;
            height: 36px;
            border: 1px solid #ddd;
            border-radius: 15px;
            background-color: #F5F5F5; 
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 14px;
            color: #1976d2;
            cursor: pointer;
            user-select: none; /* 防止按钮文字被选中 */
            transition: background 0.1s;
        }

        .btn-paste:active {
            background-color: #E0E0E0; /* 水波纹点击效果 */
        }

        .framed-container {
            border: 1.5px solid #000;
            border-radius: 8px;
            padding: 15px;
            background-color: #ffffff;
        }

        .table-column {
            display: flex;
            flex-direction: column;
            gap: 12px; 
        }

        .table-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px; 
        }

        .header-cell {
            width: 70px;
            height: 40px;
            background-color: #e0e0e0;
            border-radius: 4px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 15px; 
        }

        .cell {
            width: 70px;
            height: 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 20px; 
        }

        /* 长按选中样式 */
        .value { 
            color: red; 
            user-select: text; /* 允许选中 */
            -webkit-user-select: text;
        }
        .unit { font-size: 15px; }

        /* 复制按钮完美居中 */
        .btn-copy {
            width: 56px;
            height: 28px;
            border: 1px solid #ddd;
            border-radius: 15px;
            background-color: #F5F5F5; 
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 14px;
            color: #1976d2;
            cursor: pointer;
            user-select: none;
            transition: background 0.1s;
        }

        .btn-copy:active {
            background-color: #E0E0E0;
        }
    </style>
</head>
<body>

    <div class="phone-mockup">
        <div class="title">米重换算</div>
        <div class="divider"></div>

        <div class="input-row">
            <input type="number" placeholder="输入截面积 (mm²)">
            <div class="btn-paste">粘贴</div>
        </div>
        
        <div class="divider"></div>

        <div class="framed-container">
            <div class="table-column">
                
                <div class="table-row">
                    <div class="header-cell">材料</div>
                    <div class="header-cell">米重</div>
                    <div class="header-cell">单位</div>
                    <div class="header-cell">操作</div>
                </div>

                <div class="table-row">
                    <div class="cell">铝</div>
                    <div class="cell value">0.000</div>
                    <div class="cell unit">KG/M</div>
                    <div class="cell"><div class="btn-copy">复制</div></div>
                </div>
                <div class="table-row">
                    <div class="cell">钢</div>
                    <div class="cell value">0.000</div>
                    <div class="cell unit">KG/M</div>
                    <div class="cell"><div class="btn-copy">复制</div></div>
                </div>
                <div class="table-row">
                    <div class="cell">铁</div>
                    <div class="cell value">0.000</div>
                    <div class="cell unit">KG/M</div>
                    <div class="cell"><div class="btn-copy">复制</div></div>
                </div>
                <div class="table-row">
                    <div class="cell">金</div>
                    <div class="cell value">0.000</div>
                    <div class="cell unit">KG/M</div>
                    <div class="cell"><div class="btn-copy">复制</div></div>
                </div>
                <div class="table-row">
                    <div class="cell">银</div>
                    <div class="cell value">0.000</div>
                    <div class="cell unit">KG/M</div>
                    <div class="cell"><div class="btn-copy">复制</div></div>
                </div>
                <div class="table-row">
                    <div class="cell">铜</div>
                    <div class="cell value">0.000</div>
                    <div class="cell unit">KG/M</div>
                    <div class="cell"><div class="btn-copy">复制</div></div>
                </div>

            </div>
        </div>
    </div>

</body>
</html>
