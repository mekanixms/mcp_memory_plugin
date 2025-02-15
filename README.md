# Memory Plugin

A Python-based memory plugin that uses SQLite for persistent storage.

## Overview

This plugin provides memory storage functionality using SQLite as the backend database. It's designed to store and manage data persistently across sessions.

## Setup

1. **Environment Configuration**

   Create a `.env` file in the root directory with the following configuration:
   ```
   MEMORY_DB_PATH=/path/to/your/memory.sqlite

   ```

   You can use the provided `.env.example` as a template:
   ```bash
   cp .env.example .env
   ```

2. **Dependencies**

   The project requires Python and uses SQLite for data storage. Make sure you have Python installed on your system.

## Files

- `memory_plugin.py` - Main plugin implementation
- `.env` - Environment configuration file
- `.env.example` - Template for environment configuration
- `.gitignore` - Specifies which files Git should ignore

## Configuration

The SQLite database path is configured through the `MEMORY_DB_PATH` environment variable. This should point to where you want the SQLite database file to be stored.

Current configuration:

```
MEMORY_DB_PATH=/Volumes/Orico/ClaudeMCP-FS-Folder/memory.sqlite
```

## Usage

### Basic Usage

Use @mcp.resource and @mcp.tool decorated functions in the memory_plugin.py file

Examples to type in the chat: 

memory://load to load the saved memories at new chat start
Save into the memory, under aNewName catagory, the following: a new message twith important info to remember
Save the relevant points of the conversation into the memory under aNewName category

## Development

When contributing to this project:
1. Make sure to not commit sensitive information
2. Keep your `.env` file private
3. Use `.env.example` for sharing template configurations

## License

This project is licensed under the MIT License.
