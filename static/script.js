document.getElementById('emailForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const companyName = document.getElementById('companyName').value;
    const industry = document.getElementById('industry').value;
    const requirements = document.getElementById('requirements').value;
    
    const submitBtn = document.getElementById('submitBtn');
    const errorBox = document.getElementById('errorBox');
    const resultContainer = document.getElementById('resultContainer');
    const emailOutput = document.getElementById('emailOutput');

    // Reset UI state for a fresh search
    errorBox.style.display = 'none';
    resultContainer.style.display = 'none';
    submitBtn.innerText = 'Generating Draft... ⏳';
    submitBtn.disabled = true;

    try {
        const response = await fetch('/generate-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                company_name: companyName,
                industry: industry,
                requirements: requirements
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Something went wrong while generating.');
        }

        // Output the generated text inside the results container
        emailOutput.textContent = data.email;
        resultContainer.style.display = 'block';

    } catch (err) {
        errorBox.textContent = err.message;
        errorBox.style.display = 'block';
    } finally {
        // Restore button state
        submitBtn.innerText = 'Generate Outreach Email 🚀';
        submitBtn.disabled = false;
    }
});
