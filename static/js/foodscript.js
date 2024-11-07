async function uploadImage(event) {
    const fileInput = event.target.files[0];
    const formData = new FormData();
    formData.append("file", fileInput);
      // Update the displayed image
    const image = document.getElementById("foodImage");
    image.src = URL.createObjectURL(fileInput);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            console.log("Prediction result:", result); // Debugging line

            // Update the UI with only the foodName
            document.getElementById("foodName").innerText = result.foodName;

            // Update the nutritional information (only nutrient and value)
            const nutritionTableBody = document.getElementById("nutritionData");
            nutritionTableBody.innerHTML = ''; // Clear previous data
            result.nutritionData.forEach(item => {
                const row = `<tr><td>${item.nutrient}</td><td>${item.value}</td></tr>`;
                nutritionTableBody.innerHTML += row;
            });

            // Check if allergenData is an object with allergens and sideEffects
            if (result.allergenData && result.allergenData.allergens && result.allergenData.sideEffects) {
                const allergenTableBody = document.getElementById("allergenData");
                allergenTableBody.innerHTML = ''; // Clear previous data
                
                // Display allergens as a comma-separated string and side effects in another column
                const row = `<tr><td>${result.allergenData.allergens.join(', ')}</td><td>${result.allergenData.sideEffects}</td></tr>`;
                allergenTableBody.innerHTML += row;
            } else {
                console.error("Allergen data is missing or malformed.");
            }
        } else {
            const errorData = await response.json();
            console.error("Prediction failed:", errorData.error);
        }
    } catch (error) {
        console.error("Error during image upload:", error);
    }

  
}
