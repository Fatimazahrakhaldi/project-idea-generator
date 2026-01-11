import streamlit as st
# OpenAI-compatible client used with Hugging Face router
from openai import OpenAI
import json
import re

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Générateur d'idées de projets GenAI", page_icon="❉", layout="centered"
)

hf_api_key = st.secrets["HF_API_KEY"]

client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=hf_api_key)


# ---------------- FONCTION LLM ----------------
def generer_projets(sujet, nb_projets):

    # prompt = f"""
    # Tu dois répondre UNIQUEMENT par du JSON valide.

    # Génère exactement {nb_projets} idées de projets informatiques
    # sur le thème "{sujet}".

    # Format attendu :
    # [
    #   {{
    #     "titre": "",
    #     "description": "",
    #     "complexite": "Débutant | Intermédiaire | Avancé",
    #     "technologies": []
    #   }}
    # ]
    # """
    prompt = f"""
    Tu dois répondre UNIQUEMENT par du JSON valide.
    Aucun texte, aucune explication hors du JSON.

    Génère exactement {nb_projets} idées de projets informatiques
    sur le thème "{sujet}".

    Pour chaque projet :
    - Le titre doit être clair et concret
    - La description doit contenir 3 à 5 phrases expliquant :
    - l’objectif du projet
    - les principales fonctionnalités
    - un cas d’usage réel
    - La complexité doit être exactement l’une des valeurs suivantes :
    "Débutant", "Intermédiaire" ou "Avancé"
    - La liste des technologies doit contenir 3 à 6 éléments pertinents

    Format attendu :
    [
    {{
        "titre": "string",
        "description": "string",
        "complexite": "Débutant | Intermédiaire | Avancé",
        "technologies": ["string", "string"]
    }}
    ]
    """


    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct:cerebras",
        messages=[
            {"role": "system", "content": "Tu es un générateur JSON strict."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150 * nb_projets + 300,  # tokens adaptatifs
    )

    contenu = completion.choices[0].message.content.strip()

    if not contenu:
        raise ValueError("Réponse vide du modèle.")

    if "```" in contenu:
        contenu = contenu.split("```")[1].replace("json", "").strip()

    projets = extraire_json(contenu)

    return projets[:nb_projets]


def extraire_json(contenu):
    match = re.search(r"\[.*\]", contenu, re.DOTALL)
    if not match:
        raise ValueError("Aucun tableau JSON valide trouvé.")
    return json.loads(match.group())


# ---------------- INTERFACE ----------------
st.title("Générateur d’idées de projets")
st.markdown(
    """
Ce générateur utilise un **LLM open-source (Llama 3.1)** pour proposer  
des **idées de projets détaillées avec niveau de complexité**.
"""
)
with st.form("form_generation"):
    sujet = st.text_input("Sujet", placeholder="Ex: IA, Cybersécurité, Web, IoT...")
    nb_projets = st.slider("Nombre de projets", min_value=1, max_value=10, value=5)
    submitted = st.form_submit_button("Générer")

if submitted:
    if not sujet.strip():
        st.warning("Veuillez entrer un sujet.")
    else:
        with st.spinner("Génération en cours..."):
            try:
                projets = generer_projets(sujet, nb_projets)
                st.success(f"{len(projets)} projets générés avec succès !")

                for i, p in enumerate(projets, 1):
                    with st.expander(f"📌 Projet {i} : {p['titre']}"):
                        st.write(f"**Description :** {p['description']}")
                        st.write(f"**Complexité :** {p['complexite']}")
                        st.write("**Technologies :**")
                        st.write(", ".join(p["technologies"]))

            except Exception as e:
                st.error("Erreur lors de la génération")
                st.code(str(e))