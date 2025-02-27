from fastapi import FastAPI
from pydantic import BaseModel
import random
from fastapi.responses import HTMLResponse

app = FastAPI(title="EcoLogits Calculator", description="Tracks AI energy consumption & environmental impact")

class ProviderRequest(BaseModel):
    provider: str

def calculate_impact():
    """Simulates the environmental impact of AI model inference."""
    energy_used = round(random.uniform(0.5, 3.5), 2)  # Simulated energy use (kWh)
    carbon_footprint = round(energy_used * 0.4, 2)  # Simulated CO₂ emissions (kg)
    abiotic_resources = round(energy_used * 0.02, 4)  # Simulated abiotic resource depletion (kg Sb eq)
    primary_energy = round(energy_used * 100, 2)  # Simulated primary energy use (kJ)
    water_usage = round(energy_used * 10, 2)  # Simulated water usage (L)

    return energy_used, carbon_footprint, abiotic_resources, primary_energy, water_usage

def get_ai_efficiency_tip(energy_used):
    """Provides AI efficiency recommendations based on energy usage."""
    if energy_used > 3:
        return "⚠️ Your AI model consumes high energy! Consider using smaller models or fine-tuning instead of training from scratch to save 30% energy."
    elif energy_used > 2:
        return "🔧 Optimize inference by using quantization and batch processing to reduce energy by 20%."
    else:
        return "✅ Your AI model is running efficiently! Keep using optimized architectures for sustainability."

def get_offset_suggestion(carbon_footprint):
    """Provides a carbon offset recommendation based on CO₂ emissions."""
    if carbon_footprint > 1:
        return "🌱 Consider investing in renewable energy credits to neutralize your carbon impact!"
    else:
        return "💚 You're already doing well! Still, adopting energy-efficient hardware can further minimize your footprint."

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌱 EcoLogits Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            color: #333;
            margin: 0;
            padding: 20px;
            text-align: center;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #2e7d32;
            font-size: 28px;
        }
        p {
            font-size: 16px;
            color: #555;
        }
        select, button {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #2e7d32;
            color: white;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #43a047;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #e8f5e9;
            border-left: 5px solid #2e7d32;
            text-align: left;
            font-size: 18px;
        }
        .impact-container {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .impact-box {
            background: #ffffff;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            width: 45%;
            margin: 10px;
            font-size: 16px;
        }
        .suggestion {
            margin-top: 20px;
            padding: 15px;
            background: #fff3cd;
            border-left: 5px solid #ff9800;
            text-align: left;
            font-size: 18px;
        }
    </style>
    <script>
        async function calculate() {
            let provider = document.getElementById('provider').value;
            let response = await fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ provider })
            });
            let data = await response.json();
            document.getElementById('result').innerHTML = `
                <div class="impact-container">
                    <div class="impact-box">⚡ <strong>Energy Used:</strong> ${data.energy_used_kwh} kWh</div>
                    <div class="impact-box">🌍 <strong>CO₂ Emissions:</strong> ${data.carbon_footprint_kg} kg</div>
                    <div class="impact-box">🔩 <strong>Abiotic Resources:</strong> ${data.abiotic_resources_kg} kg Sb eq</div>
                    <div class="impact-box">🔥 <strong>Primary Energy:</strong> ${data.primary_energy_kj} kJ</div>
                    <div class="impact-box">💧 <strong>Water Usage:</strong> ${data.water_usage_l} L</div>
                </div>
                <div class="suggestion">
                    <strong>💡 AI Efficiency Tip:</strong> ${data.ai_tip}
                </div>
                <div class="suggestion">
                    <strong>🌱 Carbon Offset Suggestion:</strong> ${data.offset_suggestion}
                </div>
                <p><em>${data.eco_tip}</em></p>
            `;
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>🌱 EcoLogits Calculator</h1>
        <p>EcoLogits tracks the energy consumption and environmental footprint of AI models.</p>
        <label for="provider">🤖 Select AI Provider:</label>
        <select id="provider">
            <option value="openai">OpenAI</option>
            <option value="huggingface">Hugging Face</option>
            <option value="anthropic">Anthropic</option>
        </select>
        <button onclick="calculate()">⚡ Calculate Impact</button>
        <div id="result" class="result"></div>
    </div>
</body>
</html>
    """

@app.post("/calculate")
def track_energy(data: ProviderRequest):
    energy_used, carbon_footprint, abiotic_resources, primary_energy, water_usage = calculate_impact()
    ai_tip = get_ai_efficiency_tip(energy_used)
    offset_suggestion = get_offset_suggestion(carbon_footprint)

    return {
        "provider": data.provider,
        "energy_used_kwh": energy_used,
        "carbon_footprint_kg": carbon_footprint,
        "abiotic_resources_kg": abiotic_resources,
        "primary_energy_kj": primary_energy,
        "water_usage_l": water_usage,
        "ai_tip": ai_tip,
        "offset_suggestion": offset_suggestion,
        "eco_tip": "Consider optimizing model efficiency to reduce energy use! 🌍"
    }

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)