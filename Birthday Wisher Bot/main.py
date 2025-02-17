import smtplib
from datetime import datetime as dt
import random
import pandas as pd

# Email credentials
my_mail = "your email"
password = "your application password"

# Reading CSV file
file = pd.read_csv("./birthday.csv")
data = pd.DataFrame(file).set_index("name")

# Current date
date = dt.now()
today = f"{date.month}-{date.day}"

# Iterating over DataFrame
for index, row in data.iterrows():
    birth_day = f"{row.month}-{row.day}"
    if today == birth_day:
        with open(f"./letter_{random.randint(1,3)}.txt", mode="r") as wish_file:
            contents = wish_file.read()
            output = contents.replace('[NAME]', row.name)
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=my_mail, password=password)
                connection.sendmail(
                    from_addr=my_mail, 
                    to_addrs=row.email, 
                    msg=f"Subject:Happy Birthday\n\n{output}"
                )
                connection.close()
