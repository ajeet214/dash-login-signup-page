import pandas as pd
import os

EXCEL_PATH = "assets\\users.xlsx"


def read_users():
    if not os.path.exists(EXCEL_PATH):
        df = pd.DataFrame(columns=["username", "password", "email", "code", "branch"])
        df.to_excel(EXCEL_PATH, index=False)
    return pd.read_excel(EXCEL_PATH)


def save_users(df):
    df.to_excel(EXCEL_PATH, index=False)


def check_user(username, password):
    df = read_users()
    user = df[(df['username'] == username) & (df['password'] == password)]
    return not user.empty


def user_exists(username):
    df = read_users()
    return username in df['username'].values


def add_user(username, password, email, code, branch):
    df = read_users()
    if user_exists(username):
        return False
    new_user = pd.DataFrame([{
        "username": username,
        "password": password,
        "email": email,
        "code": code,
        "branch": branch
    }])
    df = pd.concat([df, new_user], ignore_index=True)
    save_users(df)
    return True


def reset_password(username, new_password):
    df = read_users()
    if username in df['username'].values:
        df.loc[df['username'] == username, 'password'] = new_password
        save_users(df)
        return True
    return False
