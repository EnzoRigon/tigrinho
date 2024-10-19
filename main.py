import streamlit as st
import db_handler as db
import pandas as pd
from slots import play_slots, spin_slots
import time

@st.dialog("Adicione ou acesse seu usuário")
def get_user():
    st.write("Escreva seu usuário:")
    user = st.text_input("Usuário")
    if st.button("Enviar"):
        user, balance = db.check_or_add_user(user)
        st.session_state.user = user
        st.session_state.balance = balance
        st.rerun()


if 'user' not in st.session_state:
    get_user()
else:
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

# TODO:
# - Adicionar Animação Rotação
# - Adicionar persistencia de usuario
