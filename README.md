# Aurviz Audio Pipeline API

This backend system simulates an audio data ingestion pipeline for AI wearable devices. It receives audio payloads, maps transcriptions, stores files, and generates structured datasets for AI model training.

## 1. System Architecture
* **Framework:** Python with **FastAPI**. FastAPI was selected for its asynchronous capabilities, speed, and automatic Swagger documentation generation.
* **Database:** **PostgreSQL** (hosted via Supabase). SQLAlchemy is used as the ORM to manage relational data and ensure a scalable schema.
* **Storage:** Audio files are saved to a local `storage/` directory, simulating an S3-style cloud bucket workflow.

## 2. Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Sharmaarn01/aurviz-audio-pipeline.git](https://github.com/Sharmaarn01/aurviz-audio-pipeline.git)
   cd aurviz-audio-pipeline

   ## 3. Database Schema
The database consists of two tables with a one-to-many relationship. Indexes were added to optimize querying.
* **devices**: 
  * `device_id` (String, Primary Key, Indexed)
  * `registered_at` (DateTime)
  * `device_model` (String)
* **audio_records**: 
  * `audio_id` (String, Primary Key, Indexed)
  * `device_id` (String, Foreign Key, Indexed)
  * `file_path` (String)
  * `transcription` (String)
  * `created_at` (DateTime, Indexed)

## 4. How Dataset Generation Works
The `/api/dataset/download` endpoint generates the AI training dataset automatically:
1. It queries all audio records from the PostgreSQL database.
2. It programmatically generates a `metadata.csv` file mapping the `audio_file`, `transcription`, and `device_id`.
3. It copies the corresponding physical audio files from the storage directory into a temporary dataset folder.
4. It compresses the CSV and audio files into a structured `dataset.zip` archive.
5. It returns the ZIP file to the client for download and cleans up the temporary files.