import sqlite3

query = """
SELECT 
    tv.name AS tv_name,
    tv.price AS tv_price,
    fridge.name AS fridge_name,
    fridge.price AS fridge_price,
    dw.name AS dishwasher_name,
    dw.price AS dishwasher_price,
    (tv.price + fridge.price + dw.price) AS total_price
FROM 
    tvs tv
CROSS JOIN 
    fridges fridge
CROSS JOIN 
    dishwashers dw
WHERE 
    (tv.price + fridge.price + dw.price) < 1500
ORDER BY 
    total_price ASC
LIMIT 5;
"""

with sqlite3.connect("appliances.db") as conn:
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    print("Verification Query Results:")
    print("---------------------------")
    for row in results:
        print(
            f"TV: {row[0]} (€{row[1]}), Fridge: {row[2]} (€{row[3]}), DW: {row[4]} (€{row[5]}) | Total: €{row[6]}"
        )
