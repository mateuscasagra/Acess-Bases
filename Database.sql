CREATE DATABASE AcessBases;
USE AcessBases;

CREATE TABLE Bases(
Id INT IDENTITY PRIMARY KEY NOT NULL,
Nome VARCHAR(100) NOT NULL,
Cnpj VARCHAR(14) NOT NULL UNIQUE, 
Email VARCHAR(50) NOT NULL,
Senha VARCHAR(50) NOT NULL
);


INSERT INTO Bases
(Nome, Cnpj,Email,Senha)
VALUES
("Mateus","11111111111111","mateus@mateus","123456"),
("Mateus","11111111111111","mateus@mateus","123456"),
("Mateus","11111111111111","mateus@mateus","123456"),
("Mateus","11111111111111","mateus@mateus","123456");