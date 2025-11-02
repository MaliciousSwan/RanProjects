# Ecosystem Simulation Game

A text-based Python simulation game where you manage a wildlife ecosystem! Balance predators, prey, and resources to maintain a thriving habitat.

## Game Overview

You control a wildlife ecosystem containing:
- **Herbivores**: Rabbits and Deer (eat grass, need water)
- **Predators**: Foxes and Wolves (hunt herbivores, need water)
- **Resources**: Grass and Water (regenerate each turn)

Your goal is to maintain a balanced ecosystem and achieve the highest score possible!

## Features

- **Population Dynamics**: Animals age, reproduce, and die based on energy and resources
- **Food Chain**: Predators hunt prey (foxes prefer rabbits, wolves prefer deer)
- **Resource Management**: Grass and water regenerate but can be depleted
- **Random Events**: Droughts and abundant rain affect the ecosystem
- **Score System**: Earn points by maintaining a healthy ecosystem
- **Strategic Decisions**: Intervene to add resources or introduce animals

## How to Play

### Installation

Requires Python 3.7 or higher. No external dependencies needed!

```bash
python3 ecosystem_game.py
```

### Game Controls

1. **Advance 1 turn** - Simulate one turn of the ecosystem
2. **Advance 5 turns** - Simulate five turns quickly
3. **Add grass (+200)** - Increase grass resources (costs 5 points)
4. **Add water (+200)** - Increase water resources (costs 5 points)
5. **Introduce 5 rabbits** - Add rabbits to the ecosystem (costs 10 points)
6. **Introduce 2 deer** - Add deer to the ecosystem (costs 10 points)
7. **Introduce 1 fox** - Add a fox to the ecosystem (costs 15 points)
8. **Introduce 1 wolf** - Add a wolf to the ecosystem (costs 15 points)
9. **View ecosystem tips** - See helpful information
0. **Quit game** - Exit the game

### Scoring

- **+10 points** per turn when the ecosystem is healthy
- **Costs points** to add resources or animals
- Final score shown when you quit or ecosystem collapses

### Ecosystem Health

A healthy ecosystem requires:
- At least 10 total animals alive
- Grass level above 100
- Water level above 100

## Gameplay Tips

### Maintaining Balance

- **Don't let predators outnumber prey** - They'll hunt prey to extinction
- **Watch grass levels** - Too many herbivores will deplete grass quickly
- **Monitor water** - All animals need water to survive
- **Intervene strategically** - Add resources before they run too low
- **Let nature work** - Sometimes the best action is to observe

### Species Information

| Species | Eats | Hunted By | Reproduction Rate | Lifespan |
|---------|------|-----------|-------------------|----------|
| Rabbit  | Grass | Fox | High (50%) | 8 turns |
| Deer    | Grass | Wolf | Medium (30%) | 15 turns |
| Fox     | Rabbit | - | Low (20%) | 10 turns |
| Wolf    | Deer | - | Very Low (15%) | 12 turns |

### Common Scenarios

**Too many predators?**
- Add more herbivores to sustain them
- Let some predators die off naturally
- Add grass to support more herbivores

**Running out of grass?**
- Add grass directly
- Reduce herbivore population
- Wait for natural grass regeneration

**Ecosystem collapsing?**
- Quickly add the missing link in the food chain
- Balance predators and prey
- Ensure adequate resources

## Game Mechanics

### Turn Simulation

Each turn:
1. Resources regenerate (grass +50-100, water +30-70)
2. Herbivores eat grass and gain energy
3. Predators hunt prey (30% success rate)
4. All animals drink water
5. Animals age and consume energy
6. Animals die if too old or out of energy
7. Animals reproduce if conditions are met
8. Random events may occur (5% drought, 5% rain)

### Reproduction

Animals reproduce when:
- Age is above reproduction threshold
- Energy is above 60
- At least 2 fertile animals of same species exist

### Energy System

- Animals start with 100 energy
- Energy consumed each turn (varies by species)
- Energy gained by eating
- Animals die when energy reaches 0

## Example Gameplay

```
Turn: 15  |  Score: 120

RESOURCES:
  Grass: [████████████████████░░░░░░░░░] 850
  Water: [██████████████████████░░░░░░░] 1120

POPULATION:
  Rabbits: 18
  Deer:    7
  Foxes:   4
  Wolves:  2
  Total Animals: 31

Ecosystem Status: ✓ HEALTHY
```

## Strategy Guide

### Beginner Strategy
- Advance one turn at a time
- Watch population trends
- Add resources when they drop below 500
- Maintain 3-4x more prey than predators

### Advanced Strategy
- Use 5-turn advances to see trends quickly
- Time your interventions for maximum efficiency
- Let small population fluctuations balance naturally
- Aim for sustainable equilibrium

## Game Over

The game ends when:
- You choose to quit (option 0)
- All animals die (ecosystem collapse)

Your final score is based on:
- Number of turns survived
- Points earned from maintaining balance
- Minus points spent on interventions

## Technical Details

- Written in Python 3 with no external dependencies
- Uses dataclasses for clean object management
- Implements realistic population dynamics
- Optimized for terminal/console play

## Credits

Created as a demonstration of ecosystem simulation and game design principles.

---

**Have fun maintaining your ecosystem!**