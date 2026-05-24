#!/bin/bash
# ==============================================================================
# KAFKA TOPIC INITIALIZATION SCRIPT
# ==============================================================================

set -e

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
cub kafka-ready -b kafka:29092 1 120

echo "Kafka is ready! Creating topics..."

# Create the primary e-commerce events topic
kafka-topics --create \
  --bootstrap-server kafka:29092 \
  --replication-factor 1 \
  --partitions 3 \
  --topic ecommerce_events \
  --if-not-exists

# Create a Dead Letter Queue (DLQ) topic for failed events
kafka-topics --create \
  --bootstrap-server kafka:29092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic ecommerce_events_dlq \
  --if-not-exists

echo "Topics created successfully!"
kafka-topics --list --bootstrap-server kafka:29092
