import pandas as pd
from bs4 import BeautifulSoup
import os
from typing import List, Dict, Any

# ==========================================
# ⚙️ 設定エリア
# ==========================================
# 処理対象のローカルHTMLファイル名
INPUT_FILENAME = "demo_data.html"
# 出力するCSVファイル名
OUTPUT_FILENAME = "extracted_reviews_data.csv"
# 評価の星マークと数値の対応
RATING_MAP = {
    "★★★★★": 5,
    "★★★★☆": 4,
    "★★★☆☆": 3,
    "★★☆☆☆": 2,
    "★☆☆☆☆": 1,
}

# ==========================================
# 🔍 データ抽出・整形関数
# ==========================================

def extract_and_transform_data(html_content: str) -> List[Dict[str, Any]]:
    """HTMLコンテンツから必要なデータを抽出し、整形する"""
    soup = BeautifulSoup(html_content, 'html.parser')
    all_reviews = []

    # 'review-card'クラスを持つ要素をすべて取得
    review_elements = soup.find_all('div', class_='review-card')

    if not review_elements:
        print("Error: 'review-card'要素が見つかりませんでした。")
        return []

    for card in review_elements:
        # 1. データ抽出
        product_name = card.find('h2', class_='product-name').text.strip() if card.find('h2', class_='product-name') else "N/A"
        rating_stars = card.find('span', class_='rating').text.strip() if card.find('span', class_='rating') else "N/A"
        comment = card.find('p', class_='comment').text.strip() if card.find('p', class_='comment') else ""
        date = card.find('span', class_='date').text.strip() if card.find('span', class_='date') else "N/A"
        review_id = card.get('data-id', 'N/A')

        # 2. データ整形（トランスフォーム）
        rating_score = RATING_MAP.get(rating_stars, 0)
        comment_length = len(comment)
        
        # 抽出データをリストに追加
        all_reviews.append({
            "Review ID": review_id,
            "Product Name": product_name,
            "Rating Score": rating_score,
            "Comment Length": comment_length,
            "Review Date": date,
            "Comment Snippet": comment[:20] + "..." if len(comment) > 20 else comment
        })

    return all_reviews

# ==========================================
# 📊 メイン実行ブロック
# ==========================================
def run_data_processor():
    # 1. ファイルの存在確認
    if not os.path.exists(INPUT_FILENAME):
        print(f"致命的なエラー: 入力ファイル '{INPUT_FILENAME}' が見つかりません。")
        print("実行前に 'demo_data.html' を同じフォルダに作成してください。")
        return
    
    # 2. HTMLコンテンツの読み込み
    with open(INPUT_FILENAME, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    print(f"=== Web Scraper and Data Processor Start (Source: {INPUT_FILENAME}) ===")
    
    # 3. データ抽出と整形
    processed_data = extract_and_transform_data(html_content)
    
    if not processed_data:
        print("データが抽出されませんでした。終了します。")
        return

    # 4. Pandas DataFrameに変換
    df = pd.DataFrame(processed_data)
    
    # 5. データ分析のデモ（簡単な集計）
    print("\n--- Data Analysis Sample ---")
    print(f"Total reviews collected: {len(df)}")
    print(f"Average Rating Score: {df['Rating Score'].mean():.2f}")
    
    # 6. データをCSVとして保存
    df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
    print(f"\n✅ Data successfully saved to {OUTPUT_FILENAME}")
    
    # 7. 結果の表示
    print("\n[Head of Output Data]")
    print(df)


if __name__ == "__main__":
    run_data_processor()