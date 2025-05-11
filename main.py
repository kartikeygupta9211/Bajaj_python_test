import requests

# Developer info
your_name = "John Doe"
your_reg_no = "REG12347"
your_email = "john@example.com"

# Step 1: Generate webhook and token
generate_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
generate_body = {
    "name": your_name,
    "regNo": your_reg_no,
    "email": your_email
}

response = requests.post(generate_url, json=generate_body)
if response.status_code == 200:
    data = response.json()
    webhook_url = data.get("webhook")
    access_token = data.get("accessToken")
    print("Webhook URL:", webhook_url)
    print("Access Token:", access_token)
else:
    print("Failed to generate webhook:", response.text)
    exit()

# Step 2: Show assigned question
if int(your_reg_no[-1]) % 2 == 0:
    print("Your Question (Even): https://drive.google.com/file/d/1PO1ZvmDqAZJv77XRYsVben11Wp2HVb/view")
else:
    print("Your Question (Odd): https://drive.google.com/file/d/1q8F8g0EpyNzd5BWk-voe5CKbsxoskJWY/view")

# Step 3: Final SQL query
final_sql_query = """
SELECT 
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    FLOOR(DATEDIFF(CURRENT_DATE(), e.DOB) / 365.25) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE DAY(p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1;
"""

# Step 4: Submit the SQL query
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}
submit_body = {
    "finalQuery": final_sql_query.strip()
}
submit_response = requests.post(webhook_url, json=submit_body, headers=headers)

if submit_response.status_code == 200:
    print("✅ Successfully submitted your SQL query!")
else:
    print("Submission failed:", submit_response.text)
