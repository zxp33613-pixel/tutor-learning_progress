# Plan — C 语言：类型与基本运算

## Goal

能独立声明变量、选用合适基本类型，正确使用算术/赋值运算，并识别整除、溢出与强制转换等常见陷阱；章末能过少量应试检查。

## Probe result

| strand | status |
|--------|--------|
| 摸底 | 跳过（学员选择从零开讲） |
| 变量与声明 | ✅ 已建（c1） |
| 整型/浮点/char | ✅ 已建（c2+c3） |
| 算术与赋值 | ✅ 已建（c4+c5） |
| 类型转换 | ✅ 已建（c6；块末题跳过作答） |

## Dependency map

```mermaid
flowchart LR
  k1["会用编辑器/终端"] --> c1["变量与类型直觉"]
  c1 --> c2["整型家族"]
  c1 --> c3["浮点与 char"]
  c2 --> c4["算术运算"]
  c3 --> c4
  c4 --> c5["赋值与自增"]
  c2 --> c6["隐式/强制转换"]
  c4 --> c6
  c5 --> c6
  c6 --> goal["🎯 类型与运算过关"]
  classDef done fill:#12261e,stroke:#3fb950,color:#e6edf3
  classDef doing fill:#0d2240,stroke:#58a6ff,color:#e6edf3,stroke-width:2px
  classDef todo fill:#161b22,stroke:#30363d,color:#8b949e
  classDef known fill:#12261e,stroke:#3fb950,color:#e6edf3,stroke-dasharray:4 3
  classDef gap fill:#2a1215,stroke:#f85149,color:#e6edf3
  classDef goal fill:#1f1a0d,stroke:#d29922,color:#e6edf3
  class c1,c2,c3,c4,c5,c6 done
  class k1 known
  class goal goal
```

## Chunks

| # | chunk | exam tasks | depth | status |
|---|-------|------------|-------|--------|
| c1 | 变量与类型直觉：声明、初始化、sizeof 初识 | 1.1 | 概念+小实验 | ✅ |
| c2 | 整型家族：signed/unsigned、字面量、范围直觉 | 1.2 | 表格+陷阱 | ✅ |
| c3 | 浮点与 char：精度、字符即整数 | 1.3 | 对比+代码 | ✅ |
| c4 | 算术运算：+ - * / % 与整除 | 1.4 | 必考陷阱 | ✅ |
| c5 | 赋值、复合赋值、自增自减 | 1.5 | 表达式值 | ✅ |
| c6 | 隐式提升与强制转换 | 1.6 | 易错点 | ✅ |
