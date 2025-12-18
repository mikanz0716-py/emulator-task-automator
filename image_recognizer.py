import cv2
import numpy as np
import mss
import time
from typing import Optional, Tuple

# ==========================================
# ⚙️ 設定エリア
# ==========================================
# 検出対象のテンプレートファイル名（保存した画像名と一致させてください）
TEMPLATE_OK_FILE = "template_ok.png"
TEMPLATE_ERROR_FILE = "template_error.png"

# 検出のしきい値 (0.85 = 85%の一致度が必要)
# 誤検知が多い場合は数値を上げ、見つからない場合は少し下げてください。
THRESHOLD = 0.85 

# 画面スキャン間隔（秒）
SCAN_INTERVAL_SEC = 1.0 

# ==========================================
# 🔍 画像認識コア関数
# ==========================================

def load_templates():
    """保存された画像を読み込み、グレースケールに変換する"""
    ok_template = cv2.imread(TEMPLATE_OK_FILE, cv2.IMREAD_GRAYSCALE)
    error_template = cv2.imread(TEMPLATE_ERROR_FILE, cv2.IMREAD_GRAYSCALE)
    
    if ok_template is None or error_template is None:
        print("❌ エラー: 画像ファイルが読み込めません。")
        print(f"フォルダ内に {TEMPLATE_OK_FILE} と {TEMPLATE_ERROR_FILE} があるか確認してください。")
        return None, None
        
    return ok_template, error_template

def find_template_on_screen(template, threshold: float) -> Optional[Tuple[int, int]]:
    """
    現在のPC画面から指定された画像を検索し、中心座標を返す。
    """
    with mss.mss() as sct:
        # メインモニターをキャプチャ
        monitor = sct.monitors[1]
        screenshot = np.array(sct.grab(monitor))

    # 画面をモノクロに変換して処理速度を向上
    screen_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    # テンプレートマッチング実行
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result) 
    
    # しきい値を超えた一致度があるか確認
    if max_val >= threshold:
        w, h = template.shape[::-1]
        
        # 画面上の絶対座標を計算
        center_x = max_loc[0] + w // 2 + monitor["left"]
        center_y = max_loc[1] + h // 2 + monitor["top"]

        return (center_x, center_y)
    else:
        return None

# ==========================================
# 🖥️ メインループ
# ==========================================

def run_image_recognizer():
    ok_template, error_template = load_templates()
    if ok_template is None:
        return 

    print("=== 🛠️ 画像認識条件分岐システム 起動 ===")
    print(f"設定: 一致度 {THRESHOLD * 100:.0f}% 以上で検知")
    print("動作テスト: ブラウザに表示されたアイコンを映してください。")
    print("終了するには Ctrl+C を押してください。")
    print("-" * 40)

    try:
        while True:
            # 1. OKボタンの検出
            ok_pos = find_template_on_screen(ok_template, THRESHOLD)
            if ok_pos:
                print(f"✅ [検知] OKボタンを確認しました。 座標: {ok_pos}")
                print("   >> アクション: 処理を継続します。")
                time.sleep(1) # 重複検知防止
                continue

            # 2. エラーアイコンの検出
            error_pos = find_template_on_screen(error_template, THRESHOLD)
            if error_pos:
                print(f"🛑 [検知] 警告アイコンを確認しました。 座標: {error_pos}")
                print("   >> アクション: エラー回避のためシステムを停止します。")
                break # 危険を察知してループ終了

            # 3. どちらも見つからない場合
            print("... スキャン中: アイコンは見つかりません。")
            time.sleep(SCAN_INTERVAL_SEC)
            
    except KeyboardInterrupt:
        print("\n👋 ユーザーによる停止を確認しました。")
        
    print("=== システム終了 ===")

if __name__ == "__main__":
    run_image_recognizer()