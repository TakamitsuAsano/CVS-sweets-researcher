import streamlit as st

# ページ設定
st.set_page_config(
    page_title="CVS Sweets & Bread Planner (Max Volume)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
if 'research_result' not in st.session_state:
    st.session_state.research_result = ""
if 'logic_added_result' not in st.session_state:
    st.session_state.logic_added_result = ""
if 'fgi_plan' not in st.session_state:
    st.session_state.fgi_plan = ""
if 'fgi_transcript' not in st.session_state:
    st.session_state.fgi_transcript = ""

# サイドバー：ナビゲーション
st.sidebar.title("企画プロセス（網羅重視版）")
phase = st.sidebar.radio(
    "フェーズを選択してください",
    [
        "1. 広域調査 (Deep Research)", 
        "2. ロジック付与 (Logic Mapping)", 
        "3. FGI計画 (Concept Validation)", 
        "4. 全量提案資料 (Trend Map Proposal)"
    ]
)

st.title("🍩 コンビニスイーツ・パン 網羅的トレンド発掘アプリ")

# --- フェーズ1: 調査 ---
if phase == "1. 広域調査 (Deep Research)":
    st.header("1. イノベーター層のトレンド全量調査")
    st.info("市場の16%（イノベーター・アーリーアダプター）が反応している「兆し」を、可能な限り数多くリストアップするためのプロンプトを発行します。")

    category = st.selectbox("対象カテゴリー", ["スイーツ", "パン", "総菜パン"])
    target_area = st.text_input("調査対象エリア", "日本国内およびスイーツ・パン先進国（フランス、韓国、イタリア、アメリカ等）")
    
    # プロンプト生成ボタン
    if st.button("数重視：調査用プロンプトを生成"):
        prompt_text = f"""
あなたは徹底的なトレンドハンターです。
以下の条件で、GeminiのDeep Research機能（または高度検索）を使用し、現在「イノベーター」および「アーリーアダプター」層（市場の先行16%）の間で話題になっている、または胎動し始めている「{category}」を調査してください。

## 最重要指示
**「絞り込み」や「厳選」は一切不要です。**
「これから来るかもしれない」と思われる情報は、些細な兆候であっても**可能な限り数多く（質より量を重視して）網羅的にリストアップ**してください。
数十件以上のリストになっても構いません。

## 調査対象
エリア：{target_area}
ターゲット：感度の高いインフルエンサー、パティシエ、特定界隈のオタク層が熱狂しているもの。

## 出力形式
以下の項目を含む**表形式（MarkdownのTable）**で出力してください。

| 商品・トレンド名 | 発祥・オリジン | 反応している層・エビデンス | 特徴・キーワード |
| --- | --- | --- | --- |
| (名称) | (どこの国の誰発か) | (SNSでの具体的な反応、行列の有無など) | (味、食感、見た目の特徴) |
| ... | ... | ... | ... |

※ リストは長くて構いません。とにかく「見逃し」がないように拾い上げてください。
"""
        st.code(prompt_text, language="text")
        st.success("👆 このプロンプトをコピーして、Gemini Advanced (Deep Research) に入力し、大量のリストを出力させてください。")

    # 結果入力欄
    st.subheader("Geminiからの大量リストアップ結果を入力")
    st.session_state.research_result = st.text_area(
        "調査結果（表形式のデータ）をここに全て貼り付けてください", 
        value=st.session_state.research_result, 
        height=400
    )

# --- フェーズ2: ロジック付与 ---
elif phase == "2. ロジック付与 (Logic Mapping)":
    st.header("2. コンビニ導入ロジックの付与")
    st.info("調査で挙がった大量の商品候補を**一つも捨てることなく**、全てに対して「コンビニで採用すべき理由」を付記します。スクリーニングはしません。")

    if not st.session_state.research_result:
        st.warning("⚠️ フェーズ1で調査結果を入力してください。")
    else:
        if st.button("全量ロジック付与プロンプトを生成"):
            logic_prompt = f"""
あなたは大手コンビニの商品開発コンサルタントです。
入力された「トレンド候補リスト（全量）」の**全ての商品に対して**、コンビニの商品開発担当者が社内稟議を通すための「ロジック」を付記してください。
**商品の選別や削除は絶対に行わないでください。全ての候補を表に残してください。**

## 入力データ（トレンドリスト）
{st.session_state.research_result}

## 依頼内容
上記の表に、以下の2列を追加して再出力してください。

1. **過去ヒット商品の系譜（リネージ）**: 
   - 「過去に流行った〇〇の進化版」「〇〇と〇〇のハイブリッド」というように、おじさん世代の上司でも理解できる既存のヒット文脈に紐づけて説明してください。
2. **コンビニ展開の可能性**: 
   - これをコンビニでやるならどういう切り口なら可能か（例：「専門店のような生クリームは無理だが、食感を強調すればいける」など）の前向きな仮説。

## 出力形式
Markdownの表形式で、元の列に上記2列を加えた完全なリストを出力してください。
"""
            st.code(logic_prompt, language="text")
            st.success("👆 このプロンプトをGeminiに入力してください。リストの数はそのままで、説得ロジックが追加されます。")

    st.subheader("ロジック付与済みのリストを入力")
    st.session_state.logic_added_result = st.text_area(
        "ロジックが付与された完全リストをここに貼り付けてください", 
        value=st.session_state.logic_added_result, 
        height=400
    )

# --- フェーズ3: FGI計画 ---
elif phase == "3. FGI計画 (Concept Validation)":
    st.header("3. カテゴリ別コンセプト検証計画")
    st.info("候補数が多いため、個別の商品テストではなく、似た傾向の商品を「コンセプト群」としてグルーピングし、FGIで方向性を検証する計画を立てます。")

    if not st.session_state.logic_added_result:
        st.warning("⚠️ フェーズ2でリストを入力してください。")
    else:
        participants_count = st.slider("FGI参加人数", 4, 10, 6)
        
        if st.button("グルーピング＆FGI計画プロンプトを生成"):
            fgi_prompt = f"""
あなたは定性調査のプロです。
現在、手元に大量の「新商品アイデアリスト」があります。これら全てを個別にFGIにかけるのは不可能です。
したがって、リストにある商品を**「いくつかの大きなトレンドの波（コンセプトグループ）」**に分類し、その「方向性」が消費者に刺さるかを検証するFGIを設計してください。

## 商品アイデアリスト（全量）
{st.session_state.logic_added_result}

## 依頼内容
1. **コンセプトのグルーピング**:
   - 上記のリストを、消費者のベネフィットやトレンドの背景ごとに、3〜5つの大きなグループ（例：「背徳感×ヘルシー系」「ネオ・レトロ系」など）に分類し、各グループに属する代表商品をリストから割り当ててください。

2. **FGIリクルーティングと質問設計**:
   - 参加人数: {participants_count}名
   - 上記の「3〜5つのコンセプトグループ」を提示した際、参加者がどの方向性に最も食いつくか、または拒絶反応を示すかを確認するための質問リストを作成してください。
   - 個別の商品名ではなく、「こういう気分の時に、こういう食感のものがコンビニにあったら？」という文脈での検証項目を挙げてください。
"""
            st.code(fgi_prompt, language="text")
            st.success("👆 大量のアイデアをカテゴライズし、検証するための計画書を作成させます。")

    st.subheader("FGI計画・結果メモ")
    st.session_state.fgi_plan = st.text_area("FGI計画・カテゴライズ結果", value=st.session_state.fgi_plan, height=200)
    
    st.subheader("FGI実施後の議事録")
    st.session_state.fgi_transcript = st.text_area("FGIでの消費者の反応（どのカテゴリが好評だったか等）", value=st.session_state.fgi_transcript, height=300)

# --- フェーズ4: 全量提案 ---
elif phase == "4. 全量提案資料 (Trend Map Proposal)":
    st.header("4. トレンドマップ型 企画提案")
    st.info("調査した大量のアイデアを「トレンドマップ」として提示しつつ、FGIで裏付けられた「当たりそうなゾーン」を強調した資料構成案を作ります。")

    if st.button("提案資料構成プロンプトを生成"):
        final_prompt = f"""
あなたは戦略プランナーです。
コンビニチェーンに対して、向こう12ヶ月のスイーツ・パンの「トレンド全体像（Trend Map）」を提案します。
特定の1品を提案するのではなく、**「世界中の兆し（全量リスト）」を見せつつ、「特に注力すべきゾーン」をハイライトする**形式のプレゼン資料構成を作ってください。

## 入力情報
【1. トレンド全量リストとロジック】
{st.session_state.logic_added_result}

【2. FGIによる検証結果（注力すべきゾーン）】
{st.session_state.fgi_transcript}

## 資料作成指示（Genspark等用）
以下の構成でスライド案を作成してください。

1. **表紙**: インパクトのあるタイトル（「202X年 スイーツトレンド全展望」など）
2. **市場鳥瞰図（全体像）**:
   - 調査で挙がった大量の商品群をマトリクス（例：濃厚vsさっぱり、伝統vs革新）に配置した図解の指示。
   - 「これだけのシーズ（種）が世界にはある」という圧倒的な網羅感を出すスライド。
3. **注力すべき3〜4つの潮流（Focus Areas）**:
   - FGIの結果、特に有望だったグループの提示。
   - 各グループに含まれる具体的な商品例（リストから抜粋）。
   - 各グループに対する「コンビニ的解釈（過去の系譜ロジック）」の解説。
4. **担当者への提言**:
   - 「まずこのカテゴリの、この商品から着手すべき」というロードマップ。
   
数多くの選択肢を提示しつつ、プロとして「ここを狙うべき」というナビゲーションを行う構成にしてください。
"""
        st.code(final_prompt, language="text")
        st.success("👆 網羅性と方向性を両立させた提案資料作成プロンプトです。")