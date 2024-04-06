from flask import Flask, request, jsonify, g, render_template
from flask_cors import CORS
import sqlite3
from hashlib import sha256 

app = Flask(__name__)
CORS(app)

@app.route('/')
def authentication():
    return render_template('authentication.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/ticket')
def ticket():
    return render_template('ticket.html')

@app.route('/contentHub')
def contentHub():
    return render_template('contentHub.html')

def get_db_connection():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect("uameal.db")
    return conn

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/login", methods=["POST"])
def login():
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()
    pinHash = sha256(data["pin"].encode('utf-8')).hexdigest()

    query = cur.execute("SELECT name, pin, mecNumber FROM Student WHERE mecNumber=? AND pin=? AND isActive=?", (data["mecNumber"], pinHash, 1))
    dataDB = query.fetchone()

    if dataDB is None:
        return "Pin Errado!", 404
    else:   
        obj = {
                "mecNumber": dataDB[2],
                "name": dataDB[0],
                "enc": sha256((str(dataDB[2]) + "_" + str(dataDB[0])).encode('utf-8')).hexdigest()
            } 

        return jsonify(obj), 200

@app.route("/getDashboardInitialData", methods=["POST"])
def getDashboardInitialData():
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()

    obj = {}
    transactions = []
    tickets = []

    #Alterar para data
    query = cur.execute("SELECT operation, balanceBeforeTransaction, transactionValue, balanceAfterTransaction, date FROM Transactions WHERE idUser=? AND isActive=? ORDER BY date DESC LIMIT 5", (data["mecNumber"], 1))
    dataDB = query.fetchall()

    for transaction in dataDB:
        transactions.append({
            "operation": transaction[0],
            "balanceBeforeTransaction": transaction[1],
            "transactionValue": transaction[2],
            "balanceAfterTransaction": transaction[3],
            "date": transaction[4]
        })


    query = cur.execute("""SELECT 
                        TicketMeal.id, 
                        Meal.name AS meal_name, 
                        Drink.name AS drink_name, 
                        Dessert.name AS dessert_name, 
                        TicketMeal.price, 
                        TicketMeal.date 
                        FROM TicketMeal 
                        LEFT JOIN Meal AS Meal ON TicketMeal.idMeal = Meal.id 
                        LEFT JOIN Meal AS Drink ON TicketMeal.idDrink = Drink.id 
                        LEFT JOIN Meal AS Dessert ON TicketMeal.idDessert = Dessert.id 
                        WHERE TicketMeal.idUser=? AND TicketMeal.isActive=? 
                        ORDER BY TicketMeal.date DESC 
                        LIMIT 5
                        """, (data["mecNumber"], 1))
        
    dataDB = query.fetchall()
        
    for ticket in dataDB:
        tickets.append({
            "id": ticket[0],
            "meal": ticket[1],
            "drink": ticket[2],
            "dessert": ticket[3],
            "price": ticket[4],
            "date": ticket[5]     
        })

    obj["transactions"] = transactions
    obj["tickets"] = tickets

    return jsonify(obj), 200

@app.route("/getUserInitialData", methods=["POST"])
def getUserInitialData():
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()

    query = cur.execute("SELECT name, course, mecNumber, balance FROM Student WHERE mecNumber=? AND isActive=?", (data["mecNumber"], 1))
    dataDB = query.fetchone()

    if dataDB is None:
        return "Error", 404
    else:
        if data["enc"] != (sha256((str(dataDB[2]) + "_" + str(dataDB[0])).encode('utf-8')).hexdigest()):
            return "Error", 401

        obj = {}      
        user = {
                "mecNumber": dataDB[2],
                "name": dataDB[0],
                "course": dataDB[1],
                "balance": dataDB[3]
            }        
        obj["user"] = user
        
        return jsonify(obj), 200


if __name__ == "__main__":
    app.run(debug=True)

'''
@app.route("/getDashboardInitialData", methods=["POST"])
def getDashboardInitialData():
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()

    query = cur.execute("SELECT name, course, mecNumber, balance FROM Student WHERE mecNumber=? AND isActive=?", (data["mecNumber"], 1))
    dataDB = query.fetchone()

    if dataDB is None:
        return "Error", 404
    else:

        if data["enc"] != (sha256((str(dataDB[2]) + "_" + str(dataDB[0])).encode('utf-8')).hexdigest()):
            return "Error", 401

        obj = {}
        transactions = []
        tickets = []

        user = {
                "mecNumber": dataDB[2],
                "name": dataDB[0],
                "course": dataDB[1],
                "balance": dataDB[3]
            } 
        
        obj["user"] = user
        
        #Alterar para data
        query = cur.execute("SELECT operation, balanceBeforeTransaction, transactionValue, balanceAfterTransaction, date FROM Transactions WHERE idUser=? AND isActive=? ORDER BY date DESC LIMIT 5", (data["mecNumber"], 1))
        dataDB = query.fetchall()

        for transaction in dataDB:
            transactions.append({
                "operation": transaction[0],
                "balanceBeforeTransaction": transaction[1],
                "transactionValue": transaction[2],
                "balanceAfterTransaction": transaction[3],
                "date": transaction[4]
            })


        query = cur.execute("""SELECT 
                            TicketMeal.id, 
                            Meal.name AS meal_name, 
                            Drink.name AS drink_name, 
                            Dessert.name AS dessert_name, 
                            TicketMeal.price, 
                            TicketMeal.date 
                            FROM TicketMeal 
                            LEFT JOIN Meal AS Meal ON TicketMeal.idMeal = Meal.id 
                            LEFT JOIN Meal AS Drink ON TicketMeal.idDrink = Drink.id 
                            LEFT JOIN Meal AS Dessert ON TicketMeal.idDessert = Dessert.id 
                            WHERE TicketMeal.idUser=? AND TicketMeal.isActive=? 
                            ORDER BY TicketMeal.date DESC 
                            LIMIT 5
                            """, (data["mecNumber"], 1))
        
        dataDB = query.fetchall()
        
        for ticket in dataDB:
            tickets.append({
                "id": ticket[0],
                "meal": ticket[1],
                "drink": ticket[2],
                "dessert": ticket[3],
                "price": ticket[4],
                "date": ticket[5]     
            })

        obj["transactions"] = transactions
        obj["tickets"] = tickets

        return jsonify(obj), 200

'''