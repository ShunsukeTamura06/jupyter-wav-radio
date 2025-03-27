import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import time
import glob # ファイルリスト取得用
import os   # パス操作用
import base64
import io
import wave # WAVファイルの長さ取得用
# import soundfile as sf # soundfileを使う場合

# --- 設定 ---
# !!! 重要: ご自身のWAVファイルが保存されているディレクトリパスに変更してください !!!
# 例: audio_dir = 'C:/Users/YourUser/Music/MyRadioFiles/'
#     audio_dir = './wav_files/' # Notebookと同じ階層のwav_filesフォルダ
audio_dir = './'  # Notebookと同じディレクトリにあるWAVファイルを検索する場合
file_pattern = os.path.join(audio_dir, '*.wav')
audio_files = sorted(glob.glob(file_pattern)) # ファイル名でソート

if not audio_files:
    print(f"エラー: 指定されたディレクトリ '{audio_dir}' にWAVファイルが見つかりません。")
    print("`audio_dir` 変数を確認してください。")
    # ここで処理を中断するか、適切にハンドリングしてください
    # raise FileNotFoundError(f"No WAV files found in '{audio_dir}'")

# --- ヘルパー関数 ---

def get_wav_duration(filepath):
    """WAVファイルの再生時間を秒単位で取得する"""
    try:
        with wave.open(filepath, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
            return duration
    except Exception as e:
        print(f"警告: ファイル '{os.path.basename(filepath)}' の長さ取得エラー: {e}")
        return 0 # エラー時は0秒を返す

# soundfileを使う場合 (より多くの形式に対応)
# def get_audio_duration_sf(filepath):
#     try:
#         with sf.SoundFile(filepath) as f:
#             return len(f) / f.samplerate
#     except Exception as e:
#         print(f"警告: ファイル '{os.path.basename(filepath)}' の長さ取得エラー: {e}")
#         return 0

def create_hidden_audio_html(audio_bytes):
    """非表示で自動再生するAudioタグのHTMLを生成する"""
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    # display: none で非表示、autoplayで自動再生
    html_code = f"""
    <audio autoplay style="display: none;">
      <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
      Your browser does not support the audio element.
    </audio>
    """
    return HTML(html_code)

# --- UIのセットアップ ---
# ファイルリスト表示用のHTMLウィジェットを作成
file_list_display = widgets.HTML(
    value="<p>ラジオを初期化中...</p>",
    placeholder='ファイルリスト',
    description='再生リスト:',
)
# オーディオ表示用の出力ウィジェット (ここに非表示のAudioタグを挿入/更新する)
# これにより、リスト表示とは別の場所にオーディオ出力が管理される
audio_output_area = widgets.Output()

# ウィジェットをNotebookに表示
display(file_list_display, audio_output_area)

# --- 再生ループ ---
try:
    print(f"再生を開始します。ファイル数: {len(audio_files)}")
    print("ループを停止するには、Jupyterの■ (Interrupt kernel) ボタンを押してください。")

    while True: # 無限ループ (ラジオのように)
        for filepath in audio_files:
            filename = os.path.basename(filepath)

            # --- 1. ファイルリストのHTMLを生成して更新 ---
            html_items = []
            for f_path in audio_files:
                f_name = os.path.basename(f_path)
                if f_path == filepath:
                    # 現在再生中のファイルを強調表示 (太字、色変更など)
                    html_items.append(f'<li style="color: #1E90FF; font-weight: bold;">▶ {f_name}</li>')
                else:
                    html_items.append(f'<li>{f_name}</li>')

            # ウィジェットの値を更新して表示を変更
            file_list_display.value = f'<ul style="list-style-type: none; padding-left: 0; margin: 0;">{"".join(html_items)}</ul>'

            # --- 2. 音声ファイルを読み込み、再生時間を取得 ---
            try:
                with open(filepath, 'rb') as f:
                    audio_bytes = f.read()
                # duration = get_audio_duration_sf(filepath) # soundfile使う場合
                duration = get_wav_duration(filepath)

                if duration <= 0:
                    print(f"ファイル '{filename}' の再生時間が0秒以下のためスキップします。")
                    continue # 次のファイルへ

            except FileNotFoundError:
                print(f"エラー: ファイル '{filename}' が見つかりません。スキップします。")
                # リストから削除するなどの処理も可能
                time.sleep(1) # エラー時にCPUを使いすぎないように少し待つ
                continue
            except Exception as e:
                print(f"エラー: ファイル '{filename}' の読み込み中に問題が発生しました: {e}")
                time.sleep(1)
                continue

            # --- 3. 非表示のAudioタグを生成し、専用エリアに表示 ---
            audio_html = create_hidden_audio_html(audio_bytes)
            with audio_output_area:
                clear_output(wait=True) # 前回のAudioタグを消去
                display(audio_html)     # 新しいAudioタグを表示して再生開始

            # --- 4. 音声の再生時間だけ待機 ---
            # 少しバッファを持たせても良いかもしれない
            # time.sleep(duration + 0.1)
            try:
                time.sleep(duration)
            except KeyboardInterrupt:
                # time.sleep中にCtrl+Cが押された場合
                print("\nループ中に停止が要求されました。")
                raise # ループを抜けるために例外を再発生させる

        print("ファイルリストの最後まで再生しました。最初から繰り返します。")
        # リストの最後に達したら少し待つ場合
        # time.sleep(1)

except KeyboardInterrupt:
    # ループの外でCtrl+C (Interrupt kernel) が押された場合
    print("\n再生がユーザーによって停止されました。")
    file_list_display.value = "<p>再生停止</p>"
    with audio_output_area:
        clear_output() # 最後のAudioタグも消す
except Exception as e:
    print(f"\n予期せぬエラーが発生しました: {e}")
    file_list_display.value = f"<p>エラー発生: {e}</p>"
finally:
    print("ラジオプログラムを終了します。")