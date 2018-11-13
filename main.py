import tkinter as tk
from tkinter import messagebox as ms
from tkinter import font as tkfont
from tkinter.ttk import *
import tkinter.ttk as ttk
import sqlite3
import csv
import collections
from module.modNormalize import normalize

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # root layout
        self.title('Sistem Rekomendasi Profesi')
        self.geometry('{}x{}+{}+{}'.format(900,600,200,80)) # frame location placement
        self.resizable(width='FALSE', height='FALSE') # non resizable window
        # font styling
        self.font_heading = tkfont.Font(family='Helvetica Neueu', size=24, weight='bold')
        self.font_body = tkfont.Font(family='Helvetica Neueu', size=15)
        self.font_bold = tkfont.Font(family='Helvetica Neueu', weight='bold')
        # master container
        container = tk.Frame(self)
        container.pack(fill='both', side='top')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # page controller
        self.frames = {}
        for F in (LoginPage, ProfilePage, JobPage, MatkulPage, RecPage): # inisiasi halaman
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_page('LoginPage') # default page

    def show_page(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        frame.event_generate('<<ShowPage>>')

    def get_page(self, classname):
        for page in self.frames.values():
            if str(page.__class__.__name__) == classname:
                return page
        return None

    def get_page_func(self, page_class):
        return self.frames[page_class]

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.loginUI()

    def loginUI(self):
        # master layout
        frame_body = tk.Frame(self)
        frame_body.pack(fill='both', expand=1)
        self.frame_body = frame_body
        row1 = tk.Frame(frame_body)
        row1.pack(fill='x')
        row1_element = tk.Frame(row1)
        row1_element.pack(pady=(160,0))
        row2 = tk.Frame(frame_body)
        row2.pack(fill='x', pady=(30,0))
        row2_element = tk.Frame(row2)
        row2_element.pack()
        row3 = tk.Frame(frame_body)
        row3.pack(fill='x', pady=(20,0))
        row3_element = tk.Frame(row3)
        row3_element.pack()
        # row 1 // label
        lb1 = tk.Label(row1_element, text='Masuk', font=self.controller.font_heading)
        lb1.pack(side='left')
        # row 2 // label dan entry untuk memasukkan NPM
        lb2 = tk.Label(row2_element, text='NPM', font=self.controller.font_body)
        lb2.pack(side='left', padx=(0, 40))
        e_npm = tk.Entry(row2_element, width=15)
        e_npm.pack(side='left')
        self.npm = e_npm
        self.npm.focus()
        # self.npm.insert(0, '17114454')
        self.npm.bind('<Return>', lambda _: self.login())
        # row 3 // button login
        bt_login = tk.Button(row3_element, text='LOGIN', height=2, width=8, command=self.login)
        bt_login.pack(padx=(150,0))
        bt_login.bind('<Return>', lambda _: self.login())

    def login(self):
        npm = self.npm.get()

        while True:
            # koneksi database
            with sqlite3.connect('app.db') as db:
                c = db.cursor()
            query = ('SELECT*FROM mahasiswa WHERE npm=?')
            c.execute(query,[(npm)])
            r = c.fetchall()
            if r: # user validation
                for i in r:
                    print('\n> LoginPage')
                    print('===================================================')
                    print('Login Sukses\n' + i[1] + ' berhasil masuk!')
                    print('===================================================\n')
                    ms.showinfo('Login Sukses', '' + i[1] + ' berhasil masuk!')
                    self.controller.show_page('ProfilePage')
                break
            else:
                print('\n> LoginPage')
                print('===================================================')
                print ('Login Gagal\nNPM tidak terdaftar!')
                print('===================================================\n')
                ms.showerror('Login Gagal', 'NPM tidak terdaftar!')
                self.npm.delete(0, 'end')
                self.npm.focus()
                break

class ProfilePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowPage>>", self.profileUI) # reload frame data table

    def profileUI(self, event):
        # memanggil variable dari function kelas lain (class JobPage)
        login_page = self.controller.get_page("LoginPage")
        npm = login_page.npm.get()

        # koneksi database
        with sqlite3.connect('app.db') as db:
            c = db.cursor()
        query = ('SELECT * FROM mahasiswa WHERE npm=?')
        c.execute(query,[(npm)])
        r = c.fetchall()
        for i in r:
            self.npm = i[0]
            self.nama = i[1]
            self.fakultas = i[2]
            self.jurusan = i[3]

        # master layout
        frame_body = tk.Frame(self)
        frame_body.pack(fill='both', expand=1)
        self.frame_body = frame_body
        row1 = tk.Frame(frame_body)
        row1.pack(fill='x')
        row1_element = tk.Frame(row1)
        row1_element.pack(side='left', padx=(50,0), pady=(50,0))
        row2 = tk.Frame(frame_body)
        row2.pack(fill='x', pady=(10,0))
        row2_element = tk.Frame(row2)
        row2_element.pack(side='left', padx=(50,0))
        row3 = tk.Frame(frame_body)
        row3.pack(fill='x', pady=(20,0))
        row3_element = tk.Frame(row3)
        row3_element.pack(side='left', padx=(50,0))
        row4 = tk.Frame(frame_body)
        row4.pack(fill='x', pady=(20,0))
        row4_element = tk.Frame(row4)
        row4_element.pack(side='left', padx=(50,0))
        row5 = tk.Frame(frame_body)
        row5.pack(fill='x')
        row5_element = tk.Frame(row5)
        row5_element.pack(side='left', padx=(50,0), pady=(30,0))
        # row 1 // label dan entry npm & fakultas
        lb_npm = tk.Label(row1_element, text='NPM')
        lb_npm.pack(side='left', padx=(0, 20))
        e_npm = tk.Entry(row1_element, width=8, font=self.controller.font_bold)
        e_npm.pack(side='left')
        e_npm.insert(0, self.npm)
        lb_fakultas = tk.Label(row1_element, text='Fakultas')
        lb_fakultas.pack(side='left', padx=(170, 20))
        e_fakultas = tk.Entry(row1_element, width=14, font=self.controller.font_bold)
        e_fakultas.pack(side='left')
        e_fakultas.insert(0, self.fakultas)
        # row 2 // label dan entry nama & jurusan
        lb_nama = tk.Label(row2_element, text='Nama')
        lb_nama.pack(side='left', padx=(0, 15))
        e_nama = tk.Entry(row2_element, width=18, font=self.controller.font_bold)
        e_nama.pack(side='left')
        e_nama.insert(0, self.nama)
        lb_jurusan = tk.Label(row2_element, text='Jurusan')
        lb_jurusan.pack(side='left', padx=(80, 21))
        e_jurusan = tk.Entry(row2_element, width=16, font=self.controller.font_bold)
        e_jurusan.pack(side='left')
        e_jurusan.insert(0, self.jurusan)
        # row 3 // Label
        lb1 = tk.Label(row3_element, text='MATA KULIAH YANG SUDAH DIAMBIL:', font=self.controller.font_bold)
        lb1.pack(side='left')
        # row 4 // tabel treeview buat menampilkan daftar mata kuliah yang sudah diambil user (mahasiswa)
        tree = Treeview(row4)
        self.tree = tree
        tree['columns'] = ('kode','matkul','z')
        tree.heading('#0', text='')
        tree.column('#0', anchor='center', width=0)
        tree.heading('kode', text='Kode')
        tree.column('kode', anchor='w', width=80)
        tree.heading('matkul', text='Mata Kuliah')
        tree.column('matkul', anchor='w', width=715)
        tree.heading('z', text='')
        tree.column('z', anchor='w', width=0)
        tree.pack(side='left')
        style = ttk.Style() # styling tree with configure method
        style.configure('Treeview', font=('Helvetica Neueu', 12), rowheight=25)
        style.configure('Treeview.Heading', font=('Helvetica Neueu', 14))
        treeScroll = ttk.Scrollbar(frame_body) # tree scrollbar
        treeScroll.configure(command=tree.yview)
        treeScroll.place(x=835, y=203, height=250)
        tree.configure(yscrollcommand=treeScroll.set)
        # row 5 // button cek profesi
        bt_keluar = tk.Button(row5_element, text='KELUAR', command=self.keluar, padx=30, pady=10)
        bt_keluar.pack(side='left',padx=(0,537))
        bt_keluar.bind('<Return>', lambda _: self.keluar())
        bt_cek_profesi = tk.Button(row5_element, text='CEK PROFESI', command=self.cek_profesi, padx=30, pady=10)
        bt_cek_profesi.pack()
        bt_cek_profesi.bind('<Return>', lambda _: self.cek_profesi())

        # query untuk menampilkan mata kuliah yang sudah diambil user (mahasiswa)
        query = ('SELECT kode_matkul, nama_matkul FROM matkul WHERE kode_matkul IN (SELECT kode_matkul FROM mahasiswa_matkul_mapping where npm=?) ORDER BY nama_matkul')
        c.execute(query,[(npm)])
        r = c.fetchall()
        for i in r:
            self.tree.insert('', tk.END, values=(i[0],i[1]))

        print('> ProfilePage')
        print('Data mata kuliah yang sudah diambil user (mahasiswa) ditampilkan ke table treeview.\n')

    def keluar(self):
        self.frame_body.destroy()
        self.controller.show_page('LoginPage') # untuk pindah ke halaman LoginPage

    def cek_profesi(self):
        self.frame_body.destroy()
        self.controller.show_page('JobPage')

class JobPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.jobUI()

    def jobUI(self):
        # master layout
        frame_body = tk.Frame(self)
        frame_body.pack(fill='both', expand=1)
        row1 = tk.Frame(frame_body)
        row1.pack(fill='x')
        row1_element = tk.Frame(row1)
        row1_element.pack(side='left', padx=(50,0), pady=(50,0))
        row2 = tk.Frame(frame_body)
        row2.pack(fill='x', pady=(30,0)) #pady margin dari frame body
        row2_element = tk.Frame(row2)
        row2_element.pack(side='left', padx=(50,0))
        row3 = tk.Frame(frame_body)
        row3.pack(fill='x')
        row3_element = tk.Frame(row3)
        row3_element.pack(side='left', padx=(755,0), pady=(30,0))
        # row 1 // label
        lb1 = tk.Label(row1_element, text='Daftar Profesi', font=self.controller.font_heading)
        lb1.pack(side='left')
        # row 2 // tabel treeview buat menampilkan daftar profesi
        tree = Treeview(row2)
        self.tree = tree
        tree['columns'] = ('kode','profesi','z')
        tree.heading('#0', text='')
        tree.column('#0', anchor='center', width=0)
        tree.heading('kode', text='Kode')
        tree.column('kode', anchor='w', width=80)
        tree.heading('profesi', text='Nama Profesi')
        tree.column('profesi', anchor='w', width=715)
        tree.heading('z', text='')
        tree.column('z', anchor='w', width=0)
        tree.pack(side='left')
        style = ttk.Style() # styling tree with configure method
        style.configure('Treeview', font=('Helvetica Neueu', 12), rowheight=25)
        style.configure('Treeview.Heading', font=('Helvetica Neueu', 14))
        treeScroll = ttk.Scrollbar(frame_body) # tree scrollbar
        treeScroll.configure(command=tree.yview)
        treeScroll.place(x=835, y=138, height=250)
        tree.configure(yscrollcommand=treeScroll.set)
        tree.bind("<<TreeviewSelect>>", self.on_tree_select) # fungsi item selected on treeview
        # row 3 // button pilih
        bt_pilih = tk.Button(row3_element, text='PILIH', command=self.pilih, padx=30, pady=10)
        bt_pilih.pack()
        bt_pilih.bind('<Return>', lambda _: self.pilih())

        # koneksi database
        with sqlite3.connect('app.db') as db:
            c = db.cursor()

        # query untuk menampilkan semua data profesi dari table db
        query = ('SELECT * FROM profesi')
        c.execute(query)
        r = c.fetchall()
        for i in r:
            tree.insert('', tk.END, values=(i[0],i[1])) # menampilkan data profesi dari table db ke treeview

    def pilih(self):
        if len(self.tree.selection()) > 0: # conditional if tree item selected
            self.controller.show_page('MatkulPage') # untuk pindah ke halaman JobPage
        else:
            ms.showinfo('Pesan Kesalahan', 'Silahkan pilih salah satu profesi terlebih dahulu!')

    def on_tree_select(self, event):
        '''
        function on tree item selected storing
        into variable/attribute
        '''
        for item in self.tree.selection():
            item_text = self.tree.item(item,'values')
            kode_profesi = item_text[0] # atribut
            nama_profesi = item_text[1]
            self.kode_profesi = kode_profesi # callable atribut
            self.nama_profesi = nama_profesi

class MatkulPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowPage>>", self.matkulUI)

    def matkulUI(self, event):
        # memanggil variable dari function kelas lain
        login_page = self.controller.get_page("LoginPage")
        npm = login_page.npm.get()
        job_page = self.controller.get_page("JobPage")
        kode_profesi = job_page.kode_profesi
        nama_profesi = job_page.nama_profesi

        # master layout
        frame_body = tk.Frame(self)
        frame_body.pack(fill='both', expand=1)
        self.frame_body = frame_body
        row1 = tk.Frame(frame_body)
        row1.pack(fill='x')
        row1_element = tk.Frame(row1)
        row1_element.pack(side='left', padx=(50,0), pady=(50,0))
        row2 = tk.Frame(frame_body)
        row2.pack(fill='x', pady=(30,0))
        row2_element = tk.Frame(row2)
        row2_element.pack(side='left', padx=(50,0))
        row3 = tk.Frame(frame_body)
        row3.pack(fill='x', pady=(20,0))
        row3_element = tk.Frame(row3)
        row3_element.pack(side='left', padx=(50,0))
        row4 = tk.Frame(frame_body)
        row4.pack(fill='x')
        row4_element = tk.Frame(row4)
        row4_element.pack(side='left', padx=(535,0), pady=(100,0))
        # row 1 // label dan entry untuk menampilkan nama profesi yang dipilih
        lb1 = tk.Label(row1_element, text='PROFESI', font=self.controller.font_body)
        lb1.pack(side='left')
        e_profesi = tk.Entry(row1_element, font=self.controller.font_bold, width=25)
        e_profesi.pack(side='left', padx=(20,0))
        e_profesi.insert(0, nama_profesi)
        # row 2 // label
        lb2 = tk.Label(row2_element, text='MATA KULIAH YANG DIBUTUHKAN :', font=self.controller.font_bold)
        lb2.pack(side='left')
        # row 3 // tabel treeview untuk menampilkan mata kuliah yang dibutuhkan profesi
        tree = Treeview(row3_element)
        self.tree = tree
        tree['columns'] = ('kode','matkul','z')
        tree.heading('#0', text='')
        tree.column('#0', anchor='center', width=0)
        tree.heading('kode', text='Kode')
        tree.column('kode', anchor='w', width=80)
        tree.heading('matkul', text='Mata Kuliah')
        tree.column('matkul', anchor='w', width=715)
        tree.heading('z', text='')
        tree.column('z', anchor='w', width=0)
        tree.pack(side='left')
        style = ttk.Style()
        style.configure('Treeview', font=('Helvetica Neueu', 12), rowheight=25)
        style.configure('Treeview.Heading', font=('Helvetica Neueu', 14))
        treeScroll = ttk.Scrollbar(frame_body)
        treeScroll.configure(command=tree.yview)
        treeScroll.place(x=833, y=173, height=250)
        tree.configure(yscrollcommand=treeScroll.set)
        # row 4 // button kembali dan cek kesesuaian
        bt_back = tk.Button(row4, text='KEMBALI', command=self.kembali, padx=30, pady=10)
        bt_back.pack(side='left')
        bt_back.bind('<Return>', lambda _: self.kembali())
        bt_next = tk.Button(row4, text='CEK KESESUAIAN', command=self.cek_sesuai, padx=30, pady=10)
        bt_next.pack(side='left', padx=(15,0))
        bt_next.bind('<Return>', lambda _: self.cek_sesuai())

        # koneksi database
        with sqlite3.connect('app.db') as db:
            c = db.cursor()

        # query untuk memeriksa data matkul pada table db
        query = ('SELECT kode_matkul, nama_matkul FROM matkul WHERE kode_matkul IN (SELECT kode_matkul FROM profesi_matkul_mapping WHERE kode_profesi=?)')
        c.execute(query, [(kode_profesi)]) # kode_profesi merupakan atribut dari class JobPage
        entry = c.fetchone()

        print('> MatkulPage')

        # jika data matkul yang dibutuhkan suatu profesi tidak ditemukan dalam database
        if entry is None:
            ms.showinfo('Pesan', 'Mohon ditunggu, data sedang diproses oleh sistem!')
            # dataset SKKNI dan SAP
            data_skkni = {'DATA MODEL ADMINISTRATOR': 'data/skkni_dma.csv',
                          'SENIOR SYSTEMS ANALYST': 'data/skkni_ssa.csv',
                          'DATA ARCHITECT': 'data/skkni_da.csv',
                          'DATABASE ADMINISTRATOR': 'data/skkni_dba.csv',
                          'SENIOR OPERATIONS ANALYST': 'data/skkni_soa.csv',
                          'PEMROGRAM KEPALA (LEAD PROGRAMMER)': 'data/skkni_pk.csv',
                          'ANALIS PROGRAM (PROGRAM ANALYST)': 'data/skkni_ap.csv',
                          'PENGEMBANG WEB (WEB DEVELOPER)': 'data/skkni_pw.csv',
                          'SOFTWARE ENGINEER': 'data/skkni_se.csv',
                          'DIGITAL COMPUTER TECHNOLOGY ADVISOR': 'data/skkni_dcta.csv',
                          'NETWORK SECURITY ANALYST': 'data/skkni_nsa.csv',
                          'NETWORK ADMINISTRATOR': 'data/skkni_na.csv',
                          'SYSTEM ADMINISTRATOR': 'data/skkni_sad.csv',
                          'NETWORK DESIGNER': 'data/skkni_nd.csv',
                          'SYSTEM ANALYST': 'data/skkni_san.csv',
                          'ICTPM DEPUTY MANAGER': 'data/skkni_idm.csv',
                          'DEPUTY MANAGER ICT PROJECT MANAGEMENT': 'data/skkni_dmipm.csv',
                          'ENTERPRISE ARCHITECT': 'data/skkni_ea.csv',
                          'CYBER SECURITY ANALYST': 'data/skkni_csa.csv',
                          'IT AUDITOR': 'data/skkni_ia.csv',
                          'IT AUDITOR MADYA TEKNOLOGI INFORMASI': 'data/skkni_iamti.csv',
                          'PENGEMBANG CLOUD COMPUTING (CLOUD COMPUTING DEVELOPER)': 'data/skkni_pcc.csv',
                          'MOBILE COMPUTING UTAMA (ADVANCE MOBILE COMPUTING)': 'data/skkni_mcu.csv',
                          'WEB ANALYST': 'data/skkni_wa.csv',
                          'ERP ANALYST': 'data/skkni_ean.csv',
                          'ENTERPRISE RESOURCE PLANNING SECURITY ANALYST': 'data/skkni_erpsa.csv',
                          'ENTERPRISE RESOURCE PLANNING DATA ARCHITECT': 'data/skkni_erpda.csv',
                          'ENTERPRISE RESOURCE PLANNING (ERP) INFRASTRUCTURE ADMINISTRATOR': 'data/skkni_erpia.csv',
                          'ENTERPRISE RESOURCE PLANNING MASTER DATA ANALYST': 'data/skkni_erpmda.csv'
                          }

            data_sap = {'data/sap_ap1.csv': ('PP-011302', 'ALGORITMA DAN PEMROGRAMAN 1'),
                        'data/sap_ap2.csv': ('IT-011302', 'ALGORITMA DAN PEMROGRAMAN 2'),
                        'data/sap_apsi.csv': ('AK-011302', 'ANALISIS DAN PERANCANGAN SISTEM INFORMASI'),
                        'data/sap_aks.csv': ('AK-011303', 'ANALISIS KINERJA SISTEM'),
                        'data/sap_ep.csv': ('KK-011206', 'ETIKA DAN PROFESSIONALISME TSI'),
                        'data/sap_ga.csv': ('IT-011308', 'GRAF DAN ANALISIS ALGORITMA'),
                        'data/sap_pgk.csv': ('AK-011204', 'GRAFIK KOMPUTER DAN PENGOLAHAN CITRA'),
                        'data/sap_imk.csv': ('AK-011305', 'INTERAKSI MANUSIA DAN KOMPUTER'),
                        'data/sap_kk.csv': ('AK-011307', 'KEAMANAN KOMPUTER'),
                        'data/sap_kdm.csv': ('IT-011234', 'KONSEP DATA MINING'),
                        'data/sap_ksi.csv': ('IT-011409', 'KONSEP SISTEM INFORMASI'),
                        'data/sap_ksil.csv': ('AK-011208', 'KONSEP SISTEM INFORMASI LANJUT'),
                        'data/sap_pbw.csv': ('AK-011211', 'PEMROGRAMAN BERBASIS WEB'),
                        'data/sap_pbo.csv': ('AK-011312', 'PEMROGRAMAN BERORIENTASI OBJEK'),
                        'data/sap_pbti.csv': ('PP-011201', 'PENGANTAR BISNIS TEKNOLOGI INFORMASI'),
                        'data/sap_pok.csv': ('IT-011317', 'PENGANTAR ORGANISASI KOMPUTER'),
                        'data/sap_ptk.csv': ('IT-011318', 'PENGANTAR TEKNIK KOMPILASI'),
                        'data/sap_ptsi.csv': ('IT-011416', 'PENGANTAR TEKNOLOGI SISTEM INFORMASI'),
                        'data/sap_ppsi.csv': ('AK-011215', 'PENGELOLAAN PROYEK SISTEM INFORMASI'),
                        'data/sap_sbd1.csv': ('AK-011317', 'SISTEM BASIS DATA 1'),
                        'data/sap_sbd2.csv': ('AK-011318', 'SISTEM BASIS DATA 2'),
                        'data/sap_sbdl.csv': ('AK-011219', 'SISTEM BASIS DATA LANJUT'),
                        'data/sap_sbp.csv': ('IT-011222', 'SISTEM BERBASIS PENGETAHUAN'),
                        'data/sap_sig.csv': ('AK-011225', 'SISTEM INFORMASI GEOGRAFIS'),
                        'data/sap_sim1.csv': ('AK-011209', 'SISTEM INFORMASI MANAJEMEN 1'),
                        'data/sap_sim2.csv': ('AK-011210', 'SISTEM INFORMASI MANAJEMEN 2'),
                        'data/sap_sip.csv': ('AK-011222', 'SISTEM INFORMASI PERBANKAN'),
                        'data/sap_so.csv': ('IT-011325', 'SISTEM OPERASI'),
                        'data/sap_spk.csv': ('AK-011224', 'SISTEM PENUNJANG KEPUTUSAN'),
                        'data/sap_st.csv': ('AK-011325', 'SISTEM TERDISTRIBUSI'),
                        'data/sap_sod1.csv': ('IT-011228', 'STRUKTUR ORGANISASI DATA 1'),
                        'data/sap_sod2.csv': ('IT-011229', 'STRUKTUR ORGANISASI DATA 2'),
                        'data/sap_tpt1.csv': ('IT-011230', 'TEKNIK PEMROGRAMAN TERSTRUKTUR 1'),
                        'data/sap_tpt2.csv': ('IT-011231', 'TEKNIK PEMROGRAMAN TERSTRUKTUR 2'),
                        'data/sap_tou1.csv': ('IT-011232', 'TEORI ORGANISASI UMUM 1'),
                        'data/sap_tis.csv': ('AK-011326', 'TESTING DAN IMPLEMENTASI SISTEM')
                        }

            # proses memeriksa data SKKNI
            print('Memulai memeriksa data SKKNI untuk profesi ' +nama_profesi+ '...\n')
            for profesi, dataset_skkni in data_skkni.items():
                if nama_profesi == profesi:
                    print('-------------------------------------------------------------------------------------------')
                    print('>> Data SKKNI untuk profesi ' +nama_profesi+ ' ditemukan.')
                    print('-------------------------------------------------------------------------------------------')
                    with open(dataset_skkni, 'r', encoding="utf-8") as csv_file:
                        csv_reader = csv.reader(csv_file)
                        next(csv_reader) # skip baris kolom pertama
                        list_kw_skkni = [] # daftar kata penting SKKNI dalam bentuk list
                        for row in csv_file:
                            # preprocessing
                            usenorm = normalize()
                            text_norm = usenorm.casefolding(row)
                            text_norm = usenorm.tokenize(text_norm)
                            text_norm = usenorm.stopwords(text_norm)
                            text_norm = usenorm.stemmingNorm(text_norm, 'word')
                            list_kw_skkni.extend(text_norm)
                else:
                    print('[X] Data SKKNI untuk profesi ' + nama_profesi + ' tidak ditemukan.')

            # proses memeriksa data SAP
            print('\nMemulai memeriksa data SAP...\n')
            profesi_matkul = [] # mapping mata kuliah yang dibutuhkan profesi dalam bentuk list
            for dataset_sap, matkul in data_sap.items():
                with open(dataset_sap, 'r', encoding="utf-8") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    next(csv_reader) # skip baris kolom pertama
                    list_kw_sap = [] # daftar kata penting SAP dalam bentuk list
                    for row in csv_file:
                        # preprocessing
                        usenorm = normalize()
                        text_norm = usenorm.casefolding(row)
                        text_norm = usenorm.tokenize(text_norm)
                        text_norm = usenorm.stopwords(text_norm)
                        text_norm = usenorm.stemmingNorm(text_norm, 'word')
                        list_kw_sap.extend(text_norm)

                    # menghitung simiarity kata penting SKKNI dan SAP menggunakan jaccard
                    def jaccard_similarity(x,y):
                        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
                        union_cardinality = len(set.union(*[set(x), set(y)]))
                        return intersection_cardinality/float(union_cardinality)

                    hasil = jaccard_similarity(list_kw_skkni, list_kw_sap)
                    hasil_percent = '{0:.0%}'.format(hasil)
                    kata_sama = str(set.intersection(*[set(list_kw_skkni), set(list_kw_sap)]))

                    print('>>  Hasil similarity SKKNI profesi ' +nama_profesi+ ' dan SAP matkul ' +matkul[1]+ ' adalah...')
                    print('    ' +hasil_percent+ '\n')
                    print('>> Kata yang sama di SKKNI profesi ' +nama_profesi+ ' dan SAP matkul ' +matkul[1]+ ': ')
                    print('    ' +kata_sama+ '\n')

                    # menyimpan hasil output
                    # output = open('output.txt', 'a')
                    # output.write('>> Daftar kata penting di SKKNI untuk profesi ' + nama_profesi + '\n')
                    # output.write(str(list_kw_skkni)+ '\n\n')
                    # output.write('>> Daftar kata penting di SAP mata kuliah ' +matkul[1]+ '\n')
                    # output.write(str(list_kw_sap)+ '\n\n')
                    # output.write('>> Hasil similarity SKKNI profesi ' +nama_profesi+ ' dan SAP matkul ' +matkul[1]+ ' adalah...\n')
                    # output.write(hasil_percent+ '\n\n')
                    # output.write('>> Kata yang sama di SKKNI profesi ' +nama_profesi+ ' dan SAP matkul ' +matkul[1]+ ':\n')
                    # output.write(str(kata_sama)+ '\n\n')
                    # output.write('#####\n\n')
                    # output.close()

                # conditional penentuan mata kuliah dengan profesi
                if hasil >= 0.05:
                    profesi_matkul.append(matkul) # menambahkan data matkul dari dict ke list profesi_matkul
                    print('-------------------------------------------------------------------------------------------')
                    print('[+] Mata kuliah ' +matkul[1]+ ' dibutuhkan pada profesi ' + nama_profesi)
                    print('-------------------------------------------------------------------------------------------\n')
                else:
                    print('[X] Mata kuliah ' +matkul[1]+ ' tidak dibutuhkan pada profesi ' +nama_profesi+ '\n')

            # menghitung banyaknya mata kuliah yang dibutuhkan profesi bersangkutan
            jmlmatkul = str(len(profesi_matkul))
            print('Mata kuliah yang dibutuhkan profesi ' +nama_profesi+ ' sebanyak ' +jmlmatkul+ ' mata kuliah.\n')

            # menambahkan data dari list profesi_matkul ke database
            for i in profesi_matkul:
                # koneksi database
                with sqlite3.connect('app.db') as db:
                    c = db.cursor()
                # insert data mata kuliah yang dibutuhkan profesi ke database
                c.execute("INSERT OR IGNORE INTO profesi_matkul_mapping (kode_profesi, kode_matkul) VALUES(?, ?)", (kode_profesi, i[0]) )
                db.commit()
                tree.insert('', tk.END, values=((i[0]),(i[1])))
            print('Data mata kuliah telah ditambahkan ke database table matkul')
            print('Data mata kuliah yang dibutuhkan profesi telah ditambahkan ke database table profesi_matkul_mapping\n')

        # jika data matkul yang dibutuhkan suatu profesi ditemukan dalam database
        else:
            print('Data untuk profesi ' + nama_profesi + ' ditemukan!\n')
            # query untuk menampilkan data matkul
            query = ('SELECT kode_matkul, nama_matkul FROM matkul WHERE kode_matkul IN (SELECT kode_matkul FROM profesi_matkul_mapping WHERE kode_profesi=?) ORDER BY nama_matkul')
            c.execute(query, [(kode_profesi)])
            r = c.fetchall()
            for i in r:
                tree.insert('', tk.END, values=(i[0],i[1]))

        print('Data ditampilkan ke table treeview.\n')

    def kembali(self):
        self.frame_body.destroy()
        self.controller.show_page('JobPage')

    def cek_sesuai(self):
        # memanggil variable dari function kelas lain
        login_page = self.controller.get_page("LoginPage")
        npm = login_page.npm.get()
        job_page = self.controller.get_page("JobPage")
        kode_profesi = job_page.kode_profesi
        nama_profesi = job_page.nama_profesi

        # koneksi database
        with sqlite3.connect('app.db') as db:
            c = db.cursor()

        # query untuk menarik data di mahasiswa_matkul_mapping
        query = ('SELECT kode_matkul, nama_matkul FROM matkul WHERE kode_matkul IN (SELECT kode_matkul FROM mahasiswa_matkul_mapping WHERE npm=?) ORDER BY matkul.kode_matkul')
        c.execute(query,[(npm)])
        r = c.fetchall()
        mahasiswa_matkul = [] # list baru untuk storing data dari table mahasiswa_matkul_mapping
        for i in r:
            mahasiswa_matkul.append(i)

        # query untuk menarik data di profesi_matkul_mapping
        query = ('SELECT kode_matkul, nama_matkul FROM matkul WHERE kode_matkul IN (SELECT kode_matkul FROM profesi_matkul_mapping WHERE kode_profesi=?) ORDER BY matkul.kode_matkul')
        c.execute(query, [(kode_profesi)])
        s = c.fetchall()
        profesi_matkul = [] # list baru untuk storing data dari table profesi_matkul_mapping
        for i in s:
            profesi_matkul.append(i)

        # memeriksa kesesuaian / kesamaan data mapping
        intersec_matkul_mahasiswa_profesi = set.intersection(*[set(mahasiswa_matkul), set(profesi_matkul)])
        if set(intersec_matkul_mahasiswa_profesi) == set(profesi_matkul):
            ms.showinfo('Hasil', 'Mata kuliah yang Anda ambil sudah cukup\ndengan mata kuliah yang dibutuhkan profesi ' +nama_profesi+ '\n\nKlik "OK" untuk kembali ke halaman profil.')
            print('Mata kuliah yang diambil sudah cukup dengan mata kuliah yang dibutuhkan profesi ' +nama_profesi+ '\n')
            self.frame_body.destroy()
            self.controller.show_page('ProfilePage')
        else:
            print('Mata kuliah yang sudah diambil mahasiswa:')
            print('===============================================================')
            for i in mahasiswa_matkul:
                print (i)
            print('\n')
            print('Mata kuliah yang dibutuhkan profesi ' +nama_profesi+ ':')
            print('===============================================================')
            for i in mahasiswa_matkul:
                print (i)
            print('\n')
            ms.showerror('Hasil', 'Mata kuliah yang Anda ambil belum cukup\ndengan mata kuliah yang dibutuhkan profesi ' +nama_profesi+ '\n\nKlik "OK" untuk melihat rekomendasi.')
            print('Mata kuliah yang diambil belum cukup dengan mata kuliah yang dibutuhkan profesi ' +nama_profesi+ '\n')
            print('Mata kuliah yang belum diambil:')
            for c in profesi_matkul:
                if c not in mahasiswa_matkul:
                    print (c)
            print('\n')
            self.frame_body.destroy()
            self.controller.show_page('RecPage')

class RecPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowPage>>", self.recUI)

    def recUI(self, event):
        # memanggil variable dari function kelas lain
        login_page = self.controller.get_page("LoginPage")
        npm = login_page.npm.get()
        job_page = self.controller.get_page("JobPage")
        kode_profesi = job_page.kode_profesi
        nama_profesi = job_page.nama_profesi

        # master layout
        frame_body = tk.Frame(self)
        frame_body.pack(fill='both', expand=1)
        self.frame_body = frame_body
        row1 = tk.Frame(frame_body)
        row1.pack(fill='x')
        row1_element = tk.Frame(row1)
        row1_element.pack(side='left', padx=(50,0), pady=(50,0))
        row2 = tk.Frame(frame_body)
        row2.pack(fill='x', pady=(10,0))
        row2_element = tk.Frame(row2)
        row2_element.pack(side='left', padx=(50,0))
        row3 = tk.Frame(frame_body)
        row3.pack(fill='x', pady=(20,0))
        row3_element = tk.Frame(row3)
        row3_element.pack(side='left', padx=(50,0))
        row4 = tk.Frame(frame_body)
        row4.pack(fill='x', pady=(20,0))
        row4_element = tk.Frame(row4)
        row4_element.pack(side='left', padx=(50,0))
        row5 = tk.Frame(frame_body)
        row5.pack(fill='x')
        row5_element = tk.Frame(row5)
        row5_element.pack(side='left', padx=(587,0), pady=(30,0))
        # row 1 // label
        lb1 = tk.Label(row1_element, text='Rekomendasi', font=self.controller.font_heading)
        lb1.pack(side='left')
        # row 2 // label
        lb1 = tk.Label(row2_element, text='Berikut rekomendasi mata kuliah yang harus diambil.', font=self.controller.font_body)
        lb1.pack(side='left')
        # row 3 // label
        lb2 = tk.Label(row3_element, text='MATA KULIAH YANG BELUM ANDA AMBIL UNTUK PROFESI', font=self.controller.font_bold)
        lb2.pack(side='left')
        e_profesi = tk.Entry(row3_element, font=self.controller.font_bold, width=25)
        e_profesi.pack(side='left', padx=(10,0))
        e_profesi.insert(0, nama_profesi)
        # row 4 // tabel treeview untuk menampilkan rekomendasi mata kuliah yang harus diambil
        tree = Treeview(row4)
        self.tree = tree
        tree['columns'] = ('kode','matkul','z')
        tree.heading('#0', text='')
        tree.column('#0', anchor='center', width=0)
        tree.heading('kode', text='Kode')
        tree.column('kode', anchor='w', width=80)
        tree.heading('matkul', text='Mata Kuliah')
        tree.column('matkul', anchor='w', width=715)
        tree.heading('z', text='')
        tree.column('z', anchor='w', width=0)
        tree.pack(side='left')
        style = ttk.Style()
        style.configure('Treeview', font=('Helvetica Neueu', 12), rowheight=25)
        style.configure('Treeview.Heading', font=('Helvetica Neueu', 14))
        treeScroll = ttk.Scrollbar(frame_body)
        treeScroll.configure(command=tree.yview)
        treeScroll.place(x=833, y=210, height=250)
        tree.configure(yscrollcommand=treeScroll.set)
        # row 5 // button kembali
        bt_kembali = tk.Button(row5_element, text='KEMBALI KE HALAMAN PROFIL', command=self.kembali, padx=30, pady=10)
        bt_kembali.pack()
        bt_kembali.bind('<Return>', lambda _: self.kembali())

        # koneksi database
        with sqlite3.connect('app.db') as db:
            c = db.cursor()

        # query untuk menampilkan mata kuliah yang belum diambil user (mahasiswa)
        print('> RecPage')
        query = ('SELECT DISTINCT matkul.kode_matkul, matkul.nama_matkul FROM matkul, profesi_matkul_mapping WHERE matkul.kode_matkul = profesi_matkul_mapping.kode_matkul AND profesi_matkul_mapping.kode_profesi=? AND profesi_matkul_mapping.kode_matkul NOT IN (SELECT mahasiswa_matkul_mapping.kode_matkul FROM mahasiswa_matkul_mapping WHERE mahasiswa_matkul_mapping.npm=?) ORDER BY matkul.nama_matkul')
        c.execute(query, [(kode_profesi),(npm)])
        r = c.fetchall()
        for i in r:
            tree.insert('', tk.END, values=(i[0],i[1]))
        print('Data rekomendasi mata kuliah yang harus diambil ditampilkan ke table treeview.\n')

    def kembali(self):
        self.frame_body.destroy()
        self.controller.show_page('ProfilePage')

if __name__ == '__main__':
    root = App()
    root.mainloop()
