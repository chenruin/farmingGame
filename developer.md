# Farming Simulator Game Developer's Guide

## Overview:

Welcome to the Farming Simulator Game Developer's Guide! This document provides an in-depth understanding of the Farming Simulator Game's architecture, implementation details, known issues, potential bugs, and future considerations.

### Condensed Version of Planning Specs:

The Farming Simulator Game was developed based on the initial planning specifications. The current implementation covers the core features outlined in the specs, including farming, watering and harvesting plants, picking up apples, and interacting with the environment.

## Install/Deployment/Admin Issues:

N/A

## User Interaction and Code Flow:

Provide a brief recap of the user interaction flow and then delve into the code:

1. **Farming (Hoe):**
   - Class: `Player, SoilTile`
   - Module: `player.py, sprites.py`

2. **Watering Plants (Water Can):**
   - Class: `Player, SoilTile, SoilLayer, WaterTile`
   - Module: `player.py, sprites.py, level.py`

3. **Picking Up Apples (Hand):**
   - Class: `Player, Level, Tree`
   - Module: `player.py, sprites.py, level.py`

4. **Seed Interaction (Switching and Planting):**
   - Classes: `Player, SoilTile, SoilLayer `
   - Module: `player.py, sprites.py`

5. **Interacting with Bed (Space):**
   - Class: `Player, Level, Overlay`
   - Module: `player.py, level.py, overlay.py, `

![Alt text](<Blank diagram.jpeg>)

setting.py timer.py and support.py are all support modules that support other modules whenever needed.

## Known Issues:

### Minor Issues:
- the apples may not displaying on the screen

### Major Issues:
- when apples not displaying on the screen, the game may crash when the player interact with bed.
- restart the game is recommanded.


## Future Work:

Discuss potential future enhancements and expansion opportunities:

- four season changes and the trading system.

- set up a dataset to store the process may be a good idea





