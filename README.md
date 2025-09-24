# Sundarban Mangrove Ecosystem Simulation

An agent-based model (ABM) built with Mesa framework to simulate the complex socio-ecological dynamics of the Sundarban mangrove ecosystem in Bangladesh. This simulation models the interactions between different livelihood groups (Bawalis, Fishers, Farmers) and their impact on mangrove resources under various policy interventions and environmental conditions.

## Overview

The simulation includes:
- **Agent Types**: Bawali (mangrove collectors), Mangrove Fishers, Household Fishers, and Farmers
- **Environmental Factors**: Natural hazards, golpata (mangrove palm) stock dynamics, climate variations
- **Economic Elements**: Loan systems, productivity measures, market dynamics
- **Policy Interventions**: Three different policy scenarios with varying restrictions and support measures
- **Rogue Population**: Non-compliant agents that don't follow regulations

## Key Features

- **Interactive Web Interface**: Real-time parameter adjustment and visualization
- **Policy Analysis**: Compare effects of different management strategies
- **Warning System**: Automatic alerts for unsustainable resource extraction
- **Batch Processing**: Run multiple scenarios for systematic analysis
- **Data Export**: Save results for further analysis

## Installation & Setup

### Prerequisites

- Python 3.7+ 
- pip package manager

### Required Dependencies

Install the following packages in order:

1. **Core dependencies:**
   ```bash
   pip install pandas numpy scipy matplotlib
   ```

2. **Mesa Framework (specific version required):**
   ```bash
   pip install "mesa<3.0"
   ```

3. **Visualization dependencies:**
   ```bash
   pip install solara altair
   ```

### Quick Setup

Run all installations at once:
```bash
pip install pandas numpy scipy matplotlib "mesa<3.0" solara altair
```

## Running the Simulation

Launch the web-based interface for real-time interaction:

```bash
cd scripts
python run.py
```

This will:
- Start a web server (typically on `http://localhost:8524`)
- Open an interactive dashboard in your browser
- Provide sliders to adjust parameters in real-time
- Display live charts and policy recommendations

**Important**: Please always click "Reset" after changing any parameter values.

## Running Analysis Scripts

- **Scenario Analysis**: `python scenario_graph.py`
- **Policy Comparison**: `python policy_graph.py`  
- **Rogue Population Study**: `python rogue_graph.py`

## Key Parameters

### Population Parameters
- **Number of Bawalis** (1-500): Mangrove palm collectors
- **Number of Mangrove Fishers** (1-500): Fishers working in mangrove areas
- **Number of Household Fishers** (1-500): Community-based fishers
- **Number of Farmers** (1-500): Agricultural workers

### Environmental Parameters
- **Natural Hazard Loss** (1-300): Impact of cyclones/storms on mangrove resources
- **Golpata Natural Growth Rate** (1-300): Natural regeneration of mangrove palms
- **Golpata Conservation Growth Rate** (1-300): Enhanced growth under conservation

### Economic Parameters
- **Fertilizer Cost** (0-1.5): Agricultural input costs
- **Land Crop Productivity** (5-30): Agricultural yield capacity
- **Covariance** (0.01-1): Economic correlation factor

### Policy & Behavioral Parameters
- **Policy Selection**: Choose between Policy 1, 2, or 3
- **Rogue Percentage** (0-100%): Proportion of non-compliant population

## Understanding the Output

### Key Metrics Tracked

1. **Golpata Stock**: Total mangrove palm availability
2. **Extraction Capacity**: Resource harvesting capability
3. **Catching Capacity**: Fishing productivity (Mangrove vs Household)
4. **Loan Indicators**: Financial stress levels by group
5. **Crop Production**: Agricultural output capacity
6. **Current Bawali Count**: Active mangrove collectors

### Warning System

The simulation provides automatic alerts for:
- Over-extraction of mangrove resources
- High debt levels among different groups
- Low agricultural productivity
- Declining golpata stock levels

## File Structure

```
main/
├── run.py                  # Main web interface launcher
├── run2.py                 # Batch processing script
├── server.py               # Web server configuration
├── model.py                # Core simulation model
├── agents.py               # Agent definitions and behaviors
├── config/                 # Configuration files
│   ├── initial_parameters.py
│   ├── global_variables.py
│   └── settings.py
├── dataset/               # Input data and results
│   ├── input_data/
│   ├── generated/
│   └── public/
├── plots/                 # Generated visualizations
├── statistics/            # Saved simulation results
├── utils/                 # Helper functions
└── logs/                  # Runtime logs
```

## Results & Analysis

- **Real-time Visualizations**: Charts update automatically during simulation
- **Data Export**: Results saved in `statistics/` folder as CSV files
- **Plot Generation**: Visualizations saved in `plots/` folder
- **Log Files**: Runtime information in `logs/run_log.txt`

## Troubleshooting

### Common Issues

1. **Mesa Import Errors**
   ```bash
   pip install "mesa<3.0"  # Must use version 2.x
   ```

2. **Missing Visualization Dependencies**
   ```bash
   pip install solara altair
   ```

3. **Port Already in Use**
   - Close other applications using port 8524
   - Or modify the port in `server.py` (line 374)

4. **Data File Errors**
   - Ensure all CSV files in `dataset/` are present
   - Check file permissions and formatting

## Research Context

This simulation is part of research on sustainable resource management in the Sundarban ecosystem, focusing on:
- Livelihood diversification strategies
- Policy intervention effectiveness  
- Climate change adaptation
- Sustainable resource extraction practices


*Last updated: Based on Mesa 2.4.0 compatibility*
