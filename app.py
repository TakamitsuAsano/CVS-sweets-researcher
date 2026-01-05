import streamlit as st
import datetime

# ページ設定
st.set_page_config(
    page_title="CVS Trend Hunter (Time Traveler)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態
if 'research_result' not in st.session_state:
    st.session_state.research_result = ""

st.title("🍩 コンビニスイーツ・パン トレンド予測＆発掘ラボ")
st.markdown("---")

# サイドバー設定
st.sidebar.header("検索条件の設定")

# 1. 大枠のカテゴリー
broad_category = st.sidebar.selectbox(
    "1. 大カテゴリー",
    ["スイーツ", "パン", "総菜パン/軽食"]
)

# 2. サブジャンル
if broad_category == "スイーツ":
    sub_genres = [
        "指定なし（全域）",
        "シュークリーム・エクレア類",
        "プリン・カップデザート類",
        "ケーキ・スポンジ類",
        "チーズケーキ類",
        "チョコレート・焼き菓子類",
        "和菓子・ネオ和菓子類",
        "アイス・氷菓類",
        "★未定義・新食感・ハイブリッド"
    ]
elif broad_category == "パン":
    sub_genres = [
        "指定なし（全域）",
        "食パン・食事パン系",
        "クロワッサン・デニッシュ系",
        "ハード系・ドイツパン系",
        "菓子パン（メロンパン等）系",
        "ドーナツ・揚げパン系",
        "★未定義・新食感・ハイブリッド"
    ]
else:
    sub_genres = [
        "指定なし（全域）",
        "サンドイッチ・バーガー類",
        "カレーパン・揚げ物入り類",
        "焼き込み・ピザ類",
        "中華まん・ホットスナック的パン",
        "★異業種かけ合わせ・新形態"
    ]

target_genre = st.sidebar.selectbox("2. 重点調査サブジャンル", sub_genres)

# 3. 過去トレンドとの比較設定（ここを追加）
st.sidebar.subheader("📅 時間軸設定")
use_past_comparison = st.sidebar.checkbox("過去のトレンド（昨対など）を踏まえる", value=True)

target_period_label = "企画対象時期（予測先）"
target_period = st.sidebar.text_input(target_period_label, "2026年 夏（7月〜8月）")

past_period_instruction = ""
if use_past_comparison:
    past_period = st.sidebar.text_input("比較対象の過去時期（昨対など）", "2025年 夏（7月〜8月）")
    past_period_instruction = f"""
    **【時系列分析の必須指示】**
    まず、**「{past_period}」**に流行していた{broad_category}の主要トレンド（ヒット商品、味の傾向、キーワード）を特定してください。
    その上で、それらが**「{target_period}」**に向けてどう進化・変化するかを予測してください。
    （例：去年は「レモン」等の酸味が流行った → 消費者は酸味に慣れたため、次は「苦味」を加えた柑橘や、逆に「濃厚さ」への揺り戻しが起きている、など）
    """

# 4. トレンドの「発生要因」フィルター
trend_axis = st.sidebar.multiselect(
    "トレンドの兆候・ベクトル",
    [
        "食感の革新（とろとろ、ザクザク）",
        "ビジュアル（断面、巨大、極小）",
        "背徳感（ギルティ）",
        "ヘルシー（高タンパク、低糖質）",
        "レトロ・リバイバル",
        "異国情緒（韓国、イタリア、北欧等）",
        "季節性・旬（フルーツ、気温対応）"
    ],
    default=["食感の革新（とろとろ、ザクザク）", "季節性・旬（フルーツ、気温対応）"]
)

# 5. エリアと量
target_area = st.sidebar.text_input("調査対象エリア", "日本国内（専門店）、韓国、フランス、アメリカ")
min_count = st.sidebar.slider("最低収集件数の目安", 10, 50, 20, step=5)

# メインエリア
st.subheader(f"🔍 {target_period} トレンド予測 ({target_genre})")

if st.button("Deep Research用プロンプトを生成"):
    # ジャンル特記
    genre_instruction = ""
    if "未定義" in target_genre:
        genre_instruction = "既存カテゴリに収まらない、新しい形態・食感の商品を優先的に探してください。"
    elif target_genre != "指定なし（全域）":
        genre_instruction = f"「{target_genre}」およびその進化系を中心に探してください。"

    prompt_text = f"""
あなたは「トレンドの系譜」を読み解く熟練マーケターです。
GeminiのDeep Research機能を使用し、以下の時系列分析に基づいた商品トレンドを調査してください。

## 目的
{target_area}における、**{target_period}**にヒットするであろう{broad_category}の予測と具体例のリストアップ。
「数（Volume）」を出しつつ、過去からの「進化の文脈（Context）」を付与すること。

## 調査プロセス（時系列分析）
1. **過去の振り返り**: {past_period}に何が流行っていたか（味、食感、素材）を簡単に特定。
2. **現在の兆し**: その反動、あるいは進化系として、今イノベーター層の間で何が来ているか。
3. **未来の提案**: 上記を踏まえ、{target_period}に市場に受ける商品をリストアップ。

{past_period_instruction}

## 調査条件
* **重点ジャンル**: {target_genre} ({genre_instruction})
* **トレンドの兆候**: {", ".join(trend_axis)}
* **ターゲット**: イノベーター・アーリーアダプター層
* **収集数**: 妥協なく、**最低{min_count}件以上**リストアップすること。

## 出力フォーマット
見やすさのため、以下のブロック形式で{min_count}件以上記述してください。

---
### 【No.X】 商品名 / トレンド名
**(検索用キーワード)**

* **どんな商品か**:
    * 味、構成、食感、見た目。
* **トレンドの系譜（進化のロジック）**:
    * **Last Year ({past_period}頃)**: 似た文脈で流行ったもの（例：昨年のマリトッツォ）。
    * **Next Step**: なぜ今年、これが来るのか（例：クリーム過多に飽きた層に向けた、生地重視の進化系だから）。
* **販売現場のリアル**:
    * どこで（路面店/海外）、どんな雰囲気で売られているか。客層は？
* **コンビニ担当者へのメモ**:
    * どの棚（チルド/パン/常温）に置くべきか。
---
"""
    st.code(prompt_text, language="text")
    st.success("👆 「過去（昨年）のトレンド」を踏まえて「今年」を予測させるプロンプトです。季節商品の企画に特に有効です。")

# 結果格納エリア
st.markdown("---")
st.subheader("📝 調査結果のストック")
st.session_state.research_result = st.text_area(
    "Geminiからのレポートを貼り付け",
    value=st.session_state.research_result,
    height=600
)

# 簡易リスト化
if st.session_state.research_result:
    st.markdown("---")
    if st.button("会議用比較リストを作成"):
        formatting_prompt = f"""
あなたは編集者です。以下の調査レポートを、**「去年との比較」**がわかる会議用リストに変換してください。

## 原文データ
{st.session_state.research_result}

## 出力形式（Markdown Table）
| No | 今年の候補商品名 | 特徴・食感 | トレンドの系譜（去年は何だったか→今年はなぜこれか） | 販売スタイル |
|---|---|---|---|---|
| 1 | ... | ... | (例：昨年流行ったカヌレの進化系。より食感をソフトにしたもの) | ... |

※ 全ての商品を含めてください。
"""
        st.code(formatting_prompt, language="text")
