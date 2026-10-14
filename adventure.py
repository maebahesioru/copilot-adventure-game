#!/usr/bin/env python3
"""
adventure.py - A small command-line "choose your own adventure" game.

Theme: Abandoned space station exploration. You are a stranded engineer who must
navigate the derelict Mergington Station, find an energy cell, and escape via
an escape pod. Choices are made by typing the number for the option.

How to run:
    python adventure.py

Controls:
    - Read the scene descriptions and type the number of the choice you want,
      then press Enter.
    - Input is validated; invalid choices will re-prompt you.
"""

import sys


def prompt_choice(options):
    """
    Present numbered options (list of strings) and return the chosen index.
    Re-prompts until valid input is given.
    """
    while True:
        try:
            choice = input("> ").strip()
            if choice.lower() in ("q", "quit", "exit"):
                print("Exiting game. Goodbye.")
                sys.exit(0)
            num = int(choice)
            if 1 <= num <= len(options):
                return num - 1
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Please enter the number of your choice (or 'quit' to exit).")


def scene_airlock(state):
    print("\n=== AIRLOCK ===")
    print("You wake up in the outer airlock of the abandoned Mergington Station.")
    print("Red emergency lights flicker. Your comms are dead. The station is silent.")
    print("A hatch leads into a long corridor. A battered work-suit hangs on a rack.")
    print("\nWhat do you do?")
    options = [
        "Put on the work-suit (might help later) and enter the corridor",
        "Skip the suit and step into the corridor immediately",
        "Shout into your comms (probably useless)"
    ]
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    choice = prompt_choice(options)
    if choice == 0:
        state["suit"] = True
        print("You strap into the work-suit. It feels clumsy but sturdy.")
        return "corridor"
    elif choice == 1:
        return "corridor"
    else:
        print("You shout, but only the hum of failing systems answers.")
        print("You decide to move on.")
        return "corridor"


def scene_corridor(state):
    print("\n=== CORRIDOR ===")
    print("A central corridor branches to many parts of the station:")
    print("- The Bridge (command center)")
    print("- The Engine Room (reactor core)")
    print("- The Cargo Bay")
    print("- The Medbay")
    print("- The Observation Deck (locked by a small hatch)")
    print("\nWhere do you go?")
    options = [
        "Head to the Bridge",
        "Go to the Engine Room",
        "Enter the Cargo Bay",
        "Check the Medbay",
        "Try to open the Observation Deck hatch"
    ]
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    choice = prompt_choice(options)
    if choice == 0:
        return "bridge"
    elif choice == 1:
        return "engine"
    elif choice == 2:
        return "cargo"
    elif choice == 3:
        return "medbay"
    else:
        if state.get("obs_unlocked"):
            print("The hatch is already open; you step into the Observation Deck.")
            return "obsdeck"
        # If not unlocked, maybe you need to find something to open it.
        print("The hatch is stuck. There is a power terminal nearby that might open it.")
        print("You could try the Bridge or the Engine Room to restore power.")
        return "corridor"


def scene_bridge(state):
    print("\n=== BRIDGE ===")
    print("The Bridge is dim, consoles dead. A central AI core indicator is offline.")
    print("A maintenance door leads deeper to the AI Core. A terminal blinks faintly.")
    print("\nWhat do you do?")
    options = [
        "Inspect the terminal",
        "Head to the AI Core through the maintenance door",
        "Return to the Corridor"
    ]
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    choice = prompt_choice(options)
    if choice == 0:
        if state.get("energy_cell"):
            print("You insert the energy cell into the terminal's auxiliary port.")
            print("Power surges; the terminal boots. A message appears: 'AI offline. Core power required.'")
            state["bridge_powered"] = True
            # unlocking Observation Deck now that some bridge power is available
            state["obs_unlocked"] = True
            return "bridge"
        else:
            print("The terminal requests auxiliary power (an energy cell). You don't have one.")
            return "bridge"
    elif choice == 1:
        return "ai_core"
    else:
        return "corridor"


def scene_engine(state):
    print("\n=== ENGINE ROOM ===")
    print("Heat vents whistle. The reactor's containment field is flickering.")
    print("A control console shows reactor integrity at 65%. There's a manual coolant override.")
    print("\nWhat do you do?")
    options = [
        "Attempt the coolant override",
        "Inspect the reactor controls more carefully",
        "Return to the Corridor"
    ]
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    choice = prompt_choice(options)
    if choice == 0:
        # risky action: if you have the suit, safer; otherwise danger
        if state.get("suit"):
            print("You climb into the control platform in your suit and adjust the coolant valves.")
            print("Reactor stabilizes. The containment field improves to 90%.")
            state["reactor_stable"] = True
            return "engine"
        else:
            print("You try to manipulate the valves without protection. A coolant burst knocks you back.")
            print("Radiation spikes! Systems fail as the reactor destabilizes.")
            return "reactor_overload"
    elif choice == 1:
        print("You discover the reactor can be manually cycled, but the procedure needs a secondary power source.")
        if state.get("energy_cell"):
            print("With the energy cell, you can perform the cycle safely.")
            state["reactor_stable"] = True
            return "engine"
        else:
            return "engine"
    else:
        return "corridor"


def scene_cargo(state):
    print("\n=== CARGO BAY ===")
    print("Crates float lazily in zero-g. One crate is cracked open, revealing spare parts.")
    if not state.get("energy_cell"):
        print("Among the parts, you find a charged energy cell—small but potent.")
        print("This could power dormant systems elsewhere.")
        options = [
            "Take the energy cell",
            "Search the cargo bay further",
            "Return to the Corridor"
        ]
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        choice = prompt_choice(options)
        if choice == 0:
            state["energy_cell"] = True
            print("You secure the energy cell in your pack. It might be useful.")
            return "cargo"
        elif choice == 1:
            print("You rummage but find nothing else of value.")
            return "cargo"
        else:
            return "corridor"
    else:
        print("The cargo bay is empty apart from drifting debris.")
        print("\nWhat do you do?")
        options = [
            "Return to the Corridor",
            "Climb the maintenance ladder to a sealed hatch leading toward the AI Core"
        ]
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        choice = prompt_choice(options)
        if choice == 0:
            return "corridor"
        else:
            # Ladder gives another route to AI Core
            return "ai_core"


def scene_medbay(state):
    print("\n=== MEDBAY ===")
    print("The medbay is a mess, but a sealed cabinet contains an oxygen mask.")
    if not state.get("mask"):
        print("An oxygen mask could buy you time if you are exposed to vacuum.")
        options = [
            "Take the oxygen mask",
            "Check the injured pod beds",
            "Return to the Corridor"
        ]
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        choice = prompt_choice(options)
        if choice == 0:
            state["mask"] = True
            print("You put the mask in your pack.")
            return "medbay"
        elif choice == 1:
            print("The pod beds are empty, but there's a calm hum of failing monitors.")
            return "medbay"
        else:
            return "corridor"
    else:
        print("Nothing else of use is here.")
        options = [
            "Return to the Corridor"
        ]
        print("1. Return to the Corridor")
        prompt_choice(["Return"])
        return "corridor"


def scene_obsdeck(state):
    print("\n=== OBSERVATION DECK ===")
    print("Through cracked glass, stars shine cold. In the distance, you see a small escape pod bay lit faintly.")
    print("The view gives you hope—and a hint at the escape pod's location on the station layout.")
    print("\nWhat do you do?")
    options = [
        "Study the layout and mark the escape pod position (remember it)",
        "Sit and take a moment (rest)",
        "Return to the Corridor"
    ]
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    choice = prompt_choice(options)
    if choice == 0:
        print("You memorize the route to the escape pod bay. You won't get lost now.")
        state["know_pod_route"] = True
        return "obsdeck"
    elif choice == 1:
        print("You rest a moment, feeling slightly better.")
        return "obsdeck"
    else:
        return "corridor"


def scene_ai_core(state):
    print("\n=== AI CORE MAINTENANCE ===")
    print("The maintenance passage opens into a chamber centered around the silent AI core.")
    print("A receptacle on the core could accept an energy cell to reboot the station's AI.")
    print("\nWhat do you do?")
    options = [
        "Insert the energy cell into the AI core",
        "Attempt to bypass controls manually",
        "Leave the AI Core and return to the Corridor"
    ]
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    choice = prompt_choice(options)
    if choice == 0:
        if state.get("energy_cell"):
            print("You fit the energy cell into the core. Lights surge as the AI comes online.")
            print("The AI's voice whispers: 'Initialization complete. Command?'")
            state["ai_online"] = True
            # AI assists: open observation deck if not already
            state["obs_unlocked"] = True
            return "ai_core"
        else:
            print("You have no energy cell. The core rejects your attempts.")
            print("A defensive protocol misinterprets your tampering.")
            return "vacuum"
    elif choice == 1:
        if state.get("reactor_stable"):
            print("With the reactor stable, manual bypass works. The AI stirs partially.")
            state["ai_online"] = True
            return "ai_core"
        else:
            print("Without stable power, the bypass attempt fails and triggers a purge.")
            if state.get("mask"):
                print("You quickly put on the oxygen mask and escape the purge, coughing but alive.")
                return "ai_core"
            else:
                print("You are exposed to a decompression purge.")
                return "vacuum"
    else:
        return "corridor"


def scene_escape_pod(state):
    print("\n=== ESCAPE POD BAY ===")
    print("You reach the escape pod bay. One pod looks intact but is offline.")
    print("\nWhat do you do?")
    options = [
        "Try to power the pod with the energy cell",
        "Attempt to boot the pod manually from onboard controls",
        "Call the AI for assistance (if online)"
    ]
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    choice = prompt_choice(options)
    if choice == 0:
        if state.get("energy_cell"):
            print("You jury-rig the energy cell to the pod. Systems hum. The pod powers up.")
            print("You launch away from the dying station—you're safe.")
            return "win"
        else:
            print("You don't have an energy cell to power the pod manually.")
            return "escape_pod"
    elif choice == 1:
        if state.get("know_pod_route") and state.get("ai_online"):
            print("Using the route knowledge and AI diagnostics, you troubleshoot the pod and boot it.")
            print("The pod takes you away to safety.")
            return "win"
        elif state.get("ai_online"):
            print("The AI helps partially but the pod needs auxiliary power.")
            return "escape_pod"
        else:
            print("Without power or AI help, you cannot boot the pod.")
            return "escape_pod"
    else:
        if state.get("ai_online"):
            print("The AI acknowledges and routes power to the pod. 'You may proceed,' it says.")
            print("You climb into the pod and eject—safe.")
            return "win"
        else:
            print("No AI is online to assist. The comms remain dead.")
            return "escape_pod"


def scene_reactor_overload(state):
    print("\n=== REACTOR OVERLOAD ===")
    print("You misstepped in the Engine Room and triggered a reactor breach.")
    print("Alarms scream as the station begins to tear itself apart.")
    print("The hull ruptures. You are thrown into the void.")
    print("GAME OVER — You lose.")
    return "end"


def scene_vacuum(state):
    print("\n=== DECOMPRESSION ===")
    print("A system purge vents atmosphere into space. Without protection, the vacuum is lethal.")
    if state.get("mask"):
        print("Luckily, you had an oxygen mask and take shelter until systems settle.")
        print("You survive, coughing and shaken, but many systems are ruined.")
        # Survived but some things may be inaccessible. Return to corridor.
        return "corridor"
    else:
        print("You were exposed and cannot hold on. Your vision fades.")
        print("GAME OVER — You lose.")
        return "end"


def scene_win(state):
    print("\n=== ESCAPED ===")
    print("The pod carries you away. You watch the station shrink behind you.")
    print("Against the odds, you survived. Congratulations!")
    return "end"


SCENES = {
    "airlock": scene_airlock,
    "corridor": scene_corridor,
    "bridge": scene_bridge,
    "engine": scene_engine,
    "cargo": scene_cargo,
    "medbay": scene_medbay,
    "obsdeck": scene_obsdeck,
    "ai_core": scene_ai_core,
    "escape_pod": scene_escape_pod,
    "reactor_overload": scene_reactor_overload,
    "vacuum": scene_vacuum,
    "win": scene_win,
}


def main():
    print("Welcome to 'Mergington Station: A Short Space Adventure'")
    print("Type the number of your choice and press Enter. Type 'quit' to exit at any prompt.")
    # game state stores inventory and flags
    state = {
        "suit": False,
        "energy_cell": False,
        "mask": False,
        "reactor_stable": False,
        "ai_online": False,
        "obs_unlocked": False,
        "know_pod_route": False,
        "bridge_powered": False,
    }
    current = "airlock"
    # Play until scene returns "end"
    while True:
        if current == "end":
            print("\nThank you for playing.")
            break
        # Special: allow moving to escape pod if player knows route or chooses to look for it from corridor.
        # But we'll let scenes determine navigation.
        scene_func = SCENES.get(current)
        if not scene_func:
            print(f"Unknown location '{current}'. The game ends abruptly.")
            break
        next_scene = scene_func(state)
        # Some scenes may return same string or modify state.
        if next_scene == "end":
            current = "end"
            continue
        # handle attempts to go to escape pod directly from corridor if conditions met
        if next_scene == "corridor" and state.get("know_pod_route"):
            # Player can choose to head to escape pod from corridor on next loop by being offered in corridor's options
            # To avoid forcing, we simply set current to corridor.
            current = "corridor"
        elif next_scene in SCENES:
            current = next_scene
        else:
            # unknown next; end gracefully
            print("Something strange happened. The story cannot continue.")
            break
    # End of game summary
    print("\nFinal status:")
    items = []
    if state.get("suit"):
        items.append("work-suit")
    if state.get("energy_cell"):
        items.append("energy cell")
    if state.get("mask"):
        items.append("oxygen mask")
    if items:
        print("Items collected:", ", ".join(items))
    else:
        print("You collected no items.")
    if state.get("ai_online"):
        print("AI status: online")
    else:
        print("AI status: offline")


if __name__ == "__main__":
    main()