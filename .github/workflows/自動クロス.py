import requests
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import threading

# DiscordのウェブフックURLを設定
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1341405121938194442/Jyx6A3Pmx9r3Tys7m1ouJ8n-_GaiLtZ7lsQXQ_vPbHuKpo1KisnHbzT6NWszrp5BNvk2'

def send_discord_notify(message):
    url = DISCORD_WEBHOOK_URL
    headers = {"Content-Type": "application/json"}
    payload = {"content": message}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        logging.info('通知が送信されました')
    else:
        logging.error('通知の送信に失敗しました')

def perform_operations(url, input1, input2, input3, input4, input_value, user_agent, final_xpath):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={user_agent}")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://trade.smbcnikko.co.jp/Etc/1/webtoppage/")

    # 入力フィールドに値を入力
    pad_input_0 = driver.find_element(By.ID, "padInput0")
    pad_input_0.send_keys(input1)

    pad_input_1 = driver.find_element(By.ID, "padInput1")
    pad_input_1.send_keys(input2)

    pad_input_2 = driver.find_element(By.ID, "padInput2")
    pad_input_2.send_keys(input3)

    # 指定されたXPathのボタンをクリック
    button = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/div/form/div[4]/div/button')
    button.click()

    while True:
        try:
            driver.get(url)
            # 指定されたXPathのテキストを取得
            text_element = driver.find_element(By.XPATH, '//*[@id="iurikanosu"]/span')
            text_value = text_element.text

            # テキストを数値に変換
            numeric_value = int(text_value.replace('株', '').replace(' ', '').replace(',', ''))
            # 上記のXPathのテキストを取得
            text_to_log = driver.find_element(By.XPATH, '//*[@id="printzone"]/div[2]/form/table/tbody/tr/td/div[2]/table[2]/tbody/tr[2]/td/table/tbody/tr/td[3]/h2').text
            # テキストをログに表示
            print(f"{text_to_log}")
            print(f"{text_value}")

            if numeric_value >= 100:
                # 数値が100以上であれば操作を続行
                print(f"{text_to_log}の一般信用売りを実行します")
                input_field = driver.find_element(By.XPATH, '//*[@id="isuryo"]/table/tbody/tr[1]/td[1]/input')
                input_field.send_keys(input_value)

                new_button = driver.find_element(By.XPATH, '//*[@id="j"]')
                new_button.click()

                final_button = driver.find_element(By.XPATH, '//*[@id="tojit"]')
                final_button.click()

                while True:
                    try:
                        final_input = driver.find_element(By.XPATH, '//*[@id="printzone"]/div[2]/form/table/tbody/tr/td/div[2]/table[2]/tbody/tr[4]/td/div/div[4]/table/tbody/tr/td/input')
                        final_input.click()
                        
                        # 新たに指定されたXPathの要素が存在するか確認
                        pad_input = driver.find_element(By.XPATH, '//*[@id="padInput"]')
                        pad_input.send_keys(input4)
                        
                        # 最終的なXPathのボタンをクリック
                        final_click = driver.find_element(By.XPATH, final_xpath)
                        final_click.click()

                        # 要素の存在を確認
                        try:
                            final_element = driver.find_element(By.XPATH, '//*[@id="printzone"]/form/div/table/tbody/tr/td/div[2]')
                            final_text = final_element.text
                            message = f'一般信用売りが完了しました。\n　{text_to_log} {input_value}株\n　{final_text}'
                            send_discord_notify(message)
                            print(message)
                        except:
                            print('指定された要素が見つかりません。')
                        break  # 要素が存在すればループを抜ける
                    except:
                        # 要素が存在しない場合は再試行
                        print("指定された要素が見つかりません。再試行します。")
                        continue

            else:
                # 数値が100未満であれば再度URLを読み込み
                #time.sleep(1)  # 1秒待機して再試行
                driver.get(url)
                

        except:
            print("ページロードエラー、再試行します。")
            continue

    time.sleep(5)
    driver.quit()

# メインスクリプト
urls = [
    ("リテールパートナーズ(8167)", "https://trade.smbcnikko.co.jp/OdrMng/BCA5I0702880/sinyo/tku_odr/init?meigCd=0081670000&specifyMeig=1&sinyoToriKbn=1"),
    ("イオンモール(8905)", "https://trade.smbcnikko.co.jp/OdrMng/BCA5I0714173/sinyo/tku_odr/init?meigCd=0089050000&specifyMeig=1&sinyoToriKbn=1"),
    ("西松屋チェーン(7545)", "https://trade.smbcnikko.co.jp/OdrMng/BCA5I0715606/sinyo/tku_odr/init?meigCd=0075450000&specifyMeig=1&sinyoToriKbn=1"),
    ("吉野家ホールディングス(9861)", "https://trade.smbcnikko.co.jp/OdrMng/BCA5I0726381/sinyo/tku_odr/init?meigCd=0098610000&specifyMeig=1&sinyoToriKbn=1"),
    ("リンガーハット(8200)", "https://trade.smbcnikko.co.jp/OdrMng/A4C2J0641635/sinyo/tku_odr/init?meigCd=0082000000&specifyMeig=1&sinyoToriKbn=1"),
    ("アークランズ(9842)", "https://trade.smbcnikko.co.jp/OdrMng/E51AI0650643/sinyo/tku_odr/init?meigCd=0098420000&specifyMeig=1&sinyoToriKbn=1")
]

input1 = "388"
input2 = "262915"
input3 = "boukensya7"
input4 = "yukimarusan9"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
final_xpath = '//*[@id="printzone"]/div[2]/table/tbody/tr/td/div[5]/table/tbody/tr[4]/td/div/div[2]/table/tbody/tr[2]/td/div[3]/table/tbody/tr/td/table/tbody/tr[1]/td/form/div[4]/input'

# 100〜2000の値のリストを作成
possible_values = [str(i) for i in range(100, 2100, 100)]

# ユーザーにどのURLを割り当てるか選択させ、その後にinput_valueを選択させる
url_selections = []
input_values = []

# ウィンドウ数を指定
num_windows = int(input("Enter the number of windows you want to use: "))

for i in range(1, num_windows + 1):
    print(f"Select URL for thread {i}:")
    for j, (name, url) in enumerate(urls):
        print(f"{j + 1}. {name}")
    url_selection = int(input(f"Enter the number (1-{len(urls)}) for thread {i}: ")) - 1
    url_selections.append(urls.pop(url_selection)[1])

    print(f"Select input_value for thread {i}:")
    for j, value in enumerate(possible_values):
        print(f"{j + 1}. {value}")
    input_selection = int(input(f"Enter the number (1-{len(possible_values)}) for thread {i}: ")) - 1
    input_values.append(possible_values[input_selection])

# ウィンドウを新しく開いて並列に実行
threads = []
for i in range(num_windows):
    thread = threading.Thread(target=perform_operations, args=(url_selections[i], input1, input2, input3, input4, input_values[i], user_agent, final_xpath))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
