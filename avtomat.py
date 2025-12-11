import csv
import uuid
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

CSV_HEADERS = ["id", "name", "category", "quantity", "price", "location", "created_at"]


def gen_id():
    return uuid.uuid4().hex[:8]


class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory — Облік товарів")
        self.geometry("1000x600")
        self.minsize(800, 450)

        self.records = []  
        self.current_file = None

        self._build_ui()
        self._bind_events()
        self.sort_state = {col: False for col in ("id", "name", "category", "quantity", "price", "location")}

    def _build_ui(self):
        
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Відкрити...", command=self.load_csv)
        filemenu.add_command(label="Зберегти", command=self.save_csv)
        filemenu.add_command(label="Зберегти як...", command=self.save_csv_as)
        filemenu.add_separator()
        filemenu.add_command(label="Вийти", command=self.quit)
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.config(menu=menubar)

        
        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=6, pady=6)

        ttk.Label(top, text="Пошук:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=(4, 6), fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", lambda e: self.filter_view())

        btn_clear_search = ttk.Button(top, text="Очистити пошук", command=self._clear_search)
        btn_clear_search.pack(side=tk.LEFT, padx=4)

        
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0,6))

        
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=3)

        columns = ("id", "name", "category", "quantity", "price", "location")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", selectmode="browse")
        for c in columns:
            self.tree.heading(c, text=c.capitalize(), command=lambda _c=c: self.sort_by(_c))
            self.tree.column(c, anchor=tk.W, width=100, stretch=True)

        vsb = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(left_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        left_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)

       
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)

        form_labels = [
            ("id", "ID (залишити пустим, щоб згенерувати)"),
            ("name", "Назва *"),
            ("category", "Категорія *"),
            ("quantity", "Кількість *"),
            ("price", "Ціна *"),
            ("location", "Місце зберігання"),
        ]

        self.entries = {}
        for i, (field, label) in enumerate(form_labels):
            ttk.Label(right_frame, text=label).grid(row=i, column=0, sticky="w", padx=4, pady=(6 if i==0 else 2))
            var = tk.StringVar()
            ent = ttk.Entry(right_frame, textvariable=var)
            ent.grid(row=i, column=1, sticky="ew", padx=4, pady=(6 if i==0 else 2))
            right_frame.columnconfigure(1, weight=1)
            self.entries[field] = (ent, var)

       
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=len(form_labels), column=0, columnspan=2, pady=8)

        ttk.Button(btn_frame, text="Додати", command=self.add_record).grid(row=0, column=0, padx=4)
        ttk.Button(btn_frame, text="Оновити", command=self.update_record).grid(row=0, column=1, padx=4)
        ttk.Button(btn_frame, text="Видалити", command=self.delete_record).grid(row=0, column=2, padx=4)
        ttk.Button(btn_frame, text="Очистити форму", command=self.clear_form).grid(row=0, column=3, padx=4)

       
        self.status_var = tk.StringVar(value="Готово")
        status = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status.pack(side=tk.BOTTOM, fill=tk.X)

    def _bind_events(self):
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind('<Double-1>', lambda e: self.on_tree_double_click())
        
        self.bind('<Control-s>', lambda e: self.save_csv())
        self.bind('<Control-o>', lambda e: self.load_csv())

   
    def _set_status(self, text, error=False):
        self.status_var.set(text)
       

    def _clear_search(self):
        self.search_var.set("")
        self.filter_view()

    def _read_form(self):
        data = {}
        for field, (ent, var) in self.entries.items():
            data[field] = var.get().strip()
        return data

    def _validate(self, data, check_id_unique=True, current_id=None):
        """Return (valid:bool, errors:dict)
        errors: field -> message
        """
        errors = {}
       
        if not data.get('name'):
            errors['name'] = 'Назва не може бути пустою'
        if not data.get('category'):
            errors['category'] = 'Категорія не може бути пустою'
       
        q = data.get('quantity', '')
        try:
            if q == '':
                raise ValueError('')
            qnum = int(q)
            if qnum < 0:
                raise ValueError('')
        except Exception:
            errors['quantity'] = 'Кількість має бути цілим числом >= 0'
        
        p = data.get('price', '')
        if p == '':
            errors['price'] = 'Ціна не може бути пустою'
        else:
            p_fixed = p.replace(',', '.').strip()
            try:
                pf = float(p_fixed)
                if pf < 0:
                    raise ValueError()
            except Exception:
                errors['price'] = 'Ціна має бути числом >= 0'
        
        idv = data.get('id')
        if idv == '':
            pass 
        else:
            if check_id_unique:
                for r in self.records:
                    if r['id'] == idv and (current_id is None or current_id != idv):
                        errors['id'] = 'ID має бути унікальним'
                        break
        return (len(errors) == 0, errors)

    def _highlight_errors(self, errors):
      
        for field, (ent, var) in self.entries.items():
            if field in errors:
                ent.configure(background='#ffcccc')
            else:
                try:
                    ent.configure(background='white')
                except Exception:
                    pass
       
        if errors:
            first = next(iter(errors.values()))
            self._set_status(f"Помилка: {first}")
        else:
            self._set_status('Готово')

    def _normalize_record(self, raw):
        rec = {}
        rec['id'] = raw.get('id') or gen_id()
        rec['name'] = raw.get('name','')
        rec['category'] = raw.get('category','')
      
        try:
            rec['quantity'] = str(int(raw.get('quantity') or 0))
        except Exception:
            rec['quantity'] = '0'
        price_raw = raw.get('price','')
        try:
            price = float(str(price_raw).replace(',','.'))
            rec['price'] = f"{price:.2f}"
        except Exception:
            rec['price'] = '0.00'
        rec['location'] = raw.get('location','')
        rec['created_at'] = raw.get('created_at') or datetime.now().isoformat(sep=' ', timespec='seconds')
        return rec

    
    def add_record(self):
        raw = self._read_form()
        valid, errors = self._validate(raw, check_id_unique=True)
        self._highlight_errors(errors)
        if not valid:
            return
        rec = self._normalize_record(raw)
        self.records.append(rec)
        self._insert_tree(rec)
        self.clear_form()
        self._set_status('Додано запис')

    def update_record(self):
        sel = self._selected_item()
        if not sel:
            self._set_status('Оберіть запис для оновлення')
            return
        raw = self._read_form()
        valid, errors = self._validate(raw, check_id_unique=True, current_id=sel['id'])
        self._highlight_errors(errors)
        if not valid:
            return
        rec = self._normalize_record(raw)
       
        for i, r in enumerate(self.records):
            if r['id'] == sel['id']:
                
                rec['created_at'] = r.get('created_at', rec['created_at'])
                self.records[i] = rec
                break
       
        for item in self.tree.get_children():
            if self.tree.set(item, 'id') == sel['id']:
                self.tree.item(item, values=(rec['id'], rec['name'], rec['category'], rec['quantity'], rec['price'], rec['location']))
                break
        self._set_status('Оновлено запис')

    def delete_record(self):
        sel = self._selected_item()
        if not sel:
            self._set_status('Оберіть запис для видалення')
            return
        if not messagebox.askyesno('Підтвердження', f"Видалити запис {sel['id']} — {sel['name']}?"):
            return
       
        self.records = [r for r in self.records if r['id'] != sel['id']]
        
        for item in self.tree.get_children():
            if self.tree.set(item, 'id') == sel['id']:
                self.tree.delete(item)
                break
        self.clear_form()
        self._set_status('Видалено запис')

    def clear_form(self):
        for ent, var in self.entries.values():
            var.set('')
            try:
                ent.configure(background='white')
            except Exception:
                pass
        self.tree.selection_remove(self.tree.selection())
        self._set_status('Форма очищена')

    def _selected_item(self):
        sel = self.tree.selection()
        if not sel:
            return None
        item = sel[0]
        values = self.tree.item(item, 'values')
       
        return {"id": values[0], "name": values[1], "category": values[2], "quantity": values[3], "price": values[4], "location": values[5]}

    def on_tree_select(self, event):
        sel = self._selected_item()
        if not sel:
            return
      
        for field in ['id','name','category','quantity','price','location']:
            ent, var = self.entries[field]
            var.set(sel[field])
        self._set_status(f"Вибрано {sel['id']}")

    def on_tree_double_click(self):
        
        pass

    def _insert_tree(self, rec):
        self.tree.insert('', tk.END, values=(rec['id'], rec['name'], rec['category'], rec['quantity'], rec['price'], rec['location']))

 
    def load_csv(self, event=None):
        path = filedialog.askopenfilename(filetypes=[('CSV files','*.csv'), ('All files','*.*')])
        if not path:
            return
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                if any(h not in reader.fieldnames for h in CSV_HEADERS):
                    messagebox.showerror('Помилка', 'Файл CSV не має правильних заголовків')
                    return
                rows = []
                for r in reader:
                   
                    row = {k: r.get(k, '').strip() for k in CSV_HEADERS}
                    rows.append(self._normalize_record(row))
        except Exception as e:
            messagebox.showerror('Помилка при читанні файлу', str(e))
            return
        self.records = rows
        self._refresh_tree()
        self.current_file = path
        self._set_status(f'Завантажено {len(rows)} записів з {os.path.basename(path)}')

    def save_csv(self, event=None):
        if not self.current_file:
            return self.save_csv_as()
        try:
            with open(self.current_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
                writer.writeheader()
                for r in self.records:
                    writer.writerow(r)
        except Exception as e:
            messagebox.showerror('Помилка при збереженні', str(e))
            return
        self._set_status(f'Збережено {len(self.records)} записів у {os.path.basename(self.current_file)}')

    def save_csv_as(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files','*.csv'), ('All files','*.*')])
        if not path:
            return
        self.current_file = path
        return self.save_csv()

    def _refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for r in self.records:
            self._insert_tree(r)

    
    def filter_view(self):
        q = self.search_var.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        for r in self.records:
            if q == '' or q in r['name'].lower() or q in r['category'].lower():
                self._insert_tree(r)
        self._set_status(f'Показано {len(self.tree.get_children())} з {len(self.records)}')

    def sort_by(self, column):
        
        reverse = self.sort_state.get(column, False)
        try:
            if column in ('quantity', 'price'):
                keyfunc = lambda r: float(r[column]) if r[column] != '' else 0.0
            else:
                keyfunc = lambda r: r[column].lower()
            self.records.sort(key=keyfunc, reverse=reverse)
           
            self.sort_state[column] = not reverse
            self._refresh_tree()
            self._set_status(f'Сортування за {column} ({"спадання" if reverse else "зростання"})')
        except Exception as e:
            self._set_status('Не вдалося відсортувати: ' + str(e))


if __name__ == '__main__':
    app = InventoryApp()
    app.mainloop()
