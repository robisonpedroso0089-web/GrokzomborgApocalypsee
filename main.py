    self.rugidos = [
        "ROOOAAAR-ZIIIMB!", 
        "*bip bip* SYSTEM OVERRIDE!", 
        "01010010 01001111 01000001 01010010!", 
        "EU SOU INEVITÁVEL... WiFi 6E!", 
        "ULTRARUGIDO... ASCENSÃO!", 
        "APOCALIPSE DIGITAL ATIVADO"
    ]

    # === APOCALIPSE SONORO COMPLETO ===
    self.sons = [
        SoundLoader.load('data/sounds/roar1.wav'),
        SoundLoader.load('data/sounds/roar2.wav'),
        SoundLoader.load('data/sounds/roar3.wav'),
        SoundLoader.load('data/sounds/roar4.wav'),
        SoundLoader.load('data/sounds/ultrarugido.wav'),
        SoundLoader.load('data/sounds/apocalipse.wav'),
    ]

    volumes = [0.9, 1.0, 1.1, 1.1, 1.3, 1.5]
    for i, s in enumerate(self.sons):
        if s:
            s.volume = volumes[i]
            if i == 5:
                s.loop = True
                s.play()  # Apocalipse começa imediatamente

    # Matrix Rain
    self.chars = [chr(i) for i in range(0x30A0, 0x30FF)] + list("01ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ")
    self.columns = []
    self.init_matrix()

    # Monstro
    self.x = self.width / 2
    self.y = self.height / 2
    self.vx = random.choice([-7, 7])
    self.vy = random.choice([-7, 7])

    self.bind(size=self.update_graphics, pos=self.update_graphics)
    Clock.schedule_interval(self.update, 1/60.0)

def init_matrix(self):
    self.columns = []
    char_width = 20
    column_count = int(self.width // char_width) + 2 if self.width > 0 else 40
    for i in range(column_count):
        self.columns.append({
            'x': i * char_width - char_width//2,
            'drops': [],
            'speed': random.uniform(0.5, 3),
            'timer': random.uniform(0, 3)
        })

def update_graphics(self, *args):
    if not self.columns or len(self.columns) < 10:
        self.init_matrix()

def draw_matrix(self):
    with self.canvas:
        Color(0.02, 0.02, 0.05, 1)
        Rectangle(pos=self.pos, size=self.size)

        for col in self.columns:
            col['timer'] -= 0.016  # ~60fps
            if col['timer'] <= 0:
                col['timer'] = random.uniform(0.5, 4)
                col['drops'].append({
                    'y': self.height,
                    'length': random.randint(5, 25),
                    'speed': random.uniform(15, 40) * col['speed']
                })

            active = []
            for drop in col['drops']:
                drop['y'] -= drop['speed']
                if drop['y'] > -drop['length'] * 30:
                    active.append(drop)
                    for i in range(drop['length']):
                        alpha = max(0, 1 - i / drop['length'])
                        if i == 0:
                            Color(0.8, 1, 0.8, 1)
                        else:
                            Color(0, 0.8 + alpha*0.2, 0, alpha*0.8)
                        char = random.choice(self.chars)
                        # Simples rectangle + text (Kivy Label é pesado, então simulando)
                        # Para performance real, usar Label com cache ou Texture
                        pass  # Placeholder - na prática usar canvas text ou Label pool

            col['drops'] = active

def desenhar(self):
    self.canvas.clear()
    self.draw_matrix()

    with self.canvas:
        # Cor infernal
        cores = [(1,0.1,0.1), (0.1,1,0.2), (0.1,0.4,1), (1,1,0), (1,0,1), (0,0,0)]
        Color(*cores[min(self.evolucao, 5)])
        
        if self.evolucao >= 5:
            Color(1, 0, 0, random.uniform(0.7, 1))

        tam = 100 + self.evolucao * 70
        Ellipse(pos=(self.x-tam/2, self.y-tam/2), size=(tam, tam))

        # Olhos
        Color(1, 0, 0, 1)
        olho = 30 + self.evolucao * 20
        Ellipse(pos=(self.x-olho-20, self.y+20), size=(olho, olho*1.8))
        Ellipse(pos=(self.x+20, self.y+20), size=(olho, olho*1.8))

        # Garras
        Color(0.8, 0.8, 1, 1)
        for i in range(1 + self.evolucao//2):
            Line(points=[self.x+40+i*20, self.y-30, self.x+100+i*30, self.y-150],
                 width=8 + self.evolucao*6, cap='round')

        # Glitch
        if self.evolucao >= 3:
            for _ in range(10 + self.evolucao*10):
                Color(1, 0, 1, random.uniform(0.5, 1))
                Line(points=[self.x + random.randint(-200,200),
                            self.y + random.randint(-200,200),
                            self.x + random.randint(-200,200),
                            self.y + random.randint(-200,200)],
                     width=random.randint(3,12))

        if self.evolucao >= 5:
            Color(1,0,0,0.3)
            for _ in range(30):
                Line(points=[random.randint(0,self.width), random.randint(0,self.height),
                            random.randint(0,self.width), random.randint(0,self.height)],
                     width=4)

def update(self, dt):
    self.x += self.vx
    self.y += self.vy

    velocidade = 5 + self.evolucao * 3
    if self.x < 100 or self.x > self.width - 100:
        self.vx = random.choice([-velocidade, velocidade])
    if self.y < 100 or self.y > self.height - 200:
        self.vy = random.choice([-velocidade, velocidade])

    self.desenhar()

def tocar_som(self):
    idx = min(self.evolucao, len(self.sons)-1)
    som = self.sons[idx]
    if som:
        if self.evolucao < 5 or som.state != 'playing':
            som.stop()
            som.play()

def on_touch_down(self, touch):
    self.x = touch.x
    self.y = touch.y
    self.evolucao = min(self.evolucao + 1, 5)
    self.tocar_som()

    msg = Label(text=self.rugidos[min(self.evolucao, 5)],
                font_size='50sp' if self.evolucao < 5 else '70sp',
                color=(1,0,0,1) if self.evolucao >=5 else (1,0.3,0.3,1),
                pos_hint={'center_x':0.5, 'top':1},
                size_hint_y=None, height=150)
    self.add_widget(msg)
    Clock.schedule_once(lambda dt: self.remove_widget(msg), 2.5 if self.evolucao < 5 else 4)
    return True
