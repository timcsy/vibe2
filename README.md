# vibe2

**Vibe2** 是一個規格驅動的軟體工程框架，透過自動化工具鏈將自然語言需求轉換為可執行任務。

## 工作流

遵循以下線性工作流開發任何功能：

```
自然語言描述 → 規格 → 澄清 → 計畫 → 任務 → 分析 → 實現 → GitHub Issues
```

### 工作流命令（在 VS Code 中）

| 命令 | 輸出 | 目的 |
|------|------|------|
| `/speckit.specify` | `spec.md` | 從自然語言生成正式規格 |
| `/speckit.clarify` | 更新 `spec.md` | 澄清規格不明確的地方 |
| `/speckit.plan` | `plan.md`, 設計文件 | 生成技術實現計畫 |
| `/speckit.tasks` | `tasks.md` | 將計畫轉為有序任務 |
| `/speckit.analyze` | 檢查報告 | 驗證一致性和品質 |
| `/speckit.implement` | 執行任務 | 按順序實現所有任務 |
| `/speckit.checklist` | 檢查清單 | 生成品質驗證清單 |
| `/speckit.taskstoissues` | GitHub Issues | 將任務轉為 GitHub 議題 |

## 憲法

所有開發必須遵守 [Vibe2 規格憲法](./.specify/memory/constitution.md)，該憲法定義了 5 個核心原則：

1. **規格驅動** - 所有功能從清晰的自然語言規格開始
2. **設計優先** - 實現前先完成詳盡的設計文件
3. **自動化工作流** - 使用 speckit 工具鏈自動轉換需求到任務
4. **測試驅動開發 (TDD)** - 測試在實現前完成
5. **簡潔性優先** - 避免過度設計，遵循 YAGNI 原則

## 專案結構

```
vibe2/
├── .specify/
│   ├── templates/          # 規格、計畫、任務等模板
│   ├── memory/
│   │   └── constitution.md # 專案治理憲法
│   └── scripts/            # 自動化腳本
├── .github/
│   ├── agents/             # Agent 定義
│   ├── prompts/            # 對應的 prompt 文件
│   └── skills/             # Agent 技能說明
└── README.md               # 此文件
```

## 開始使用

1. **定義功能需求** - 用自然語言描述您的功能
2. **執行工作流** - 在 VS Code 中按順序使用 `/speckit.*` 命令
3. **遵守憲法** - 確保每個階段都符合規格憲法的原則
4. **提交變更** - 在每個工作流階段進行 git commit

## 相關資源

- [Vibe2 規格憲法](./.specify/memory/constitution.md) - 治理原則和開發標準
- [規格模板](./.specify/templates/spec-template.md)
- [計畫模板](./.specify/templates/plan-template.md)
- [任務模板](./.specify/templates/tasks-template.md)