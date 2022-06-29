from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests


class Food(ABC):
 
    def __init__(self, area):
        self.area = area  
 
    @abstractmethod
    def scrape(self):
        pass
    

# 愛食記爬蟲
class IFoodie(Food):
 
    def scrape(self):
        response = requests.get(
            "https://ifoodie.tw/explore/" + self.area +
            "/list?opening=true&sortby=popular")
            
        soup = BeautifulSoup(response.content, "html.parser")
        

        
         # 爬取前五筆餐廳卡片資料
        cards = soup.find_all(
            'div', {'class': 'jsx-3296965063 title-info'}, limit=5)

        return cards
    
        content = ""
        for card in cards:
 
            # title = card.find(  # 餐廳名稱
            #     "a", {"class": "jsx-1776651079 title-text"}).getText()
 
            # stars = card.find(  # 餐廳評價
            #     "div", {"class": "jsx-1207467136 text"}).getText()
 
            address = card.find(  # 餐廳地址
                "span", {"class": "jsx-1969054371 detail"}).getText()
 
 
            # content += f"{title} \n{stars}顆星 \n{address} \n\n"
            content += f"{address} \n\n"
        
        # return content
        