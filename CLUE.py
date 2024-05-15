import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

class ClueGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Clue Game")
        self.master.attributes("-fullscreen", True)  # Pantalla completa

        # Inicializar las variables de asesino, arma y lugar
        self.asesino = None
        self.arma = None
        self.lugar = None

        # Mostrar imágenes de bienvenida después de que la ventana principal se haya creado
        self.show_welcome_images()

    def show_welcome_images(self):
        # Cargar imágenes de bienvenida
        welcome_images = [
            Image.open("bienvenida1.jpg").resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()), Image.LANCZOS),
            Image.open("bienvenida2.jpg").resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()), Image.LANCZOS),
            Image.open("bienvenida3.jpg").resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()), Image.LANCZOS)
        ]

        # Convertir imágenes a objetos ImageTk
        welcome_images_tk = [ImageTk.PhotoImage(img) for img in welcome_images]

        # Mostrar imágenes de bienvenida durante 7 segundos cada una
        for img in welcome_images_tk:
            label = tk.Label(self.master, image=img)
            label.pack(fill="both", expand=True)
            self.master.update()
            self.master.after(500)  # Mostrar cada imagen durante 7 segundos
            label.pack_forget()  # Ocultar la imagen después de 7 segundos

        # Una vez mostradas todas las imágenes, iniciar el juego
        self.start_game()

    def start_game(self):
        # Cargar imágenes de los personajes, armas y escenarios
        self.character_images = [
            Image.open("dr_blanco.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("scarlett.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("victor.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("olivia.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("carmen.jpg").resize((100, 100), Image.LANCZOS)
        ]
        self.weapon_images = [
            Image.open("candelabro.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("veneno.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("cuchillo.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("bat.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("cuerda.jpg").resize((100, 100), Image.LANCZOS)
        ]
        self.location_images = [
            Image.open("biblioteca.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("jardin.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("salon.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("cocina.jpg").resize((100, 100), Image.LANCZOS),
            Image.open("sotano.jpg").resize((100, 100), Image.LANCZOS)
        ]

        # Nombres de personajes, armas y escenarios
        self.character_names = ["Dr. Blanco", "Scarlett", "Victor", "Olivia", "Carmen"]
        self.weapon_names = ["Candelabro", "Veneno", "Cuchillo", "Bate", "Cuerda"]
        self.location_names = ["Biblioteca", "Jardín", "Salón", "Cocina", "Sótano"]

        # Convertir imágenes a objetos ImageTk
        self.character_images_tk = [ImageTk.PhotoImage(img) for img in self.character_images]
        self.weapon_images_tk = [ImageTk.PhotoImage(img) for img in self.weapon_images]
        self.location_images_tk = [ImageTk.PhotoImage(img) for img in self.location_images]

        # Botón para reiniciar el juego
        self.restart_button = tk.Button(self.master, text="Reiniciar Juego", command=self.restart_game)
        self.restart_button.pack()

        # Botones para mostrar imágenes de personajes, armas y escenarios
        self.character_button = tk.Button(self.master, text="Mostrar Personajes", command=self.show_character_images)
        self.character_button.pack()

        self.weapon_button = tk.Button(self.master, text="Mostrar Armas", command=self.show_weapon_images)
        self.weapon_button.pack()

        self.location_button = tk.Button(self.master, text="Mostrar Escenarios", command=self.show_location_images)
        self.location_button.pack()

        # Botón para hacer una suposición
        self.make_guess_button = tk.Button(self.master, text="Hacer Suposición", command=self.make_guess)
        self.make_guess_button.pack()

        # Marco para contener los botones de imagen y etiquetas de texto
        self.image_buttons_frame = tk.Frame(self.master)
        self.image_buttons_frame.pack()

        # Registro de pistas mostradas
        self.shown_clues = {
            "personaje": {},
            "arma": {},
            "lugar": {}
        }

        # Asignar solución al iniciar el juego
        self.asesino, self.arma, self.lugar = self.asignar_solucion()

    def show_character_images(self):
        # Eliminar los botones de imágenes anteriores si existen
        self.clear_image_buttons()

        # Mostrar botones de imágenes de personajes con etiquetas de texto
        for img, name in zip(self.character_images_tk, self.character_names):
            button = tk.Button(self.image_buttons_frame, image=img, command=lambda n=name: self.show_clues("personaje", n))
            button.pack(side="left")
            label = tk.Label(self.image_buttons_frame, text=name)
            label.pack(side="left")

    def show_weapon_images(self):
        # Eliminar los botones de imágenes anteriores si existen
        self.clear_image_buttons()

        # Mostrar botones de imágenes de armas con etiquetas de texto
        for img, name in zip(self.weapon_images_tk, self.weapon_names):
            button = tk.Button(self.image_buttons_frame, image=img, command=lambda n=name: self.show_clues("arma", n))
            button.pack(side="left")
            label = tk.Label(self.image_buttons_frame, text=name)
            label.pack(side="left")

    def show_location_images(self):
        # Eliminar los botones de imágenes anteriores si existen
        self.clear_image_buttons()

        # Mostrar botones de imágenes de escenarios con etiquetas de texto
        for img, name in zip(self.location_images_tk, self.location_names):
            button = tk.Button(self.image_buttons_frame, image=img, command=lambda n=name: self.show_clues("lugar", n))
            button.pack(side="left")
            label = tk.Label(self.image_buttons_frame, text=name)
            label.pack(side="left")

    def show_clues(self, category, item_name):
        # Verificar si ya se mostró una pista para este elemento
        if item_name in self.shown_clues[category]:
            messagebox.showinfo("Pista", f"Ya se ha mostrado una pista para {item_name}.")
        else:
            # Obtener las pistas específicas para el elemento seleccionado
            if category == "personaje":
                pista = random.choice(self.pistas_personajes[item_name])
            elif category == "arma":
                pista = random.choice(self.pistas_armas[item_name])
            elif category == "lugar":
                pista = random.choice(self.pistas_lugares[item_name])

            # Mostrar la pista específica
            messagebox.showinfo("Pista", pista)
            self.shown_clues[category][item_name] = pista

    def clear_image_buttons(self):
        # Limpiar el marco de botones de imagen y etiquetas de texto
        for widget in self.image_buttons_frame.winfo_children():
            widget.destroy()

    def restart_game(self):
        # Reiniciar el juego: seleccionar aleatoriamente los personajes, armas y escenarios
        self.asesino, self.arma, self.lugar = self.asignar_solucion()

        # Mostrar mensaje con la solución asignada al reiniciar el juego
        messagebox.showinfo("Solución del juego", f"El asesino fue: {self.asesino}\nEl arma utilizada fue: {self.arma}\nEl crimen ocurrió en: {self.lugar}")

        # Aquí podrías agregar lógica adicional para reiniciar el juego

    def asignar_solucion(self):
        # Listas de personajes, armas y lugares
        personajes = ["Dr. Blanco", "Scarlett", "Victor", "Olivia", "Carmen"]
        armas = ["Candelabro", "Veneno", "Cuchillo", "Bate", "Cuerda"]
        lugares = ["Biblioteca", "Jardín", "Salón", "Cocina", "Sótano"]

        # Seleccionar aleatoriamente la solución correcta
        asesino = random.choice(personajes)
        arma = random.choice(armas)
        lugar = random.choice(lugares)

        # Generar pistas específicas para el asesino, el arma y el lugar correctos
        pista_asesino = self.generar_pistas_personajes()
        pista_arma = self.generar_pistas_armas()
        pista_lugar = self.generar_pistas_lugares()

        # Almacenar la pista específica para el asesino, el arma y el lugar correctos
        pistas_personajes = {asesino: pista_asesino}
        pistas_armas = {arma: pista_arma}
        pistas_lugares = {lugar: pista_lugar}

        # Generar pistas específicas para los personajes restantes
        for personaje in personajes:
            if personaje != asesino:
                pistas_personajes[personaje] = self.generar_pistas_personajes()

        # Generar pistas específicas para las armas restantes
        for arma_ in armas:
            if arma_ != arma:
                pistas_armas[arma_] = self.generar_pistas_armas()

        # Generar pistas específicas para los lugares restantes
        for lugar_ in lugares:
            if lugar_ != lugar:
                pistas_lugares[lugar_] = self.generar_pistas_lugares()

        # Almacenar las pistas en diccionarios
        self.pistas_personajes = pistas_personajes
        self.pistas_armas = pistas_armas
        self.pistas_lugares = pistas_lugares

        # Devolver la solución
        return asesino, arma, lugar

    def generar_pistas_personajes(self):
        # Lista de pistas posibles para los personajes
        pistas_posibles = [
            "Tiene un pasado oscuro.",
            "Es conocido por su doble personalidad.",
            "Fue visto discutiendo con la víctima poco antes del crimen.",
            "Tiene un motivo claro para cometer el crimen.",
            "Estaba celoso(a) de la víctima.",
            "Ha estado involucrado(a) en crímenes similares en el pasado.",
            "Muestra signos de comportamiento antisocial."
        ]
        # Seleccionar tres pistas aleatorias para los personajes
        return random.sample(pistas_posibles, 5)

    def generar_pistas_armas(self):
        # Lista de pistas posibles para las armas
        pistas_posibles = [
            "Fue encontrada en el lugar del crimen.",
            "Es un arma poco común.",
            "Estaba limpio(a) de huellas dactilares.",
            "Parece haber sido utilizada recientemente.",
            "Estaba oculta en un lugar sospechoso.",
            "Corresponde a la descripción dada por un testigo.",
            "Es del mismo tipo de arma utilizada en crímenes anteriores."
        ]
        # Seleccionar cinco pistas aleatorias para las armas
        return random.sample(pistas_posibles, 5)

    def generar_pistas_lugares(self):
        # Lista de pistas posibles para los lugares
        pistas_posibles = [
            "Es un lugar poco frecuentado.",
            "Es conocido por ser peligroso durante la noche.",
            "Tiene múltiples salidas.",
            "Fue el último lugar visitado por la víctima.",
            "Está aislado del resto de la casa.",
            "Es un lugar donde se guardan objetos de valor.",
            "Es el lugar más oscuro de la casa."
        ]
        # Verificar si hay suficientes pistas para seleccionar 5
        if len(pistas_posibles) < 5:
            return "No hay suficientes pistas disponibles."
        else:
            # Seleccionar cinco pistas aleatorias para los lugares
            return random.sample(pistas_posibles, 5)
        
    def make_guess(self):
        # Ventana emergente para hacer una suposición
        guess_window = tk.Toplevel(self.master)
        guess_window.title("Hacer Suposición")

        # Variables para almacenar la selección del usuario
        selected_character_var = tk.StringVar(guess_window)
        selected_weapon_var = tk.StringVar(guess_window)
        selected_location_var = tk.StringVar(guess_window)

        # Etiquetas y listas desplegables para seleccionar sospechoso, arma y lugar
        character_label = tk.Label(guess_window, text="Selecciona un sospechoso:")
        character_label.grid(row=0, column=0, padx=10, pady=5)
        character_dropdown = ttk.Combobox(guess_window, textvariable=selected_character_var, values=self.character_names)
        character_dropdown.grid(row=0, column=1, padx=10, pady=5)

        weapon_label = tk.Label(guess_window, text="Selecciona un arma:")
        weapon_label.grid(row=1, column=0, padx=10, pady=5)
        weapon_dropdown = ttk.Combobox(guess_window, textvariable=selected_weapon_var, values=self.weapon_names)
        weapon_dropdown.grid(row=1, column=1, padx=10, pady=5)

        location_label = tk.Label(guess_window, text="Selecciona un lugar:")
        location_label.grid(row=2, column=0, padx=10, pady=5)
        location_dropdown = ttk.Combobox(guess_window, textvariable=selected_location_var, values=self.location_names)
        location_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Función para verificar la suposición del usuario
        def check_guess():
            if (selected_character_var.get(), selected_weapon_var.get(), selected_location_var.get()) == (self.asesino, self.arma, self.lugar):
                messagebox.showinfo("¡Correcto!", "¡Felicitaciones! Has resuelto el caso.")
            else:
                messagebox.showinfo("Incorrecto", "Lo siento, esa no es la solución correcta. Sigue intentando.")

        # Botón para aceptar la suposición del usuario
        accept_button = tk.Button(guess_window, text="Aceptar", command=check_guess)
        accept_button.grid(row=3, columnspan=2, padx=10, pady=10)

def main():
    root = tk.Tk()
    app = ClueGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
