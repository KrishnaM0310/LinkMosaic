# 🧠 LinkMosaic

**LinkMosaic** is an AI-powered document knowledge mapping system built on AWS.  
It automatically extracts text from uploaded PDF or TXT files, processes it through a modular Lambda pipeline, and generates a structured JSON “map” showing key clusters, summaries, and relationships between concepts.

This project demonstrates how to design a scalable, event-driven system using **AWS Lambda**, **S3**, and **API Gateway**, with a lightweight front end hosted via **GitHub Pages**.

---

## 🚀 Features

- 📄 **File Uploads via Pre-Signed URLs**  
  Secure browser uploads to S3 without exposing AWS credentials.

- 🧩 **Modular Lambda Architecture**
  - `Orchestrator` – coordinates the entire workflow  
  - `EmbeddingTool`, `ClusterTool`, `SummaryExtractor`, `RelationshipInfer` – modular sub-functions  
  - `MapBuilder` – generates a simple knowledge-graph JSON  
  - `UploadSigner` – issues pre-signed S3 upload URLs for the frontend

- ☁️ **Fully Serverless Backend**
  - Event-driven pipeline powered by **AWS Lambda + S3 triggers**
  - Orchestration logic written in **Python 3.11**
  - S3 buckets for uploads (`linkmosaic-uploads-…`) and map outputs (`linkmosaic-maps-…`)

- 💻 **Frontend Interface**
  - Hosted on **GitHub Pages**
  - Lets users upload a PDF or TXT file  
  - Automatically calls AWS backend and displays the generated map

---

## 🏗️ Architecture Overview

```text
[ GitHub Pages Frontend ]
         │
         ▼
 [ API Gateway (UploadSigner) ]
         │
         ▼
  [ S3 Uploads Bucket ]
         │
  ┌──────┴────────┐
  │               │
  ▼               ▼
[ Lambda: Orchestrator ] → triggers → [ ClusterTool / Summary / Relationship / MapBuilder ]
         │
         ▼
 [ S3 Maps Bucket (output) ]
