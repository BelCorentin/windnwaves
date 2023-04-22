import sqlite3
from flask import Flask, render_template, request, redirect, url_for


def populate_db():

    create_db()

    spots = [
        {
            "level_required": "Beginner",
            "city": "La Rochelle",
            "wind_orientation": "North-West",
            "wave_or_flat": "Flat",
        },
        {
            "level_required": "Intermediate",
            "city": "Biarritz",
            "wind_orientation": "South-West",
            "wave_or_flat": "Wave",
        },
        {
            "level_required": "Confirmed",
            "city": "Marseille",
            "wind_orientation": "South-East",
            "wave_or_flat": "Flat",
        },
    ]

    for spot_data in spots:
        add_spot(
            level_required=spot_data["level_required"],
            city=spot_data["city"],
            wind_orientation=spot_data["wind_orientation"],
            wave_or_flat=spot_data["wave_or_flat"],
        )


# Get wingfoil spots from the database
def get_spots(level_required, wave_or_flat, city="all"):
    conn = get_db_connection()
    c = conn.cursor()

    # Build the query based on the search criteria
    query = "SELECT * FROM wingfoil_spots WHERE level_required = ? AND wave_or_flat = ? AND city = ?"
    params = (level_required, wave_or_flat, city)

    # Execute the query and get the results
    c.execute(query, params)
    rows = c.fetchall()

    # Build a list of dictionaries containing the spot information
    spots = []
    for row in rows:
        spot = {
            "id": row["id"],
            "level_required": row["level_required"],
            "city": row["city"],
            "wind_orientation": row["wind_orientation"],
            "wave_or_flat": row["wave_or_flat"],
        }
        spots.append(spot)

    # Close the connection and return the list of spots
    conn.close()
    return spots


# Add a wingfoil spot to the database
def add_spot(level_required, city, wind_orientation, wave_or_flat):
    conn = get_db_connection()
    c = conn.cursor()

    # Insert wingfoil spot information into the wingfoil_spots table
    c.execute(
        "INSERT INTO wingfoil_spots (level_required, city, wind_orientation, wave_or_flat) VALUES (?, ?, ?, ?)",
        (level_required, city, wind_orientation, wave_or_flat),
    )

    # Commit changes and close connection
    conn.commit()
    conn.close()


def create_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Create the wingfoil_spots table
    c.execute(
        """CREATE TABLE IF NOT EXISTS wingfoil_spots
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  level_required TEXT NOT NULL,
                  city TEXT NOT NULL,
                  wind_orientation TEXT NOT NULL,
                  wave_or_flat TEXT NOT NULL)"""
    )

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Define the database connection
def get_db_connection():
    conn = sqlite3.connect("wingfoiling.db")
    conn.row_factory = sqlite3.Row
    return conn
