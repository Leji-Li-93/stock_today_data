import requests
from bs4 import BeautifulSoup

base_url = "https://finance.yahoo.com/quote/{0}/history?p={0}"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64)"}

def get_data(stock_name):
    has_result = False
    result = {}
    req = requests.get(base_url.format(stock_name), headers=headers)
    if(req.status_code != 200):
        print("Failed to connect to yahoo finance.")
        return result
    #print(req.text)
    doc = BeautifulSoup(req.content, "html.parser")
    try:
        for table in doc.find_all("table"):
        # if user provides a wrong stock name
        # yahoo will still return a page 
        # that can be processed by beautifulsoup
        # but the price table will has a class call "loopup-table"
            if("lookup-table" in table.get("class")):
                break
            else:
                has_result = True
                # start process the correct price table
                # prepare for table headers
                header_row = table.find_all("thead")
                table_headers = []
                for heads in header_row[0].find_all("th"):
                    table_headers.append(heads.get_text())

                # get the data of today
                tbody = table.find_all("tbody")
                first_row = tbody[0].find_all("tr", limit=1)
                if(len(first_row) <= 0):
                    print("This stock has no record yet")
                    break;

                today_data = []
                for data in first_row[0].find_all("td"):
                    today_data.append(data.get_text())

                # put data to dictionary
                for i in range(0, len(today_data)):
                    result[table_headers[i]] = today_data[i]

    except Exception as e:
        raise(e)
    
    if(not has_result):
        print("Stock name wrong.")
    return result
    

if __name__ == "__main__":
    is_continue = True
    while(is_continue):
        print("Please type in the stock name: ", end="")
        stock_name = input()
        print(get_data(stock_name))
        print("Enter Q to quit, other keys to continue:", end="")
        key = input()
        if(key.lower() == 'q'):
            is_continue = False