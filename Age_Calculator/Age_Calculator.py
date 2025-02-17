from datetime import date

def calculate_age(birthday):
    today = date.today()
    
    if today < birthday:
        return "Invalid birthdate. Please enter a valid date."
    
    year_diff = today.year - birthday.year
    has_had_birthday = ((today.month, today.day) < (birthday.month, birthday.day))
    year_diff -= has_had_birthday
    
    remaining_months = today.month - birthday.month if today.month >= birthday.month else 12 + today.month - birthday.month
    remaining_days = today.day - birthday.day if today.day >= birthday.day else (date(today.year, today.month + 1, 1) - date(today.year, today.month, birthday.day)).days
    
    return f"Age: {year_diff} years, {remaining_months} months, and {remaining_days} days"

if __name__ == "__main__":
    print("Age Calculator by Python")
    
    try:
        birthYear = int(input("Enter the birth year: "))
        birthMonth = int(input("Enter the birth month: "))
        birthDay = int(input("Enter the birth day: "))
        dateOfBirth = date(birthYear, birthMonth, birthDay)
        age = calculate_age(dateOfBirth)
        print(age)
    except ValueError:
        print("Invalid input. Please enter valid integers for the year, month, and day.")
