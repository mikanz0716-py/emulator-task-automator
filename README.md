# emulator-task-automator
A practical Python script using ADB (Android Debug Bridge) to automate repetitive tasks on Android emulators. Reduces working hours by systematically executing coordinate-based inputs.
---

# 📊 Webデータ抽出・整形デモ (Pandasを活用)

## 🎯 プロジェクトの概要
このスクリプトは、Webデータ（ローカルHTML）から構造化された情報を抽出し、PythonのPandasライブラリを使用して**集計・分析可能なCSVファイルに整形**するプロセスを示します。

## ✨ 技術的なアピールポイント
- **データ収集・整形能力**: `BeautifulSoup`でデータ抽出を行い、`Pandas`でデータフレームに変換し、平均スコアの算出（簡単な分析）を実行しています。
- **堅牢なデモ設計**: 外部Webアクセスに依存せず、ローカルのダミーファイル (`demo_data.html`) からデータを読み込むため、誰でも簡単に動作確認が可能です。

## 🛠️ ファイル構成と実行方法
- **入力ファイル:** `demo_data.html`
- **出力ファイル:** `extracted_reviews_data.csv`
- **実行コマンド:**
    ```bash
    # 環境に合わせてPythonのフルパスを指定
    [Pythonのパス] web_scraper.py
    ```
    ---

# 🔍 高度な画像認識・条件分岐デモ

## 🎯 プロジェクトの概要
`OpenCV` を活用し、画面上の特定のアイコンをリアルタイムで検出し、それに基づいた操作の自動分岐を行うスクリプトです。

## ✨ 技術的なアピールポイント
- **画像処理**: `OpenCV` によるテンプレートマッチング。
- **リアルタイム解析**: `mss` ライブラリによる高速キャプチャ。