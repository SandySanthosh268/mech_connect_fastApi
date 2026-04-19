import psycopg2
from app.core.config import settings

def promote_to_admin(user_id, new_email):
    # Convert async engine URL to sync psycopg2 URL if needed
    db_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Corrected SQL with single quotes for strings
        query = "UPDATE users_user SET role = %s, email = %s WHERE id = %s"
        cur.execute(query, ('ROLE_ADMIN', new_email, user_id))
        
        conn.commit()
        if cur.rowcount > 0:
            print(f"Successfully updated User ID {user_id} to ROLE_ADMIN with email {new_email}")
        else:
            print(f"No user found with ID {user_id}")
            
        conn.close()
    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == "__main__":
    promote_to_admin(2, "admin@test.com")
