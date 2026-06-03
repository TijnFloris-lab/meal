import streamlit as st

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

CATALOG = [
    "Melk", "Brood", "Yoghurt", "Kipfilet", "Rijst", "Pasta",
    "Eieren", "Tonijn", "Havermout", "Paprika", "Courgette",
    "Aardappelen", "Gehakt", "Kwark"
]

RECIPES = [
    {
        "name": "Proteïne kip bowl",
        "price": 4.80,
        "kcal": 650,
        "protein": 48,
        "ingredients": ["Kipfilet", "Rijst", "Paprika", "Yoghurt"]
    },
    {
        "name": "Snelle tonijn pasta",
        "price": 3.60,
        "kcal": 590,
        "protein": 36,
        "ingredients": ["Pasta", "Tonijn", "Paprika"]
    },
    {
        "name": "Airfryer aardappel bowl",
        "price": 4.20,
        "kcal": 720,
        "protein": 42,
        "ingredients": ["Aardappelen", "Gehakt", "Courgette"]
    },
    {
        "name": "Vega yoghurt bowl",
        "price": 2.90,
        "kcal": 520,
        "protein": 31,
        "ingredients": ["Yoghurt", "Havermout", "Kwark"]
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
        "extra_products": []
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


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
    .small-muted {
        color: #777;
        font-size: 14px;
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
        if st.button("Genereer recepten →", use_container_width=True):
            go_to("recipes")


def recipes_page():
    header("📋 Receptvoorstellen", "Scroll door de recepten en sla favorieten op met het hartje")

    st.info(
        f"Supermarkt: {st.session_state.supermarket} | "
        f"Budget: €{st.session_state.budget:.2f} | "
        f"{st.session_state.persons} personen | "
        f"{st.session_state.days} dagen"
    )

    for recipe in RECIPES:
        with st.container():
            st.markdown("<div class='recipe-card'>", unsafe_allow_html=True)

            col1, col2 = st.columns([4, 1])

            with col1:
                st.subheader(recipe["name"])
                st.write(f"Prijs per persoon: €{recipe['price']:.2f}")
                st.write(f"Voeding: {recipe['kcal']} kcal | {recipe['protein']}g eiwit")
                st.write("Ingrediënten: " + ", ".join(recipe["ingredients"]))

            with col2:
                if st.button("❤️", key=f"heart_{recipe['name']}"):
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
            recipe_total = recipe["price"] * st.session_state.persons
            total += recipe_total

            st.write(f"**{recipe['name']}** — €{recipe_total:.2f}")

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
        shopping_items.extend(recipe["ingredients"])

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

    if search:
        results = [p for p in CATALOG if search.lower() in p.lower()]

        if results:
            for product in results:
                if st.button(f"+ Voeg {product} toe", key=f"add_{product}"):
                    if product not in st.session_state.extra_products:
                        st.session_state.extra_products.append(product)
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