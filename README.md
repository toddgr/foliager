# foliager

## Description

Foliager is a Python program designed to enhance the generation of virtual forests in Unreal Engine by providing a list of foliage based on user input regarding a specific climate, city, or area. It leverages Natural Language Processing (NLP) to understand user queries and produces a curated list of foliage that can be used to create realistic and diverse virtual environments.

## Features

- Utilizes NLP to interpret user queries related to foliage preferences.
- Retrieves and compiles a list of foliage based on the specified climate, city, or area.
- Outputs a formatted list suitable for use in Unreal Engine for forest generation.

## Prerequisites

- Python 3.x
- OpenAI
- Pandas

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/foliager.git
    ```

2. Navigate to the project directory:

    ```bash
    cd foliager
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the program:

    ```bash
    python foliager.py
    ```

2. Follow the on-screen prompts to provide information about the desired climate, city, or area.

3. The program will generate a list of foliage suitable for Unreal Engine forest generation.

## Example

```bash
$ python foliager.py

Enter the climate, city, or area: Tropical Rainforest
Generating foliage list for Tropical Rainforest...

Foliage List:
1. Palm Tree
2. Banana Plant
3. Fern
4. ...

Foliage list saved to 'foliage_list.txt'.
