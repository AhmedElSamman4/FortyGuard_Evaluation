
## Test 01 — Environmental Parameters (env_params)

Status: PASS

Location: New York City, USA
Coordinates: 40.7128, -74.0060
Date/Time: 2026-11-14 07:00 AM
Timezone: America/New_York

### Results
- Temperature: 4.4°C
- Apparent Temperature: -0.4°C
- Wet Bulb Temperature: 0.9°C
- Relative Humidity: 82.9%
- Precipitation: 0 mm
- AQI: 29.6
- GHI: 9.57 W/m²
- DNI: 93.59 W/m²
- DHI: 5.40 W/m²

### Performance
- Latency: 3,747 ms
- Credits consumed: 2,900
- Plan: Premium
- Warnings: None

### Positive Feedback
- Successful MCP execution.
- Multiple environmental parameters returned.
- Automatic timezone detection.
- Structured JSON response.
- Execution metadata and credit cost included.

### Improvement Opportunities
- Summary parameters expose fewer fields than raw response.
- Credit consumption is significant for a single hourly point.
- Compare against REST API for data consistency and performance.

### Overall
Successful first environmental data retrieval.
REST API comparison is still pending.

## Test 02 — Credit Balance

Status: PASS

Available Credits: 984,440
Execution Cost: 0 Credits

### Tool Properties
- Read-only
- Idempotent
- Free

### Positive Feedback
- Instant access to account credit balance.
- No credit consumption.
- Simple output with a clear numeric value.

### Overall
Successful credit balance retrieval.

## Test 03 — Read Heatmap (heatmap_read)

Status: PASS

Heatmap ID: 78aa1720-0920-49c6-97a1-93cc667601c7

### Retrieved Statistics
- Minimum Temperature: 28.841°C
- Maximum Temperature: 29.7458°C
- Mean Temperature: 29.1064°C
- Standard Deviation: 0.2991°C

### Performance
- Latency: 1,085 ms
- Credits Consumed: 0
- Plan: Premium
- Warnings: None

### REST API Comparison
- Minimum: Match
- Maximum: Match
- Mean: Match

### Positive Feedback
- Successfully retrieved an existing heatmap.
- No additional credits consumed.
- Core statistics match REST API results.
- Fast response time.

### Improvement Opportunities
- Evidence field is empty.
- Response provides summary statistics only.

### Overall
Successful read operation with consistent results
between REST API and MCP.

## Test 04 — List Monitors

Status: PASS

Operation: list_monitors

### Results
- Monitors Found: 0
- Has More: false
- Status: completed

### Performance
- Latency: 366 ms
- Credits Consumed: 0
- Plan: Premium
- Warnings: None

### Positive Feedback
- Fast response.
- Free read operation.
- Empty results handled correctly.
- Clear pagination indicator.

### Overall
Successful monitoring list operation.
No existing monitors were found.