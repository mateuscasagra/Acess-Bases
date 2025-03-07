
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyodbc


conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\MSSQLSERVER01;'  
    'DATABASE=AcessBases;'
    'Trusted_Connection=yes;'  
)

cursor = conn.cursor()

opcao = input("(1) - Cadastrar Base\n(2) - Logar em Base\n(3) - Excluir Base\n")

if opcao == "1":
    nome = input("Digite o nome: ")
    cnpj = input("Digite o CNPJ: ")
    email = input("Digite o email: ")
    senha = input("Digite a senha: ")

    cursor.execute("""
        INSERT INTO Bases (Nome, Cnpj, Email, Senha) 
        VALUES (?, ?, ?, ?);
    """, (nome, cnpj, email, senha))
    conn.commit()
    print("Base Cadastrada")




elif opcao == "2":
    cursor.execute("""SELECT Id, Nome FROM Bases ORDER BY Id""")
    bases = cursor.fetchall()
    for base in bases:
        print(f"({base.Id}) - {base.Nome}")
    opcao_bases = input("Qual base deseja acessar?\n")
    opcao_bases = int(opcao_bases)
    cursor.execute("SELECT Cnpj, Email, Senha FROM Bases WHERE Id = ?", (opcao_bases,))
    dados_base = cursor.fetchone()
    user_cnpj, user_email, user_senha = dados_base
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get("https://mob.nox.com.br/Login")
    driver.implicitly_wait(0.5)
    login = driver.find_element(By.NAME, value="cnpj").send_keys(user_cnpj)
    driver.implicitly_wait(0.5)
    email = driver.find_element(By.NAME, value="user").send_keys(user_email)
    driver.implicitly_wait(0.5)
    senha = driver.find_element(By.NAME, value="password").send_keys(user_senha)
    driver.implicitly_wait(0.5)
    submit_button = driver.find_element(By.ID, value="btnLogin").click()


elif opcao == "3":
    cursor.execute("""SELECT Id, Nome FROM Bases""")
    bases = cursor.fetchall()
    for base in bases:
        print(f"({base.Id}) - {base.Nome}")
    
    opcao_delete = input("Qual base deseja excluir?\n")
    opcao_delete = int(opcao_delete)
    cursor.execute("DELETE FROM Bases WHERE Id = ?", (opcao_delete))
    conn.commit()
    print("Base Removida!")
    


