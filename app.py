import streamlit as st
import pandas as pd

st.set_page_config(page_title="社内ツールポータル", page_icon="🔗", layout="wide")

@st.cache_data
def load_links(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # 欠損対策
    for col in ["category", "name", "url", "desc", "tags"]:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("").astype(str)
    return df

st.title("🔗 社内ツールポータル")
st.caption("URL一覧（links.csv）を編集すると自動で反映できます。")

DATA_PATH = "links.csv"
df = load_links(DATA_PATH)

# 検索・絞り込み
left, right = st.columns([1, 3], gap="large")

with left:
    q = st.text_input("検索（名前/説明/タグ）", "")
    categories = ["すべて"] + sorted([c for c in df["category"].unique() if c.strip() != ""])
    cat = st.selectbox("カテゴリ", categories, index=0)
    st.divider()
    st.write("📌 件数:", len(df))

with right:
    view = df.copy()

    if cat != "すべて":
        view = view[view["category"] == cat]

    if q.strip():
        key = q.strip().lower()
        view = view[
            view["name"].str.lower().str.contains(key)
            | view["desc"].str.lower().str.contains(key)
            | view["tags"].str.lower().str.contains(key)
            | view["url"].str.lower().str.contains(key)
        ]

    # カード表示
    if view.empty:
        st.info("該当するリンクがありません。")
    else:
        # カテゴリごとにまとめて表示
        for c, g in view.sort_values(["category", "name"]).groupby("category"):
            st.subheader(c if c.strip() else "未分類")
            cols = st.columns(3, gap="medium")

            for i, (_, r) in enumerate(g.iterrows()):
                with cols[i % 3]:
                    st.markdown(f"### {r['name']}")
                    if r["desc"].strip():
                        st.write(r["desc"])
                    if r["tags"].strip():
                        st.caption(f"🏷️ {r['tags']}")
                    st.link_button("開く", r["url"], use_container_width=True)
            st.divider()
