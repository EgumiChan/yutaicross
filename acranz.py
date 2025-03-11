import requests
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading

# ログの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

# 日興証券の一般信用売りを実行する関数
def perform_operations(url, loginShitenNo, loginKouzaNo, loginPass, torihikiPass, neStock, inStock, user_agent, final_xpath, joken):
    # Chromeの設定
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={user_agent}")

    # 日興証券のログインページにアクセス
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://trade.smbcnikko.co.jp/Etc/1/webtoppage/")

    
    # ログイン情報を入力してログイン
    logging.info("指定された入力フィールドに値を入力")
    pad_input_0 = driver.find_element(By.ID, "padInput0")
    pad_input_0.send_keys(loginShitenNo)

    pad_input_1 = driver.find_element(By.ID, "padInput1")
    pad_input_1.send_keys(loginKouzaNo)

    pad_input_2 = driver.find_element(By.ID, "padInput2")
    pad_input_2.send_keys(loginPass)

    button = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div/div[1]/div[1]/div/form/div[4]/div/button')
    button.click()

    # 指定した銘柄の一般信用売りのページにアクセス
    driver.get(url)

    # 残り必要株数と取得株数の大小関係が正しいかで分岐
    if neStock < inStock:
        inStock = neStock

    while True:
        try:
            # アクセスしたページの銘柄の名称を取得して代入
            text_to_log = driver.find_element(By.XPATH, '//*[@id="printzone"]/div[2]/form/table/tbody/tr/td/div[2]/table[2]/tbody/tr[2]/td/table/tbody/tr/td[3]/h2').text

            # 株数等を入力
            logging.info(f"{text_to_log}の一般信用売り連打を実行します")
            input_field = driver.find_element(By.XPATH, '//*[@id="isuryo"]/table/tbody/tr[1]/td[1]/input')
            input_field.send_keys(inStock)

            new_button = driver.find_element(By.XPATH, '//*[@id="j"]')
            new_button.click()

            if joken == "寄付":
                joken_button = driver.find_element(By.XPATH, '//*[@id="nyori"]')
                joken_button.click()                                    
            elif joken == "引け":
                joken_button = driver.find_element(By.XPATH, '//*[@id="nhike"]')
                joken_button.click()

            final_button = driver.find_element(By.XPATH, '//*[@id="tojit"]')
            final_button.click()

            while True:
                try:
                    # 信用売りのボタンをクリック（連打対象）
                    #time.sleep(0.1)
                    final_input = driver.find_element(By.XPATH, '//*[@id="printzone"]/div[2]/form/table/tbody/tr/td/div[2]/table[2]/tbody/tr[4]/td/div/div[4]/table/tbody/tr/td/input')
                    final_input.click()

                    try:
                        # 取引パスワードの入力
                        pad_input = driver.find_element(By.XPATH, '//*[@id="padInput"]')
                        pad_input.send_keys(torihikiPass)

                        # 取引確定ボタンのクリック
                        final_click = driver.find_element(By.XPATH, final_xpath)
                        final_click.click()

                        try:
                            # 取引確定ボタンクリック後、争奪戦に勝利したかどうかを要素の有無で判断
                            final_element = driver.find_element(By.XPATH, '//*[@id="printzone"]/form/div/table/tbody/tr/td/div[2]')
                            final_text = final_element.text

                            # Discordに一般信用売りの在庫取得完了の通知
                            message = f'一般信用売りが完了しました。\n　{text_to_log} {inStock}株\n　{final_text}'
                            send_discord_notify(message)
                            logging.info(message)

                            # 取得した在庫数を必要残り株数からマイナスし、残り必要数を算出
                            neStock = neStock - inStock

                            # 残り必要数が0の場合は、ループ停止。0以外の場合はループ継続
                            if neStock > 0:
                                # 残り必要数が入力株数よりも少ない場合、入力株数を残り必要数にするように条件分岐
                                if neStock < inStock:
                                    inStock = neStock

                                driver.get(url)
                        
                                text_to_log = driver.find_element(By.XPATH, '//*[@id="printzone"]/div[2]/form/table/tbody/tr/td/div[2]/table[2]/tbody/tr[2]/td/table/tbody/tr/td[3]/h2').text
                    
                                logging.info(f"{text_to_log}の一般信用売り連打を追加実行します")
                                input_field = driver.find_element(By.XPATH, '//*[@id="isuryo"]/table/tbody/tr[1]/td[1]/input')
                                input_field.send_keys(inStock)
                    
                                new_button = driver.find_element(By.XPATH, '//*[@id="j"]')
                                new_button.click()

                                if joken == "寄付":
                                    joken_button = driver.find_element(By.XPATH, '//*[@id="nyori"]')
                                    joken_button.click()                                    
                                elif joken == "引け":
                                    joken_button = driver.find_element(By.XPATH, '//*[@id="nhike"]')
                                    joken_button.click()
                    
                                final_button = driver.find_element(By.XPATH, '//*[@id="tojit"]')
                                final_button.click()
                                
                                continue

                            else:
                                break

                        except:
                            logging.error('争奪戦に負けましたので在庫リスポーン取得を試みます。')
                            
                            driver.get(url)
                    
                            text_to_log = driver.find_element(By.XPATH, '//*[@id="printzone"]/div[2]/form/table/tbody/tr/td/div[2]/table[2]/tbody/tr[2]/td/table/tbody/tr/td[3]/h2').text
                
                            logging.info(f"{text_to_log}の一般信用売り連打を再度実行します")
                            input_field = driver.find_element(By.XPATH, '//*[@id="isuryo"]/table/tbody/tr[1]/td[1]/input')
                            input_field.send_keys(inStock)
                
                            new_button = driver.find_element(By.XPATH, '//*[@id="j"]')
                            new_button.click()

                            if joken == "寄付":
                                joken_button = driver.find_element(By.XPATH, '//*[@id="nyori"]')
                                joken_button.click()                                    
                            elif joken == "引け":
                                joken_button = driver.find_element(By.XPATH, '//*[@id="nhike"]')
                                joken_button.click()
                
                            final_button = driver.find_element(By.XPATH, '//*[@id="tojit"]')
                            final_button.click()
                            
                            continue
                        break
                    except:
                        logging.error("在庫なし")
                        continue
                    break
                except Exception as e:
                    logging.error('ページに不正検知されましたのでURLを再度読み込みます')
                    
                    driver.get(url)
                    
                    text_to_log = driver.find_element(By.XPATH, '//*[@id="printzone"]/div[2]/form/table/tbody/tr/td/div[2]/table[2]/tbody/tr[2]/td/table/tbody/tr/td[3]/h2').text
        
                    logging.info(f"{text_to_log}の一般信用売り連打を再度実行します")
                    input_field = driver.find_element(By.XPATH, '//*[@id="isuryo"]/table/tbody/tr[1]/td[1]/input')
                    input_field.send_keys(inStock)
        
                    new_button = driver.find_element(By.XPATH, '//*[@id="j"]')
                    new_button.click()

                    if joken == "寄付":
                        joken_button = driver.find_element(By.XPATH, '//*[@id="nyori"]')
                        joken_button.click()                                    
                    elif joken == "引け":
                        joken_button = driver.find_element(By.XPATH, '//*[@id="nhike"]')
                        joken_button.click()
        
                    final_button = driver.find_element(By.XPATH, '//*[@id="tojit"]')
                    final_button.click()
                    continue
            break    
        except Exception as e:
            logging.error(f"ページロードエラー: {e}")
            driver.get(url)
            continue

    time.sleep(5)
    driver.quit()

# メインスクリプト
url = "https://trade.smbcnikko.co.jp/OdrMng/6BC1B0359122/sinyo/tku_odr/init?meigCd=0027490000&specifyMeig=1&sinyoToriKbn=1"
loginShitenNo = "388"
loginKouzaNo = "262915"
loginPass = "boukensya7"
torihikiPass = "yukimarusan9"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
final_xpath = '//*[@id="printzone"]/div[2]/table/tbody/tr/td/div[5]/table/tbody/tr[4]/td/div/div[2]/table/tbody/tr[2]/td/div[3]/table/tbody/tr/td/table/tbody/tr[1]/td/form/div[4]/input'
input_value = "500"
num_windows = 1
joken = "引け"
neStock = 500
inStock = 500



threads = []
for i in range(num_windows):
    thread = threading.Thread(target=perform_operations, args=(url, loginShitenNo, loginKouzaNo, loginPass, torihikiPass, neStock, inStock, user_agent, final_xpath, joken))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
