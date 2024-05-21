import re
import json
import requests
from bs4 import BeautifulSoup

url = 'https://mall.icbc.com.cn/products/pd_9003867817.jhtml'
response = requests.get(url)

if response.status_code == 200:
    content = response.text

    soup = BeautifulSoup(content, 'html.parser')
    prod_sku_div = soup.find('div', {'id': 'prodSkuDiv'})
    # 将响应内容保存到本地文件
    with open('response.html', 'w', encoding='utf-8') as file:
        file.write(prod_sku_div.text)

    if prod_sku_div:
        script_content = prod_sku_div.find('script').string
        json_string = script_content[script_content.find(
            "[{\"totalStorage\":"):script_content.find("\"}];")+3]
        data_array = json.loads(json_string)
        target_prod_sku_id = "90000000000031379287"

        for item in data_array:
            if item['prodSkuId'] == target_prod_sku_id:
                sku_price = item['skuPrice']
                print(
                    f"prodSkuId 为 {target_prod_sku_id} 对应的 skuPrice 值为: {sku_price}")
                # 注意：替换成自己的飞书机器人webhook地址
                url = 'https://www.feishu.cn/flow/api/trigger-webhook/6effdc0bf7e18ac0bf38d6b9d3e27a2b'
                data = {'price': sku_price}
                print(data)
                response = requests.post(url, json=data)
                print(response.status_code, response.text)
                break
        else:
            print(f"未找到 prodSkuId 为 {target_prod_sku_id} 的记录")
    else:
        print("<div id='prodSkuDiv'> not found in the response.")
else:
    print(f'Request failed with status code: {response.status_code}')
