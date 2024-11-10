import folium
import random
import webbrowser
import time

# Monuments dictionary with detailed information
monuments = {
    "Eiffel Tower": {
        "description": "La Tour Eiffel est une grande tour métallique située à Paris, France. Elle est un symbole mondial de la France.",
        "location": "Champ de Mars, 5 Avenue Anatole France, 75007 Paris",
        "coordinates": (48.8584, 2.2945),
        "year_built": 1889,
        "architect": "Gustave Eiffel",
        "historical_significance": "La Tour Eiffel a été construite pour l'Exposition Universelle de 1889. Elle a été le plus haut monument du monde jusqu'en 1930."
    },
    "Louvre Museum": {
        "description": "Le musée du Louvre est le plus grand musée d'art du monde et un monument emblématique de Paris.",
        "location": "Rue de Rivoli, 75001 Paris",
        "coordinates": (48.8606, 2.3376),
        "year_built": 1793,
        "architect": "Pierre Lescot (initial), I. M. Pei (Pyramide)",
        "historical_significance": "Le Louvre était à l'origine un palais royal. Aujourd'hui, il abrite des œuvres célèbres telles que la Mona Lisa et la Vénus de Milo."
    },
    "Notre-Dame Cathedral": {
        "description": "La cathédrale Notre-Dame de Paris est une cathédrale gothique située sur l'île de la Cité.",
        "location": "6 Parvis Notre-Dame - Pl. Jean-Paul II, 75004 Paris",
        "coordinates": (48.8529, 2.3500),
        "year_built": 1345,
        "architect": "Maurice de Sully (initial), Jean-Baptiste-Antoine Lassus (restauration)",
        "historical_significance": "Notre-Dame a été un centre spirituel et culturel majeur en France, notamment pendant les événements de la Révolution française et les guerres mondiales."
    },
    "Sacré-Cœur Basilica": {
        "description": "La basilique du Sacré-Cœur est une église située au sommet de la colline de Montmartre.",
        "location": "35 Rue du Chevalier de la Barre, 75018 Paris",
        "coordinates": (48.8867, 2.3431),
        "year_built": 1914,
        "architect": "Paul Abadie",
        "historical_significance": "La basilique est un symbole de la foi chrétienne et un lieu de pèlerinage. Elle a été construite après la défaite de la France dans la guerre franco-prussienne."
    },
    "Arc de Triomphe": {
        "description": "L'Arc de Triomphe est un monument historique situé sur la place Charles de Gaulle, à l'extrémité ouest des Champs-Élysées.",
        "location": "Place Charles de Gaulle, 75008 Paris",
        "coordinates": (48.8738, 2.2950),
        "year_built": 1836,
        "architect": "Jean Chalgrin",
        "historical_significance": "L'Arc de Triomphe commémore les victoires militaires de Napoléon Bonaparte et les soldats français tombés au combat. Il abrite la tombe du Soldat Inconnu."
    }
}

# Global variable for keeping track of the score
score = 0
time_limit = 30  # Time limit for each question in seconds

# Function to ask more complex trivia questions
def ask_trivia_question(monument):
    global score
    
    correct_answer = monument
    other_choices = random.sample([m for m in monuments.keys() if m != correct_answer], 3)
    choices = random.sample([correct_answer] + other_choices, 4)

    # Display the trivia question with more information than just location
    print(f"\nVoici quelques informations sur un monument :")
    print(f"Description: {monuments[monument]['description']}")
    print(f"Emplacement: {monuments[monument]['location']}")
    print(f"Année de construction: {monuments[monument]['year_built']}")
    print(f"Architecte: {monuments[monument]['architect']}")
    print(f"Signification historique: {monuments[monument]['historical_significance']}")
    print(f"\nQuel monument correspond à ces informations ?")
    
    # Present choices without the number or name explicitly mentioned in the question
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")
    
    # Start a timer for the answer
    start_time = time.time()
    
    try:
        answer = int(input(f"Entrez le numéro de votre réponse (temps limité à {time_limit} secondes) : "))
        elapsed_time = time.time() - start_time
        
        # If the time limit is exceeded, penalize the player
        if elapsed_time > time_limit:
            print("Temps écoulé! Vous avez perdu des points.")
            display_monument_info(monument)  # Show location and information regardless of answer
            return False  # Incorrect answer because of time
        elif choices[answer - 1] == correct_answer:
            print("Bonne réponse !\n")
            score += 10  # Award points for correct answers
            display_monument_info(monument)  # Show location and information regardless of answer
            return True
        else:
            print(f"Mauvaise réponse ! La bonne réponse était {correct_answer}.\n")
            score -= 5  # Deduct points for incorrect answers
            display_monument_info(monument)  # Show location and information regardless of answer
            return False
    except (ValueError, IndexError):
        print("Réponse invalide. Vous avez perdu des points.")
        score -= 5  # Deduct points for invalid answers
        display_monument_info(monument)  # Show location and information regardless of answer
        return False

# Function to display monument information with an additional fact
def display_monument_info(monument_name):
    info = monuments[monument_name]
    print(f"\nMonument: {monument_name}")
    print(f"Description: {info['description']}")
    print(f"Emplacement: {info['location']}")
    print(f"Coordonnées géographiques: {info['coordinates']}")
    print(f"Année de construction: {info['year_built']}")
    print(f"Architecte: {info['architect']}")
    print(f"Signification historique: {info['historical_significance']}\n")
    
    # Show the map of the monument
    show_map(monument_name)

# Function to show the map with the monument location
def show_map(monument_name):
    location = monuments[monument_name]['coordinates']
    monument_map = folium.Map(location=location, zoom_start=15)
    folium.Marker(location, popup=monument_name).add_to(monument_map)
    
    # Save the map to an HTML file and open it in the browser
    map_filename = f"{monument_name.replace(' ', '_')}_map.html"
    monument_map.save(map_filename)
    webbrowser.open(map_filename)

# Function to display the current score
def display_score():
    print(f"\nVotre score actuel est : {score} points")

# Main game loop
def play_game():
    global score
    print("Bienvenue dans le jeu de monuments !\n")
    
    monument_names = list(monuments.keys())
    random.shuffle(monument_names)  # Shuffle the order of the monuments
    
    for monument_name in monument_names:
        display_score()
        
        # Show monument information and ask trivia question
        if not ask_trivia_question(monument_name):
            print("Votre performance était insuffisante. Recommencez pour obtenir un meilleur score!")
        
    print(f"Merci d'avoir joué! Votre score final est : {score} points. À bientôt!")

# Start the game
if __name__ == "__main__":
    play_game()