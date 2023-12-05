# Farming Simulator Game User Guide

Welcome to the Farming Simulator Game! This interactive simulation game allows you to explore a virtual farm world and engage with various tools to farm, water plants, harvest plants and pick up apples. Follow this user guide to get started.

## Setup:

1. **Clone the GitHub Code:**
   - Open your terminal or command prompt.
   - Navigate to the directory where you want to clone the repository.
   - Run the following command:
     
     git clone https://github.com/chenruin/farmingGame
    


2. **Open the Folder in VS Code:**
   - Open Visual Studio Code.
   - Go to "File" > "Open Folder" and select the folder where you cloned the GitHub repository.

3. **Install Dependencies:**
   - Ensure you have Python installed on your system.
   - Open the terminal in VS Code.
   - Run the following command to install Pygame, the game's dependency:
     
    pip install pygame/ pip3 install pygame

## Running the farming Simulator Game:
   - Run the following command to start the Pygame Simulator Game:
  
    python main.py

 **Controls:**
   - movement: use direction key to move
   - other actions: Use Q to switch tools, J to use tools, E to switch seeds, K to use seeds, and Space to interact with the bed.

## Tools:

1. **Hoe:**
   - *Functionality:* Use the hoe to farm the land and prepare it for planting seeds.

2. **Water Can:**
   - *Functionality:* Water plants to promote growth and speed up the maturation process.

3. **Hand:**
   - *Functionality:* Use the hand to pick up apples from the trees.

## Seeds:

- **Switch Seed (E):**
  - Press the E key to cycle through available seeds.
  - Different seeds result in the growth of various crops.

- **Use Seed (K):**
  - Once a seed is selected, press the K key to plant it in the prepared soil.

  ![Alt text](<截屏2023-12-04 22.54.25.png>)

## Interactions:

- **Interact with Bed (Space):**
  - Press the Space key to interact with the bed and initiate sleep.
  - Sleeping advances time, affecting the growth of your crops.

**Pro Tip:**
- Watering plants with the Water Can can facilitate the speed of maturity. 

- when plant is mature, it can be simply harvested by walk on it.

## Potential bugs

- if the apples not displaying on the tree, the crash may happen when player interact with bed, restart the game is recommended in this situation.

![Alt text](<截屏2023-12-04 22.53.30.png>)!
