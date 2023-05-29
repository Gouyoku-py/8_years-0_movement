# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json


st.title('Μηνιαία εξέταση μη κινούμενων υλικών οκταετίας')
st.markdown('Μια εφαρμογή με στόχο να βοηθήσει τη Διαχείριση Αποθέματος στη μηνιαία εξέταση των υλικών που αναλώθηκαν τελευταία φορά τον ίδιο μήνα, πριν 8 χρόνια.')

help_date = 'Υπό κανονικές συνθήκες, η εφαρμογή αυτή χρησιμοποιείται μια φορά το μήνα. Σε περίπτωση που αυτό δεν είναι δυνατό για κάποιο μήνα, μπορεί να χρησιμοποιηθεί σε επόμενο χρόνο, εισάγοντας μια οποιαδήποτε ημερομηνία μέσα στον μήνα για τον οποίο θέλετε να κάνετε την ανάλυση.'

date = st.date_input(label = 'Εισάγετε μια οποιαδήποτε ημερομηνία μέσα στον μήνα για τον οποίο θέλετε να εργαστείτε (π.χ. τρέχοντα).',
                     value = pd.to_datetime('today'),
                     key = 'key_date',
                     help = help_date,
                     on_change = None,
                     disabled = False,
                     label_visibility = 'visible')

uploaded_file_CS9 = st.file_uploader(label = 'Εισάγετε το αρχείο που προκύπτει από την κίνηση CS.9, εφαρμόζοντας τις οδηγίες της βοήθειας (αμέσως παρακάτω).',
                                     type = 'txt',
                                     accept_multiple_files = False,
                                     key = 'key_upload_CS9',
                                     help = None,
                                     on_change = None,
                                     disabled = False,
                                     label_visibility = 'visible')


with st.expander('Βοήθεια για κίνηση CS.9', expanded = False):
    st.markdown(':o:Ανοίξτε την κίνηση **CS.9**, συμπληρώστε τις τιμές *Εγκατάσταση* = 4000, *Αποθηκευτικός Χώρος* = MG01 και *Μήνας* από τον προηγούμενο έως τον τρέχοντα και εκτελέστε την κίνηση **(F8)**.  \n\
                 :o:Πατήστε το εικονίδιο **Επιλογή Αριθμοδεικτών (F6)**, αφαιρέστε από τα **Κριτήρια Επιλογής** όλες τις παραμέτρους, προσθέστε αποκλειστικά την *Τελευταία Ανάλωση* και πατήστε **Συνέχεια (Καταχώρηση)**.  \n\
                 :o:Πατήστε το εικονίδιο **Αποθήκευση σε αρχείο PC (Shift + F8)**, επιλέξτε **Κείμενο σε καρτέλες**, αποθηκεύστε το αρχείο σε κάποια θέση όπου έχετε εύκολη πρόσβαση και εισάγετέ το παραπάνω.')

try:
    df = pd.read_csv(uploaded_file_CS9,
                     sep = '\s+',
                     header = 0,
                     names = ['code', 'last_used'], 
                     skiprows = [0,1,3,4],
                     parse_dates = ['last_used'],
                     encoding = 'utf-8')
    
    offset_date = date - pd.DateOffset(years = 8)
    date0 = offset_date.replace(day = 1)
    date1 = offset_date.replace(day = 1, month = offset_date.month + 1)
    
    codes = df[df['last_used'].between(date0, date1, inclusive = 'left')].copy(deep = True)
    csv_codes = codes['code'].to_csv(header = False, index = False)
    
    
    st.download_button(label = 'Κατεβάστε τους κωδικούς που πρέπει να εισάγετε στην κίνηση MB51.',
                       data = csv_codes,
                       file_name = 'codes_for_MB51.csv',
                       mime = 'text/csv',
                       key = 'key_download_codes',
                       help = None,
                       on_click = None,
                       disabled = False,
                       use_container_width = False)
except:
    st.markdown('*Όταν εισάγετε ένα έγκυρο αρχείο από την CS.9, στο σημείο αυτό θα εμφανιστεί η επιλογή να κατεβάσετε τους κωδικούς που πρέπει να εισάγετε στην MB51.*')

uploaded_file_MB51 = st.file_uploader(label = 'Εισάγετε το αρχείο που προκύπτει από την κίνηση MB51, εφαρμόζοντας τις οδηγίες της βοήθειας (αμέσως παρακάτω).',
                                      type = 'xlsx',
                                      accept_multiple_files = False,
                                      key = 'key_upload_MB51',
                                      help = None,
                                      on_change = None,
                                      disabled = False,
                                      label_visibility = 'visible')

with st.expander('Βοήθεια για κίνηση ΜΒ51', expanded = False):
    st.markdown(':o:Ανοίξτε την κίνηση **MB51** και στο *Υλικό* εισάγετε πολλαπλές επιλογές, αντιγράφοντας τους κωδικούς του αρχείου που κατεβάσατε παραπάνω και πραγματοποιώντας **Φόρτωση από πίνακα σημειώσεων (Shift + F12)**, πριν τελικά πατήσετε **Αντιγραφή (F8)**. Ακόμη συμπληρώστε τις τιμές *Εγκατάσταση* = 4000, *Αποθηκευτικός Χώρος* = MG01 και *Ενιαία Λίστα - Διάταξη* = /EVA.  \n\
                 :o:Εκτελέστε την κίνηση **(F8)** και όταν ανοίξει ο πίνακας με το αποτέλεσμα, από το μενού στην κορυφή της σελίδας επιλέξτε **Λίστα > Εξαγωγή > Λογιστικό Φύλλο (Shift + F4)**. Από τις διαθέσιμες μορφοποιήσεις επιλέξτε *Excel σε μορφή 2007 (XLSX)* και πατήστε **Συνέχεια (Καταχώρηση)**.  \n\
                 :o:Αποθηκεύστε το αρχείο σε κάποια θέση όπου έχετε εύκολη πρόσβαση και εισάγετέ το παραπάνω.')

@st.cache_data
def load_transaction_types():
    data = pd.read_excel('transaction_types.xlsx', 
                         names = ['type', 'descr'], 
                         index_col = 'type')
    return data
    
@st.cache_data
def load_transaction_columns():
    with open('transaction_columns.txt', 'r', encoding = 'utf-8') as f:
        data = json.loads(f.read())
    return data

@st.cache_data
def load_transaction_data(io):
    data = pd.read_excel(io,
                         header = 0,
                         names = trans_col_names.values(),
                         index_col = 'code',
                         converters = {'Κέντρο Κόστους': str}, 
                         parse_dates = ['date'])
    return data

def report(x):
    x = int(x)
    y = trans.query('code == @x').set_index('date')
    y_unit = y['unit'].unique()[0]
    y_q = y['quantity'].copy(deep = True)

    y_df = pd.concat([y_q.where(y_q > 0), y_q.where(y_q < 0)], axis = 1)
    y_df.columns = ['Εισαγωγή σε ΚΑ', 'Εξαγωγή από ΚΑ']

    freq = 'Y'
    y_df = y_df.resample(freq, closed = 'right', label = 'right').sum()

    new_date_range = pd.date_range(start = "1998-12-31", 
                                   end = pd.to_datetime('today').replace(month = 12, day = 31), 
                                   freq = freq)
    y_df = y_df.reindex(new_date_range, fill_value = 0)
    y_df.index = y_df.index.year

    fig_i, ax_i = plt.subplots()
    y_df.plot(kind = 'bar', ax = ax_i, title = 'Κινήσεις υλικού {}'.format(x), grid = True, 
              xlabel = 'Έτος', ylabel = 'Ποσότητα / {}'.format(y_unit), rot = 45, color = ['C2', 'C3'])
    ax_i.axhline(y = 0, c = 'k', ls = '--', lw = 1.0)
    
    y.fillna('-', inplace = True)
    y.index = y.index.strftime('%d/%m/%Y')
    for col in ['cost_center', 'order']:
        y[col] = y[col].apply(lambda x: int(x) if isinstance(x, float) else x)
    y['value'] = y['value'].apply(lambda x: '{:,.1f} €'.format(x))
    
    y.columns = ['ΚΙΝ.', 'ΠΕΡΙΓΡΑΦΗ', 'Κ.Κ.', 'ΕΝΤ.', 'WBS', 'ΠΟΣ.', 'ΜΟΝ.', 'ΑΞΙΑ', 'ΠΑΡΑΛΗΠΤΗΣ']
    y.index.name = 'ΗΜ/ΝΙΑ'
    
    st.pyplot(fig_i)
    st.dataframe(y, use_container_width = True)
     
    return None

trans_types = load_transaction_types()
trans_col_names = load_transaction_columns()
today = pd.to_datetime('today')

try:
    trans = load_transaction_data(uploaded_file_MB51)
    trans.drop(columns = ['date0', 'user', 'descr', 'res_id'], inplace = True)
    trans.query('date <= @today', inplace = True) ### do not comment or delete
    trans.insert(1, 'trans_descr', trans['trans_type'].apply(lambda x: trans_types.loc[x]))
    trans.sort_values(['code', 'date', 'trans_type'], inplace = True)
    
    help_select_code = ''
    
    code = st.selectbox('Επιλέξτε τον κωδικό για τον οποίο ενδιαφέρεστε', 
                        trans.index.unique(), 
                        index = 0,
                        format_func = int,
                        key = 'key_select_code', 
                        help = help_select_code, 
                        on_change = None, 
                        disabled = False, 
                        label_visibility = 'visible')
        
    report(code)
    
    # users = trans.groupby('code')['receiver'].unique().copy(deep = True)
    # csv_users = users.to_csv(header = ['ΧΡΗΣΤΕΣ'], index = True, index_label = 'ΥΛΙΚΟ')
    # st.dataframe(users)
    
    # st.download_button(label = 'Κατεβάστε τους διαφορετικούς χρήστες ανά κωδικό.',
    #                     data = csv_users,
    #                     file_name = 'users_per_code.csv',
    #                     mime = 'text/csv',
    #                     key = 'key_download_users',
    #                     help = None,
    #                     on_click = None,
    #                     disabled = False,
    #                     use_container_width = False)
except:
    st.markdown('*Όταν εισάγετε ένα έγκυρο αρχείο από την MB51, στο σημείο αυτό θα εμφανιστεί η ανάλυση κινήσεων για τους κωδικούς που σας ενδιαφέρουν.*')
