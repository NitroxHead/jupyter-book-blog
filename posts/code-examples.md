---
title: "Code Examples and Programming Snippets"
date: "2024-03-18"
description: "This post showcases syntax highlighting and code examples across multiple programming languages commonly used in data science and software development."
---

# Code Examples and Programming Snippets

This post showcases syntax highlighting and code examples across multiple programming languages commonly used in data science and software development.

## Python Data Science

### Data Processing with Pandas

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load and explore data
df = pd.read_csv('data.csv')
print(f"Dataset shape: {df.shape}")
print(df.head())

# Data preprocessing
df['feature_engineered'] = df['feature1'] * df['feature2']
df_clean = df.dropna()

# Feature selection
X = df_clean[['feature1', 'feature2', 'feature_engineered']]
y = df_clean['target']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluation
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy:.3f}")
```

### Neural Network with PyTorch

```python
import torch
import torch.nn as nn
import torch.optim as optim

class SimpleNeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(SimpleNeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        return out

# Initialize model
model = SimpleNeuralNet(input_size=784, hidden_size=128, num_classes=10)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop (simplified)
for epoch in range(num_epochs):
    for batch_idx, (data, targets) in enumerate(train_loader):
        # Forward pass
        outputs = model(data.view(data.size(0), -1))
        loss = criterion(outputs, targets)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

## R Statistical Computing

### Data Analysis and Visualization

```r
library(ggplot2)
library(dplyr)
library(tidyr)

# Load and explore data
data <- read.csv("data.csv")
summary(data)

# Data manipulation with dplyr
clean_data <- data %>%
  filter(!is.na(value)) %>%
  mutate(
    log_value = log(value + 1),
    category_clean = str_to_lower(category)
  ) %>%
  group_by(category_clean) %>%
  summarise(
    mean_value = mean(value),
    median_value = median(value),
    count = n(),
    .groups = 'drop'
  )

# Visualization
ggplot(clean_data, aes(x = category_clean, y = mean_value)) +
  geom_col(fill = "steelblue", alpha = 0.7) +
  geom_text(aes(label = count), vjust = -0.5) +
  theme_minimal() +
  labs(
    title = "Average Values by Category",
    x = "Category",
    y = "Mean Value"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Statistical modeling
model <- lm(value ~ category_clean + other_feature, data = data)
summary(model)
```

## JavaScript and Web Development

### Data Visualization with D3.js

```javascript
// Create SVG container
const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Load and process data
d3.csv("data.csv").then(function(data) {
    // Parse data
    data.forEach(d => {
        d.date = d3.timeParse("%Y-%m-%d")(d.date);
        d.value = +d.value;
    });

    // Set up scales
    const xScale = d3.scaleTime()
        .domain(d3.extent(data, d => d.date))
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .range([height, 0]);

    // Create line generator
    const line = d3.line()
        .x(d => xScale(d.date))
        .y(d => yScale(d.value))
        .curve(d3.curveMonotoneX);

    // Add the line
    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2)
        .attr("d", line);

    // Add axes
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(xScale));

    svg.append("g")
        .call(d3.axisLeft(yScale));
});
```

## SQL Database Queries

### Complex Data Analysis

```sql
-- CTE for data aggregation
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', sale_date) as month,
        product_category,
        SUM(amount) as total_sales,
        COUNT(*) as transaction_count,
        AVG(amount) as avg_transaction
    FROM sales s
    JOIN products p ON s.product_id = p.id
    WHERE sale_date >= '2024-01-01'
    GROUP BY DATE_TRUNC('month', sale_date), product_category
),
category_growth AS (
    SELECT
        *,
        LAG(total_sales) OVER (
            PARTITION BY product_category
            ORDER BY month
        ) as prev_month_sales,
        CASE
            WHEN LAG(total_sales) OVER (
                PARTITION BY product_category
                ORDER BY month
            ) > 0 THEN
                (total_sales - LAG(total_sales) OVER (
                    PARTITION BY product_category
                    ORDER BY month
                )) * 100.0 / LAG(total_sales) OVER (
                    PARTITION BY product_category
                    ORDER BY month
                )
            ELSE NULL
        END as growth_rate
    FROM monthly_sales
)
SELECT
    month,
    product_category,
    total_sales,
    transaction_count,
    avg_transaction,
    ROUND(growth_rate, 2) as growth_percentage,
    RANK() OVER (PARTITION BY month ORDER BY total_sales DESC) as sales_rank
FROM category_growth
ORDER BY month DESC, total_sales DESC;
```

## Shell Scripting

### Data Processing Pipeline

```bash
#!/bin/bash

# Data processing pipeline
DATA_DIR="/path/to/data"
OUTPUT_DIR="/path/to/output"
LOG_FILE="$OUTPUT_DIR/processing.log"

# Function for logging
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Create output directory
mkdir -p "$OUTPUT_DIR"

log_message "Starting data processing pipeline"

# Process each CSV file
for file in "$DATA_DIR"/*.csv; do
    if [[ -f "$file" ]]; then
        filename=$(basename "$file" .csv)
        log_message "Processing $filename"

        # Clean data: remove empty lines and sort
        grep -v '^$' "$file" | sort > "$OUTPUT_DIR/${filename}_cleaned.csv"

        # Count records
        record_count=$(wc -l < "$OUTPUT_DIR/${filename}_cleaned.csv")
        log_message "Processed $record_count records in $filename"

        # Create summary statistics
        awk -F',' '
            NR==1 {
                for (i=1; i<=NF; i++) headers[i] = $i
                next
            }
            {
                for (i=1; i<=NF; i++) {
                    if ($i ~ /^[0-9.]+$/) {
                        sum[i] += $i
                        count[i]++
                    }
                }
            }
            END {
                for (i=1; i<=length(headers); i++) {
                    if (count[i] > 0) {
                        printf "%s: avg=%.2f, count=%d\n",
                               headers[i], sum[i]/count[i], count[i]
                    }
                }
            }
        ' "$OUTPUT_DIR/${filename}_cleaned.csv" > "$OUTPUT_DIR/${filename}_summary.txt"
    fi
done

log_message "Pipeline completed successfully"
```

## Configuration Files

### YAML Configuration

```yaml
# Application configuration
app:
  name: "Data Processing Service"
  version: "1.0.0"
  environment: "production"

database:
  host: "localhost"
  port: 5432
  name: "analytics_db"
  user: "${DB_USER}"
  password: "${DB_PASSWORD}"
  pool_size: 10
  timeout: 30

api:
  host: "0.0.0.0"
  port: 8080
  workers: 4
  rate_limit:
    requests_per_minute: 100
    burst_size: 10

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  handlers:
    - type: "file"
      filename: "logs/app.log"
      max_bytes: 10485760
      backup_count: 5
    - type: "console"

features:
  enable_caching: true
  cache_ttl: 3600
  enable_monitoring: true
  debug_mode: false
```

## Dockerfile Example

```dockerfile
# Multi-stage build for Python application
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Expose port
EXPOSE 8080

# Run application
CMD ["python", "src/main.py"]
```

## Conclusion

This post demonstrates the excellent syntax highlighting capabilities of Jupyter Book across multiple programming languages. The code blocks are rendered with proper indentation, keyword highlighting, and language-specific syntax coloring.

---

*This example showcases various programming languages and their syntax highlighting in MyST Markdown.*