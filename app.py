import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="cistech IT Inventory", page_icon="🖥️")
DATA_FILE = "inventory.csv"

def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["ID", "Nama", "Kategori", "Lokasi", "Tanggal Pembelian", "Nomor Seri", "Spesifikasi", "No. Computer"])

def save_data(data):
    data.to_csv(DATA_FILE, index=False)

def generate_id(data):
    if data.empty:
        return 1
    else:
        return data["ID"].max() + 1

st.title("IT INVENTORY")
st.image("cistech.png", width=450)

inventory = load_data()

menu = st.sidebar.selectbox("Menu", ["View Asset", "Add Asset", "Clear Asset", "Download Data"])

if menu == "View Asset":
    st.header("LIST ASSET IT")
    if inventory.empty:
        st.warning("No IT assets in inventory.")
    else:
        kategori = st.selectbox("Select Category", ["All", "Laptop", "Desktop", "Peripherals"])
        if kategori == "All":
            st.dataframe(inventory.reset_index(drop=True))
        else:
            filtered_inventory = inventory[inventory["Kategori"] == kategori]
            if filtered_inventory.empty:
                st.warning(f"No assets in category {kategori}.")
            else:
                st.dataframe(filtered_inventory.reset_index(drop=True))

elif menu == "Add Asset":
    st.header("Add Asset IT")
    nama = st.text_input("Asset Name")
    kategori = st.selectbox("Category Asset", ["Laptop", "Desktop", "Peripherals"])
    lokasi = st.text_input("Location Asset")
    nomor_seri = st.text_input("SN")
    spesifikasi = st.text_area("Specification", placeholder="Contoh: CPU i5, RAM 8GB, SSD 256GB")
    nomor_komputer = st.text_input("No. Computer")
    tanggal_pembelian = st.date_input("Purchase Date",
    min_value=datetime.date(2010, 1, 1),
    max_value=datetime.date.today()
)

    if st.button("Add Asset"):
        if nama and kategori and lokasi and nomor_seri and spesifikasi and nomor_komputer and tanggal_pembelian:
            id_baru = generate_id(inventory)
            new_asset = {
                "ID": id_baru,
                "Nama": nama,
                "Kategori": kategori,
                "Lokasi": lokasi,
                "Tanggal Pembelian": tanggal_pembelian.strftime("%Y-%m-%d"),
                "Nomor Seri": nomor_seri,
                "Spesifikasi": spesifikasi,
                "No. Computer": nomor_komputer
            }
            inventory = pd.concat([inventory, pd.DataFrame([new_asset])], ignore_index=True)
            save_data(inventory)
            st.success(f"Asset '{nama}' successfully added with ID {id_baru}.")
        else:
            st.error("All fields must be filled.")

elif menu == "Clear Asset":
    st.header("Clear Asset IT")
    if inventory.empty:
        st.warning("No IT assets to clear.")
    else:
        aset_terpilih = st.selectbox("Select ID asset you want to clear", inventory["ID"])
        if st.button("Clear Asset"):
            inventory = inventory[inventory["ID"] != aset_terpilih]
            save_data(inventory)
            st.success(f"Asset with ID '{aset_terpilih}' successfully deleted.")

elif menu == "Download Data":
    st.header("Download Data Inventory")
    if inventory.empty:
        st.warning("No data to download.")
    else:
        st.download_button(
            label="Download CSV",
            data=inventory.to_csv(index=False),
            file_name="inventory.csv",
            mime="text/csv"
        )
