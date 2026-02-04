async function checkScam() {
    const message = document.getElementById("message").value;
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "Checking...";

    try {
        const response = await fetch(
            "https://scamguard-m7h6.onrender.com/api/honeypot/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "x-api-key": "my-honeypot-key"
                },
                body: JSON.stringify({
                    message: message,
                    turn: 1
                })
            }
        );

        const data = await response.json();

        resultDiv.innerHTML = `
            <b>Scam Detected:</b> ${data.scam_detected}<br>
            <b>Scam Type:</b> ${data.scam_type}<br>
            <b>Agent Reply:</b> ${data.reply}<br><br>
            <b>Extracted Intelligence:</b>
            <pre>${JSON.stringify(data.extracted_intelligence, null, 2)}</pre>
        `;
    } catch (error) {
        resultDiv.innerHTML = "Error connecting to API.";
    }
}
