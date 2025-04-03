
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyodbc
import time
import os
import random


conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=HUGIE;'  
    'DATABASE=AcessBases;'
    'Trusted_Connection=yes;'  
)


pagAberta = 0
cursor = conn.cursor()
estado = True
def loginBase ():
    global driver  
    global pagAberta
    if pagAberta == 1:
        driver.quit()
        pagAberta = 0 
    cursor.execute("""SELECT Id, Nome FROM Bases ORDER BY Id""")
    bases = cursor.fetchall()
    for base in range(0, len(bases)):
        print(f"({base}) - {bases[base][1]}")
    
    opcao_bases = input("Qual base deseja acessar?\n")
    opcao_bases = int(opcao_bases)
    opcao_bases = bases[opcao_bases][0]
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
    pagAberta = 1

def gerar_cnpj():
    base = [random.randint(0, 9) for _ in range(8)]
    filial = [random.randint(0, 9) for _ in range(4)]  
    cnpj_parcial = base + filial  
    peso_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_1 = sum([cnpj_parcial[i] * peso_1[i] for i in range(12)])
    digito_1 = (soma_1 % 11)
    digito_1 = 0 if digito_1 < 2 else 11 - digito_1
    peso_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_2 = sum([cnpj_parcial[i] * peso_2[i] for i in range(12)]) + (digito_1 * 2)
    digito_2 = (soma_2 % 11)
    digito_2 = 0 if digito_2 < 2 else 11 - digito_2
    cnpj = f"{''.join(map(str, base))}{''.join(map(str, filial))}{digito_1}{digito_2}"
    print(cnpj)

while estado:
    
    opcao = input("\n(1) - Cadastrar Base\n(2) - Logar em Base\n(3) - Editar dados\n(4) - Consultar Base\n(5) - Excluir Base\n(6) - Limpar\n(7) - Gerar CNPJ\n(8) - Fechar Navegador\n(9) - Sair\n")
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
        print("\nBase Cadastrada\n")




    elif opcao == "2":
        loginBase()
        
        
            
    elif opcao =="3":
        cursor.execute("""SELECT Id, Nome FROM Bases""")
        bases = cursor.fetchall()
        for base in range(0,len(bases)):
            print(f"({base}) - {bases[base][1]}")
        opcao_edicao = input("\nQual base deseja editar?\n")
        opcao_edicao = int(opcao_edicao)
        opcao_edicao = bases[opcao_edicao][0]
        cursor.execute("""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME != 'Id' AND TABLE_NAME = 'Bases'""")
        base_columns = cursor.fetchall()
        for i in range(0,len(base_columns)):
            print(f"({i}) - {base_columns[i][0]}")
            
        opcao_campo = input("\nQual campo deseja editar?\n")
        opcao_campo = int(opcao_campo)
        opcao_campo = base_columns[opcao_campo][0]
        modificacao = input("Digite o novo valor\n")
        query = f"UPDATE Bases SET {opcao_campo} = ? WHERE Id = ?"
        cursor.execute(query, (modificacao, opcao_edicao))
        conn.commit()
        print("\nAlteração Realizada!\n")
            


        
    elif opcao == "4":
        cursor.execute("""SELECT Id, Nome FROM Bases""")
        bases = cursor.fetchall()
        for base in range(0,len(bases)):
            print(f"({base}) - {bases[base][1]}")
        opcao_busca = input("\nDeseja ver os dados de qual base?\n")
        opcao_busca = int(opcao_busca)
        opcao_busca = bases[opcao_busca][0]
        cursor.execute("""SELECT Nome, Cnpj, Email, Senha FROM Bases WHERE Id = ?""", opcao_busca)
        base_buscada = cursor.fetchall()
        for i in base_buscada:
            for valor in i:
                print(valor)
    
        
    elif opcao == "5":
        cursor.execute("""SELECT Id, Nome FROM Bases""")
        bases = cursor.fetchall()
        for base in range(0,len(bases)):
            print(f"({base}) - {bases[base][1]}")
        opcao_delete = input("\nQual base deseja excluir?\n")
        opcao_delete = int(opcao_delete)
        opcao_delete = bases[opcao_delete][0]
        cursor.execute("DELETE FROM Bases WHERE Id = ?", opcao_delete)
        conn.commit()
        print("\nBase Removida!\n")
           
        
    elif opcao == "6":
        os.system('cls')
        
        
    elif opcao == "7":
        gerar_cnpj()
    elif opcao == "8":
        driver.quit()
        pagAberta = 0
        
    elif opcao == "9":
        
        if pagAberta == 1:
            driver.quit()
            
        estado = False
        print("\nSistema Encerrado\n")
