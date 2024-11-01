document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.getElementById('calorie-form');
    const formContainer = document.getElementById('form-container');
    const resultContainer = document.getElementById('result-container');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Perform the form submission using AJAX to avoid page reload
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                formContainer.style.display = 'none';
                resultContainer.style.display = 'block';

                resultContainer.innerHTML = `
                    <p>Maintenance Calories: ${data.calculated_calories.maintain_weight}</p>
                    <p>Mild Weight Loss: ${data.calculated_calories.mild_weight_loss}</p>
                    <p>Weight Loss: ${data.calculated_calories.weight_loss}</p>
                    <p>Extreme Weight Loss: ${data.calculated_calories.extreme_weight_loss}</p>
                    <p>Mild Weight Gain: ${data.calculated_calories.mild_weight_gain}</p>
                    <p>Weight Gain: ${data.calculated_calories.weight_gain}</p>
                    <p>Extreme Weight Gain: ${data.calculated_calories.extreme_weight_gain}</p>
                `;
            } else {
                // Handle errors
                console.error('Error calculating calories');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
