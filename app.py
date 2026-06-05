
import streamlit as st, sqlite3

st.set_page_config(page_title="Consulta de Produtos CBZ", layout="wide")

con = sqlite3.connect("db.sqlite", check_same_thread=False)
con.execute('CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT, cbz_code TEXT, description TEXT, ean TEXT)')

st.markdown('<h1 style="color:white">Consulta de Produtos CBZ</h1>', unsafe_allow_html=True)

menu = st.sidebar.radio("Menu", ["Consulta Pública","Admin"])

if menu=="Consulta Pública":
    q = st.text_input("Pesquisar")
    rows = con.execute("SELECT cbz_code,description,ean FROM products").fetchall()
    if q:
        q=q.lower()
        rows=[r for r in rows if q in str(r).lower()]
    st.dataframe(rows, use_container_width=True)

else:
    if "auth" not in st.session_state:
        st.session_state.auth=False

    if not st.session_state.auth:
        u=st.text_input("Usuário")
        p=st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if u=="suporte" and p=="1":
                st.session_state.auth=True
                st.rerun()
    else:
        with st.form("f"):
            cbz=st.text_input("Código CBZ")
            d=st.text_input("Descrição")
            e=st.text_input("EAN")
            ok=st.form_submit_button("Salvar")
        if ok:
            con.execute("INSERT INTO products(cbz_code,description,ean) VALUES(?,?,?)",(cbz,d,e))
            con.commit()
        for r in con.execute("SELECT id,cbz_code,description,ean FROM products ORDER BY id DESC"):
            c1,c2=st.columns([8,1])
            c1.write(r)
            if c2.button("Excluir", key=str(r[0])):
                con.execute("DELETE FROM products WHERE id=?",(r[0],))
                con.commit()
                st.rerun()
