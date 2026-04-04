from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/latest/meta-data/iam/security-credentials/ssrf-role')
def metadata():
    return jsonify({
        "Code": "Success",
        "Type": "AWS-HMAC",
        "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
        "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "Token": "IQoJb3JpZ2luX2VjEBAaCXVzLWVhc3QtMSJHMEUCIQ...",
        "Expiration": "2026-04-05T11:31:30Z"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)