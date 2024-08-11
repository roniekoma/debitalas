import streamlit as st

def backtrack_cutting(requests, bar_length=1200, current_cut=None, cuts=None, best_solution=None):
    if current_cut is None:
        current_cut = {'pieces': [], 'remaining': bar_length}
    if cuts is None:
        cuts = []
    if best_solution is None:
        best_solution = {'cuts': [], 'waste': float('inf')}
    
    # Ha minden kérést teljesítettünk
    if not requests:
        total_waste = sum(cut['remaining'] for cut in cuts) + current_cut['remaining']
        if total_waste < best_solution['waste']:
            best_solution['cuts'] = cuts + [current_cut] if current_cut['pieces'] else cuts
            best_solution['waste'] = total_waste
        return best_solution

    size, quantity = next(iter(requests.items()))
    new_requests = requests.copy()
    new_requests[size] -= 1
    if new_requests[size] == 0:
        del new_requests[size]

    # Próbáljuk hozzáadni az aktuális rúdhoz
    if current_cut['remaining'] >= size:
        new_cut = {'pieces': current_cut['pieces'] + [size], 'remaining': current_cut['remaining'] - size}
        backtrack_cutting(new_requests, bar_length, new_cut, cuts, best_solution)

    # Próbáljunk új rudat kezdeni
    new_cuts = cuts + [current_cut] if current_cut['pieces'] else cuts
    new_cut = {'pieces': [size], 'remaining': bar_length - size}
    backtrack_cutting(new_requests, bar_length, new_cut, new_cuts, best_solution)

    return best_solution

def calculate_cutting_plan(requests, bar_length=1200):
    total_requests = sum(requests.values())
    solution = backtrack_cutting(requests, bar_length)
    return solution['cuts'], len(solution['cuts']), solution['waste']

st.title("Vasdarab Vágási Terv")

st.subheader("Adja meg a szükséges méreteket!")
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

st.subheader("Jelenlegi kérések:")
if st.session_state.requests:
    for size, quantity in st.session_state.requests.items():
        st.write(f"Méret: {size} centiméter, Darabszám: {quantity}")
else:
    st.write("Nincsenek kérések.")

if st.button("Számítás"):
    if st.session_state.requests:
        cuts, total_bars, total_waste = calculate_cutting_plan(st.session_state.requests)
        st.write(f"Összesen szükséges 12 méteres (1200 centiméteres) darabok száma: {total_bars}")
        st.write(f"Teljes hulladék: {total_waste} centiméter")
        for i, cut in enumerate(cuts):
            st.write(f"{i+1}. 1200 centiméteres darab vágásai: {cut['pieces']}, maradék: {cut['remaining']} centiméter")
    else:
        st.error("Kérjük, adjon meg méreteket és darabszámot.")