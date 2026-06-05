import time
import psycopg2
import os
import sys

def wait_for_db():
    db_url = os.environ.get('DATABASE_URL', 'postgresql://user:password@db:5432/locative_db')
    
    # Parser l'URL
    parts = db_url.replace('postgresql://', '').split('@')
    user_pass = parts[0].split(':')
    host_db = parts[1].split('/')
    host_port = host_db[0].split(':')
    
    user = user_pass[0]
    password = user_pass[1] if len(user_pass) > 1 else ''
    host = host_port[0]
    port = host_port[1] if len(host_port) > 1 else '5432'
    dbname = host_db[1] if len(host_db) > 1 else 'locative_db'
    
    print(f"Attente de PostgreSQL sur {host}:{port}...")
    
    for i in range(30):
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname=dbname,
                connect_timeout=2
            )
            conn.close()
            print("PostgreSQL est prêt !")
            return True
        except Exception as e:
            print(f"Tentative {i+1}/30: {str(e)[:50]}...")
            time.sleep(2)
    
    print("Impossible de se connecter à PostgreSQL")
    return False

if __name__ == '__main__':
    if wait_for_db():
        sys.exit(0)
    else:
        sys.exit(1)
