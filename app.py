import streamlit as st
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="トレンド・タイムマシン・プロンプト",
    page_icon="🥐",
    layout="centered"
)

# タイトルと説明
st.title("🥐 トレンド・タイムマシン")
st.markdown("""
過去の流行調査用プロンプト生成ツールです。
調査したい「対象」「時期」「地域」を入力すると、Gemini Deep Research用の強力なプロンプトを作成します。
""")

st.divider()

# --- 入力フォーム ---

col1, col2 = st.columns(2)

with col1:
    # 調査対象（デフォルトはスイーツだが変更可能）
    target_item = st.text_input("調査対象（例：スイーツ、パン、タピオカ）", value="スイーツ・パン")

with col2:
    # 時期指定
    current_year = datetime.now().year
    start_year = st.number_input("開始年", min_value=1950, max_value=current_year, value=2010)
    end_year = st.number_input("終了年", min_value=1950, max_value=current_year, value=2015)

# 地域指定（複数選択可能に）
# よくある地域をプリセットしつつ、自由入力も追加できるようにする
default_regions = ["日本全国", "東京", "大阪", "韓国", "台湾", "ニューヨーク", "パリ"]
selected_regions = st.multiselect(
    "調査対象の地域（複数選択可）",
    options=default_regions,
    default=["日本全国"]
)

# 自由記述の地域追加（もしリストにない場合）
custom_region = st.text_input("その他の地域（上記にない場合入力）")
if custom_region:
    selected_regions.append(custom_region)

# --- プロンプト生成ロジック ---

if st.button("プロンプトを作成する", type="primary"):
    
    # 地域リストを文字列化
    regions_str = "、".join(selected_regions)
    if not regions_str:
        regions_str = "特に指定なし（世界的なトレンド含む）"

    # プロンプト本文
    prompt_text = f"""
あなたはプロフェッショナルな「トレンドリサーチャー」兼「文化史家」です。
以下のテーマについて、Geminiの検索能力（Deep Research）を最大限に活用し、徹底的な調査を行ってください。

## 調査テーマ
* **対象:** {target_item}
* **期間:** {start_year}年 〜 {end_year}年
* **地域:** {regions_str}

## 「流行った」の定義と基準
1.  **認知度:** 当時を知る人が「あー、それあったね！」「懐かしい！」と共感できるレベルの認知度があるもの。
2.  **メディア露出:** 雑誌、テレビ番組、ニュースなどで特集が組まれた実績があるもの。
3.  **社会的現象:** 行列ができた、売り切れが続出した、SNS（ブログ、Twitter/X、Instagram等）で話題になったもの。

## 重要な制約事項（必ず守ってください）
1.  **「数」を最優先してください:** 代表的な3〜5個に絞ることは**禁止**です。AIによる勝手な選抜や要約を行わず、Deep Researchで見つかる限り**As much as possible（可能な限り全て）**列挙してください。
2.  **証拠の提示:** なぜそれが流行ったと言えるのか、具体的な「証拠（当時のメディア掲載、販売数、ブームの背景、SNSでの反応など）」を必ず記載してください。
3.  **網羅性:** 一過性のブームだけでなく、その時期に定着し始めたものも含めてください。

## 出力フォーマット
情報は以下の表形式で整理して出力してください。数が多いため、必要であれば表を分割しても構いません。

| 品目名（商品名） | 発祥/流行地域 | 流行時期（ピーク） | 流行の証拠・背景・数値データ | 概要・特徴 |
| :--- | :--- | :--- | :--- | :--- |
| (例) マリトッツォ | イタリア→日本 | 2021年頃 | Instagramでの投稿数激増、カルディでの売り切れ続出 | ブリオッシュ生地に生クリームを挟んだ菓子 |

**リサーチを開始してください。**
"""

    st.success("プロンプトを作成しました！右上のコピーボタンを押してGeminiに貼り付けてください。")
    
    # プロンプトの表示（コピーボタン付き）
    st.code(prompt_text, language="markdown")

    st.info("💡 **Tips:** Geminiからの回答が途中で止まった場合は、「続けて」と入力するか、「表の続きを出力して」と指示してください。")
