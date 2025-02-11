import os
import json
import mysql.connector
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)


GOOGLE_CREDENTIALS_JSON ={
  "type": "service_account",
  "project_id": "dogwood-vision-446617-m3",
  "private_key_id": "8678845b1069c2132f8a99e41da0ced09286d91a",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCGjYw7MNEP8TGg\n8YPGnHYOUm3gz1wNuFwZ/hDFs2+X+CsVC+MUKiUJaBcgkPoXZVxwU5yfMH5Fbsyf\nzlXzupNd5llgCVnNowrA/Mm09mu9png7rb1O9kMFPvyePFTP6xgkwyGIRYt3hvkV\ndJTe+xXoFcEP/SCmEKp5r1ZyDzaT3H2ThqHYzrnrw4QF7jVf3K/uXsOe90/b6/zR\nIOQx5dhNtZXWs6Q2EHzsJwNlL83EgErcH3mO0KPxcbp23gu/tfm8x4aT8qrudXXb\n7LpGainIXz9TJKTVY6EKaraS7MSpYXklZ4ME+HuZuvyfV3HgpPNNVzKNVc8ZWnMG\nwjw5pjzjAgMBAAECggEAFhNmNRXqzxtLAbVuYeksw2fJyE8tMsETN16EYPNyNTRN\n2Tuki5vojLULyleO+MS0GGfXdBTQOtMVdoizeHQdlpPjCQsvtTnxWz1+WJbvkWOd\nKWl1fF2SHGu7pbiPT7eqM+nh+Ao0+izmdBs3C6iVbQkYrmdg8m4cki9u1vLhCPww\noutIgOm0p+8hH85VeMBSDu7+6p3mKs8UBeIlN3JT9GvxnEufbtDhpHwNVZaISOSa\n1U6SypAhOJQ7HDa4qCcDL7x40xsKDb5fbh99NDCPu0xYmCLm6cq1QAiwbBtJ0h+f\ncal/h2FkdgLu7QMCManzGkUxg3NnyvOSfJw6/WjjjQKBgQC9CDljJjwO5jndQmDX\nqW9qBggZwl4sYdsOZkFhFg8bmHRrdOA2ajqCieG8SstFLbVd59Qwjs31DnRoPr0e\nx/LEHXS0aNGdQqijkRHXpfZqawHkxNWKbNzyurA38HoW0lfGVmyaPh31CBm7+N1F\n0+RYDxYi6o12GN9mCNLK3ABIBQKBgQC2OHljNwm4bCUqpvKIh68Ykf77DsFI4wUL\nAyXQ5oro4OvuP49d+hyngozZo/wWzGlvyJucx1MT0Ub3zuAobq555iNMRKGUUBeB\nGxXZ1lMDSBP9m7aV05bz9Qsus+HzDZutnIsZtLmyl8lxUOZB49KBBl5l8B1BLE2j\nPhT5c44NxwKBgQCzxraNTTehE+PEQfTIJiQHuWTK2selfgtPToCvTMNhg0R1TdpO\n5ghvTaKZ6KgZSrdKb8ilxaqqfOzIl6JVO+PuD/WF/oob/eFUbguCBByuaMaMQ4ay\n94XKczJUgSgbvEAuKNNwfdMPznxrAOuwFSz9cpui6V9QCaes6odO1pyN4QKBgHHV\nU9esMVFZldpQUuEByluSEPTrocmTsLnRbJVVAGA86oZ6hGiT78ShZLYtoDTp29Au\nRTAqwPZ3XVs/jH8Vrb+PCmwBz+LkKdrIfd0I6/D33S0oUmbEuN+MLEEvtK5uyNsr\nGSak5QDxm7FDdaSh2wYpYV1TJCNrttCM3vN6wbpPAoGAWyRXgZ4HYfYQsLeVv0Ru\nejo8ShgW4WAShcIT+EBM+dkA9MJsgzR35ux1U3wwty6iXviOsfVoC8t8uN1losXk\nvhZwZvfU6lI68GzZpqsIuXhluJdj04WP6k/pQIvMZBVeT7yum06SKP3bbN+pk1SU\nPb9UZqWq9ecURmkqnbIpz2M=\n-----END PRIVATE KEY-----\n",
  "client_email": "mysql-917@dogwood-vision-446617-m3.iam.gserviceaccount.com",
  "client_id": "102785969578088866452",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mysql-917%40dogwood-vision-446617-m3.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


if GOOGLE_CREDENTIALS_JSON:
    with open("/tmp/google_creds.json", "w") as f:
        f.write(json.dumps(GOOGLE_CREDENTIALS_JSON))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/google_creds.json"
else:
    raise ValueError("Google Credentials not found in environment variables!")

# 🔹 Set up Gemini API Key
genai.configure(api_key="AIzaSyAWqysTvHZtAM8qkHmu0OFbK45HM_Io0Vo")  # Replace with your Gemini API key

# 🔹 Database connection details
DB_CONFIG = {
    "host": "34.47.219.83",  # Public IP of your Cloud SQL instance
    "port": 3306,
    "user": "nimo",
    "password": "nimo",
    "database": "usformulary"
    


    
}

# 📌 **Function to Generate SQL Query Using Gemini AI**
def generate_sql(user_input):
    prompt = f'''You are a SQL expert. Generate a safe, read-only SQL query.
    
    ## Dataset Information:
    - **basic_drug_formulary**: FORMULARY_ID, FORMULARY_VERSION, CONTRACT_YEAR, RXCUI, NDC, TIER_LEVEL_VALUE, QUANTITY_LIMIT_YN, QUANTITY_LIMIT_AMOUNT, QUANTITY_LIMIT_DAYS, PRIOR_AUTHORIZATION_YN, STEP_THERAPY_YN
    - **beneficiary_cost_file**: CONTRACT_ID, PLAN_ID, SEGMENT_ID, COVERAGE_LEVEL, TIER, DAYS_SUPPLY, COST_TYPE_PREF, COST_AMT_PREF, COST_MIN_AMT_PREF, COST_MAX_AMT_PREF, COST_TYPE_NONPREF, COST_AMT_NONPREF, COST_MIN_AMT_NONPREF, COST_MAX_AMT_NONPREF, COST_TYPE_MAIL_PREF, COST_AMT_MAIL_PREF, COST_MIN_AMT_MAIL_PREF, COST_MAX_AMT_MAIL_PREF, COST_TYPE_MAIL_NONPREF, COST_AMT_MAIL_NONPREF, COST_MIN_AMT_MAIL_NONPREF, COST_MAX_AMT_MAIL_NONPREF, TIER_SPECIALTY_YN, DED_APPLIES_YN
    - **geo_loc**: COUNTY_CODE, STATENAME, COUNTY, MA_REGION_CODE, MA_REGION, PDP_REGION_CODE, PDP_REGION
    - **plan_info**: CONTRACT_ID, PLAN_ID, SEGMENT_ID, CONTRACT_NAME, PLAN_NAME, FORMULARY_ID, PREMIUM, DEDUCTIBLE, MA_REGION_CODE, PDP_REGION_CODE, STATE, COUNTY_CODE, SNP, PLAN_SUPPRESSED_YN

    ## Rules:
    - Generate **only SELECT queries**. No `DELETE`, `UPDATE`, `DROP`, or `INSERT`.
    - Ensure query is safe and read-only.
    
    **User Request:** {user_input}
    
    Generate the SQL query below (without ` ```sql ` code blocks):'''

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    if response and response.candidates:
        return response.candidates[0].content.parts[0].text.strip()
    else:
        return None

# 📌 **API Route to Generate and Run SQL Queries**
@app.route("/query", methods=["POST"])

def execute_query():
    try:
        # Log incoming request
        print("Received Request:", request.data)

        # Parse JSON input
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON format"}), 400  # More detailed error

        user_input = data.get("question")
        if not user_input:
            return jsonify({"error": "No question provided"}), 400

        # 🔹 Generate SQL Query using Gemini AI
        sql_query = generate_sql(user_input)
        if not sql_query:
            return jsonify({"error": "Failed to generate SQL query"}), 500

        # 🔹 Connect to MySQL Database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 🔹 Execute Query
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # 🔹 Format Response
        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in rows]

        # Close Connection
        cursor.close()
        conn.close()

        return jsonify({"query": sql_query, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# 📌 **Run Flask App**
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)