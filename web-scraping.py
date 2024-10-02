from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


class Web_Scrape:
    def __init__(self, total_pages):
        self.total_pages = total_pages
    
    def initialize_driver(self):
        self.driver = webdriver.Chrome()  
        self.driver.get('https://cekbpom.pom.go.id/obat')
    
    def click_item(self,item):
        try:
            detail_button = self.driver.find_element(By.XPATH, f'//*[@id="inbox-list"]/div[{item+1}]')
            detail_button.click()
            time.sleep(1.5) 
        except Exception as e:
            print("Item not found or clickable:", e)
        
    def click_close(self):
        try:
            close_button = self.driver.find_element(By.XPATH, '//*[@id="exampleModal2"]/div/div/div[3]/button')
            close_button.click()
        except Exception as e:
            print("Close button not found or clickable:", e)
        
    def click_next_page(self):
        try:
            next_button = self.driver.find_element(By.XPATH, '//*[@id="next"]') 
            next_button.click()
            time.sleep(2) 
        except Exception as e:
            print("Next button not found or clickable:", e)
    
    def get_unique_id(self, item, page):
        prod = str((page*10)+(item+1))
        return prod

    def extract_details(self,prod):
        self.product_dict[prod] = {}
        self.product_dict[prod]['kode_registrasi'] = self.driver.find_element(By.XPATH, '//*[@id="id_produk"]').text
        self.product_dict[prod]['tanggal_terbit'] = (self.driver.find_element(By.XPATH, '//*[@id="tgl_permohonan"]')).text
        self.product_dict[prod]['masa_berlaku'] = (self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/form/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/div/span')).text
        self.product_dict[prod]['diterbitkan_oleh'] = (self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/form/table/tbody/tr/td[1]/table/tbody/tr[5]/td[2]/div/span')).text
        self.product_dict[prod]['nama_produk'] = (self.driver.find_element(By.XPATH, '//*[@id="id_produk"]/a')).text
        self.product_dict[prod]['bentuk_sediaan'] = (self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/form/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/div/span')).text
        self.product_dict[prod]['merk'] = (self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/form/table/tbody/tr/td[2]/table/tbody/tr[4]/td[2]/div/span')).text
        self.product_dict[prod]['kemasan'] = (self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/form/table/tbody/tr/td[2]/table/tbody/tr[5]/td[2]/div/span')).text
        self.product_dict[prod]['pendaftar'] = (self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/form/table/tbody/tr/td[2]/table/tbody/tr[6]/td[2]/div/span/a/b')).text
        self.product_dict[prod]['diproduksi_oleh'] = (self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/form/table/tbody/tr/td[2]/table/tbody/tr[7]/td[2]/div/span/a/b')).text

    def create_df(self, product_dict):
        return pd.DataFrame.from_dict(product_dict).T

    def end_to_end(self):
        self.initialize_driver()
        
        # initialize empty dict to store all data
        self.product_dict = {}

        for page in range(self.total_pages):
            for item in range(10):
                self.click_item(item)
                prod = self.get_unique_id(item, page)
                self.extract_details(prod)
                self.click_close()

            # click the 'Next' button
            self.click_next_page()

        self.driver.quit()
        return self.create_df(self.product_dict)


class Write_Output:
    def __init__(self, df):
        self.df = df
    
    def adjust_columns(self,writer):
        # adjust excel file columns to fit
        for column in self.df:
            column_length = max(self.df[column].astype(str).map(len).max(), len(column))
            col_idx = self.df.columns.get_loc(column)
            writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length+5)

    def write_output(self):
        # create output file
        writer = pd.ExcelWriter('output.xlsx')
        self.df.to_excel(writer, sheet_name='Sheet1', index=False)
        self.adjust_columns(writer)
        
        # save file
        writer.save()

     
def main():
    web_scrape = Web_Scrape(total_pages=10)
    df = web_scrape.end_to_end()
    save_file = Write_Output(df)
    save_file.write_output()


if __name__ == '__main__':
    main()
