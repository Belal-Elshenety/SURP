from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
import csv

# Update the URI and password to connect to the Neo4j database
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "newpassword"))

def drop_all_constraints(tx):
    # Drop all constraints
    constraints = tx.run("SHOW CONSTRAINTS")
    for record in constraints:
        constraint_name = record["name"]
        drop_query = f"DROP CONSTRAINT {constraint_name}"
        print(f"Dropping constraint: {constraint_name}")
        tx.run(drop_query)

def delete_all_nodes(tx):
    # Delete all nodes and relationships
    tx.run("MATCH (n) DETACH DELETE n")

def create_initial_schema(tx):
    # Define the constraints to be created
    constraints = [
        "CREATE CONSTRAINT FOR (p:Person) REQUIRE p.name IS UNIQUE",
        "CREATE CONSTRAINT FOR (c:Condition) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT FOR (l:Location) REQUIRE l.name IS UNIQUE"
    ]
    for constraint in constraints:
        try:
            tx.run(constraint)
        except ClientError as er:
            if 'EquivalentSchemaRuleAlreadyExists' in str(er):
                print(f"Constraint already exists: {constraint}")
            else:
                raise

def create_static_guides(tx):
    guides = [
        {"condition": "dementia", "recommendation": "Search in places near water and rivers"},
        {"condition": "diabetes", "recommendation": "Check medical facilities and bakeries"},
    ]
    for guide in guides:
        tx.run("""
        MERGE (c:Condition {name: $condition})
        SET c.recommendation = $recommendation
        """, condition=guide["condition"], recommendation=guide["recommendation"])

def create_person_data(tx, person):
    # Create or match the nodes and relationships
    tx.run("""
    MERGE (p:Person {name: $name, age: $age, health: $health})
    MERGE (l:Location {name: $location})
    MERGE (f:FreeResponse {text: $free_response})
    MERGE (p)-[:LAST_KNOWN_LOCATION]->(l)
    WITH p, f
    MATCH (c:Condition {name: $health})
    MERGE (p)-[:HAS_CONDITION]->(c)
    MERGE (p)-[:HAS_FREE_RESPONSE]->(f)
    """, name=person["name"], age=person["age"], health=person["health"], location=person["location"], free_response=person["free_response"])

# Connect to the database and drop all constraints, delete all nodes
with driver.session() as session:
    session.execute_write(drop_all_constraints)
    session.execute_write(delete_all_nodes)

# Connect to the database and create the initial schema
with driver.session() as session:
    try:
        session.execute_write(create_initial_schema)
    except ClientError as e:
        print(f"Schema initialization failed: {e}")

    try:
        session.execute_write(create_static_guides)
    except ClientError as e:
        print(f"Static guides creation failed: {e}")

# Load person data from CSV and ingest into the database
with open('person_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    with driver.session() as session:
        for row in reader:
            try:
                session.execute_write(create_person_data, row)
            except ClientError as e:
                print(f"Person data creation failed for {row['name']}: {e}")

driver.close()
