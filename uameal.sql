-- Dropping the table if exists
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS MealType;
DROP TABLE IF EXISTS Meal;
DROP TABLE IF EXISTS TicketMeal;

-- Creating the table
CREATE TABLE Student (
    mecNumber INTEGER PRIMARY KEY,
    name TEXT,
    pin TEXT,
    balance FLOAT,
    course TEXT,
    isActive INTEGER
);


CREATE TABLE Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idUser INT,
    operation TEXT,
    balanceBeforeTransaction FLOAT,
    transactionValue FLOAT,
    balanceAfterTransaction FLOAT,
    date DATE,
    isActive INT,   
    FOREIGN KEY (idUser) REFERENCES Student(mecNumber)
);

CREATE TABLE MealType (
    id INT PRIMARY KEY,
    name TEXT,
    isActive INT
);

CREATE TABLE Meal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    idMealType INT,
    price FLOAT,
    isActive INT,   
    FOREIGN KEY (idMealType) REFERENCES MealType(id)
);

CREATE TABLE TicketMeal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idUser INT,
    idMeal INT,
    idDrink INT,
    idDessert INT,
    price FLOAT,
    date DATE,
    isActive INT,   
    FOREIGN KEY (idUser) REFERENCES Student(mecNumber),
    FOREIGN KEY (idMeal) REFERENCES Meal(id),
    FOREIGN KEY (idDrink) REFERENCES Meal(id),
    FOREIGN KEY (idDessert) REFERENCES Meal(id)
);

-- Inserting data into the table Student
INSERT INTO Student(mecNumber, name, pin, balance, course, isActive) VALUES (000000, 'admin', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 999, 'Desenvolvimento de Software', 1);
INSERT INTO Student(mecNumber, name, pin, balance, course, isActive) VALUES (120764, 'Gonçalo Silva', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 100, 'Desenvolvimento de Software', 1);

-- Inserting data into the table Transactions
INSERT INTO Transactions(idUser, operation, balanceBeforeTransaction, transactionValue, balanceAfterTransaction, date,isActive) VALUES (120764, 'Carregamento', 100, -2, 98, '2024-04-03 17:38:00', 1);
INSERT INTO Transactions(idUser, operation, balanceBeforeTransaction, transactionValue, balanceAfterTransaction, date,isActive) VALUES (120764, 'Carregamento', 100, 5, 98, '2024-04-02 12:38:00', 1);
INSERT INTO Transactions(idUser, operation, balanceBeforeTransaction, transactionValue, balanceAfterTransaction, date,isActive) VALUES (120764, 'Carregamento', 100, 10, 98, '2024-04-01 15:38:00', 1);
INSERT INTO Transactions(idUser, operation, balanceBeforeTransaction, transactionValue, balanceAfterTransaction, date,isActive) VALUES (120764, 'Carregamento', 100, -6, 98, '2024-03-30 13:38:00', 1);
INSERT INTO Transactions(idUser, operation, balanceBeforeTransaction, transactionValue, balanceAfterTransaction, date,isActive) VALUES (120764, 'Carregamento', 100, -2, 98, '2024-03-29 16:38:00', 1);
INSERT INTO Transactions(idUser, operation, balanceBeforeTransaction, transactionValue, balanceAfterTransaction, date,isActive) VALUES (120764, 'Carregamento', 100, 10, 98, '2024-03-28 11:38:00', 1);
INSERT INTO Transactions(idUser, operation, balanceBeforeTransaction, transactionValue, balanceAfterTransaction, date,isActive) VALUES (120764, 'Carregamento', 100, -4, 98, '2024-03-15 12:38:00', 1);

-- Inserting data into the table MealType
INSERT INTO MealType(id, name, isActive) VALUES (1, 'Prato Principal', 1);
INSERT INTO MealType(id, name, isActive) VALUES (2, 'Bebida', 1);
INSERT INTO MealType(id, name, isActive) VALUES (3, 'Sobremesa', 1);

-- Inserting data into the table Meal
INSERT INTO Meal(name, idMealType, price, isActive) VALUES ('Massa à bolonhesa', 1, 0.99, 1);
INSERT INTO Meal(name, idMealType, price, isActive) VALUES ('Água', 2, 0.49, 1);
INSERT INTO Meal(name, idMealType, price, isActive) VALUES ('Mousse de Chocolate', 3, 0.49, 1);

-- Inserting data into the table TicketMeal
INSERT INTO TicketMeal(idUser, idMeal, idDrink, idDessert, price, date, isActive) VALUES (120764, 1, 2, 3, 1.97, '2024-04-04', 1);
INSERT INTO TicketMeal(idUser, idMeal, idDrink, idDessert, price, date, isActive) VALUES (120764, 1, 2, NULL, 1.48, '2024-04-05', 1);
INSERT INTO TicketMeal(idUser, idMeal, idDrink, idDessert, price, date, isActive) VALUES (120764, 1, NULL, 3, 1.97, '2024-04-04', 1);
INSERT INTO TicketMeal(idUser, idMeal, idDrink, idDessert, price, date, isActive) VALUES (120764, 1, 2, NULL, 1.48, '2024-04-05', 1);
INSERT INTO TicketMeal(idUser, idMeal, idDrink, idDessert, price, date, isActive) VALUES (120764, 1, 2, 3, 1.97, '2024-04-02', 1);
INSERT INTO TicketMeal(idUser, idMeal, idDrink, idDessert, price, date, isActive) VALUES (120764, 1, 2, NULL, 1.48, '2024-04-01', 1);
