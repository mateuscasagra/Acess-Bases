
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyodbc
import time

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-O7IC417\MSSQLSERVER01;'  
    'DATABASE=AcessBases;'
    'Trusted_Connection=yes;'  
)

cursor = conn.cursor()

def loginBase ():
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
    driver.maximize_window()
    driver.find_element(By.NAME, "cnpj").send_keys(user_cnpj)
    driver.find_element(By.NAME, "user").send_keys(user_email)
    driver.find_element(By.NAME, "password").send_keys(user_senha)
    time.sleep(0.5)
    driver.find_element(By.ID, "btnLogin").click()

opcao = input("(1) - Cadastrar Base\n(2) - Logar em Base\n(3) - Editar dados\n(4) - Consultar Base\n(5) - Excluir Base\n")

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
    loginBase()
    
    
        
elif opcao =="3":
    cursor.execute("""SELECT Id, Nome FROM Bases""")
    bases = cursor.fetchall()
    for base in bases:
        print(f"({base.Id}) - {base.Nome}")
    opcao_edicao = input("Qual base deseja editar?\n")
    opcao_edicao = int(opcao_edicao)
    cursor.execute("""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME != 'Id' AND TABLE_NAME = 'Bases'""")
    base_columns = cursor.fetchall()
    for i in range(0,len(base_columns)):
        print(f"({i}) - {base_columns[i][0]}")
        
    opcao_campo = input("Qual campo deseja editar?\n")
    opcao_campo = int(opcao_campo)
    opcao_campo = base_columns[opcao_campo][0]
    modificacao = input("Digite o novo valor\n")
    query = f"UPDATE Bases SET {opcao_campo} = ? WHERE Id = ?"
    cursor.execute(query, (modificacao, opcao_edicao))
    conn.commit()
    print("Alteração Realizada!")
        


    
elif opcao == "4":
    cursor.execute("""SELECT Id, Nome FROM Bases""")
    bases = cursor.fetchall()
    for base in bases:
        print(f"({base.Id}) - {base.Nome}")
    opcao_busca = input("Deseja ver os dados de qual base?\n")
    opcao_busca = int(opcao_busca)
    cursor.execute("""SELECT Nome, Cnpj, Email, Senha FROM Bases WHERE Id = ?""", opcao_busca)
    base_buscada = cursor.fetchall()
    for i in base_buscada:
        for valor in i:
            print(valor)
   
    
elif opcao == "5":
    cursor.execute("""SELECT Id, Nome FROM Bases""")
    bases = cursor.fetchall()
    for base in bases:
        print(f"({base.Id}) - {base.Nome}")
    
    opcao_delete = input("Qual base deseja excluir?\n")
    opcao_delete = int(opcao_delete)
    cursor.execute("DELETE FROM Bases WHERE Id = ?", opcao_delete)
    conn.commit()
    print("Base Removida!")
    
    
    
    


