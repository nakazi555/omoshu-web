# omoshu-web

ポッドキャスト「オーモシロ・シュワルツェネッガー」の公式サイト。
GitHub Pages でホストし、エピソード更新・ショート追加を自動コミットで運用する静的サイト。

**URL**: https://omoshuwa-podcast.com/
**リポジトリ**: nakazi555/omoshu-web（main push → 自動デプロイ）

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| ホスティング | GitHub Pages（カスタムドメイン CNAME） |
| フロントエンド | 静的HTML + インラインCSS + Vanilla JS（ビルド不要） |
| デザイン | サイバーパンク/ネオン系ダークテーマ（Orbitron + Noto Sans JP） |
| 外部連携 | Spotify Embed, YouTube Shorts iframe, Google Analytics (G-7HE7Z42J1F) |
| SEO | sitemap.xml, robots.txt, Schema.org (PodcastSeries), OGP, Twitter Card |
| 改善記録 | improvement_log.json（自動コミットログ） |

## ディレクトリ構成

```
omoshu-web/
├── index.html          # メインSPA（全セクション + インラインCSS/JS）
├── episodes/           # 個別エピソードページ（ep-01.html 〜 ep-17.html等）
├── shorts/             # ショート動画関連
├── sitemap.xml         # 自動更新
├── improvement_log.json # 改善・更新履歴
├── CNAME               # omoshuwa-podcast.com
└── EXPLORATION_NOTES.md # ページ構造の詳細リファレンス
```

## index.html 構成（主要セクション）

NAV → HERO → STATS BAR → CONCEPT → HOSTS → SHORTS → EPISODES → PLATFORMS → JPA → SHARE → FOOTER

- **SHORTS セクション**: YouTube Shortsカード（再生数バッジ付き、人気順）
- **EPISODES セクション**: Spotify埋め込みプレイヤー（タップで展開）
- **JPA セクション**: ジャパンポッドキャストアワード カウントダウン（2026-12-01）

## コーディング規約

- **CSS変数**: `--red:#e63946` `--cyan:#00f0ff` `--green:#39ff14` 等。追加時はルート変数として定義
- **JS**: Vanilla JS のみ。外部ライブラリ追加禁止
- **インラインCSS**: 外部CSSファイルを作らない（1ファイル完結設計を維持）
- **改善後**: improvement_log.json に変更サマリーを追記し、git commit

## 自動コミットパターン

```
auto: サイト改善 (YYYY-MM-DD HH:MM) - N本ショート(人気順) / Nエピソード | TOP: タイトル(N再生)
```

手動変更時もこの形式に準拠する。

## セッション開始プロトコル（最優先）

1. `git -C ~/omoshu-web log --oneline -5` で最新の変更を確認
2. `EXPLORATION_NOTES.md` でページ構造を把握（index.html 全読み不要）
3. improvement_log.json の末尾で前回の変更内容を確認
4. 大きな変更前は index.html をバックアップ（git stash or 別ブランチ）

## セッション終了プロトコル

1. improvement_log.json に変更エントリを追記（timestamp + changes配列）
2. sitemap.xml の lastmod を更新（エピソード追加時）
3. git add → git commit（自動コミット形式）→ git push

## 継続的改善

- ショート追加時: index.html の SHORTS セクション + 該当エピソードページ + sitemap.xml を同時更新
- エピソード追加時: index.html の EPISODES セクション + episodes/ep-XX.html 新規作成 + sitemap.xml
- SEO改善: Schema.org の episode/video 件数を実態に合わせて更新
- KNOWLEDGE.md にハマりポイントを記録（同じミスを繰り返さない）
- 横展開: omoshu-shorts（動画生成側）との連携を意識（ショートID・タイトル整合性）
