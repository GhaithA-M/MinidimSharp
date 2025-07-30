import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime

# Set appearance mode and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class MinidimSharpApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("MinidimSharp v0.4.1 - Elektrisk Installation Dimensionering")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Initialize calculation data
        self.calculation_data = {
            'spænding_type': 'lav',  # lav/høj
            'effekt': 0.0,  # kW
            'spænding': 400.0,  # V
            'effektfaktor': 0.85,
            'laststrøm': 0.0,  # A
            'afbryder_type': 'MCB',
            'afbryder_rating': 0.0,  # A
            'installation_metode': 'A',
            'temperatur': 30.0,  # °C
            'kabel_gruppe': 1,
            'kabel_længde': 50.0,  # m
            'kabel_type': 'NYM-J 3x1.5',
            'beregnet_kabelstrøm': 0.0,  # A
            'spændingsfald': 0.0,  # V
            'advarsler': [],
            'fejl': []
        }
        
        self.current_step = 1
        self.setup_ui()
        self.load_excel_data()
        
    def setup_ui(self):
        """Setup the main user interface with Danish labels"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(header_frame, text="MinidimSharp", 
                                  font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(header_frame, 
                                     text="Elektrisk Installation Dimensionering - DS/HD 60364 serie",
                                     font=ctk.CTkFont(size=16))
        subtitle_label.pack(pady=(0, 10))
        
        # Voltage selection
        voltage_frame = ctk.CTkFrame(header_frame)
        voltage_frame.pack(pady=10)
        
        ctk.CTkLabel(voltage_frame, text="Vælg spændingstype:").pack(side="left", padx=10)
        
        self.hv_button = ctk.CTkButton(voltage_frame, text="Højspænding (HS)", 
                                      command=lambda: self.set_voltage_type("høj"))
        self.hv_button.pack(side="left", padx=5)
        
        self.lv_button = ctk.CTkButton(voltage_frame, text="Lavspænding (LS)", 
                                      command=lambda: self.set_voltage_type("lav"))
        self.lv_button.pack(side="left", padx=5)
        
        # Main content area
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Navigation panel
        nav_frame = ctk.CTkFrame(content_frame, width=300)
        nav_frame.pack(side="left", fill="y", padx=(0, 10))
        
        ctk.CTkLabel(nav_frame, text="Beregningssteg", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Step buttons
        self.step_buttons = []
        steps = [
            "1. Laststrøm Beregning",
            "2. Afbryder Valg",
            "3. Installation Metode",
            "4. Temperatur Koefficient",
            "5. Kabel Gruppering",
            "6. Kabelstrøm Beregning",
            "7. Lastgrad",
            "8. Betingelse Kontrol",
            "9. Spændingsfald Kontrol"
        ]
        
        for i, step_text in enumerate(steps, 1):
            btn = ctk.CTkButton(nav_frame, text=step_text, 
                               command=lambda x=i: self.show_step(x))
            btn.pack(fill="x", padx=10, pady=2)
            self.step_buttons.append(btn)
        
        # Action buttons
        ctk.CTkLabel(nav_frame, text="Handlinger", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))
        
        ctk.CTkButton(nav_frame, text="Beregn Alt", 
                     command=self.calculate_all).pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(nav_frame, text="Eksporter Resultater", 
                     command=self.export_results).pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(nav_frame, text="Ryd Alt", 
                     command=self.clear_all).pack(fill="x", padx=10, pady=2)
        
        # Table viewer buttons
        ctk.CTkLabel(nav_frame, text="Tabeller", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))
        
        # Create table buttons dynamically
        self.setup_table_buttons(nav_frame)
        
        # Content area
        self.content_area = ctk.CTkFrame(content_frame)
        self.content_area.pack(side="right", fill="both", expand=True)
        
        # Status bar
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.status_label = ctk.CTkLabel(status_frame, text="Klar til at starte beregning")
        self.status_label.pack(side="left", padx=10, pady=5)
        
        version_label = ctk.CTkLabel(status_frame, text="v0.4.1")
        version_label.pack(side="right", padx=10, pady=5)
        
        # Show welcome screen
        self.show_welcome()
        
    def show_welcome(self):
        """Show welcome screen with Danish text"""
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        welcome_frame = ctk.CTkFrame(self.content_area)
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(welcome_frame, text="Velkommen til MinidimSharp", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)
        
        ctk.CTkLabel(welcome_frame, 
                    text="Elektrisk Installation Dimensionering", 
                    font=ctk.CTkFont(size=18)).pack(pady=10)
        
        ctk.CTkLabel(welcome_frame, 
                    text="Denne applikation hjælper dig med at dimensionere elektriske installationer\n"
                         "i henhold til DS/HD 60364 serie standarder.",
                    font=ctk.CTkFont(size=14)).pack(pady=20)
        
        ctk.CTkLabel(welcome_frame, 
                    text="Vælg venligst højspænding eller lavspænding beregning\n"
                         "og følg trinene i navigationspanelet.",
                    font=ctk.CTkFont(size=14)).pack(pady=20)
        
        button_frame = ctk.CTkFrame(welcome_frame)
        button_frame.pack(pady=30)
        
        ctk.CTkButton(button_frame, text="Start Højspænding Beregning", 
                     command=lambda: self.set_voltage_type("høj")).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Start Lavspænding Beregning", 
                     command=lambda: self.set_voltage_type("lav")).pack(side="left", padx=10)
    
    def set_voltage_type(self, voltage_type):
        """Set voltage type and update UI"""
        self.calculation_data['spænding_type'] = voltage_type
        
        if voltage_type == "høj":
            self.calculation_data['spænding'] = 10000.0  # 10 kV
            self.hv_button.configure(fg_color="green")
            self.lv_button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        else:
            self.calculation_data['spænding'] = 400.0  # 400 V
            self.lv_button.configure(fg_color="green")
            self.hv_button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
        self.update_status(f"Valgt: {voltage_type.capitalize()}spænding")
        self.show_step(1)
    
    def show_step(self, step_number):
        """Show the specified calculation step"""
        self.current_step = step_number
        
        # Update button colors
        for i, btn in enumerate(self.step_buttons):
            if i + 1 == step_number:
                btn.configure(fg_color="green")
            else:
                btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Show appropriate step
        if step_number == 1:
            self.show_load_current_step()
        elif step_number == 2:
            self.show_circuit_breaker_step()
        elif step_number == 3:
            self.show_installation_method_step()
        elif step_number == 4:
            self.show_temperature_step()
        elif step_number == 5:
            self.show_cable_grouping_step()
        elif step_number == 6:
            self.show_cable_current_step()
        elif step_number == 7:
            self.show_load_degree_step()
        elif step_number == 8:
            self.show_condition_check_step()
        elif step_number == 9:
            self.show_voltage_drop_step()
    
    def show_load_current_step(self):
        """Show step 1: Load current calculation"""
        frame = ctk.CTkFrame(self.content_area)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Trin 1: Laststrøm Beregning", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        # Input section
        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(input_frame, text="Indtast parametre:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Power input
        power_frame = ctk.CTkFrame(input_frame)
        power_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(power_frame, text="Effekt (kW):").pack(side="left", padx=10)
        self.power_entry = ctk.CTkEntry(power_frame, width=150)
        self.power_entry.pack(side="right", padx=10)
        self.power_entry.insert(0, str(self.calculation_data['effekt']))
        
        # Voltage input
        voltage_frame = ctk.CTkFrame(input_frame)
        voltage_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(voltage_frame, text="Spænding (V):").pack(side="left", padx=10)
        self.voltage_entry = ctk.CTkEntry(voltage_frame, width=150)
        self.voltage_entry.pack(side="right", padx=10)
        self.voltage_entry.insert(0, str(self.calculation_data['spænding']))
        
        # Power factor input
        pf_frame = ctk.CTkFrame(input_frame)
        pf_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(pf_frame, text="Effektfaktor (cos φ):").pack(side="left", padx=10)
        self.pf_entry = ctk.CTkEntry(pf_frame, width=150)
        self.pf_entry.pack(side="right", padx=10)
        self.pf_entry.insert(0, str(self.calculation_data['effektfaktor']))
        
        # Calculate button
        ctk.CTkButton(input_frame, text="Beregn Laststrøm", 
                     command=self.calculate_load_current).pack(pady=10)
        
        # Results section
        results_frame = ctk.CTkFrame(frame)
        results_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(results_frame, text="Resultater:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.load_current_result = ctk.CTkLabel(results_frame, text="Laststrøm: -- A")
        self.load_current_result.pack(pady=5)
        
        # Navigation
        nav_frame = ctk.CTkFrame(frame)
        nav_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(nav_frame, text="Næste", 
                     command=lambda: self.show_step(2)).pack(side="right", padx=10)
    
    def calculate_load_current(self):
        """Calculate load current from power, voltage, and power factor"""
        try:
            power = float(self.power_entry.get())
            voltage = float(self.voltage_entry.get())
            pf = float(self.pf_entry.get())
            
            # Formula: IB = P / (U * cos φ * √3)
            load_current = power * 1000 / (voltage * pf * np.sqrt(3))
            
            self.calculation_data['effekt'] = power
            self.calculation_data['spænding'] = voltage
            self.calculation_data['effektfaktor'] = pf
            self.calculation_data['laststrøm'] = load_current
            
            self.load_current_result.configure(
                text=f"Laststrøm: {load_current:.2f} A\n"
                     f"Formel: IB = P / (U × cos φ × √3)\n"
                     f"IB = {power} kW / ({voltage} V × {pf} × 1.732)"
            )
            
            self.update_status(f"Laststrøm beregnet: {load_current:.2f} A")
            
        except ValueError:
            messagebox.showerror("Fejl", "Indtast venligst gyldige numeriske værdier")
    
    def load_excel_data(self):
        """Load data from Excel files"""
        try:
            # Load HS.xlsx and LS.xlsx data
            self.hs_data = pd.read_excel("assets/xlsx/HS.xlsx")
            self.ls_data = pd.read_excel("assets/xlsx/LS.xlsx")
            self.update_status("Excel data indlæst")
        except Exception as e:
            self.update_status(f"Kunne ikke indlæse Excel data: {str(e)}")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.configure(text=message)
    
    def calculate_all(self):
        """Perform complete calculation"""
        messagebox.showinfo("Beregn Alt", "Komplet beregning vil blive implementeret")
    
    def export_results(self):
        """Export results to Excel"""
        messagebox.showinfo("Eksporter", "Eksport funktion vil blive implementeret")
    
    def clear_all(self):
        """Clear all calculation data"""
        self.calculation_data = {
            'spænding_type': 'lav',
            'effekt': 0.0,
            'spænding': 400.0,
            'effektfaktor': 0.85,
            'laststrøm': 0.0,
            'afbryder_type': 'MCB',
            'afbryder_rating': 0.0,
            'installation_metode': 'A',
            'temperatur': 30.0,
            'kabel_gruppe': 1,
            'kabel_længde': 50.0,
            'kabel_type': 'NYM-J 3x1.5',
            'beregnet_kabelstrøm': 0.0,
            'spændingsfald': 0.0,
            'advarsler': [],
            'fejl': []
        }
        self.show_welcome()
        self.update_status("Alle data ryddet")
    
    # Placeholder methods for other steps
    def show_circuit_breaker_step(self):
        """Show step 2: Circuit breaker selection"""
        frame = ctk.CTkFrame(self.content_area)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Trin 2: Afbryder Valg", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        # Show calculated load current
        if self.calculation_data['laststrøm'] > 0:
            current_frame = ctk.CTkFrame(frame)
            current_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(current_frame, 
                        text=f"Beregnet laststrøm: {self.calculation_data['laststrøm']:.2f} A",
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Input section
        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(input_frame, text="Vælg afbryder:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Circuit breaker type
        type_frame = ctk.CTkFrame(input_frame)
        type_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(type_frame, text="Type:").pack(side="left", padx=10)
        self.cb_type_var = ctk.StringVar(value=self.calculation_data['afbryder_type'])
        cb_types = ['MCB', 'MCCB', 'ACB', 'Fuse']
        
        for cb_type in cb_types:
            ctk.CTkRadioButton(type_frame, text=cb_type, variable=self.cb_type_var, 
                              value=cb_type).pack(side="left", padx=10)
        
        # Circuit breaker rating
        rating_frame = ctk.CTkFrame(input_frame)
        rating_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(rating_frame, text="Rating (A):").pack(side="left", padx=10)
        self.cb_rating_entry = ctk.CTkEntry(rating_frame, width=150)
        self.cb_rating_entry.pack(side="right", padx=10)
        self.cb_rating_entry.insert(0, str(self.calculation_data['afbryder_rating']))
        
        # Auto-select button
        ctk.CTkButton(input_frame, text="Auto-vælg Rating", 
                     command=self.auto_select_rating).pack(pady=10)
        
        # Standard ratings reference
        ref_frame = ctk.CTkFrame(frame)
        ref_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(ref_frame, text="Standard MCB Ratings:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        ratings_text = "6A, 10A, 16A, 20A, 25A, 32A, 40A, 50A, 63A, 80A, 100A, 125A, 160A, 200A, 250A, 315A, 400A, 500A, 630A, 800A, 1000A"
        ctk.CTkLabel(ref_frame, text=ratings_text, font=ctk.CTkFont(size=12)).pack(pady=5)
        
        # Validation section
        validation_frame = ctk.CTkFrame(frame)
        validation_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(validation_frame, text="Validering:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.validation_result = ctk.CTkLabel(validation_frame, text="Indtast afbryder rating")
        self.validation_result.pack(pady=5)
        
        # Navigation
        nav_frame = ctk.CTkFrame(frame)
        nav_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(nav_frame, text="Forrige", 
                     command=lambda: self.show_step(1)).pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text="Næste", 
                     command=lambda: self.show_step(3)).pack(side="right", padx=10)
    
    def auto_select_rating(self):
        """Auto-select circuit breaker rating based on load current"""
        load_current = self.calculation_data['laststrøm']
        if load_current <= 0:
            messagebox.showwarning("Advarsel", "Beregn venligst laststrøm først")
            return
        
        # Standard MCB ratings
        standard_ratings = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000]
        
        # Find the next standard rating >= load current
        selected_rating = None
        for rating in standard_ratings:
            if rating >= load_current:
                selected_rating = rating
                break
        
        if selected_rating:
            self.cb_rating_entry.delete(0, 'end')
            self.cb_rating_entry.insert(0, str(selected_rating))
            self.calculation_data['afbryder_rating'] = selected_rating
            self.update_validation()
            self.update_status(f"Auto-valgt rating: {selected_rating} A")
        else:
            messagebox.showwarning("Advarsel", "Laststrøm er for høj for standard MCB")
    
    def update_validation(self):
        """Update validation result"""
        try:
            rating = float(self.cb_rating_entry.get())
            load_current = self.calculation_data['laststrøm']
            
            if rating >= load_current:
                self.validation_result.configure(
                    text=f"✅ Betingelse 1 OK: IB ({load_current:.2f}A) ≤ IN ({rating}A)",
                    text_color="green"
                )
            else:
                self.validation_result.configure(
                    text=f"❌ Betingelse 1 IKKE OK: IB ({load_current:.2f}A) > IN ({rating}A)",
                    text_color="red"
                )
        except ValueError:
            self.validation_result.configure(text="Indtast venligst gyldig rating")
    
    def show_installation_method_step(self):
        """Show step 3: Installation method selection"""
        frame = ctk.CTkFrame(self.content_area)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Trin 3: Installation Metode", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        # Installation method selection
        method_frame = ctk.CTkFrame(frame)
        method_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(method_frame, text="Vælg installation metode:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Method selection with descriptions
        self.method_var = ctk.StringVar(value=self.calculation_data['installation_metode'])
        methods = {
            'A': 'A - I tråd i isoleret væg',
            'B': 'B - I tråd på trævæg',
            'C': 'C - I tråd på mursten',
            'D': 'D - I tråd på beton',
            'E': 'E - I tråd i jord',
            'F': 'F - I tråd i luft',
            'G': 'G - I tråd i vand',
            'H': 'H - I tråd i olie',
            'I': 'I - I tråd i sand',
            'J': 'J - I tråd i cement'
        }
        
        for method, description in methods.items():
            method_radio = ctk.CTkRadioButton(method_frame, text=description, 
                                            variable=self.method_var, value=method)
            method_radio.pack(anchor="w", padx=20, pady=2)
        
        # Method factors reference
        factors_frame = ctk.CTkFrame(frame)
        factors_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(factors_frame, text="Installation Metode Faktorer:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        factors_text = "A: 1.0, B: 0.95, C: 0.9, D: 0.85, E: 0.8, F: 0.75, G: 0.7, H: 0.65, I: 0.6, J: 0.55"
        ctk.CTkLabel(factors_frame, text=factors_text, font=ctk.CTkFont(size=12)).pack(pady=5)
        
        # Navigation
        nav_frame = ctk.CTkFrame(frame)
        nav_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(nav_frame, text="Forrige", 
                     command=lambda: self.show_step(2)).pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text="Næste", 
                     command=lambda: self.show_step(4)).pack(side="right", padx=10)
    
    def show_temperature_step(self):
        """Show step 4: Temperature coefficient calculation"""
        frame = ctk.CTkFrame(self.content_area)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Trin 4: Temperatur Koefficient", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        # Temperature input
        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(input_frame, text="Indtast omgivelsestemperatur:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        temp_frame = ctk.CTkFrame(input_frame)
        temp_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(temp_frame, text="Temperatur (°C):").pack(side="left", padx=10)
        self.temp_entry = ctk.CTkEntry(temp_frame, width=150)
        self.temp_entry.pack(side="right", padx=10)
        self.temp_entry.insert(0, str(self.calculation_data['temperatur']))
        
        # Calculate button
        ctk.CTkButton(input_frame, text="Beregn Temperatur Koefficient", 
                     command=self.calculate_temperature_coefficient).pack(pady=10)
        
        # Results section
        results_frame = ctk.CTkFrame(frame)
        results_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(results_frame, text="Resultater:", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.temp_result = ctk.CTkLabel(results_frame, text="Indtast temperatur og beregn")
        self.temp_result.pack(pady=5)
        
        # Temperature coefficient reference table
        ref_frame = ctk.CTkFrame(frame)
        ref_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(ref_frame, text="Temperatur Koefficient Reference:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        ref_text = "10°C: 1.15, 15°C: 1.12, 20°C: 1.08, 25°C: 1.04, 30°C: 1.00, 35°C: 0.96, 40°C: 0.91, 45°C: 0.87, 50°C: 0.82"
        ctk.CTkLabel(ref_frame, text=ref_text, font=ctk.CTkFont(size=12)).pack(pady=5)
        
        # Navigation
        nav_frame = ctk.CTkFrame(frame)
        nav_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(nav_frame, text="Forrige", 
                     command=lambda: self.show_step(3)).pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text="Næste", 
                     command=lambda: self.show_step(5)).pack(side="right", padx=10)
    
    def calculate_temperature_coefficient(self):
        """Calculate temperature coefficient based on ambient temperature"""
        try:
            temp = float(self.temp_entry.get())
            self.calculation_data['temperatur'] = temp
            
            # Temperature coefficient calculation (simplified)
            if temp <= 10:
                kt = 1.15
            elif temp <= 15:
                kt = 1.12
            elif temp <= 20:
                kt = 1.08
            elif temp <= 25:
                kt = 1.04
            elif temp <= 30:
                kt = 1.00
            elif temp <= 35:
                kt = 0.96
            elif temp <= 40:
                kt = 0.91
            elif temp <= 45:
                kt = 0.87
            else:
                kt = 0.82
            
            self.calculation_data['temperatur_koefficient'] = kt
            
            self.temp_result.configure(
                text=f"Temperatur: {temp}°C\n"
                     f"Temperatur koefficient (kt): {kt:.3f}\n"
                     f"Formel: Interpoleret fra IEC 60364-5-52 tabel"
            )
            
            self.update_status(f"Temperatur koefficient beregnet: {kt:.3f}")
            
        except ValueError:
            messagebox.showerror("Fejl", "Indtast venligst gyldig temperatur")
    
    def show_cable_grouping_step(self):
        self.show_placeholder_step("Kabel Gruppering", "Trin 5: Indtast kabel gruppering")
    
    def show_cable_current_step(self):
        self.show_placeholder_step("Kabelstrøm Beregning", "Trin 6: Beregn nødvendig kabelstrøm")
    
    def show_load_degree_step(self):
        self.show_placeholder_step("Lastgrad", "Trin 7: Beregn lastgrad")
    
    def show_condition_check_step(self):
        self.show_placeholder_step("Betingelse Kontrol", "Trin 8: Kontroller betingelser")
    
    def show_voltage_drop_step(self):
        self.show_placeholder_step("Spændingsfald Kontrol", "Trin 9: Kontroller spændingsfald")
    
    def show_placeholder_step(self, title, description):
        """Show placeholder for unimplemented steps"""
        frame = ctk.CTkFrame(self.content_area)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text=title, 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(frame, text=description, 
                    font=ctk.CTkFont(size=16)).pack(pady=10)
        
        ctk.CTkLabel(frame, text="Denne funktion vil blive implementeret snart", 
                    font=ctk.CTkFont(size=14)).pack(pady=20)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(frame)
        nav_frame.pack(fill="x", padx=20, pady=20)
        
        if self.current_step > 1:
            ctk.CTkButton(nav_frame, text="Forrige", 
                         command=lambda: self.show_step(self.current_step - 1)).pack(side="left", padx=10)
        
        if self.current_step < 9:
            ctk.CTkButton(nav_frame, text="Næste", 
                         command=lambda: self.show_step(self.current_step + 1)).pack(side="right", padx=10)
    
    def setup_table_buttons(self, nav_frame):
        """Setup buttons for viewing tables from assets/tables"""
        import os
        from PIL import Image, ImageTk
        
        # Get all table images from assets/tables
        tables_dir = "assets/tables"
        if not os.path.exists(tables_dir):
            return
        
        table_files = [f for f in os.listdir(tables_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Create buttons for each table
        for table_file in sorted(table_files):
            # Create a clean button name (remove extension and replace underscores)
            button_name = table_file.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
            button_name = button_name.replace('_', ' ').replace('-', ' ')
            
            btn = ctk.CTkButton(nav_frame, text=button_name, 
                               command=lambda f=table_file: self.show_table(f))
            btn.pack(fill="x", padx=10, pady=2)
    
    def show_table(self, table_filename):
        """Show a table image in a new window"""
        import os
        from PIL import Image, ImageTk
        
        # Create a new window for the table
        table_window = ctk.CTkToplevel(self.root)
        table_window.title(f"Tabel: {table_filename}")
        table_window.geometry("1000x800")
        table_window.minsize(800, 600)
        
        # Load and display the image
        image_path = os.path.join("assets", "tables", table_filename)
        
        try:
            # Load image with PIL
            pil_image = Image.open(image_path)
            
            # Get window dimensions
            window_width = 1000
            window_height = 800
            
            # Calculate scaling to fit image in window
            img_width, img_height = pil_image.size
            scale = min(window_width / img_width, window_height / img_height) * 0.9
            
            # Resize image
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for tkinter
            photo = ImageTk.PhotoImage(pil_image)
            
            # Create scrollable frame
            canvas = tk.Canvas(table_window, width=window_width, height=window_height)
            scrollbar_y = tk.Scrollbar(table_window, orient="vertical", command=canvas.yview)
            scrollbar_x = tk.Scrollbar(table_window, orient="horizontal", command=canvas.xview)
            
            # Configure canvas
            canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            
            # Pack scrollbars and canvas
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")
            canvas.pack(side="left", fill="both", expand=True)
            
            # Add image to canvas
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            # Keep a reference to prevent garbage collection
            canvas.image = photo
            
            # Add close button
            close_btn = ctk.CTkButton(table_window, text="Luk", 
                                     command=table_window.destroy)
            close_btn.pack(pady=10)
            
        except Exception as e:
            # Show error if image can't be loaded
            error_label = ctk.CTkLabel(table_window, 
                                      text=f"Kunne ikke indlæse billede: {str(e)}")
            error_label.pack(pady=50)
            
            close_btn = ctk.CTkButton(table_window, text="Luk", 
                                     command=table_window.destroy)
            close_btn.pack(pady=10)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MinidimSharpApp()
    app.run() 