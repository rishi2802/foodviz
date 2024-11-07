async function uploadImage(event) {
    const fileInput = event.target.files[0];
    const formData = new FormData();
    formData.append("file", fileInput);

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

            // Update allergen information (if needed)
            const allergenTableBody = document.getElementById("allergenData");
            allergenTableBody.innerHTML = ''; // Clear previous data
            result.allergenData.forEach(item => {
                const row = `<tr><td>${item.allergen}</td><td>${item.sideEffects}</td></tr>`;
                allergenTableBody.innerHTML += row;
            });
        } else {
            const errorData = await response.json();
            console.error("Prediction failed:", errorData.error);
            alert("Error: " + errorData.error);
        }
    } catch (error) {
        console.error("Error during image upload:", error);
        alert("Error uploading image, please try again.");
    }

    // Update the displayed image
    const image = document.getElementById("foodImage");
    image.src = URL.createObjectURL(fileInput);
}
