import requests
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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

def perform_operations(url, input1, input2, input3, input4, input_value, user_agent, final_xpath):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://trade.smbcnikko.co.jp/Etc/1/webtoppage/")

    logging.info("指定された入力フィールドに値を入力")
    pad_input_0 = driver.find_element(By.ID, "padInput0")
    pad_input_0.send_keys(input1)

    pad_input_1 = driver.find_element(By.ID, "padInput1")
    pad_input_1.send_keys(input2)

    pad_input_2 = driver.find_element(By.ID, "padInput2")
    pad_input_2.send_keys(input3)

    button = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/div/form/div[4]/div/button')
    button.click()

    driver.get(url)

    while True:
        try:
            text_to_log = driver.find_element(By.XPATH, '//*[@id="printzone"]/div[2]/form/table/tbody/tr/td/div[2]/table[2]/tbody/tr[2]/td/table/tbody/tr/td[3]/h2').text
            logging.info(f"{text_to_log}")

            logging.info(f"{text_to_log}の一般信用売りを実行します")
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

                    try:
                        pad_input = driver.find_element(By.XPATH, '//*[@id="padInput"]')
                        pad_input.send_keys(input4)

                        final_click = driver.find_element(By.XPATH, final_xpath)
                        final_click.click()

                        try:
                            final_element = driver.find_element(By.XPATH, '//*[@id="printzone"]/form/div/table/tbody/tr/td/div[2]')
                            final_text = final_element.text
                            message = f'一般信用売りが完了しました。\n　{text_to_log} {input_value}株\n　{final_text}'
                            send_discord_notify(message)
                            logging.info(message)
                            break
                        except:
                            logging.error('争奪戦に負けましたので在庫リスポーン取得を試みます。')
                            
                            driver.get(url)
                    
                            text_to_log = driver.find_element(By.XPATH, '//*[@id="printzone"]/div[2]/form/table/tbody/tr/td/div[2]/table[2]/tbody/tr[2]/td/table/tbody/tr/td[3]/h2').text
                            logging.info(f"{text_to_log}")
                
                            logging.info(f"{text_to_log}の一般信用売りを実行します")
                            input_field = driver.find_element(By.XPATH, '//*[@id="isuryo"]/table/tbody/tr[1]/td[1]/input')
                            input_field.send_keys(input_value)
                
                            new_button = driver.find_element(By.XPATH, '//*[@id="j"]')
                            new_button.click()
                
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
                    logging.info(f"{text_to_log}")
        
                    logging.info(f"{text_to_log}の一般信用売りを実行します")
                    input_field = driver.find_element(By.XPATH, '//*[@id="isuryo"]/table/tbody/tr[1]/td[1]/input')
                    input_field.send_keys(input_value)
        
                    new_button = driver.find_element(By.XPATH, '//*[@id="j"]')
                    new_button.click()
        
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
url = "https://trade.smbcnikko.co.jp/OdrMng/A4C2J0641635/sinyo/tku_odr/init?meigCd=0082000000&specifyMeig=1&sinyoToriKbn=1"
input1 = "388"
input2 = "262915"
input3 = "boukensya7"
input4 = "yukimarusan9"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
final_xpath = '//*[@id="printzone"]/div[2]/table/tbody/tr/td/div[5]/table/tbody/tr[4]/td/div/div[2]/table/tbody/tr[2]/td/div[3]/table/tbody/tr/td/table/tbody/tr[1]/td/form/div[4]/input'
input_value = "100"
num_windows = 1

threads = []
for i in range(num_windows):
    thread = threading.Thread(target=perform_operations, args=(url, input1, input2, input3, input4, input_value, user_agent, final_xpath))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
