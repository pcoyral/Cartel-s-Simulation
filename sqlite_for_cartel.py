import sqlite3
import json

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("cartel_simulation.db")
cursor = conn.cursor()

# Step 1: Create main SimulationRuns table
cursor.execute("""
CREATE TABLE IF NOT EXISTS SimulationRuns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    parameters TEXT,
    software_version TEXT
)
""")

# Step 2: Create ProductionEvents table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ProductionEvents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    field_name TEXT NOT NULL,
    amount_produced INTEGER NOT NULL,
    FOREIGN KEY (simulation_id) REFERENCES SimulationRuns(id)
)
""")

# Step 3: Create ProcessingEvents table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ProcessingEvents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    factory_name TEXT NOT NULL,
    raw_amount INTEGER NOT NULL,
    processed_amount INTEGER NOT NULL,
    FOREIGN KEY (simulation_id) REFERENCES SimulationRuns(id)
)
""")

# Step 4: Create DeliveryEvents table
cursor.execute("""
CREATE TABLE IF NOT EXISTS DeliveryEvents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    truck_id TEXT NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    cargo_amount INTEGER NOT NULL,
    success BOOLEAN NOT NULL,
    delivery_time FLOAT,
    failure_reason TEXT,
    FOREIGN KEY (simulation_id) REFERENCES SimulationRuns(id)
)
""")

# Step 5: Create LawEnforcementEvents table
cursor.execute("""
CREATE TABLE IF NOT EXISTS LawEnforcementEvents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    event_type TEXT NOT NULL,
    location TEXT NOT NULL,
    impact TEXT,
    FOREIGN KEY (simulation_id) REFERENCES SimulationRuns(id)
)
""")

# Step 6: Create StatusSnapshots table (periodic health checks)
cursor.execute("""
CREATE TABLE IF NOT EXISTS StatusSnapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    queue_lengths TEXT,
    factory_idle_times TEXT,
    distributor_status TEXT,
    FOREIGN KEY (simulation_id) REFERENCES SimulationRuns(id)
)
""")

# Step 7: Create UpgradeEvents table (dynamic upgrades)
cursor.execute("""
CREATE TABLE IF NOT EXISTS UpgradeEvents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL,
    upgrade_type TEXT NOT NULL,
    target_entity TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (simulation_id) REFERENCES SimulationRuns(id)
)
""")

# Commit changes
conn.commit()

print("Database schema for cartel simulation created successfully.")

# Close connection
conn.close()
