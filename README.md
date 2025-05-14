### slideshow-video-mkr

**slideshow-video-mkr** é um utilitário em Python que transforma rapidamente uma pasta de imagens em um vídeo‐slideshow totalmente configurável. Ideal para criar apresentações, timelapses ou compilações de fotos sem depender de editores de vídeo pesados.

#### ✨ Principais recursos

* **Codec personalizável** – escolha qualquer codec suportado pelo FFmpeg (padrão: `libx264`/MP4).
* **Resolução livre** – gere vídeos em 720p, 1080p, 4K ou qualquer tamanho (`--resolution 1920x1080`).
* **Modos de ajuste**

  * `fit` – preserva proporção e adiciona barras laterais/superiores.
  * `crop` – preenche a tela e corta o excedente.
  * `stretch` – estica a imagem para ocupar todo o quadro.
* **Duração por foto** ajustável (`--duration 5`).
* **FPS configurável** (`--fps 24`).
* **Compatível com MoviePy ≥ 2** – usa APIs modernas (`resized`, `with_duration`, etc.).
* Código enxuto (\~150 linhas) sem dependências pesadas além de **MoviePy** e **imageio‑ffmpeg**.

#### 🚀 Uso rápido

```bash
# Instale dependências
pip install moviepy imageio-ffmpeg

# Gere um slideshow 1080p, 5 s por imagem
python slideshow.py ./fotos \
    --output viagem.mp4 \
    --codec libx264 \
    --resolution 1920x1080 \
    --mode fit \
    --duration 5
```
