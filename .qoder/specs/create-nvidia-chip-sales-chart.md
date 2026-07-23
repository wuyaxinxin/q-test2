# 英伟达芯片销量曲线图实现规格说明

## 项目概述
将现有的猪肉价格可视化应用改造为英伟达芯片销量可视化应用。保持相同的技术架构（Flask + Plotly + Pandas），替换数据模型、业务逻辑和UI文本。

## 关键技术栈
- **后端**: Flask 3.0.0
- **图表库**: Plotly 5.18.0
- **数据处理**: Pandas 2.1.4
- **前端**: Jinja2 模板 + Plotly.js

## 实施计划

### 第一阶段：数据模型改造

#### 1. 修改 `pork_price_app/data_manager.py`

**关键改动点：**

1. **函数重命名**
   - `generate_mock_data()` → 保持不变（仅修改内部逻辑）
   - 数据文件路径：`pork_prices.json` → `nvidia_chip_sales.json`

2. **数据生成逻辑** (第10-54行)
   - 时间范围：保持 2023-01-01 至 2024-12-31（730天）
   - 数据字段：
     - `date`: 保持不变（字符串格式 "YYYY-MM-DD"）
     - `price` → `sales` (销量字段)
   
3. **销量模型设计**
   ```python
   # 芯片型号：NVIDIA A100 80GB GPU
   base_sales = 15000  # 基础日销量（台）
   
   # 趋势因素：AI热潮推动增长（+30%年增长率）
   days_since_start = (current_date - start_date).days
   growth_factor = (days_since_start / 365) * 0.3 * base_sales
   
   # 季节性因素：Q4财年末采购高峰
   seasonal_factor = 3000 * math.sin(2 * math.pi * (day_of_year - 274) / 365)
   # 274对应10月1日，Q4开始
   
   # 周期性因素：新品发布周期影响
   cycle_factor = 2000 * math.sin(2 * math.pi * day_of_year / 180)
   
   # 随机波动：供应链和市场波动
   random_noise = random.gauss(0, 800)
   
   sales = base_sales + growth_factor + seasonal_factor + cycle_factor + random_noise
   sales = max(8000, min(25000, sales))  # 销量范围：8000-25000台/日
   sales = int(round(sales))  # 销量为整数
   ```

4. **元数据更新** (第45-52行)
   ```python
   "metadata": {
       "source": "模拟数据",
       "unit": "台/日",
       "chip_model": "NVIDIA A100 80GB GPU",
       "description": "全球NVIDIA A100芯片日销量"
   }
   ```

5. **函数文档字符串更新**
   - 第11-15行：猪肉价格 → 英伟达芯片销量
   - 第73-76行：价格数据 → 销量数据

#### 文件路径：`/data/workspace/Qoder2/pork_price_app/data_manager.py`

---

### 第二阶段：图表生成模块改造

#### 2. 修改 `pork_price_app/chart_generator.py`

**关键改动点：**

1. **函数参数和变量重命名** (第7-18行)
   ```python
   def create_sales_chart(data):  # 函数名从 create_price_chart 改为 create_sales_chart
       """
       创建Plotly交互式销量曲线图
       
       参数:
           data (dict): 包含销量数据的字典
       返回:
           str: Plotly图表的HTML代码
       """
       dates = [item['date'] for item in data['data']]
       sales = [item['sales'] for item in data['data']]  # price → sales
   ```

2. **图表配置更新** (第22-29行)
   ```python
   fig.add_trace(go.Scatter(
       x=dates,
       y=sales,
       mode='lines',
       name='A100销量',
       line=dict(color='#76b900', width=2),  # 使用英伟达品牌绿色
       hovertemplate='<b>日期:</b> %{x}<br><b>销量:</b> %{y:,}台<extra></extra>'
   ))
   ```

3. **图表标题和轴标签** (第31-60行)
   ```python
   fig.update_layout(
       title={
           'text': 'NVIDIA A100 芯片全球销量趋势',
           'x': 0.5,
           'xanchor': 'center',
           'font': {'size': 24, 'family': 'Arial, sans-serif'}
       },
       xaxis=dict(
           title='日期',
           # ... 保持时间范围选择器不变
       ),
       yaxis=dict(
           title='销量 (台/日)',
           showgrid=True,
           gridcolor='lightgray'
       ),
       # ... 其他布局配置保持不变
   )
   ```

4. **HTML div ID** (第71行)
   ```python
   div_id='sales-chart',  # 从 'price-chart' 改为 'sales-chart'
   ```

#### 文件路径：`/data/workspace/Qoder2/pork_price_app/chart_generator.py`

---

### 第三阶段：Flask应用主入口改造

#### 3. 修改 `pork_price_app/app.py`

**关键改动点：**

1. **导入语句更新** (第5行)
   ```python
   from pork_price_app.chart_generator import create_sales_chart
   ```

2. **路由函数更新** (第11-27行)
   ```python
   @app.route('/')
   def index():
       """
       主页路由,展示英伟达芯片销量曲线图
       """
       data = load_data()
       
       chart_html = create_sales_chart(data)  # 调用新函数
       
       metadata = data.get('metadata', {})
       
       return render_template(
           'index.html',
           chart_html=chart_html,
           data_source=metadata.get('source', '未知'),
           unit=metadata.get('unit', '台/日'),
           chip_model=metadata.get('chip_model', 'NVIDIA A100'),
           description=metadata.get('description', '')
       )
   ```

#### 文件路径：`/data/workspace/Qoder2/pork_price_app/app.py`

---

### 第四阶段：前端模板改造

#### 4. 修改 `pork_price_app/templates/index.html`

**关键改动点：**

1. **页面标题** (第6行)
   ```html
   <title>NVIDIA芯片销量趋势</title>
   ```

2. **页面标题和副标题** (第11-13行)
   ```html
   <header>
       <h1>NVIDIA {{ chip_model }} 销量曲线</h1>
       <p class="subtitle">{{ description }}</p>
   </header>
   ```

3. **页脚信息** (第22-24行)
   ```html
   <footer>
       <p>芯片型号: {{ chip_model }} | 数据来源: {{ data_source }} | 单位: {{ unit }}</p>
       <p class="note">提示: 使用鼠标滚轮缩放,拖动查看不同时间段,悬停查看详细数据</p>
   </footer>
   ```

#### 文件路径：`/data/workspace/Qoder2/pork_price_app/templates/index.html`

---

### 第五阶段：启动脚本改造

#### 5. 修改 `run_pork_app.py`

**关键改动点：**

1. **启动信息更新** (第6-11行)
   ```python
   if __name__ == '__main__':
       print("=" * 60)
       print("NVIDIA芯片销量可视化应用启动中...")
       print("=" * 60)
       print("访问地址: http://localhost:5000")
       print("按 Ctrl+C 停止服务")
       print("=" * 60)
       app.run(debug=True, port=5000, host='127.0.0.1')
   ```

#### 文件路径：`/data/workspace/Qoder2/run_pork_app.py`

---

### 第六阶段：数据文件处理

#### 6. 删除旧数据文件（如果存在）

**操作：**
- 删除文件：`/data/workspace/Qoder2/pork_price_app/data/pork_prices.json`
- 新数据文件将在首次运行时自动生成：`nvidia_chip_sales.json`

---

## 实施顺序优先级

1. **P0 - 数据层改造** (第一阶段)
   - 修改 `data_manager.py` 中的数据生成逻辑
   - 更新数据文件路径和字段名
   - 确保销量模型合理

2. **P0 - 图表层改造** (第二阶段)
   - 修改 `chart_generator.py` 函数名和变量名
   - 更新图表标题、轴标签、悬停提示
   - 调整颜色主题

3. **P1 - 应用层改造** (第三阶段)
   - 修改 `app.py` 导入和函数调用
   - 更新模板参数传递

4. **P1 - 前端改造** (第四阶段)
   - 修改 `index.html` 页面文本

5. **P2 - 启动脚本** (第五阶段)
   - 修改 `run_pork_app.py` 启动信息

6. **P2 - 数据清理** (第六阶段)
   - 删除旧数据文件

---

## 关键文件清单

| 文件路径 | 修改类型 | 说明 |
|---------|---------|------|
| `/data/workspace/Qoder2/pork_price_app/data_manager.py` | 重点修改 | 数据生成逻辑核心 |
| `/data/workspace/Qoder2/pork_price_app/chart_generator.py` | 重点修改 | 图表配置核心 |
| `/data/workspace/Qoder2/pork_price_app/app.py` | 轻度修改 | 函数调用更新 |
| `/data/workspace/Qoder2/pork_price_app/templates/index.html` | 轻度修改 | UI文本更新 |
| `/data/workspace/Qoder2/run_pork_app.py` | 轻度修改 | 启动信息更新 |
| `/data/workspace/Qoder2/pork_price_app/data/pork_prices.json` | 删除 | 旧数据文件 |

---

## 数据字段对照表

| 原字段 | 新字段 | 数据类型 | 示例值 |
|-------|-------|---------|--------|
| `price` | `sales` | integer | 15234 |
| 价格 (元/公斤) | 销量 (台/日) | - | - |
| 18.0-28.0 | 8000-25000 | - | - |

---

## UI文本更新清单

| 位置 | 原文本 | 新文本 |
|-----|-------|-------|
| index.html - title | 国内猪肉价格走势 | NVIDIA芯片销量趋势 |
| index.html - h1 | 国内猪肉价格浮动曲线 | NVIDIA {{ chip_model }} 销量曲线 |
| chart_generator.py - 图表标题 | 国内猪肉价格走势 | NVIDIA A100 芯片全球销量趋势 |
| chart_generator.py - Y轴标签 | 价格 (元/公斤) | 销量 (台/日) |
| chart_generator.py - 悬停提示 | 价格: ¥%{y:.2f}/公斤 | 销量: %{y:,}台 |
| chart_generator.py - trace name | 猪肉价格 | A100销量 |
| data_manager.py - metadata.description | 全国猪肉平均批发价格 | 全球NVIDIA A100芯片日销量 |
| run_pork_app.py - 启动信息 | 国内猪肉价格可视化应用 | NVIDIA芯片销量可视化应用 |

---

## 销量模型说明

**选择芯片型号**: NVIDIA A100 80GB GPU
- **理由**: A100是数据中心GPU的标杆产品，在AI训练和推理领域应用广泛，市场认知度高

**销量特征设计**:
1. **基础销量**: 15,000台/日（反映主流数据中心GPU的市场规模）
2. **增长趋势**: 年增长率30%（反映AI热潮推动的强劲需求）
3. **季节性**: Q4采购高峰（企业财年末预算消耗）
4. **周期性**: 180天周期（新品发布和产能爬坡影响）
5. **波动性**: ±800台随机波动（供应链和市场变化）
6. **销量范围**: 8,000-25,000台/日

---

## 验证步骤

完成改造后，执行以下验证：

1. **删除旧数据文件**
   ```bash
   rm -f /data/workspace/Qoder2/pork_price_app/data/pork_prices.json
   ```

2. **启动应用**
   ```bash
   python /data/workspace/Qoder2/run_pork_app.py
   ```

3. **验证点**
   - [ ] 应用成功启动在 http://localhost:5000
   - [ ] 自动生成 `nvidia_chip_sales.json` 文件
   - [ ] 页面标题显示为 "NVIDIA芯片销量趋势"
   - [ ] 图表标题显示为 "NVIDIA A100 芯片全球销量趋势"
   - [ ] Y轴标签显示为 "销量 (台/日)"
   - [ ] 悬停提示显示整数销量（如 "15,234台"）
   - [ ] 曲线颜色为英伟达绿色 (#76b900)
   - [ ] 时间范围选择器工作正常
   - [ ] 销量数据在 8000-25000 范围内
   - [ ] 数据呈现增长趋势和季节性波动

4. **功能测试**
   - [ ] 鼠标滚轮缩放功能正常
   - [ ] 拖动查看不同时间段功能正常
   - [ ] 范围选择器（1月、3月、6月、1年、全部）工作正常
   - [ ] 范围滑块拖动功能正常

---

## 注意事项

1. **保持文件头注释**: 所有修改的文件顶部必须保留 `# 始终生效` 注释（符合项目规范 aa.md）
2. **保持依赖不变**: 无需修改 `requirements.txt`，所有依赖已满足
3. **保持目录结构**: 不重命名 `pork_price_app` 目录，仅修改文件内容
4. **数据类型一致性**: 销量字段使用整数类型（int），价格使用浮点数（float）
5. **数字格式化**: 悬停提示中销量使用千位分隔符（如 15,234）提高可读性
6. **颜色主题**: 使用英伟达品牌绿色 #76b900 作为主色调

---

## 预期成果

完成改造后，用户将获得：
- 一个功能完整的英伟达A100芯片销量可视化Web应用
- 730天的模拟日销量数据（2023-2024年）
- 交互式Plotly图表，支持缩放、拖动、悬停查看
- 符合芯片销售特征的数据模型（增长趋势+季节性波动）
- 清晰的UI文本和数据标签