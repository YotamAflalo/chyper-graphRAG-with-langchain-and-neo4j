# README

## Setup

1. **Create a Virtual Environment**

   To create a virtual environment, run the following command:
   ```bash
   python -m venv venv
   ```

2. **Install the Requirements**

   Activate the virtual environment and install the required packages by running:
   ```bash
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Create the .env File**

   Create a `.env` file with the necessary passwords and configurations, following the format provided in `example_env.txt`.

## Knowledge Graph Creation

1. **Add Files to the Books Directory**

   Place the relevant files into the `books` directory.

2. **Run the Insert_to_the_graph Script**

   Extract nodes and upload them to AuraDB by running:
   ```bash
   python Insert_to_the_graph.py
   ```

3. **Run the clean_graph Script**

   Clean up irrelevant relationships by running:
   ```bash
   python clean_graph.py
   ```

## Document Index Creation

1. **Run the create_doc_vector_index Script**

   Create the document vector index by running:
   ```bash
   python create_doc_vector_index.py
   ```

## Running the Bot

1. **Run the bot Script**

   To start the bot, run:
   ```bash
   python bot.py
   ```
