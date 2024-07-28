import streamlit as st

def calculate_cutting_plan(requests, bar_length=1200):
    cuts = []
    total_bars = 0
    for size, quantity in requests.items():
        for _ in range(quantity):
            found = False
            for cut in cuts:
                if cut['remaining'] >= size:
                    cut['pieces'].append(size)
                    cut['remaining'] -= size
                    found = True
                    break
            if not found:
                new_cut = {'pieces': [size], 'remaining': bar_length - size}
                cuts.append(new_cut)
                total_bars += 1
    return cuts, total_bars

st.title("Vasdarab Vágási Terv")

st.header("Adja meg a szükséges méreteket (méret centiméterben és darabszám):")
input_size = st.text_input("Méret (centiméterben):")
input_quantity = st.text_input("Darabszám:")

if 'requests' not in st.session_state:
    st.session_state.requests = {}

if st.button("Hozzáadás"):
    if input_size and input_quantity:
        try:
            size = int(input_size)
            quantity = int(input_quantity)
            if size > 0 and quantity > 0:
                st.session_state.requests[size] = st.session_state.requests.get(size, 0) + quantity
                st.success(f"{quantity} darab {size} centiméteres darab hozzáadva.")
            else:
                st.error("A méretnek és a darabszámnak pozitív számnak kell lennie.")
        except ValueError:
            st.error("Kérjük, adjon meg érvényes számokat.")
    else:
        st.error("Kérjük, adjon meg érvényes méretet és darabszámot.")

if st.button("Számítás"):
    if st.session_state.requests:
        cuts, total_bars = calculate_cutting_plan(st.session_state.requests)
        st.write(f"Összesen szükséges 12 méteres (1200 centiméteres) darabok száma: {total_bars}")
        for i, cut in enumerate(cuts):
            st.write(f"{i+1}. 1200 centiméteres darab vágásai: {cut['pieces']}, maradék: {cut['remaining']} centiméter")
    else:
        st.error("Kérjük, adjon meg méreteket és darabszámot.")

st.header("Jelenlegi kérések:")
if st.session_state.requests:
    for size, quantity in st.session_state.requests.items():
        st.write(f"Méret: {size} centiméter, Darabszám: {quantity}")
else:
    st.write("Nincsenek kérések.")