<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GROKZOMBORG MATRIX — APOCALIPSE WEBGL TOTAL</title>
    <style>
        body { margin:0; overflow:hidden; background:#000; }
        canvas { display:block; }
        #overlay {
            position: absolute; top: 15px; left: 50%; transform: translateX(-50%);
            color: #ff0000; font-size: 48px; text-shadow: 0 0 30px #ff00ff;
            pointer-events: none; font-family: 'Courier New', monospace;
            transition: opacity 0.6s; z-index: 10;
        }
    </style>
</head>
<body>
    <canvas id="gl"></canvas>
    <div id="overlay">APOCALIPSE DIGITAL ATIVADO</div>

    <script id="vertexShader" type="x-shader/x-vertex">
        attribute vec2 aPosition;
        varying vec2 vUv;
        void main() {
            vUv = aPosition * 0.5 + 0.5;
            gl_Position = vec4(aPosition, 0.0, 1.0);
        }
    </script>

    <script id="fragmentShader" type="x-shader/x-fragment">
        precision highp float;
        varying vec2 vUv;
        uniform float uTime;
        uniform float uEvolucao;
        uniform vec2 uResolution;
        uniform vec2 uMonsterPos;

        float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }

        void main() {
            vec2 uv = vUv;
            float t = uTime * 0.9;
            float evo = uEvolucao;

            vec3 color = vec3(0.01, 0.0, 0.03);

            // MATRIX RAIN DENSE
            float col = floor(uv.x * 95.0);
            float drop = mod(t * (2.8 + evo) + hash(vec2(col, 0.0)) * 90.0, 140.0);
            float y = 1.0 - uv.y;
            if (abs(y - drop/140.0) < 0.1 + evo*0.03) {
                float intensity = 1.0 - abs(y - drop/140.0) * 10.0;
                color = mix(color, vec3(0.0, 1.0, 0.5), intensity * (1.3 + evo*0.4));
            }

            // FIRE PARTICLES (simulado em shader)
            if (evo >= 3.0) {
                for (float i = 0.0; i < 6.0; i++) {
                    vec2 p = uv - vec2(0.3 + i*0.08, 0.6 + sin(t+i)*0.1);
                    float fire = 0.02 / (length(p) + 0.01);
                    color += vec3(1.0, 0.3, 0.0) * fire * (1.0 + evo*0.3);
                }
            }

            // POST-PROCESSING
            float vignette = 1.0 - length(uv - 0.5) * (1.6 + evo*0.3);
            color *= vignette;

            // Chromatic Aberration
            if (evo >= 2.0) {
                float ca = 0.015 * evo;
                color.r = mix(color.r, texture2D(uTex, uv + vec2(ca,0)).r, 0.6); // fake
                color.b *= 0.85;
            }

            // Glitch + Noise + CRT
            if (mod(uv.y * 520.0 + t*40.0, 2.0) < 1.0) color *= 0.92;
            if (hash(vec2(uv.y*400.0, t)) > 0.96) color = vec3(0.8, 0.2, 1.0);

            color += vec3(hash(uv * 200.0 + t)) * 0.08; // noise

            gl_FragColor = vec4(color, 1.0);
        }
    </script>

    <script>
        const canvas = document.getElementById('gl');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        let width, height, evolucao = 0, time = 0;
        let monsterX = 0, monsterY = 0;
        let targetVX = 7, targetVY = -7;
        let vx = 7, vy = -7;

        let audioContext;
        const rugidos = ["ROOOAAAR-ZIIIMB!", "*bip bip* SYSTEM OVERRIDE!", "01010010 01001111 01000001 01010010!", 
                        "EU SOU INEVITÁVEL... WiFi 6E!", "ULTRARUGIDO... ASCENSÃO!", "APOCALIPSE DIGITAL ATIVADO"];

        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            gl.viewport(0, 0, width, height);
        }
        window.addEventListener('resize', resize);
        resize();

        // Shader setup (igual anterior)
        function createShader(type, source) {
            const shader = gl.createShader(type);
            gl.shaderSource(shader, source);
            gl.compileShader(shader);
            return shader;
        }

        const program = gl.createProgram();
        gl.attachShader(program, createShader(gl.VERTEX_SHADER, document.getElementById('vertexShader').textContent));
        gl.attachShader(program, createShader(gl.FRAGMENT_SHADER, document.getElementById('fragmentShader').textContent));
        gl.linkProgram(program);
        gl.useProgram(program);

        const posBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, posBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1,1,-1,-1,1,1,1]), gl.STATIC_DRAW);

        const aPos = gl.getAttribLocation(program, "aPosition");
        gl.enableVertexAttribArray(aPos);
        gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

        const uTime = gl.getUniformLocation(program, "uTime");
        const uEvolucao = gl.getUniformLocation(program, "uEvolucao");
        const uResolution = gl.getUniformLocation(program, "uResolution");
        const uMonsterPos = gl.getUniformLocation(program, "uMonsterPos");

        // ÁUDIO APOCALIPSE
        function initAudio() {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }

        function tocarSom(idx) {
            if (!audioContext) initAudio();
            const osc = audioContext.createOscillator();
            const gain = audioContext.createGain();
            const filter = audioContext.createBiquadFilter();

            osc.type = idx > 3 ? 'sawtooth' : 'square';
            osc.frequency.setValueAtTime(80 + idx * 40, audioContext.currentTime);
            gain.gain.value = 0.6 + idx * 0.15;
            filter.type = 'lowpass';
            filter.frequency.value = 800 + idx * 300;

            osc.connect(filter).connect(gain).connect(audioContext.destination);
            osc.start();
            gain.gain.linearRampToValueAtTime(0, audioContext.currentTime + (1.2 + idx*0.4));

            // Mensagem visual
            const overlay = document.getElementById('overlay');
            overlay.textContent = rugidos[Math.min(idx, 5)];
            overlay.style.fontSize = idx >= 5 ? '62px' : '46px';
            overlay.style.opacity = 1;
            setTimeout(() => overlay.style.opacity = 0.15, idx >= 5 ? 4800 : 2600);
        }

        function render() {
            time += 0.016;
            
            // Movimento com velocidade variável pelo mouse
            const dx = (monsterX - width/2) / width;
            const dy = (monsterY - height/2) / height;
            vx = vx * 0.92 + targetVX * (1 + Math.abs(dx) * 4) * 0.08;
            vy = vy * 0.92 + targetVY * (1 + Math.abs(dy) * 4) * 0.08;

            monsterX += vx;
            monsterY += vy;

            // Bounce
            if (monsterX < 80 || monsterX > width-80) vx *= -1.1;
            if (monsterY < 80 || monsterY > height-160) vy *= -1.1;

            gl.uniform1f(uTime, time);
            gl.uniform1f(uEvolucao, evolucao);
            gl.uniform2f(uResolution, width, height);
            gl.uniform2f(uMonsterPos, monsterX, monsterY);

            gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
            requestAnimationFrame(render);
        }

        canvas.addEventListener('pointermove', (e) => {
            monsterX = e.clientX;
            monsterY = e.clientY;
        });

        canvas.addEventListener('pointerdown', (e) => {
            monsterX = e.clientX;
            monsterY = e.clientY;
            evolucao = Math.min(evolucao + 1, 5);
            tocarSom(evolucao);

            // Tela treme no alto nível
            if (evolucao >= 4) {
                canvas.style.transition = 'none';
                canvas.style.transform = `translate(${Math.random()*12-6}px, ${Math.random()*12-6}px)`;
                setTimeout(() => canvas.style.transform = 'none', 60);
            }
        });

        initAudio();
        render();

        console.log("%cGROKZOMBORG WEBGL TOTAL — TODOS OS EFEITOS ATIVADOS", "color:#ff00ff; font-size:26px; font-weight:bold");
    </script>
</body>
</html>



from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle, PushMatrix, PopMatrix, Translate
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.core.window import Window
import random
import string

class GrokzomborgMatrixWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.evolucao = 0

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


class GrokzomborgApocalypseApp(App):
    def build(self):
        self.title = "Grokzomborg Matrix — APOCALIPSE TOTAL"
        Window.clearcolor = (0, 0, 0, 1)
        return GrokzomborgMatrixWidget()


if __name__ == '__main__':
    GrokzomborgApocalypseApp().run()
