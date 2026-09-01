# 🧠 SSK — STUDENT SMART KNOWLEDGE

### 🚀 An AI Assistant Designed to Remember, Understand, and Retrieve

SSK is an AI-powered personal assistant designed to go beyond traditional chatbot systems by providing **short-term memory, long-term semantic memory, intelligent memory retrieval, document understanding, and voice interaction**.

Instead of treating every conversation as a completely new interaction, SSK is designed to maintain useful information over time and retrieve it only when it is relevant to the user's current request.

The system uses multiple specialized AI models, each responsible for a different part of the intelligence pipeline.

The primary models used in SSK are:

- 🤖 **Granite 4.1:3b** — lightweight decision-making and memory intelligence
- 🧠 **Qwen 3:8b** — primary response-generation model
- 🔎 **Qwen3-Embedding:4b** — semantic embedding and vector search
- 🎙️ **Faster-Whisper** — speech-to-text processing

SSK is designed as a modular system where memory, document processing, models, input handling, and retrieval are separated into individual components.

---

# 🌟 What is SSK?

SSK stands for **Smart Semantic Knowledge**.

The main idea behind SSK is to create an AI assistant that can maintain useful knowledge about a user without continuously sending an entire conversation history to a large language model.

A normal chatbot can become inefficient when conversations become very long because the model has to process a large amount of previous context.

SSK approaches this problem by separating information into different memory layers.

### 🧩 The system contains:

- ⚡ Short-term active memory
- 🧠 Long-term memory
- 🔎 Semantic retrieval
- 📚 Document knowledge
- 🗂️ Categorized memories
- 📊 Memory importance
- 🤖 Intelligent retrieval decisions
- 🎙️ Voice interaction
- 💬 Text interaction
- 🧠 Context-aware response generation

The goal is to make the assistant capable of remembering **useful information rather than blindly remembering everything**.

---

# 🎯 Main Objective

The primary objective of SSK is to create an intelligent assistant that can:

- Remember important information about the user
- Maintain recent conversation context
- Store useful long-term memories
- Organize memories into meaningful categories
- Retrieve relevant memories using semantic similarity
- Understand uploaded documents
- Decide when memory retrieval is necessary
- Decide when document retrieval is necessary
- Generate responses using relevant context
- Support both voice and text interaction

The system is designed to make AI interaction more personalized while keeping the context supplied to the main language model controlled and relevant.

---

# 🧠 Memory System

One of the most important components of SSK is its memory architecture.

SSK separates memory into **short-term active memory** and **long-term semantic memory**.

## ⚡ Short-Term Memory

Short-term memory is handled using **Redis**.

Redis stores the recent conversation between the user and the assistant.

The active memory is limited to approximately **10 messages**.

This allows the assistant to maintain the immediate context of a conversation without continuously loading an unlimited conversation history.

For example, the active memory can contain:

- 👤 Recent user messages
- 🤖 Recent assistant responses
- 💬 Current conversation context
- 📝 Recently discussed topics

This active memory is directly available to the response-generation system.

---

# 🧠 Long-Term Memory

When the active memory reaches the configured message limit, the conversation can be processed for long-term memory.

The system analyzes the accumulated messages and determines whether any information is worth preserving.

Not every message should become a permanent memory.

For example:

### ❌ Usually unnecessary

> "Okay."

> "Thanks."

> "What time is it?"

### ✅ Potentially useful

> "My main project is SSK."

> "I am using Chroma as my vector database."

> "My project uses Qwen 3:8b."

> "I am working on a document retrieval system."

The goal is to preserve information that can be useful in future conversations.

---

# 🗂️ Memory Categories

Long-term memory is separated into different logical categories.

These categories include:

- 👤 **User**
- 🚀 **Project**
- 🎮 **Hobby**
- 🎓 **Academics**
- 💼 **Work**
- 📌 **Other**

This separation makes memory retrieval more meaningful.

For example, if a user asks:

> "What was the technology I selected for my project?"

The system can prioritize the **Project** memory category.

If the user asks:

> "What was I studying?"

The system can prioritize the **Academics** category.

This prevents unrelated memories from unnecessarily entering the context of the response model.

---

# 🤖 Granite 4.1:3b

SSK uses **Granite 4.1:3b** as the lightweight intelligence layer.

Granite is not intended to be the primary conversational response model.

Instead, it performs smaller and faster reasoning tasks.

### Granite is responsible for decisions such as:

- 🔎 Should long-term memory be retrieved?
- 📚 Should uploaded documents be retrieved?
- 🗂️ Which memory category is relevant?
- 🧠 Is a memory potentially important?
- 📌 Which information should be stored?
- 📝 How should information be categorized?

This allows SSK to avoid performing unnecessary expensive retrieval operations.

Granite essentially acts as an intelligent decision layer between the current conversation and the long-term knowledge system.

---

# 🧠 Qwen 3:8b

SSK uses **Qwen 3:8b** as the primary large language model.

Qwen is responsible for generating the final response to the user.

The model can receive multiple sources of context:

- 💬 Current user message
- ⚡ Recent Redis conversation
- 🧠 Retrieved long-term memories
- 📚 Retrieved document information

The response model then uses this information to produce the final answer.

The goal is to provide Qwen with **relevant context instead of overwhelming it with unnecessary historical information**.

---

# 🔎 Qwen3-Embedding:4b

SSK uses **Qwen3-Embedding:4b** as its embedding model.

The embedding model converts text into numerical vector representations.

This is used for:

- 🧠 Memory embeddings
- 📚 Document embeddings
- 🔎 Semantic similarity search
- 📌 Long-term memory retrieval
- 📖 Document retrieval

Instead of searching only for exact words, the system can search for information based on semantic meaning.

For example, a stored memory such as:

> "The user selected MySQL for the SSK project."

can potentially be retrieved when the user asks:

> "Which database did I choose for SSK?"

Even though the wording is different, the semantic meaning is similar.

---

# 🗄️ Chroma Vector Database

SSK uses **Chroma** as the vector database.

Chroma stores vector representations generated by the embedding model.

Long-term memories and document chunks can be represented as vectors and stored for later retrieval.

The vector database enables semantic search over:

- 🧠 Personal memories
- 🚀 Project information
- 🎓 Academic information
- 🎮 Hobby information
- 💼 Work information
- 📚 Uploaded documents

This provides the foundation for SSK's long-term semantic knowledge system.

---

# 🔎 Intelligent Memory Retrieval

SSK does not need to perform a complete long-term memory search for every user message.

Instead, the lightweight Granite model first evaluates the current request.

Granite determines whether retrieving additional information would help answer the question.

For example:

### 🟢 No retrieval required

User:

> "What is a binary tree?"

The question can be answered using the model's existing knowledge.

In this situation, long-term memory retrieval may not be necessary.

---

### 🔵 Memory retrieval required

User:

> "What database did I decide to use for SSK?"

This depends on information from the user's previous project discussions.

Granite can determine that long-term project memory should be retrieved.

---

### 🟣 Document retrieval required

User:

> "What does my uploaded physics document say about diffraction?"

This requires information from an uploaded document.

Granite can determine that document retrieval should be performed.

---

### 🟠 Both memory and document retrieval

Some questions may require both personal context and document information.

In that case, the retrieval system can retrieve information from both sources before providing the context to Qwen.

---

# 📚 Document Reader

SSK also includes a document-processing system.

The purpose of the document reader is to allow users to provide external knowledge to the assistant.

Supported document types include:

- 📄 PDF
- 📝 DOCX
- 📃 TXT

The document system extracts readable text from the uploaded file.

The extracted content can then be processed into smaller chunks.

These chunks can be converted into embeddings using:

**Qwen3-Embedding:4b**

The embeddings can then be stored in Chroma.

This makes the documents searchable using semantic retrieval.

---

# 📖 Document Question Answering

Once a document has been processed, the user can ask questions about it.

For example, a user could upload:

```text
physics_notes.pdf
