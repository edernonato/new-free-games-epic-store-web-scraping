from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from selenium import webdriver
import smtplib
from datetime import date

URL = "https://store.epicgames.com/en-US/"

# SMTP connection
EMAIL_FROM = "edernonato47teste@hotmail.com"
PASSWORD = "Eder@teste321"
SMTP = "smtp-mail.outlook.com"
PORT = 587

connection = smtplib.SMTP(SMTP, PORT)
connection.starttls()
connection.login(user=EMAIL_FROM, password=PASSWORD)
EMAIL_TO = "edernonato@outlook.com"


# Using selenium webdriver to render html javascript generated
driver = webdriver.Chrome()
driver.get(URL)
website = driver.page_source

# Using driver.find_element instead of BeautiFulSoup
# free_game_name = driver.find_element(By.CLASS_NAME, "css-1h2ruwl").text
# print(free_game_name)

soup = BeautifulSoup(website, "lxml")
free_games_name = [game.text for game in soup.find_all(class_="css-1h2ruwl")]
free_games_div = soup.find_all(name="div", class_="css-1p2cbqg")
free_games_link = [[link.get("href") for link in game.find_all(name="a")][1::1] for game in free_games_div][0]
free_games_date = [[date.text for date in game.find_all(name="span", class_="css-nf3v9d")] for game in free_games_div][0]
free_games_img = [[image_link.get("data-image") for image_link in game.find_all(name="img", class_="css-1b2k567")] for game in free_games_div][0]

html_start = f"""
<html>
    <head>
    </head>
        <body>
            <h3>New Free Games Epic Store - {date.today()}</h3>"""

html_end = """
        </body>
</html>"""

html_body = ""

for gameIndex in range(len(free_games_name)):
    # html_body += f"\t\t\t<h4>{free_games_name[gameIndex]}</h4> \n"
    game_url = URL + free_games_link[gameIndex].replace("/en-US/", "")
    html_body += f"\t\t\t<a href={game_url}><h4>{free_games_name[gameIndex]}</h4></a> \n"
    html_body += f"\t\t\t<img src={free_games_img[gameIndex]}> \n"
    html_body += f"\t\t\t<h5>{free_games_date[gameIndex]} </h5> \n"

html_final = html_start + html_body + html_end

with open("games.txt", "r") as old_file:
    old_html = old_file.read()
    old_file.close()
    if old_html == html_final:
        print("SAME GAMES")
    else:
        with open("games.txt", "w") as file:
            file.write(html_final)
            print("games.txt updated")
            email_message = MIMEMultipart()
            email_message["from"] = EMAIL_FROM
            email_message["to"] = EMAIL_TO
            email_message["subject"] = f"New Free Games Epic Store - {date.today()}"
            email_message.attach(MIMEText(html_final, "html"))

            connection.sendmail(from_addr=EMAIL_FROM, to_addrs=EMAIL_TO, msg=email_message.as_string())
            print("New games Alert sent by email!")
