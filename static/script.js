// Vanilla JavaScript - No external libraries
async function predict() {
    const symptomsArray = [];
    const btn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');

    // Gather selected checkboxes
    document.querySelectorAll("input:checked").forEach(el => {
        symptomsArray.push(el.value);
    });

    if (symptomsArray.length === 0) {
        alert("SYSTEM ALERT: Please select at least one symptom to proceed.");
        return;
    }

    // 1. Trigger Loading Animation State
    btn.disabled = true;
    btnText.innerText = "Processing AI Data...";
    btnSpinner.style.display = "block";

    const symptomsString = symptomsArray.join(", ");

    try {
        // 2. Fetch data from Flask backend
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                symptoms: symptomsArray,
                symptoms_text: symptomsString
            })
        });

        const data = await res.json();

        // Determine risk level class for dynamic styling
        let riskClass = "risk-low";
        if (data.risk) {
            const r = data.risk.toLowerCase();
            if (r.includes("high")) riskClass = "risk-high";
            else if (r.includes("medium")) riskClass = "risk-medium";
        }

        // 3. Inject HTML into the modal
        document.getElementById("popup-result").innerHTML = `
                    <h2 class="result-title">[ Analysis Complete ]</h2>

                    <div class="data-row">
                        <strong>Primary Match:</strong> 
                        <span style="color:var(--text-main);">${data.disease || 'Undetermined'}</span>
                    </div>

                    <div class="data-row ${riskClass}">
                        <strong>Threat Level:</strong> 
                        <span>${data.risk || 'Unknown'}</span>
                    </div>

                    <div class="data-row">
                        <strong>Protocol:</strong> 
                        <span style="color:var(--text-main);">${data.suggestion || 'Awaiting medical advice.'}</span>
                    </div>

                    <div class="ai-analysis-container">
                        <h3>> Agent Report //</h3>
                        <div class="ai-text">${data.ai_result || 'No AI data returned.'}</div>
                    </div>
                `;

        // 4. Show the modal
        document.getElementById("popup").style.display = "flex";

    } catch (error) {
        console.error(error);
        alert("Connection Error. Please ensure your Flask server is running.");
    } finally {
        // 5. Reset the button state whether it succeeded or failed
        btn.disabled = false;
        btnText.innerText = "Initiate Scan";
        btnSpinner.style.display = "none";
    }
}

// Close the modal
function closePopup() {
    document.getElementById("popup").style.display = "none";
}

// Close modal if user clicks outside the content box
window.onclick = function (event) {
    const popup = document.getElementById("popup");
    if (event.target === popup) {
        closePopup();
    }
}
