from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Dummy data simulating a real database query
    users = [
        {"id": 1, "username": "admin", "role": "Administrator", "status": "Active"},
        {"id": 2, "username": "alice", "role": "Standard User", "status": "Active"},
        {"id": 3, "username": "bob", "role": "Standard User", "status": "Suspended"}
    ]
    
    # Sensitive backend configurations exposed to the internal network
    config = {
        "DB_MASTER_PASSWORD": "super_secret_internal_password_123",
        "AWS_BACKUP_BUCKET": "s3://internal-company-backups-xyz",
        "INTERNAL_API_KEY": "xoxb-1234567890-qwertyuiop"
    }
    
    return render_template('index.html', users=users, config=config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)