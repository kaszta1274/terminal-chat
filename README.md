# terminal-chat

A lightweight, terminal-based real-time multi-user chat application built in Python. The project implements a multi-threaded client-server architecture using raw TCP sockets, featuring an event-driven split-screen Terminal User Interface (TUI) powered by `prompt_toolkit`.


### Features

- Thread-safe UI redrawing
- Graceful socket termination
- Auto-scrolling chat history window

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python package and environment manager)


### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/kaszta1274/terminal-chat.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd terminal-chat
    ```


### Usage

`uv` will automatically manage dependencies and set up the execution environment on the first run.

1. **Start the central server:**
    ```bash
    uv run server.py
    ```

2. **Launch a client instance** (in a seperate terminal window):
    ```bash
    uv run client.py
    ```

3. **Configure and Chat:** Enter your username when prompted to register with the server and begin broadcasting messages.

4. **Exit:** Press `CTRL + C` inside the interface to gracefully disconnect from the chat room and shut down the interface.