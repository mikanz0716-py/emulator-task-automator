import time
import subprocess
from typing import List, Dict, Any

# ==========================================
# ⚙️ 設定エリア
# ==========================================

# ADB実行ファイルの環境変数名またはパス（Windowsの例: 'HD-Adb.exe' またはフルパス）
# ※ 実際の環境に応じてユーザーが設定する想定
ADB_COMMAND = r"C:\Program Files\BlueStacks_nxt\HD-Adb.exe"

# 接続先デバイスアドレス (BlueStacksの一般的なアドレス)
ADB_DEVICE_ADDR = "127.0.0.1:5555"

# メインタスクの実行間隔（秒）
MAIN_TASK_INTERVAL_SEC = 7320 

# 各タップ操作間の基本待機時間（秒）
DEFAULT_TAP_DELAY = 2

# ==========================================
# 🗺️ メイン任務 タップ手順リスト
# 
# 座標と付随するアクションを抽象化し、コメントで示す。
# 'is_double_tap': 反応を良くするためのダブルタップ処理を行うか (True/False)
# ==========================================
MAIN_TASK_ACTIONS: List[Dict[str, Any]] = [
    # --- ルート1 (基本ルート) ---
    {"x": 1525, "y": 716, "action": "Start Button", "is_double_tap": True},
    {"x": 1455, "y": 87, "action": "Menu Button"},
    {"x": 323, "y": 117, "action": "Option A Selection"},
    {"x": 237, "y": 416, "action": "Sub Option 1"},
    {"x": 907, "y": 320, "action": "Confirm/Execute (Wait 1)"},
    {"x": 907, "y": 320, "action": "Confirm/Execute (Wait 2)"},
    
    # --- ルート2 (バリエーション) ---
    {"x": 1525, "y": 716, "action": "Start Button", "is_double_tap": True},
    {"x": 1455, "y": 87, "action": "Menu Button"},
    {"x": 323, "y": 117, "action": "Option A Selection"},
    {"x": 608, "y": 416, "action": "Sub Option 2"},
    {"x": 907, "y": 320, "action": "Confirm/Execute (Wait 1)"},
    {"x": 907, "y": 320, "action": "Confirm/Execute (Wait 2)"},
    
    # --- 新しいルート (追加分) ---
    {"x": 1525, "y": 716, "action": "Start Button", "is_double_tap": True},
    {"x": 1455, "y": 87, "action": "Menu Button"},
    {"x": 1650, "y": 141, "action": "Sub Menu Access"},
    {"x": 517, "y": 117, "action": "Option B Selection"},
    {"x": 235, "y": 424, "action": "Task Initiation"},
    {"x": 807, "y": 283, "action": "Final Confirmation (1)"},
    {"x": 807, "y": 283, "action": "Final Confirmation (2)"},
]

# ==========================================
# 🛠️ ADB操作用関数
# ==========================================
def adb_command(args: List[str]):
    """ADBコマンドを実行する共通関数"""
    # エラー出力を抑制
    full_cmd = [ADB_COMMAND] + args
    subprocess.run(full_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def adb_connect():
    """ADB接続を確立する"""
    print(f"Connecting to {ADB_DEVICE_ADDR}...")
    adb_command(["connect", ADB_DEVICE_ADDR])
    time.sleep(1)

def adb_tap(x: int, y: int, action_name: str, is_double_tap: bool = False):
    """指定座標をタップする"""
    shell_cmd = ["-s", ADB_DEVICE_ADDR, "shell", "input", "tap", str(x), str(y)]
    
    print(f"   タップ: ({x}, {y}) - {action_name}", end="")
    
    if is_double_tap:
        # 反応を良くするためダブルタップ気味に実行
        adb_command(shell_cmd)
        time.sleep(0.2) 
        adb_command(shell_cmd)
        print(" [Double Tap]")
    else:
        adb_command(shell_cmd)
        print(" [Single Tap]")
        
    time.sleep(DEFAULT_TAP_DELAY)

# ==========================================
# 🏃 メイン実行ループ
# ==========================================
def run_automation_loop():
    loop_count = 1
    
    while True:
        print(f"\n=== 自動タスク実行開始 (回数: {loop_count}) ===")
        
        # 最初のスタートボタンを押す（念のため）
        # ※ デモとして、ここでは特定の座標に依存しない処理は行わない
        adb_tap(1525, 716, "Return to Start Screen", is_double_tap=True) 
        time.sleep(2)

        # 設定された手順を順番に実行
        total_steps = len(MAIN_TASK_ACTIONS)
        for i, action in enumerate(MAIN_TASK_ACTIONS, 1):
            print(f"[{i}/{total_steps}]", end="")
            adb_tap(
                action["x"],
                action["y"],
                action["action"],
                action.get("is_double_tap", False)
            )

        print("=== サイクル完了 ===")
        print(f"次回実行まで {MAIN_TASK_INTERVAL_SEC}秒 待機します...")
        
        # 待機処理
        time.sleep(MAIN_TASK_INTERVAL_SEC)
        loop_count += 1

# ==========================================
# 起動ブロック
# ==========================================
if __name__ == "__main__":
    adb_connect()
    print("=== ADB/Androidエミュレータ自動化システム ===")
    print(f"- 実行間隔: {MAIN_TASK_INTERVAL_SEC}秒 (約{MAIN_TASK_INTERVAL_SEC/3600:.2f}時間)")
    print(f"- 合計アクション数: {len(MAIN_TASK_ACTIONS)}")
    print("停止するには Ctrl+C を押してください。")
    time.sleep(3)

    try:
        run_automation_loop()
    except KeyboardInterrupt:
        print("\nシステムを停止しました。")