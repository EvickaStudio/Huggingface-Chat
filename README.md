<!--
 Copyright 2024 EvickaStudio

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

# Huggingface Chat 🤗🚀

<p align="center">
  <a href="https://github.com/EvickaStudio/Huggingface-Chat/actions"><img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/EvickaStudio/Huggingface-Chat/ci.yml?+label=Build%20Status"></a>
  <a href="https://github.com/EvickaStudio/Huggingface-Chat/blob/main/LICENSE.md"><img alt="GitHub license" src="https://img.shields.io/github/license/EvickaStudio/Huggingface-Chat"></a>
  <a href="https://github.com/EvickaStudio/Huggingface-Chat/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/EvickaStudio/Huggingface-Chat"></a>
  <a href="https://github.com/EvickaStudio/Huggingface-Chat/pulls"><img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/EvickaStudio/Huggingface-Chat"></a>
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/EvickaStudio/Huggingface-Chat">
</p>

A simple Python application utilizing Hugging Face's chat models as an open-source alternative to OpenAI. The project is not complete and is still under development (Only Login/ Auth is working).

## Table of Contents

1. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Setup Guide](#setup-guide)
2. [Usage Examples](#usage-examples)
3. [Project Structure](#project-structure)
4. [Contribution Guidelines](#contribution-guidelines)
5. [License](#license)
6. [Contact Us](#contact-us)

## Getting Started <a name="getting-started"></a>

\_

### Prerequisites <a name="prerequisites"></a>

To run the application locally, please ensure the following prerequisites are met (optional when no new major features are added)

- **Python >=3.8**
- **httpx ~0.26.0**
- **configparser >=6.0.0**

### Setup Guide <a name="setup-guide"></a>

1. Download and install the latest version of [Python](https://www.python.org/downloads/).
2. Install the required libraries by running:

```bash
pip install -r requirements.txt
```

#### Optional Virtual Environment Setup

It is recommended to create a virtual environment to isolate package dependencies. To do so, follow these steps:

**On Windows:**

```powershell
py -m venv venv
venv\Scripts\activate
```

**On Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Running Application

Execute the main script `main.py` located in the root directory:

```bash
python main.py
```

Start interacting with the AI chatbot! 🎉

## Usage Examples <a name="usage-examples"></a>

Use the application to interactively ask questions and engage in meaningful conversations powered by Hugging Face AI models. Explore the wide range of pre-trained models available at [HuggingChat Settings](https://huggingface.co/chat/settings). (Customize the model settings in the `config.ini` file according to your preference.)

## Project Structure <a name="project-structure"></a>

The project contains the following components:

1. Backend API Wrapper
2. Configuration Management
3. Text Extraction for Response (coming soon)

Key directories and files include:

- `config.ini`: Global configuration file controlling app settings, including authentication tokens (and preferred chatbot models).
- `auth` folder: Holds scripts for accessing Hugging Face APIs and processing responses effectively.
- `utils` folder: Contains utility scripts for text extraction, configuration management, and additional tasks.
- `requirements.txt`: Provides a list of essential packages and respective versions for the proper functioning of the complete system.

## Contribution Guidelines <a name="contribution-guidelines"></a>

<!-- We appreciate contributions from everyone. Before submitting pull requests, please review our contribution guidelines, which we will provide shortly. -->

_TODO_

## License <a name="license"></a>

This project is governed by the Apache 2.0 License - refer to the [LICENSE.md](LICENSE.md) file for further details.

## Contact Us <a name="contact-us"></a>

_TODO_
Have fun coding! 😊
