import json
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Meal Planner AI",
    page_icon="🍽️",
    layout="wide"
)

SUPERMARKETS = ["AH", "Jumbo", "Deka", "Vomar", "Dirk", "Plus", "Lidl", "ALDI", "Coop"]
APPLIANCES = ["Airfryer", "Magnetron", "Oven", "Kookplaat"]

PREFERENCES = [
    "Snel", "Gezond", "Vega", "Vegan", "Proteïne rijk",
    "Luxe", "Zomers", "Winter", "Glutenvrij"
]

BASE_PRODUCTS = [
    {"name": "kipfilet", "price": 6.49, "protein": 46},
    {"name": "rijst", "price": 1.79, "protein": 7},
    {"name": "pasta", "price": 1.49, "protein": 12},
    {"name": "paprika", "price": 0.99, "protein": 1},
    {"name": "ui", "price": 0.89, "protein": 1},
    {"name": "knoflook", "price": 0.99, "protein": 1},
    {"name": "broccoli", "price": 1.49, "protein": 4},
    {"name": "courgette", "price": 1.29, "protein": 2},
    {"name": "wraps", "price": 2.19, "protein": 8},
    {"name": "kaas", "price": 3.49, "protein": 25},
    {"name": "tomatensaus", "price": 1.29, "protein": 2},
    {"name": "tonijn", "price": 1.89, "protein": 28},
    {"name": "mager gehakt", "price": 5.99, "protein": 45},
    {"name": "aardappelen", "price": 2.49, "protein": 8},
    {"name": "krieltjes", "price": 2.49, "protein": 4},
    {"name": "sperziebonen", "price": 1.99, "protein": 3},
    {"name": "groentemix", "price": 1.99, "protein": 4},
    {"name": "eieren", "price": 3.29, "protein": 42},
    {"name": "magere kwark", "price": 1.99, "protein": 50},
    {"name": "yoghurt", "price": 1.49, "protein": 18},
    {"name": "melk", "price": 1.19, "protein": 8},
    {"name": "brood", "price": 1.69, "protein": 20},
    {"name": "havermout", "price": 0.99, "protein": 13},
    {"name": "zalm", "price": 5.99, "protein": 35},
    {"name": "kipdijfilet", "price": 5.49, "protein": 42},
    {"name": "mais", "price": 1.19, "protein": 3},
    {"name": "kidneybonen", "price": 1.09, "protein": 8},
    {"name": "couscous", "price": 1.39, "protein": 12},
    {"name": "creme fraiche", "price": 1.49, "protein": 3},
    {"name": "komkommer", "price": 0.99, "protein": 1},
    {"name": "sla", "price": 1.29, "protein": 1},
]

CATALOG = {
    "AH": BASE_PRODUCTS,
    "Jumbo": BASE_PRODUCTS,
    "Deka": BASE_PRODUCTS,
    "Vomar": BASE_PRODUCTS,
    "Dirk": BASE_PRODUCTS,
    "Plus": BASE_PRODUCTS,
    "Lidl": BASE_PRODUCTS,
    "ALDI": BASE_PRODUCTS,
    "Coop": BASE_PRODUCTS,
}


def get_catalog_for_supermarket(supermarket):
    return CATALOG.get(supermarket, BASE_PRODUCTS)


RECIPES = [
    {
        "name": "Kip met rijst en paprika",
        "price": 4.80,
        "kcal": 650,
        "protein": 48,
        "ingredients": ["kipfilet", "rijst", "paprika"],
        "instructions": "Bak de kipfilet, kook de rijst en serveer met paprika."
    },
    {
        "name": "Pasta tonijn met tomatensaus",
        "price": 3.60,
        "kcal": 590,
        "protein": 36,
        "ingredients": ["pasta", "tonijn", "tomatensaus"],
        "instructions": "Kook de pasta en meng met tonijn en tomatensaus."
    },
    {
        "name": "Airfryer aardappelen met gehakt",
        "price": 4.20,
        "kcal": 720,
        "protein": 42,
        "ingredients": ["aardappelen", "mager gehakt", "groentemix"],
        "instructions": "Bereid de aardappelen in de airfryer en bak het gehakt met groente."
    }
]


def init_state():
    defaults = {
        "page": "home",
        "supermarket": None,
        "budget": 50.0,
        "persons": 2,
        "days": 5,
        "appliances": [],
        "preferences": [],
        "custom_prompt": "",
        "wishlist": [],
        "extra_products": [],
        "ai_recipes": []
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def generate_ai_recipes():
    catalog = get_catalog_for_supermarket(st.session_state.supermarket)

    if "GEMINI_API_KEY" not in st.secrets:
        st.error("GEMINI_API_KEY ontbreekt in Streamlit Secrets.")
        return RECIPES

    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    prompt = f"""
Je bent een Nederlandse maaltijdplanner-app.

Maak exact 12 normale Nederlandse maaltijdideeën in geldig JSON-formaat.

Gebruikerskeuzes:
- Supermarkt: {st.session_state.supermarket}
- Budget totaal: €{st.session_state.budget}
- Personen: {st.session_state.persons}
- Aantal dagen: {st.session_state.days}
- Keukenapparaten: {st.session_state.appliances}
- Voorkeuren: {st.session_state.preferences}
- Extra wens: {st.session_state.custom_prompt}

Gebruik alleen producten uit deze catalogus:
{catalog}

Belangrijk:
- Gebruik alleen ingrediënten die letterlijk in de catalogus staan.
- Houd rekening met budget.
- Houd rekening met keukenapparaten.
- Geef prijs per persoon.
- Geef kcal en eiwit per persoon als schatting.
- Antwoord alleen met JSON, geen uitleg.
- Maak alleen realistische Nederlandse avondmaaltijden.
- Geen rare combinaties zoals yoghurt met gehakt, kwark met pasta of havermout met tonijn.
- Elk recept moet minimaal 3 ingrediënten bevatten.
- Maak recepten die mensen daadwerkelijk zouden koken.
- Maak exact 12 recepten.
- Gebruik duidelijke receptnamen zoals:
  - Kip met rijst en paprika
  - Pasta tonijn met groente
  - Airfryer aardappelen met gehakt
  - Wraps met kip en groenten

JSON structuur:
[
  {{
    "name": "naam recept",
    "price": 4.50,
    "kcal": 650,
    "protein": 45,
    "ingredients": ["product 1", "product 2", "product 3"],
    "instructions": "korte bereidingswijze"
  }}
]
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        recipes = json.loads(text)

        if not isinstance(recipes, list):
            return RECIPES

        return recipes

    except Exception as e:
        st.error(f"AI-generatie mislukt: {e}")
        return RECIPES


def go_to(page):
    st.session_state.page = page
    st.rerun()


def card_css():
    st.markdown("""
    <style>
    .main-title {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 0;
    }
    .sub-title {
        font-size: 20px;
        color: #666;
        margin-bottom: 30px;
    }
    .recipe-card {
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #e5e5e5;
        background: #ffffff;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        margin-bottom: 18px;
    }
    </style>
    """, unsafe_allow_html=True)


def header(title, subtitle=""):
    st.markdown(f"<div class='main-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='sub-title'>{subtitle}</div>", unsafe_allow_html=True)


def home_page():
    header("🍽️ Meal Planner AI", "Kies eerst je supermarkt")

    cols = st.columns(3)

    for index, market in enumerate(SUPERMARKETS):
        with cols[index % 3]:
            if st.button(market, use_container_width=True):
                st.session_state.supermarket = market
                st.session_state.ai_recipes = []
                st.session_state.wishlist = []
                go_to("settings")


def settings_page():
    header(f"🛒 {st.session_state.supermarket}", "Vul je budget en planning in")

    st.session_state.budget = st.number_input(
        "Budget totaal (€)",
        min_value=1.0,
        value=float(st.session_state.budget),
        step=5.0
    )

    st.session_state.persons = st.number_input(
        "Aantal personen",
        min_value=1,
        value=int(st.session_state.persons),
        step=1
    )

    st.session_state.days = st.number_input(
        "Aantal dagen",
        min_value=1,
        value=int(st.session_state.days),
        step=1
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Terug", use_container_width=True):
            go_to("home")

    with col2:
        if st.button("Volgende →", use_container_width=True):
            go_to("appliances")


def appliances_page():
    header("🍳 Keukenapparaten", "Selecteer wat je wilt gebruiken")

    selected = []
    cols = st.columns(4)

    icons = {
        "Airfryer": "🍟",
        "Magnetron": "📦",
        "Oven": "🔥",
        "Kookplaat": "🍳"
    }

    for index, appliance in enumerate(APPLIANCES):
        with cols[index]:
            checked = st.checkbox(
                f"{icons[appliance]} {appliance}",
                value=appliance in st.session_state.appliances
            )
            if checked:
                selected.append(appliance)

    st.session_state.appliances = selected

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Terug", use_container_width=True):
            go_to("settings")

    with col2:
        if st.button("Volgende →", use_container_width=True):
            go_to("preferences")


def preferences_page():
    header("🤖 AI voorkeuren", "Wat voor soort menu wil je?")

    st.session_state.preferences = st.multiselect(
        "Kies één of meer stijlen",
        PREFERENCES,
        default=st.session_state.preferences
    )

    st.session_state.custom_prompt = st.text_input(
        "Of typ zelf iets",
        value=st.session_state.custom_prompt,
        placeholder="Bijvoorbeeld: goedkoop, weinig afwas, veel kip, geen vis..."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Terug", use_container_width=True):
            go_to("appliances")

    with col2:
        if st.button("Genereer recepten met AI →", use_container_width=True):
            with st.spinner("Gemini maakt recepten op basis van jouw keuzes..."):
                st.session_state.ai_recipes = generate_ai_recipes()
            go_to("recipes")


def recipes_page():
    header("📋 AI Receptvoorstellen", "Scroll door de recepten en sla favorieten op met het hartje")

    st.info(
        f"Supermarkt: {st.session_state.supermarket} | "
        f"Budget: €{st.session_state.budget:.2f} | "
        f"{st.session_state.persons} personen | "
        f"{st.session_state.days} dagen | "
        f"Apparaten: {', '.join(st.session_state.appliances)}"
    )

    recipes_to_show = st.session_state.ai_recipes or RECIPES

    for recipe in recipes_to_show:
        with st.container():
            st.markdown("<div class='recipe-card'>", unsafe_allow_html=True)

            col1, col2 = st.columns([4, 1])

            with col1:
                st.subheader(recipe.get("name", "Naamloos recept"))
                st.write(f"Prijs per persoon: €{float(recipe.get('price', 0)):.2f}")
                st.write(
                    f"Voeding: {recipe.get('kcal', '?')} kcal | "
                    f"{recipe.get('protein', '?')}g eiwit"
                )
                st.write("Ingrediënten: " + ", ".join(recipe.get("ingredients", [])))
                st.caption(recipe.get("instructions", ""))

            with col2:
                if st.button("❤️", key=f"heart_{recipe.get('name', '')}"):
                    if recipe not in st.session_state.wishlist:
                        st.session_state.wishlist.append(recipe)
                        st.success("Toegevoegd")

            st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Terug", use_container_width=True):
            go_to("preferences")

    with col2:
        if st.button("Naar wishlist →", use_container_width=True):
            go_to("wishlist")


def wishlist_page():
    header("❤️ Wishlist", "Maak je selectie compleet")

    if not st.session_state.wishlist:
        st.warning("Je wishlist is nog leeg.")
    else:
        total = 0

        for recipe in st.session_state.wishlist:
            recipe_total = float(recipe.get("price", 0)) * st.session_state.persons
            total += recipe_total
            st.write(f"**{recipe.get('name', 'Naamloos recept')}** — €{recipe_total:.2f}")

        st.success(f"Totaal geschat: €{total:.2f}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Terug", use_container_width=True):
            go_to("recipes")

    with col2:
        if st.button("Boodschappenlijst maken →", use_container_width=True):
            go_to("shopping")


def shopping_page():
    header("🧾 Boodschappenlijst", "Ingrediënten + extra producten uit de catalogus")

    shopping_items = []

    for recipe in st.session_state.wishlist:
        shopping_items.extend(recipe.get("ingredients", []))

    shopping_items.extend(st.session_state.extra_products)

    unique_items = sorted(set(shopping_items))

    st.subheader("Jouw lijst")

    if unique_items:
        for item in unique_items:
            st.checkbox(item, value=False)
    else:
        st.warning("Nog geen producten geselecteerd.")

    st.divider()

    st.subheader(f"Zoek in catalogus van {st.session_state.supermarket}")

    search = st.text_input("Zoek product", placeholder="Bijvoorbeeld melk, brood, yoghurt...")

    catalog = get_catalog_for_supermarket(st.session_state.supermarket)

    if search:
        results = [
            product for product in catalog
            if search.lower() in product["name"].lower()
        ]

        if results:
            for product in results:
                button_text = f"+ Voeg {product['name']} toe (€{product['price']:.2f})"

                if st.button(button_text, key=f"add_{product['name']}"):
                    if product["name"] not in st.session_state.extra_products:
                        st.session_state.extra_products.append(product["name"])
                        st.rerun()
        else:
            st.write("Geen producten gevonden.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Terug", use_container_width=True):
            go_to("wishlist")

    with col2:
        if st.button("Opnieuw beginnen", use_container_width=True):
            st.session_state.clear()
            st.rerun()


init_state()
card_css()

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "settings":
    settings_page()
elif st.session_state.page == "appliances":
    appliances_page()
elif st.session_state.page == "preferences":
    preferences_page()
elif st.session_state.page == "recipes":
    recipes_page()
elif st.session_state.page == "wishlist":
    wishlist_page()
elif st.session_state.page == "shopping":
    shopping_page()
