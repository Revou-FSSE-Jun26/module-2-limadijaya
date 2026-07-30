<!-- [![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wGq_UtnU) -->

# RevoShop Database Design (Checkpoint 1)

This repository contains the core PostgreSQL database schema design, initial seed data, and verification queries for RevoShop.

## 📊 Entity Relationship Diagram (ERD)

The database structure consists of 5 tables: `users`, `categories`, `products`, `orders`, and `order_items`.

![Schema Diagram](./schema_diagram.png)

---

## 🚀 Local Setup Instructions

### Prerequisites

- [PostgreSQL](https://www.postgresql.org/) (v14 or higher recommended)
- [pgAdmin 4](https://www.pgadmin.org/) or PostgreSQL CLI (`psql`)

### Step 1: Create Database

1. Open pgAdmin or login via `psql`.
2. Execute:
   ```sql
   CREATE DATABASE revoshop_db;
   ```
