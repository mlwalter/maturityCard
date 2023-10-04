import streamlit as st
import requests
import pandas as pd
import altair as alt

# Base URL for the API
BASE_URL = "https://game.maturitycard.com/api/"

def send_token(email):
    # API endpoint for SendToken
    url = BASE_URL + "auth/sendToken"
    response = requests.post(url, json={"email": email})
    return response.json()

def login(email, token):
    # API endpoint for Login
    url = BASE_URL + "auth/login"
    response = requests.post(url, json={"email": email, "token": token})
    return response.json()

def fetch_data(auth_token, start_date, end_date):
    # Formate as datas para "yyyy-mm-dd"
    formatted_start_date = start_date.strftime('%Y-%m-%d')
    formatted_end_date = end_date.strftime('%Y-%m-%d')
    
    # Endpoint da API corrigido para List Audit
    url = "https://game.maturitycard.com/api/audit"
    headers = {"Authorization": ("Bearer " + auth_token)}
    params = {
        "dataBegin": formatted_start_date,
        "dataEnd": formatted_end_date
    }
    response = requests.get(url, headers=headers, params=params)

    # Verifique se o código de status da resposta indica sucesso (2xx)
    if response.status_code // 100 == 2:
        try:
            return response.json()
        except ValueError:  # Trate erros de decodificação de JSON
            return {"error": "Received an invalid JSON response from the server."}
    else:
        # Retorne o status de erro e o texto, se disponível
        return {"error": f"Error {response.status_code}: {response.text}"}

def plot_line_chart(df, x_col, y_col, title):
    st.subheader(title)
    st.line_chart(df.set_index(x_col)[y_col], use_container_width=True)

# Function to plot the evolution of daily usersLogin
def plot_users_login_evolution(df):
    # Calculate the daily number of usersLogin
    df['daily_usersLogin'] = df['usersLogin'].apply(len)
    # Plot the evolution of daily usersLogin
    plot_line_chart(df, 'dataLog', 'daily_usersLogin', "Evolução Diária de Usuários que Fizeram Login")

# Function to plot the evolution of licenses

def plot_combined_licenses_evolution(df):
    # Calculate the daily number for licenses
    df['daily_licensesCreated'] = df['licensesCreated'].apply(len)
    df['daily_licensesExpired'] = df['licensesExpired'].apply(len)
    df['daily_licensesActivationPending'] = df['licensesActivationPending'].apply(len)
    
    # Prepare the data for plotting
    melted_df = df.melt(id_vars=['dataLog'], 
                        value_vars=['daily_licensesCreated', 'daily_licensesExpired', 'daily_licensesActivationPending'],
                        var_name='License Type', value_name='Count')
    
    # Create an Altair line chart
    chart = alt.Chart(melted_df).mark_line().encode(
        x='dataLog:T',
        y='Count:Q',
        color=alt.Color('License Type:N', scale=alt.Scale(domain=['daily_licensesCreated', 'daily_licensesExpired', 'daily_licensesActivationPending'],
                                                         range=['blue', 'red', 'green'])),
        tooltip=['dataLog', 'Count', 'License Type']
    ).properties(title="Evolução Diária das Licenças", width=600)
    
    st.altair_chart(chart, use_container_width=True)

# This function should be called in the Streamlit app after fetching the data and converting it to the 'details_df' DataFrame:
# plot_combined_licenses_evolution(details_df)



# Streamlit UI
st.title("MaturityCards Dashboard")

# Initialize session state for auth_token
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

# Input for email
email = st.text_input("Enter your email:")

# Button to send token
if st.button("Send Token"):
    response = send_token(email)
    st.write(response)  # Display the response (for debugging)

# Input for token
token = st.text_input("Enter the token sent to your email:")

# Button to login
if st.button("Login"):
    response = login(email, token)
    st.session_state.auth_token = response.get("token")  # Store token in session state
    #st.write(response)  # Display the response (for debugging)

# Check for auth_token in session state to display date inputs and fetch data button
if st.session_state.auth_token:
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Fetch Data"):
        data = fetch_data(st.session_state.auth_token, start_date, end_date)
        #st.write(data)  # Display the fetched data (for debugging)
        # Verifique se os dados contêm a chave 'details' e se não está vazia
        if 'details' in data and data['details']:

            # Converta a lista 'details' em um DataFrame
            details_df = pd.DataFrame(data['details'])

            # Converta a coluna 'dataLog' para o formato datetime
            details_df['dataLog'] = pd.to_datetime(details_df['dataLog'])
            plot_users_login_evolution(details_df)
            plot_combined_licenses_evolution(details_df)
