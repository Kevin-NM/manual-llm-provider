# manual-llm-provider: 解決沒錢買API的測試方式

讓程式代理在既有軟體中加入**可續作、可追溯的人工聊天模型生成流程**。

把原本需要呼叫模型 API 的開發測試，改成複製 Prompt 到既有 AI 聊天介面、再人工貼回結果，降低測試時的 API 支出。

[English](README.md) · [Skill 指引](skills/manual-llm-provider/SKILL.md) · [MIT 授權](LICENSE)

```text
準備 Prompt → 人工貼到外部 AI 聊天介面 → 貼回結果
→ 保存候選並驗證 → 使用者接受或退回 → 繼續下一任務
```

人工生成傳輸不需要模型 API Key，並保留原專案的 Prompt Builder、來源版本、驗證、Checkpoint 與最終審核流程。

## 適用範圍

這是提供給 coding agent 的**開發型 Skill**，包含實作與審查指引。實際軟體的介面、儲存、驗證器與執行服務，仍由各專案整合。安裝 Skill 本身不會直接替軟體增加 Provider。

可用於翻譯批次、文件段落、小說場景、結構化輸出任務等，不限定框架、資料庫或任務數量。它不會自動操作外部聊天網站，也無法驗證使用者實際使用哪個模型。

## 安裝或先行試用

Skill 目錄為 [`skills/manual-llm-provider`](skills/manual-llm-provider)。在提供 `$skill-installer` 的 Codex 環境，可要求：

```text
使用 $skill-installer 安裝以下 GitHub 目錄中的 Skill：
https://github.com/Kevin-NM/manual-llm-provider/tree/main/skills/manual-llm-provider
```

若環境已有共用 Skill Hub 或受管理的技能庫，請沿用其安裝流程，保留既有項目，不覆寫同名 Skill。Codex 的[官方 Skill 文件](https://learn.chatgpt.com/docs/build-skills)說明了安裝及探索位置，包括專案的 `.agents/skills` 與使用者的 `~/.agents/skills`。

也可以先不安裝，直接請程式代理讀取 `skills/manual-llm-provider/SKILL.md`，針對指定開發工作套用指引；這不會自動修改全域設定。

`agents/openai.yaml` 是選用的 Codex 介面資訊。其他工具是否支援原生安裝、探索及呼叫，須依各自環境確認；能讀取 Markdown 不代表已完成整合。

## 使用範例

```text
使用 $manual-llm-provider，替這個既有翻譯工具加入人工 LLM 選項。
沿用目前的 Prompt Builder、SQLite 任務、驗證器及最終審核流程。

使用者要能複製 Prompt 到外部聊天介面、貼回翻譯結果，並在重啟後繼續。
只有經使用者接受的翻譯，才能進入下一段的上下文。
保留目前的 HTTP Provider 功能。

先檢查實際程式，提出最小相容修改。未經指示，不要發布或提交 Git。
```

若要審查既有實作，請指出人工 Provider、儲存方式及想驗證的行為。

## 核心原則

- 共用原有核准上下文與 Prompt Builder，保存精確快照、雜湊及來源選擇差異。
- 人工生成不發送模型 API、不暗中切換 Provider，也不捏造 Token 用量或 HTTP 送達證據；模型名稱僅為自填標籤。
- 貼回內容先保存為候選，分開記錄程式檢查、語意審查與使用者接受。
- 只有接受的結果能供後續任務使用；上游修改時，下游 Prompt 與衍生接受紀錄須失效。
- 保留 Attempt 與候選歷史，處理並行版本，以及驗證、下一任務準備、最終寫入中斷後的恢復。
- 任務接受不等於發布，也不會直接核准全域事實；最終結果仍走原本審核流程。

儲存與恢復設計見[任務契約](skills/manual-llm-provider/references/task-contract.md)，測試選擇見[驗收情境](skills/manual-llm-provider/references/acceptance.md)。

## 目錄與開發檢查

```text
skills/manual-llm-provider/
  SKILL.md
  agents/openai.yaml
  references/task-contract.md
  references/acceptance.md
scripts/validate_skill.py
tests/
requirements-dev.txt
```

使用 Python 3.10 以上版本，在倉庫根目錄執行：

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate_skill.py
python -m unittest discover -s tests -v
```

這些檢查驗證 Skill 套件及其工具，不會執行生成後的應用，也不代表外部模型品質已通過驗收。Skill 曾以合成翻譯工具進行規劃試用；各專案仍須完成自己的執行與整合測試。

## 信任邊界與限制

安裝或執行 Skill 前，請先檢視其內容。套件不含模型服務憑證、NGSE 執行程式、實際 Run Prompt 或私人小說資料；設計概念由 NGSE 的人工 Provider 抽取並通用化。

整合聊天 Prompt 是一般使用者訊息，不會取得外部聊天服務真正的 System 權限。憑證檢測只能降低風險，不能保證任意輸入都沒有秘密。另行設定的語意審查器若呼叫 API，必須符合當次授權並明確揭露；完全不使用 API 的流程，會把未確定的語意留待人工審核。

## 貢獻與授權

歡迎以 Issue 或 Pull Request 提供具體使用情境或可重現問題。修改應聚焦可重用的整合決策、保留既有應用行為，並附適當驗證。測試使用合成資料，不提交憑證或私人內容。

本倉庫採用 [MIT 授權](LICENSE)，copyright © 2026 Kevin-NM。這不會改變 NGSE 或採用此 Skill 的應用程式授權。
