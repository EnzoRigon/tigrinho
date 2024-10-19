import streamlit as st
import db_handler as db
import pandas as pd
from slots import play_slots, spin_slots
import time
from streamlit_cookies_controller import CookieController

cookie_controller = CookieController()

@st.dialog("Adicione ou acesse seu usuário")
def get_user():
    st.write("Escreva seu usuário:")
    user = st.text_input("Usuário")
    if st.button("Enviar"):
        user, balance = db.check_or_add_user(user)
        st.session_state.user = user
        st.session_state.balance = balance
        cookie_controller.set("user", user)
        st.rerun()

cookies_user = cookie_controller.get("user")

if cookies_user is None:
    get_user()
else:
    if 'balance' not in st.session_state:
        st.session_state.user = cookies_user
        balance = db.get_balance(cookies_user)
        st.session_state.balance = balance

    st.title('Enzas Bet 🐯')
    st.subheader(f"Usuário: {st.session_state.user}")

    bet = st.number_input("Valor da aposta:", min_value=1, max_value=int(st.session_state.balance), value=1)
    if st.button("Jogar"):
        slot_placeholder = st.empty()

        total_time = 1
        delays = [0.1, 0.2, 0.3, 0.4, 0.5]

        spins_per_delay = [max(3, int(total_time // delay)) if delay < 0.8 else 1 for delay in delays]

        for i, delay in enumerate(delays):
            for _ in range(spins_per_delay[i]):
                slots = spin_slots()

                slot_placeholder.markdown(f"""
                <div style="font-size:48px; text-align: center;">
                    {slots[0][0]} | {slots[0][1]} | {slots[0][2]}<br>
                    {slots[1][0]} | {slots[1][1]} | {slots[1][2]}<br>
                    {slots[2][0]} | {slots[2][1]} | {slots[2][2]}<br>
                </div>
                """, unsafe_allow_html=True)

                time.sleep(delay)

        balance, prize, final_slots = play_slots(bet, st.session_state.balance)
        st.session_state.balance = balance
        db.alter_balance(st.session_state.user, balance)

        slot_placeholder.markdown(f"""
        <div style="font-size:48px; text-align: center;">
            {final_slots[0][0]} | {final_slots[0][1]} | {final_slots[0][2]}<br>
            {final_slots[1][0]} | {final_slots[1][1]} | {final_slots[1][2]}<br>
            {final_slots[2][0]} | {final_slots[2][1]} | {final_slots[2][2]}<br>
        </div>
        """, unsafe_allow_html=True)

        if prize > 0:
            st.success(f"Você ganhou R$ {prize}.")
            st.balloons()
        else:
            st.error(f"Você perdeu.")
        st.info(f"Saldo: R$ {st.session_state.balance:.2f}")
            
    ranking = db.get_ranking()
    df_rank = pd.DataFrame(ranking, columns=['Usuário', 'Saldo'])
    st.dataframe(df_rank)

    if st.button("Sair"):
        for key in st.session_state.keys():
            del st.session_state[key]
        cookie_controller.remove('user')
        st.rerun()