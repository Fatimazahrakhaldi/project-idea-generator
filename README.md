# 🚀 Générateur d’idées de projets GenAI / LLM

## 📌 Description
Ce projet est une application **Streamlit** basée sur un **LLM open-source (Llama 3.1)** permettant de générer automatiquement des **idées de projets informatiques** à partir d’un sujet donné.

Pour chaque sujet, l’application propose :
- une liste d’idées de projets,
- une description détaillée,
- un niveau de complexité (Débutant / Intermédiaire / Avancé),
- les technologies recommandées.

### Captures d'écran
<img src="./screenshot.png">
Exemple output
<img src="./example/screenshot_output.png">

---

## 🧠 Fonctionnement général
1. L’utilisateur saisit un **sujet** (IA, Web, Cybersécurité, IoT…).
2. Il choisit le **nombre de projets** à générer.
3. Le LLM génère une réponse **au format JSON strict**.
4. L’application extrait, valide et affiche les projets de manière structurée.

---

## 🛠️ Technologies utilisées
- **Python 3**
- **Streamlit** (interface web)
- **LLM Open-source : Llama 3.1 (Meta)**
- **Hugging Face Router**
- **OpenAI compatible client**
- JSON / Regex

---

## 📂 Structure du projet
📁 project-idea-generator <br>
│── streamlit_app.py <br>
│── README.md <br>
│── screenshot.png <br>
│── requirements.txt <br>
│── .gitignore <br>
│── .streamlit/ <br>
│ └── secrets.toml

## 🔐 Configuration
Créer le fichier suivant :

### `.streamlit/secrets.toml`
```toml
HF_API_KEY = "votre_cle_api_huggingface"
```
## Installation et exécution

### 1. Récupérer le code :
```sh
$ git clone https://github.com/streamlit/project-idea-generator.git
```
### 2. Créer et activer l'environnement virtuel et installer les dépendances :
```sh
python -m venv venv
venv\Scripts\Activate.ps1 
pip install -r requirements.txt
```
### 3. Lancer l’application
```sh
streamlit run
```