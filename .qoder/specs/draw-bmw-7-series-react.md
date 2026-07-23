# 始终生效

# 宝马7系SVG可视化 - React项目实现规范

## 概述
创建一个新的React项目，使用SVG矢量图技术绘制宝马7系轿车外观（3/4视图角度）。

## 技术选型
- **构建工具**: Vite + React + TypeScript
- **绘图技术**: SVG矢量图
- **视角**: 3/4视图（斜45度）

## 项目结构

```
bmw-7-series-viz/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── App.css
│   ├── index.css
│   └── components/
│       └── BMW7Series/
│           ├── index.tsx              # 主SVG组件
│           ├── BMW7Series.css
│           ├── parts/
│           │   ├── CarBody.tsx        # 车身主体
│           │   ├── KidneyGrille.tsx   # 双肾格栅
│           │   ├── AngelEyeHeadlight.tsx  # 天使眼大灯
│           │   ├── HofmeisterKink.tsx # 霍氏弯角
│           │   ├── Wheels.tsx         # 车轮
│           │   ├── Windows.tsx        # 车窗
│           │   ├── BMWLogo.tsx        # 宝马Logo
│           │   ├── SideMirror.tsx     # 后视镜
│           │   └── TailLights.tsx     # 尾灯
│           └── constants/
│               ├── colors.ts          # 颜色常量
│               └── dimensions.ts      # 尺寸常量
```

## 实施步骤

### 步骤1: 项目初始化
1. 使用 `npm create vite@latest bmw-7-series-viz -- --template react-ts` 创建项目
2. 进入目录并安装依赖
3. 清理默认模板文件

### 步骤2: 创建常量文件
- `colors.ts`: 定义BMW蓝、白、镀铬渐变等颜色
- `dimensions.ts`: 定义画布尺寸(800x400)、各部件位置比例

### 步骤3: 创建核心部件（按顺序）
1. **CarBody.tsx** - 车身主体轮廓（使用`<path>`贝塞尔曲线）
2. **Wheels.tsx** - 车轮（轮胎+多辐轮毂）
3. **Windows.tsx** - 车窗（挡风玻璃+侧窗+反光效果）
4. **KidneyGrille.tsx** - 双肾格栅（肾形+竖条纹理+镀铬边框）
5. **AngelEyeHeadlight.tsx** - 天使眼大灯（双环LED+发光效果）
6. **HofmeisterKink.tsx** - 霍氏弯角（C柱标志性弯折）
7. **BMWLogo.tsx** - 蓝白四象限圆形Logo

### 步骤4: 细节部件
- SideMirror.tsx - 后视镜
- TailLights.tsx - L形尾灯

### 步骤5: 整合与调试
1. 在 `BMW7Series/index.tsx` 中按层级整合所有部件
2. 调整透视效果（后端元素缩小10-15%）
3. 添加车身阴影

## SVG技术要点

### 图层顺序（从底到顶）
1. 阴影层
2. 后轮
3. 车身主体
4. 车窗
5. 前轮
6. 格栅+大灯
7. 细节层（Logo、门把手等）

### 关键技术
- `<path>`: 复杂曲线轮廓
- `<linearGradient>`: 金属光泽
- `<radialGradient>`: 轮毂中心、大灯光晕
- `<filter>` + `feDropShadow`: 阴影效果
- `<pattern>`: 格栅竖条纹理

### 宝马7系设计特征
- **双肾格栅**: 两个大型相连肾形，带竖条纹理和镀铬边框
- **天使眼**: 双圆环LED日行灯，添加发光滤镜
- **霍氏弯角**: C柱与后车窗交界处的向前弯折线条
- **流线型车身**: 平滑下降的车顶曲线

## 依赖包
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "typescript": "^5.3.0",
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.0"
}
```

## 关键文件
1. `src/components/BMW7Series/index.tsx` - 核心整合组件
2. `src/components/BMW7Series/parts/CarBody.tsx` - 车身主体
3. `src/components/BMW7Series/parts/KidneyGrille.tsx` - 双肾格栅
4. `src/components/BMW7Series/parts/AngelEyeHeadlight.tsx` - 天使眼大灯
5. `src/components/BMW7Series/constants/dimensions.ts` - 尺寸常量

## 注意事项
- 每个文件开头添加 `// 始终生效` 注释
- CSS文件使用 `/* 始终生效 */`
- SVG viewBox设置为 "0 0 800 400"
- 3/4视角需考虑透视变形
