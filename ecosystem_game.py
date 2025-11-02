#!/usr/bin/env python3
"""
Ecosystem Simulation Game
A wildlife management simulation where you balance predators, prey, and resources.
"""

import random
import time
import os
from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum


class AnimalType(Enum):
    RABBIT = "Rabbit"
    DEER = "Deer"
    FOX = "Fox"
    WOLF = "Wolf"


@dataclass
class Animal:
    """Represents an animal in the ecosystem"""
    species: AnimalType
    age: int = 0
    energy: int = 100
    is_alive: bool = True

    def __post_init__(self):
        self.max_age = self._get_max_age()
        self.reproduction_age = self._get_reproduction_age()
        self.energy_consumption = self._get_energy_consumption()
        self.is_predator = self.species in [AnimalType.FOX, AnimalType.WOLF]

    def _get_max_age(self) -> int:
        ages = {
            AnimalType.RABBIT: 8,
            AnimalType.DEER: 15,
            AnimalType.FOX: 10,
            AnimalType.WOLF: 12
        }
        return ages[self.species]

    def _get_reproduction_age(self) -> int:
        ages = {
            AnimalType.RABBIT: 1,
            AnimalType.DEER: 2,
            AnimalType.FOX: 2,
            AnimalType.WOLF: 3
        }
        return ages[self.species]

    def _get_energy_consumption(self) -> int:
        consumption = {
            AnimalType.RABBIT: 5,
            AnimalType.DEER: 8,
            AnimalType.FOX: 12,
            AnimalType.WOLF: 15
        }
        return consumption[self.species]

    def can_reproduce(self) -> bool:
        return self.age >= self.reproduction_age and self.energy > 60 and self.is_alive

    def age_one_turn(self):
        self.age += 1
        self.energy -= self.energy_consumption
        if self.age > self.max_age or self.energy <= 0:
            self.is_alive = False


@dataclass
class Ecosystem:
    """Manages the entire ecosystem"""
    grass: int = 1000
    water: int = 1000
    animals: List[Animal] = field(default_factory=list)
    turn: int = 0

    def __post_init__(self):
        # Initialize starting population
        for _ in range(20):
            self.animals.append(Animal(AnimalType.RABBIT))
        for _ in range(10):
            self.animals.append(Animal(AnimalType.DEER))
        for _ in range(5):
            self.animals.append(Animal(AnimalType.FOX))
        for _ in range(3):
            self.animals.append(Animal(AnimalType.WOLF))

    def simulate_turn(self):
        """Simulate one turn of the ecosystem"""
        self.turn += 1

        # Grow resources
        self.grass = min(2000, self.grass + random.randint(50, 100))
        self.water = min(2000, self.water + random.randint(30, 70))

        # Shuffle animals for random interaction order
        random.shuffle(self.animals)

        # Herbivores eat grass
        self._herbivores_eat()

        # Predators hunt
        self._predators_hunt()

        # All animals consume water
        self._animals_drink()

        # Age animals
        for animal in self.animals:
            animal.age_one_turn()

        # Reproduction
        self._reproduce()

        # Remove dead animals
        self.animals = [a for a in self.animals if a.is_alive]

        # Random events
        self._random_events()

    def _herbivores_eat(self):
        """Herbivores consume grass"""
        herbivores = [a for a in self.animals if not a.is_predator and a.is_alive]
        for animal in herbivores:
            if self.grass > 0:
                eat_amount = 20 if animal.species == AnimalType.DEER else 10
                actual_eat = min(eat_amount, self.grass)
                self.grass -= actual_eat
                animal.energy = min(100, animal.energy + actual_eat)

    def _predators_hunt(self):
        """Predators hunt prey"""
        predators = [a for a in self.animals if a.is_predator and a.is_alive]
        prey = [a for a in self.animals if not a.is_predator and a.is_alive]

        for predator in predators:
            if prey and random.random() < 0.3:  # 30% hunt success rate
                # Wolves prefer deer, foxes prefer rabbits
                if predator.species == AnimalType.WOLF:
                    target_prey = [p for p in prey if p.species == AnimalType.DEER]
                    if not target_prey:
                        target_prey = prey
                else:
                    target_prey = [p for p in prey if p.species == AnimalType.RABBIT]
                    if not target_prey:
                        target_prey = prey

                if target_prey:
                    victim = random.choice(target_prey)
                    victim.is_alive = False
                    predator.energy = min(100, predator.energy + 40)
                    prey.remove(victim)

    def _animals_drink(self):
        """All animals consume water"""
        for animal in self.animals:
            if self.water > 0 and animal.is_alive:
                self.water -= 2
                animal.energy = min(100, animal.energy + 2)

    def _reproduce(self):
        """Animals reproduce if conditions are met"""
        new_animals = []

        for species in AnimalType:
            population = [a for a in self.animals if a.species == species and a.is_alive]
            fertile = [a for a in population if a.can_reproduce()]

            # Need at least 2 to reproduce
            if len(fertile) >= 2:
                # Reproduction rate varies by species
                reproduction_chance = {
                    AnimalType.RABBIT: 0.5,
                    AnimalType.DEER: 0.3,
                    AnimalType.FOX: 0.2,
                    AnimalType.WOLF: 0.15
                }

                num_births = int(len(fertile) / 2 * reproduction_chance[species])
                for _ in range(num_births):
                    new_animals.append(Animal(species))

        self.animals.extend(new_animals)

    def _random_events(self):
        """Random events that affect the ecosystem"""
        event_chance = random.random()

        if event_chance < 0.05:  # 5% chance of drought
            self.water = max(0, self.water - 300)
            self.grass = max(0, self.grass - 200)
        elif event_chance < 0.1:  # 5% chance of abundant rain
            self.water = min(2000, self.water + 400)
            self.grass = min(2000, self.grass + 300)

    def get_population_stats(self) -> Dict[AnimalType, int]:
        """Get current population counts"""
        stats = {species: 0 for species in AnimalType}
        for animal in self.animals:
            if animal.is_alive:
                stats[animal.species] += 1
        return stats

    def is_balanced(self) -> bool:
        """Check if ecosystem is in a healthy state"""
        stats = self.get_population_stats()
        total = sum(stats.values())
        return total > 10 and self.grass > 100 and self.water > 100


class EcosystemGame:
    """Main game controller"""

    def __init__(self):
        self.ecosystem = Ecosystem()
        self.game_over = False
        self.score = 0

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_status(self):
        """Display the current ecosystem status"""
        self.clear_screen()

        print("=" * 60)
        print(" 🌲 ECOSYSTEM SIMULATION GAME 🌲".center(60))
        print("=" * 60)
        print()

        print(f"Turn: {self.ecosystem.turn}  |  Score: {self.score}")
        print()

        # Resources
        grass_bar = "█" * (self.ecosystem.grass // 40) + "░" * (50 - self.ecosystem.grass // 40)
        water_bar = "█" * (self.ecosystem.water // 40) + "░" * (50 - self.ecosystem.water // 40)

        print("RESOURCES:")
        print(f"  Grass: [{grass_bar}] {self.ecosystem.grass}")
        print(f"  Water: [{water_bar}] {self.ecosystem.water}")
        print()

        # Population
        stats = self.ecosystem.get_population_stats()
        print("POPULATION:")
        print(f"  🐰 Rabbits: {stats[AnimalType.RABBIT]}")
        print(f"  🦌 Deer:    {stats[AnimalType.DEER]}")
        print(f"  🦊 Foxes:   {stats[AnimalType.FOX]}")
        print(f"  🐺 Wolves:  {stats[AnimalType.WOLF]}")
        print(f"  Total Animals: {sum(stats.values())}")
        print()

        # Ecosystem health
        if self.ecosystem.is_balanced():
            print("Ecosystem Status: ✓ HEALTHY")
        else:
            print("Ecosystem Status: ⚠ AT RISK")

        print()
        print("-" * 60)

    def show_menu(self):
        """Display action menu"""
        print("\nACTIONS:")
        print("  1. Advance 1 turn")
        print("  2. Advance 5 turns")
        print("  3. Add grass (+200)")
        print("  4. Add water (+200)")
        print("  5. Introduce 5 rabbits")
        print("  6. Introduce 2 deer")
        print("  7. Introduce 1 fox")
        print("  8. Introduce 1 wolf")
        print("  9. View ecosystem tips")
        print("  0. Quit game")
        print()

    def show_tips(self):
        """Display gameplay tips"""
        print("\n" + "=" * 60)
        print("ECOSYSTEM TIPS:")
        print("=" * 60)
        print("• Herbivores (rabbits, deer) eat grass and need water")
        print("• Predators (foxes, wolves) hunt herbivores")
        print("• Foxes prefer rabbits, wolves prefer deer")
        print("• Animals need energy to survive and reproduce")
        print("• Balance is key - too many predators will collapse the food chain")
        print("• Too many herbivores will deplete grass resources")
        print("• Watch for random events like droughts and rain")
        print("• Score increases each turn if ecosystem is healthy")
        print("=" * 60)
        input("\nPress Enter to continue...")

    def process_action(self, action: str):
        """Process player action"""
        if action == "1":
            self.ecosystem.simulate_turn()
            if self.ecosystem.is_balanced():
                self.score += 10

        elif action == "2":
            for _ in range(5):
                self.ecosystem.simulate_turn()
                if self.ecosystem.is_balanced():
                    self.score += 10

        elif action == "3":
            self.ecosystem.grass = min(2000, self.ecosystem.grass + 200)
            self.score -= 5

        elif action == "4":
            self.ecosystem.water = min(2000, self.ecosystem.water + 200)
            self.score -= 5

        elif action == "5":
            for _ in range(5):
                self.ecosystem.animals.append(Animal(AnimalType.RABBIT))
            self.score -= 10

        elif action == "6":
            for _ in range(2):
                self.ecosystem.animals.append(Animal(AnimalType.DEER))
            self.score -= 10

        elif action == "7":
            self.ecosystem.animals.append(Animal(AnimalType.FOX))
            self.score -= 15

        elif action == "8":
            self.ecosystem.animals.append(Animal(AnimalType.WOLF))
            self.score -= 15

        elif action == "9":
            self.show_tips()

        elif action == "0":
            self.game_over = True

        # Check for game over conditions
        stats = self.ecosystem.get_population_stats()
        if sum(stats.values()) == 0:
            self.game_over = True
            print("\n⚠ All animals have died! Ecosystem collapsed!")
            print(f"Final Score: {self.score}")
            input("\nPress Enter to exit...")

    def run(self):
        """Main game loop"""
        self.display_status()
        self.show_tips()

        while not self.game_over:
            self.display_status()
            self.show_menu()

            action = input("Choose an action: ").strip()
            self.process_action(action)

        if self.game_over and sum(self.ecosystem.get_population_stats().values()) > 0:
            self.clear_screen()
            print("\n" + "=" * 60)
            print("GAME OVER".center(60))
            print("=" * 60)
            print(f"\nFinal Score: {self.score}")
            print(f"Turns Survived: {self.ecosystem.turn}")
            print("\nFinal Population:")
            for species, count in self.ecosystem.get_population_stats().items():
                print(f"  {species.value}: {count}")
            print("\nThanks for playing!")
            print("=" * 60)


def main():
    """Entry point for the game"""
    print("\nWelcome to Ecosystem Simulation Game!")
    print("Your goal is to maintain a balanced ecosystem.")
    input("\nPress Enter to start...")

    game = EcosystemGame()
    game.run()


if __name__ == "__main__":
    main()
