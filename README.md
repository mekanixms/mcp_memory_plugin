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

## Configuration

1. rename .env.example to .env and edit the values to your needs:

2. Locate claude_desktop_config.json and use the template below to add "MQTT Bridge" to the mcpServers section.
MacOs: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: C:\Users\<username>\AppData\Roaming\Claude\claude_desktop_config.json
  
```json
{
  "mcpServers": {
    "memory_recall": {
      "command": "/Volumes/SamPM991/AnaConda/anaconda3/bin/python3.12",
      "args": [
        "/path/2/your/cloned/repository/memory_plugin.py"
      ]
    }
  }
}
```

The SQLite database path is configured through the `MEMORY_DB_PATH` environment variable. This should point to where you want the SQLite database file to be stored.

Current configuration:

```
MEMORY_DB_PATH=/path/to/your/dabatase.sqlite
```

## Usage

### Basic Usage

Refer to the @mcp.resource and @mcp.tool decorated functions in the memory_plugin.py file

Examples to type in the chat: 

* `memory://load` to load the saved memories at new chat start
* `Save into the memory, under aNewName category, the following: a new message with important info to remember`
* `Save the relevant points of the conversation into the memory under aNewName category`

## Development

When contributing to this project:
1. Make sure to not commit sensitive information
2. Keep your `.env` file private
3. Use `.env.example` for sharing template configurations

## License

This project is licensed under the MIT License.
