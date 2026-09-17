# atreyayelishetti-indian-rummy-game-rust

> 类型：Point Rummy 详情页
> 创建日期：2026-09-17
> 原文链接：https://github.com/atreyayelishetti/indian-rummy-game-rust
> 返回日报：[[Daily/2026-09-17]]

## 一句话结论

这是 Rust 版 Indian Rummy 候选，可用于检查规则表达和类型安全实现，但需要确认完整度。

## 信息压缩图示

```mermaid
flowchart TB
  A[牌局状态] --> B[Rust 类型建模]
  B --> C[合法动作]
  C --> D[计分]
  D --> E[可复用规则库]
```

```mermaid
quadrantChart
  title 规则引擎复用价值
  x-axis 低可落地性 --> 高可落地性
  y-axis 低价值 --> 高价值
  RustRummy: [0.50, 0.48]
```

## 相关链接

- 原文：https://github.com/atreyayelishetti/indian-rummy-game-rust
