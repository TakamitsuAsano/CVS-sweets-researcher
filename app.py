import streamlit as st
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="トレンド・タイムマシン・プロンプト",
    page_icon="🥐",
    layout="wide"  # 横長レイアウトにして見やすくします
)

# タイトルと説明
st.title("🥐 トレンド・タイムマシン")
st.markdown("""
過去の流行調査用プロンプト生成ツールです。
調査したい「対象」「時期」「地域」を入力すると、Gemini Deep Research用の強力なプロンプトを作成します。
""")

st.divider()

# --- 入力フォーム ---

# レイアウトを2カラムに分割
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("1. 調査対象と地域")
    
    # 調査対象
    target_item = st.text_input(
        "調査対象（自由入力）", 
        value="スイーツ・パン",
        help="例：タピオカ、高級食パン、平成レトロスイーツ など"
    )

    # 地域指定
    default_regions = ["日本全国", "東京", "大阪", "韓国", "台湾", "ニューヨーク", "パリ"]
    selected_regions = st.multiselect(
        "調査地域（複数選択可）",
        options=default_regions,
        default=["日本全国"]
    )
    
    # 自由記述の地域追加
    custom_region = st.text_input("その他の地域（リストにない場合）", placeholder="例：福岡、原宿、ロンドン")
    if custom_region:
        # 重複していなければ追加
        if custom_region not in selected_regions:
            selected_regions.append(custom_region)

with col_right:
    st.subheader("2. 期間指定")
    st.caption("月は「指定なし」のままでもOKです。")
    
    current_year = datetime.now().year
    
    # 月の選択肢（先頭に指定なし）
    month_options = ["指定なし"] + [f"{i}月" for i in range(1, 13)]

    # --- 開始時期 ---
    st.markdown("**開始時期**")
    c1, c2 = st.columns(2)
    with c1:
        start_year = st.number_input("開始年", min_value=1950, max_value=current_year, value=2010, key="s_year")
    with c2:
        start_month = st.selectbox("開始月", options=month_options, key="s_month")

    # --- 終了時期 ---
    st.markdown("**終了時期**")
    c3, c4 = st.columns(2)
    with c3:
        end_year = st.number_input("終了年", min_value=1950, max_value=current_year, value=2015, key="e_year")
    with c4:
        end_month = st.selectbox("終了月", options=month_options, key="e_month")

# --- プロンプト生成ロジック ---

st.divider()

if st.button("プロンプトを作成する", type="primary", use_container_width=True):
    
    # 1. 地域リストの整形
    final_regions = selected_regions.copy()
    regions_str = "、".join(final_regions)
    if not regions_str:
        regions_str = "特に指定なし（世界的なトレンド含む）"

    # 2. 期間の整形関数
    def format_period(year, month_str):
        if month_str == "指定なし":
            return f"{year}年"
        else:
            return f"{year}年{month_str}"

    start_str = format_period(start_year, start_month)
    end_str = format_period(end_year, end_month)

    # 3. プロンプト本文の構築
    prompt_text = f"""
あなたはプロフェッショナルな「トレンドリサーチャー」兼「文化史家」です。
以下のテーマについて、Geminiの検索能力（Deep Research）を最大限に活用し、徹底的な調査を行ってください。

## 調査テーマ
* **対象:** {target_item}
* **期間:** {start_str} 〜 {end_str}
* **地域:** {regions_str}

## 「流行った」の定義と基準
1.  **認知度:** 当時を知る人が「あー、それあったね！」「懐かしい！」と共感できるレベルの認知度があるもの。
2.  **メディア露出:** 雑誌、テレビ番組、ニュースなどで特集が組まれた実績があるもの。
3.  **社会的現象:** 行列ができた、売り切れが続出した、SNS（ブログ、Twitter/X、Instagram等）で話題になったもの。

## 重要な制約事項（必ず守ってください）
1.  **「数」を最優先してください:** 代表的な数個に絞ることは**禁止**です。AIによる勝手な選抜や要約を行わず、Deep Researchで見つかる限り**As much as possible（可能な限り全て）**列挙してください。
2.  **証拠の提示:** なぜそれが流行ったと言えるのか、具体的な「証拠（当時のメディア掲載、販売数、ブームの背景、SNSでの反応など）」を必ず記載してください。
3.  **網羅性:** 一過性のブームだけでなく、その時期に定着し始めたものも含めてください。指定期間内（{start_str}〜{end_str}）のトレンド推移も意識してください。

## 出力フォーマット
情報は以下の表形式で整理して出力してください。数が多いため、必要であれば表を分割しても構いません。

| 品目名（商品名） | 発祥/流行地域 | 流行時期（ピーク） | 流行の証拠・背景・数値データ | 概要・特徴 |
| :--- | :--- | :--- | :--- | :--- |
| (例) マリトッツォ | イタリア→日本 | 2021年春頃 | Instagramでの投稿数激増、カルディでの売り切れ続出 | ブリオッシュ生地に生クリームを挟んだ菓子 |

**リサーチを開始してください。**
"""

    st.success("プロンプトを作成しました！右上のコピーボタンを押してGeminiに貼り付けてください。")
    
    # プロンプトの表示
    st.code(prompt_text, language="markdown")
    
    st.info("💡 **Tips:** 期間を「月」まで指定した場合、Geminiはその特定の月の季節性（例：ハロウィン、クリスマス商戦など）も考慮して検索するようになります。")
