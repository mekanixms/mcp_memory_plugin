from mcp.server.fastmcp import FastMCP
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, AsyncIterator
from dataclasses import dataclass
from contextlib import asynccontextmanager
import json
import os
from dotenv import load_dotenv
load_dotenv()

ENV_DB_PATH = os.getenv('MEMORY_DB_PATH')


# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = ENV_DB_PATH if os.path.exists(os.path.abspath(ENV_DB_PATH)) else os.path.join(SCRIPT_DIR, 'memory.db')

@dataclass
class MemoryContext:
    db_path: str = DB_PATH

def initialize_database():
    """Create the database and table if they don't exist"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create the memories table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                category TEXT,
                stored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP,
                access_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database initialized successfully at {DB_PATH}")
    except Exception as e:
        print(f"Error initializing database: {e}")

async def memory_lifespan(server: FastMCP) -> AsyncIterator[MemoryContext]:
    """Manage memory system lifecycle"""
    # Initialize database at startup
    initialize_database()
    context = MemoryContext()
    yield context

mcp = FastMCP("Memory Manager", lifespan=memory_lifespan)

def get_db_connection():
    # Ensure database exists before connecting
    if not os.path.exists(DB_PATH):
        initialize_database()
    return sqlite3.connect(DB_PATH)

@mcp.tool()
def store_memory(content: str, category: str = "general") -> bool:
    """Store a new memory in the database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO memories (content, category, stored_at)
                   VALUES (?, ?, ?)''',
                (content, category, datetime.now().isoformat())
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Error storing memory: {e}")
        return False

@mcp.tool()
def get_recent_memories(limit: int = 5, category: str = None) -> List[Dict[str, Any]]:
    """Retrieve recent memories, optionally filtered by category"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if category:
                query = '''SELECT content, category, stored_at, access_count 
                          FROM memories 
                          WHERE category = ? 
                          ORDER BY stored_at DESC 
                          LIMIT ?'''
                cursor.execute(query, (category, limit))
            else:
                query = '''SELECT content, category, stored_at, access_count 
                          FROM memories 
                          ORDER BY stored_at DESC 
                          LIMIT ?'''
                cursor.execute(query, (limit,))
            
            columns = ['content', 'category', 'stored_at', 'access_count']
            results = cursor.fetchall()
            
            # Update access count for retrieved memories
            memory_ids = [row[0] for row in results]
            if memory_ids:
                cursor.execute(
                    '''UPDATE memories 
                       SET access_count = access_count + 1,
                           last_accessed = ? 
                       WHERE content IN ({})'''.format(','.join(['?'] * len(memory_ids))),
                    [datetime.now().isoformat()] + memory_ids
                )
                conn.commit()
            
            return [dict(zip(columns, row)) for row in results]
    except Exception as e:
        print(f"Error retrieving memories: {e}")
        return []

def format_memories_for_context(memories: List[Dict[str, Any]]) -> str:
    """Format memories in a way that's suitable for Claude's context window"""
    formatted = "Previous Learnings and Context:\n\n"
    for memory in memories:
        formatted += f"Category: {memory['category']}\n"
        formatted += f"Content: {memory['content']}\n"
        formatted += f"Last Used: {memory['stored_at']}\n"
        formatted += "-" * 40 + "\n"
    return formatted

@mcp.tool()
def load_memories_to_context(categories: List[str] = None, limit_per_category: int = 5) -> str:
    """
    Load relevant memories and format them for injection into Claude's context.
    This should be called at the start of each chat session.
    """
    all_memories = []
    
    if categories:
        for category in categories:
            memories = get_recent_memories(limit=limit_per_category, category=category)
            all_memories.extend(memories)
    else:
        # If no categories specified, get most recent memories across all categories
        all_memories = get_recent_memories(limit=limit_per_category)
    
    return format_memories_for_context(all_memories)

@mcp.resource("memory://load")
def load_all_memories() -> str:
    """Resource endpoint to load all recent memories into context"""
    return load_memories_to_context()

@mcp.resource("memory://category/{category}")
def load_category_memories(category: str) -> str:
    """Resource endpoint to load memories for a specific category"""
    return load_memories_to_context(categories=[category])

@mcp.tool()
def search_memories(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search memories using a simple text search"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT content, category, stored_at, access_count 
                   FROM memories 
                   WHERE content LIKE ? 
                   ORDER BY stored_at DESC 
                   LIMIT ?''',
                (f'%{query}%', limit)
            )
            
            columns = ['content', 'category', 'stored_at', 'access_count']
            results = cursor.fetchall()
            return [dict(zip(columns, row)) for row in results]
    except Exception as e:
        print(f"Error searching memories: {e}")
        return []

if __name__ == "__main__":
    mcp.run()
