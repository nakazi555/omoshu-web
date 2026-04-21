# オモシュワ（omoshu-web）プロジェクト探索レポート

## 1. ディレクトリ構造

```
/Users/s22312/omoshu-web/
├── .git/                          # GitHub git リポジトリ
├── episodes/                      # 個別エピソードページ（HTMLファイル×15話）
│   ├── ep-01.html
│   ├── ep-02-28.html
│   ├── ep-03.html
│   ├── ... (ep-15まで)
│   └── ep-15.html
├── shorts/                        # ショート動画関連
├── index.html                     # メインページ（812行）
├── CNAME                          # DNS: omoshuwa-podcast.com
├── robots.txt                     # SEO設定
├── sitemap.xml                    # XMLサイトマップ
├── google9b4e95759480bed0.html   # Google認証ファイル
└── improvement_log.json           # 改善ログ
```

## 2. デプロイ方式

- **リポジトリ**: GitHub (nakazi555/omoshu-web)
- **ホスティング**: GitHub Pages
- **カスタムドメイン**: omoshuwa-podcast.com（CNAME設定済み）
- **デプロイ**: mainブランチへのpush自動デプロイ

## 3. メインページHTML（index.html）の全体構成

### ページ全体セクション
1. **NAV** (固定ナビゲーション)
   - ロゴ + セクションリンク（CONCEPT, HOSTS, SHORTS, EPISODES, LISTEN, JPA）
   - Spotifyフォロー CTA
   - ハンバーガーメニュー（モバイル）

2. **HERO** (ヒーローセクション)
   - アートワーク画像
   - タイトル（グリッチエフェクト付き）
   - キャッチコピー
   - CTA群（Spotify, Apple Podcasts, LISTEN, お便り）

3. **STATS BAR**
   - 15 EPISODES
   - WEEKLY UPDATE
   - 5+ PLATFORMS
   - 2025.12 SINCE

4. **CONCEPT** (番組コンセプト)
   - VS DIVIDER: "HUMAN vs AI"
   - 「AIに勝てる、くだらなさを探せ。」

5. **HOSTS** (パーソナリティ)
   - ミヤザワ（Voice）
   - ナカジマ（Muscle）
   - オモシュワくん（公式AI LINE BOT）

6. **SHORTS** (YouTube Shorts)
   - 12個のショート動画カード
   - 再生数バッジ

### ⭐ 「全エピソード一覧」セクション（566行目）

```html
<!-- EPISODES -->
<div class="vs-divider"><span class="vs-text">ALL EPISODES</span></div>

<section id="episodes">
  <div class="fade-in">
    <div class="section-label">Episode Archive</div>
    <h2 class="section-title">全エピソード一覧</h2>
    <p class="section-subtitle">タップするとその場で再生できます。全話無料。</p>
  </div>
  <div class="episode-list">
    <!-- EP15〜EP01の15話分 -->
  </div>
</section>
```

#### エピソード一覧の直後に続く内容

**すぐ後:**
- Spotify全話聴くボタン（行632）

**その後:**
1. **FOLLOW BANNER** (637-640行)
   - 「まだフォローしてない？」プロモーション
   - Spotifyフォローボタン

2. **PLATFORMS** 「配信プラットフォーム」セクション
   - Spotify
   - Apple Podcasts
   - LISTEN
   - Amazon Music
   - YouTube Shorts
   - お便りフォーム

3. **JPA** 「ジャパンポッドキャストアワード」セクション
   - VS DIVIDER: "AWARD"
   - 第8回 一般クリエイター部門
   - カウントダウン（投票開始まで）

4. **SHARE** バナー
   - X (Twitter) シェア
   - LINE シェア

5. **HASHTAGS**
   - #オモシュワ #AIvs人間 #声と筋肉 #ポッドキャスト #男子校ノリ #大喜利バトル #JPA2027

6. **FLOATING PLAYER**
   - 画面下部固定Spotifyプレイヤー

7. **FOOTER**
   - ロゴ
   - リンク集（Spotify, Apple, LISTEN, お便り）
   - コピーライト

## 4. CSS スタイリング方式

**完全にインラインCSS**（外部CSSファイルなし）

### CSS構成（68-351行のstyleタグ内）

#### CSSルート変数
```css
:root{
  --red:#e63946;
  --dark:#0a0a0f;
  --darker:#050508;
  --cyan:#00f0ff;
  --green:#39ff14;
  --orange:#ff6b35;
  --white:#f1faee;
  --gray:#a8a8b3;
  --card-bg:rgba(15,15,25,0.85);
  --spotify:#1ed760;
}
```

#### スタイル特性
- **グラデーション & グロー**: サイバーパンク系の視覚表現
- **アニメーション多数**:
  - gridMove（背景グリッド）
  - shimmer（テキストグラデーション）
  - glitch（タイトルグリッチエフェクト）
  - float-up（パーティクル）
  - ctaPulse（ボタン）
  - rotateBg（JPA背景）
  
- **バックドロップフィルター**: モダングラスモーフィズム
- **レスポンシブ**: @media (max-width:768px) で対応

### フォント
```css
font-family: 'Noto Sans JP' (メイン)
font-family: 'Orbitron' (見出し・ラベル - SF的な未来感)
```

**Google Fontsから読み込み:**
- Noto Sans JP: 400, 700, 900 weights
- Orbitron: 700, 900 weights

## 5. JavaScript機能（717-810行）

### パーティクル生成
- 30個のランダムパーティクルを動的生成
- colors: cyan, red, green

### ナビゲーション
- ハンバーガーメニュー開閉

### Fade-in Observer
- IntersectionObserver で要素のスクロール表示アニメ
- .fade-in クラス付き要素の遅延表示

### YouTube Shorts再生
- playShort()関数
- iframe動的生成で埋め込み再生

### Spotify Embed
- toggleEpEmbed()関数
- クリックでエピソード毎にiframe埋め込み再生

### JPA カウントダウン
- 2026-12-01 00:00:00 まで計算
- 日数表示更新

### Floating Player制御
- 閉じるボタンで非表示可能

## 6. 外部リソース & API

### CDN & 外部サービス
- **Google Analytics**: G-7HE7Z42J1F
- **Google Fonts**: Noto Sans JP, Orbitron
- **Cloudfront**: podcast artwork画像
- **Spotify API**: 埋め込みプレイヤー・Webプレイヤー
- **Apple Podcasts**: リンク
- **YouTube**: Shorts埋め込み
- **LINE**: オモシュワくんBOT連携

### Schema.org Markup
- PodcastSeries スキーマ付き
- 15エピソード+6ショート動画のメタデータ

## 7. エピソード一覧の技術実装

### エピソードアイテム構造
```html
<div class="episode-item fade-in" data-spotify="[SPOTIFY_ID]" onclick="toggleEpEmbed(this)">
  <div class="episode-row">
    <span class="episode-num">EP15</span>
    <div class="episode-info">
      <div class="episode-title">タイトル</div>
      <div class="episode-meta">日付 &#183; 再生時間</div>
    </div>
    <span class="episode-play">▶</span>
  </div>
  <div class="episode-embed"></div><!-- Spotify iframe埋め込み先 -->
</div>
```

### エピソード一覧CSS
- flex レイアウト（行ベース）
- ホバー時: translateX(6px)アニメーション
- episode-embed: max-height トランジション（開閉エフェクト）

### インタラクション
- タップでエピソード毎にSpotify埋め込みプレイヤーを展開
- 他のエピソードは自動的に閉じる

## 8. メタデータ & SEO

### OGP設定
- og:title, og:description, og:image, og:type, og:url
- og:locale: ja_JP

### Twitter Card
- twitter:card: summary_large_image

### Twitter/Xシェア対応
- ハードコードされたシェアURL

### Canonical Link
- https://omoshuwa-podcast.com/

### Apple iTunes App
- Podcast アプリへのディープリンク

## 9. 特筆すべき設計

1. **完全なシングルページ設計**: 1つのHTML + インラインCSS + vanilla JavaScript
   - ビルドプロセス不要
   - CDNキャッシュ効率良好

2. **ダークテーマ**: サイバーパンク/ネオン系の視覚デザイン
   - 背景: #050508（ほぼ黒）
   - テキスト: #f1faee（ほぼ白）
   - アクセント: cyan, red, green

3. **マルチプラットフォーム対応**: 
   - 配信先5+ (Spotify, Apple, Amazon, LISTEN, YouTube)
   - SNS連携（Twitter, LINE）

4. **動的カウントダウン**: JPA投票開始までのカウント機能

5. **アクセシビリティ**: 
   - aria-label 属性
   - semantic HTML5（nav, section, footer）
   - Lighthouse対応

## 10. 改善ポイント（参考: improvement_log.json）

- improvement_log.json にて改善履歴管理
- 毎回異なるデザイン方向性への対応可能な構造

## まとめ

omoshu-web は**シンプル、高速、保守性重視**な設計。
- GitHub Pages で無料ホスト
- 1ファイルで完結（index.html）
- Spotify/Apple/LINE等プラットフォーム統合
- グリッチ・グロー等アニメーション豊富なUI
- 「全エピソード一覧」は内容豊富で、その後すぐに配信プラットフォーム、JPA、シェア、フッターと続く
