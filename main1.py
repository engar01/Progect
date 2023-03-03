import customtkinter as tk
from selenium import webdriver
import requests as rq
import os
from bs4 import BeautifulSoup
import time
tk.set_appearance_mode("dark")
tk.set_default_color_theme("green")

output = "output"

def get_url(path, url):
    driver_service = webdriver.chrome.service.Service(executable_path=r"{}".format(path))
    driver = webdriver.Chrome(options=webdriver.ChromeOptions(), service=driver_service)
    driver_service.start()  # Додати цей рядок
    driver.get(url)
    print("loading.....")
    res = driver.execute_script("return document.documentElement.outerHTML")
    return res

def get_img_links(res):
    soup = BeautifulSoup(res, "lxml")
    imglinks = soup.find_all("img", src=True)
    return imglinks

def download_img(img_link, index):
    try:
        extensions = [".jpeg", ".jpg", ".png", ".gif"]
        extension = ".jpg"
        for exe in extensions:
            if img_link.find(exe) > 0:
                extension = exe
                break

        img_data = rq.get(img_link).content
        with open(output + "\\" + str(index + 1) + extension, "wb+") as f:
            f.write(img_data)

        f.close()
    except Exception:
        pass

def download():
    path = entry1.get()

    url = entry2.get()

    result = get_url(path, url)
    time.sleep(60)
    img_links = get_img_links(result)
    if not os.path.isdir(output):
        os.mkdir(output)

    for index, img_link in enumerate(img_links):
        img_link = img_link["src"]
        print("Downloading...")
        if img_link:
            download_img(img_link, index)
    print("Download Complete!!")


root = tk.CTk()
root.geometry("600x500")
root.title("Downloading pictures")
# створення рядка для введення тексту
entry1 = tk.CTkEntry(root, placeholder_text="Enter Path")
entry1.pack(pady=10)

entry2 = tk.CTkEntry(root, placeholder_text="Enter URL")
entry2.pack(pady=10)

# entry3 = tk.CTkEntry(root, placeholder_text="output")
# entry3.pack(pady=10)

# створення кнопки
button = tk.CTkButton(root, text="Скачати", command=download)
button.pack(pady=10)

root.mainloop()
