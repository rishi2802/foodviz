function uploadImage(event) {
            const image = document.getElementById('foodImage');
            image.src = URL.createObjectURL(event.target.files[0]);

            setTimeout(() => {
                document.getElementById('foodName').innerText = 'Grilled Chicken Salad';

                const nutritionData = [
                    { nutrient: 'Protein', value: '3.4869g' },
                    { nutrient: 'Total Fat', value: '17.2414g' },
                    { nutrient: 'Total Carbohydrates', value: '23.9056g' },
                    { nutrient: 'Calories', value: '261.4983kcal' },
                    { nutrient: 'Sugars', value: '1.5911g' },
                    { nutrient: 'Fiber', value: '2.0846g' },
                    { nutrient: 'Calcium', value: '16.7377mg' },
                    { nutrient: 'Iron', value: '0.7234mg' },
                    { nutrient: 'Magnesium', value: '17.0777mg' },
                    { nutrient: 'Phosphorus', value: '52.0771mg' },
                    { nutrient: 'Potassium', value: '189.0885mg' },
                    { nutrient: 'Sodium', value: '423.2966mg' },
                    { nutrient: 'Vitamin A', value: '133.6676µg' },
                    { nutrient: 'Vitamin E', value: '0.9749mg' },
                    { nutrient: 'Vitamin D', value: '0.1917µg' },
                    { nutrient: 'Vitamin C', value: '9.9027mg' },
                    { nutrient: 'Vitamin B1 (Thiamin)', value: '0.0981mg' },
                    { nutrient: 'Vitamin B2 (Riboflavin)', value: '0.0375mg' },
                    { nutrient: 'Vitamin B3 (Niacin)', value: '0.9344mg' },
                    { nutrient: 'Vitamin B6', value: '0.1391mg' },
                    { nutrient: 'Folate', value: '18.5009µg' },
                    { nutrient: 'Vitamin B12', value: '0.0217µg' },
                    { nutrient: 'Vitamin K', value: '18.9010µg' }
                ];

                const nutritionTableBody = document.getElementById('nutritionData');
                nutritionTableBody.innerHTML = ''; // Clear previous data
                nutritionData.forEach(item => {
                    const row = `<tr><td>${item.nutrient}</td><td>${item.value}</td></tr>`;
                    nutritionTableBody.innerHTML += row;
                });

                const allergenData = [
                    { allergen: 'Peanuts', sideEffects: 'Anaphylaxis, hives, swelling' },
                    { allergen: 'Soy', sideEffects: 'Respiratory issues, skin irritation' }
                ];

                const allergenTableBody = document.getElementById('allergenData');
                allergenTableBody.innerHTML = ''; // Clear previous data
                allergenData.forEach(item => {
                    const row = `<tr><td>${item.allergen}</td><td>${item.sideEffects}</td></tr>`;
                    allergenTableBody.innerHTML += row;
                });
            }, 1000);
        }