# 發布 `fugle-marketdata`（PyPI）

| | |
|---|---|
| 套件 | `fugle-marketdata`（PyPI） |
| 版本 bump | **手動改 3 個檔** |
| tag 格式 | `2.8.0rc1`（**沒有** `v`） |
| 上架觸發 | **建 GitHub Release** → `.github/workflows/python-publish.yml` |
| 預發布通道 | PyPI 原生 prerelease |
| 發版分支 | `main`（預設分支） |

發版前先讀「[版號相容承諾](#版號相容承諾下游套件用區間依賴)」——下游用區間依賴，**本 repo 發的 rc 會直接被下游使用者裝到**。

---

## 流程

先開 PR 合進 `main`，再直接在 `main` 上發。本 repo 沒有 release 工具，照歷來 release commit 的做法手動改 3 個檔：

```bash
git switch main && git pull --ff-only origin main      # HEAD 應是剛合進去的 merge commit

# 1. pyproject.toml                  version = "2.8.0rc1"
# 2. fugle_marketdata/__init__.py    __version__ = '2.8.0rc1'
# 3. CHANGELOG.md                    在 "# Changelog" 下方插新段落（格式見下）

python3 -m pytest tests/ -q                            # 發之前先綠

git add pyproject.toml fugle_marketdata/__init__.py CHANGELOG.md
git commit -m "chore(release): 2.8.0rc1"
git tag -a 2.8.0rc1 -m "Release 2.8.0rc1"
git push origin main
git push origin 2.8.0rc1
gh release create 2.8.0rc1 --repo fugle-dev/fugle-marketdata-python \
  --prerelease --title "2.8.0rc1" --notes "..."        # 正式版拿掉 --prerelease
```

### 兩個會踩到的地方

**tag 要明確推。** `git push --follow-tags` 只推 annotated tag；用 lightweight tag（`git tag 2.8.0rc1`）的話分支推上去、tag 靜靜留在本機，接著 `gh release create` 就對不到東西。上面用 `git tag -a` 並明確 `git push origin <tag>`，兩道保險。

**最後那行 `gh release create` 不能省。** `python-publish.yml` 的觸發條件是 `release: published`，**不是** push tag。只推 tag 的話 PyPI 永遠等不到東西。標成 `--prerelease` 一樣會觸發。

**不要用 release-it。** 若本機有未追蹤的 `.release-it.json`／`package.json`，那是舊的殘留，版號基準是錯的，而且只會改到 `package.json`。

### CHANGELOG 格式

照既有段落抄（`##` 標題、compare 連結、`### Features`／`### Bug Fixes` 分節、commit 連結用完整 sha），內容取上一個 tag 之後的 commit subject：

```markdown
## [2.8.0rc1](https://github.com/fugle-dev/fugle-marketdata-python/compare/2.7.0...2.8.0rc1) (2026-10-06)


### Features

* **futopt:** <commit subject> ([72f6092](https://github.com/fugle-dev/fugle-marketdata-python/commit/<full-sha>))
```

---

## Commit message

用 Conventional Commits（`feat` / `fix` / `chore` …）。本 repo **沒有** commitlint hook，格式要自己顧。CHANGELOG 只放 subject，使用者需要知道的變更（例如預設行為改了）**必須寫進 subject**，body 不會出現在 changelog。

---

## 版號相容承諾（下游套件用區間依賴）

下游套件以**區間依賴**本套件（例如 `fugle-marketdata >=2.8.0rc1, <2.9`），目的是本套件修 bug 時下游不必重新發版。

**同一個 minor 線（2.8.x；之後的 minor 同理）只能放相容的修正。** 下面這些一律升 minor（或 major），不准進 patch：

- 新增參數、新增端點或功能
- 改回應型別（加欄位、改 nullable、改名都算）
- 任何 breaking（改參數名、改預設行為、拿掉東西）

判斷依據是 commit 類型：發版前看 `git log <上一個 tag>..HEAD --format=%s`，只要有 `feat`，就不能發 patch。

發 patch 前先確認新版號仍落在下游區間內；要升 minor 時，先跟下游對齊何時放寬區間，否則下游使用者拿不到新版。

### ⚠ 2.8.x 的 rc 會直接被下游裝到

下界含 prerelease，依 PEP 440 pip 會接受**整條 2.8 線的 rc**：

| 版本 | `>=2.8.0rc1, <2.9` |
|---|---|
| `2.8.0rc2` | ✅ 接受 |
| `2.8.1rc1` | ✅ **接受** |
| `2.9.0rc1` | ❌ |

所以在 2.8.x 發 rc **等同直接推給下游使用者**（已確認可接受）——發之前要當正式版看待：測試、changelog、對外行為都要到位，不能拿 rc 當試水溫。（Node 版不同：npm 只接受 `1.8.0` 的 rc。）

---

## 發完之後驗

```bash
# rc 上架、stable 沒被動到
python3 -c "import json,urllib.request; \
d=json.load(urllib.request.urlopen('https://pypi.org/pypi/fugle-marketdata/json')); \
print('stable:', d['info']['version']); print('has 2.8.0rc1:', '2.8.0rc1' in d['releases'])"

gh run list --repo fugle-dev/fugle-marketdata-python --limit 3
```

rc 裝法：`pip install fugle-marketdata==2.8.0rc1`。**別用 `pip install --pre fugle-marketdata`**——同一個套件名下還有 v3 的 `3.0.0rcN`，`--pre` 會裝到 v3。

---

## 環境與前置

- `origin` 是 `fugle-dev/fugle-marketdata-python`；本機可能另有鏡像 remote，**別推錯**。
- `gh` 要登入且有 `repo` scope：`gh auth status`。
- 早期曾在獨立的 release 分支上發版，已不再使用。
